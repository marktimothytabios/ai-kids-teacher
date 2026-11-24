"""FastAPI app for Little Whys.

Everything is free to download for now. The one place that decides who may download is
``can_download``; when payments are added (Stripe), that is where the purchase check goes.
"""
from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from builder import spelling

from .catalog import PREVIEW_PAGES, SAMPLE_PAGES, Catalog

HERE = Path(__file__).resolve().parent
COOKIE = "spelling"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365


@dataclass(frozen=True)
class Settings:
    free: bool = True  # while True every book is a free download
    site_name: str = "Little Whys"
    # Hidden from search engines until you are ready to launch: set SITE_INDEXABLE=1 to allow indexing.
    indexable: bool = os.environ.get("SITE_INDEXABLE", "0") == "1"


def can_download(request: Request, settings: Settings, book) -> bool:
    """Single place that decides whether a visitor may download ``book``.

    Free launch: always true. With Stripe, check the visitor's paid order here.
    """
    return settings.free


def can_read_page(request: Request, settings: Settings, book, page: int) -> bool:
    """Whether a visitor may see page ``page`` (1-based) in the online reader.

    Free launch: everything. When paid, the front matter and first 3 stories stay open as a sample.
    """
    return can_download(request, settings, book) or page <= SAMPLE_PAGES


def pick_spelling(request: Request) -> tuple[str, bool]:
    """Return (variant, from_query). Query beats cookie beats browser language."""
    q = request.query_params.get("spelling")
    if q in spelling.VARIANTS:
        return q, True
    c = request.cookies.get(COOKIE)
    if c in spelling.VARIANTS:
        return c, False
    lang = request.headers.get("accept-language", "").lower()
    first = lang.split(",")[0].strip()
    if first.startswith(("en-gb", "en-au", "en-nz", "en-ie", "en-za", "en-in")):
        return "uk", False
    return "us", False


def create_app(out_dir: Path | None = None, warm: bool = False, settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    catalog = Catalog(out_dir)
    templates = Jinja2Templates(directory=str(HERE / "templates"))
    app = FastAPI(title="Little Whys", docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/static", StaticFiles(directory=str(HERE / "static")), name="static")
    app.state.catalog = catalog

    def render(request: Request, name: str, status_code: int = 200, **ctx):
        variant, from_query = pick_spelling(request)
        ctx.update(settings=settings, spelling=variant, totals=catalog.totals(), path=request.url.path)
        response = templates.TemplateResponse(request, name, ctx, status_code=status_code)
        if from_query:
            response.set_cookie(COOKIE, variant, max_age=COOKIE_MAX_AGE, samesite="lax")
        return response

    def get_book(slug: str):
        book = catalog.by_slug.get(slug)
        if book is None:
            raise HTTPException(404, "Book not found")
        return book

    def get_variant(value: str) -> str:
        if value not in spelling.VARIANTS:
            raise HTTPException(404, "Unknown spelling")
        return value

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request):
        variant, _ = pick_spelling(request)
        return render(request, "home.html", books=[catalog.view(b, variant) for b in catalog.books])

    @app.get("/books/{slug}", response_class=HTMLResponse)
    def book_page(request: Request, slug: str):
        book = get_book(slug)
        variant, _ = pick_spelling(request)
        others = [catalog.view(b, variant) for b in catalog.books if b.slug != slug]
        return render(request, "book.html", book=catalog.view(book, variant), previews=PREVIEW_PAGES,
                      others=others, allowed=can_download(request, settings, book))

    @app.get("/books/{slug}/download/{variant}")
    def download(request: Request, slug: str, variant: str, sample: bool = False):
        book, variant = get_book(slug), get_variant(variant)
        if not sample and not can_download(request, settings, book):
            raise HTTPException(402, "Purchase required")
        path = catalog.pdf_path(book, variant, sample)
        return FileResponse(path, media_type="application/pdf", filename=path.name)

    @app.get("/books/{slug}/read", response_class=HTMLResponse)
    def read(request: Request, slug: str, page: int = 1):
        book = get_book(slug)
        variant, _ = pick_spelling(request)
        total = catalog.page_total(book, variant)
        page = max(1, min(page, total))
        texts = catalog.page_texts(book, variant)
        open_pages = [can_read_page(request, settings, book, n) for n in range(1, total + 1)]
        alts = [texts[i][:400] if open_pages[i] else "" for i in range(total)]  # never leak locked text
        limit = 0 if all(open_pages) else SAMPLE_PAGES
        story_pages = [(i, s.question, 4 + 2 * (i - 1)) for i, s in enumerate(catalog.view(book, variant).stories, start=1)]
        return render(request, "read.html", book=catalog.view(book, variant), page=page, total=total, alts=alts,
                      limit=limit, story_pages=story_pages, unlocked=open_pages[page - 1],
                      downloadable=can_download(request, settings, book))

    @app.get("/books/{slug}/pages/{variant}/{page}.webp")
    def page_image(request: Request, slug: str, variant: str, page: int):
        book, variant = get_book(slug), get_variant(variant)
        if not 1 <= page <= catalog.page_total(book, variant):
            raise HTTPException(404, "No such page")
        if not can_read_page(request, settings, book, page):
            raise HTTPException(402, "Purchase required")
        return FileResponse(catalog.page_image(book, variant, page), media_type="image/webp",
                            headers={"Cache-Control": "private, max-age=3600"})

    @app.get("/previews/{slug}/{variant}/{page}.png")
    def preview(slug: str, variant: str, page: int):
        book, variant = get_book(slug), get_variant(variant)
        if page not in PREVIEW_PAGES:
            raise HTTPException(404, "No such preview")
        return FileResponse(catalog.preview_path(book, variant, page), media_type="image/png",
                            headers={"Cache-Control": "public, max-age=3600"})

    @app.get("/parents", response_class=HTMLResponse)
    def parents(request: Request):
        return render(request, "parents.html")

    @app.get("/about", response_class=HTMLResponse)
    def about(request: Request):
        return render(request, "about.html")

    @app.get("/set-spelling/{variant}")
    def set_spelling(request: Request, variant: str, next: str = "/"):
        variant = get_variant(variant)
        target = next if next.startswith("/") and not next.startswith("//") else "/"
        response = RedirectResponse(target, status_code=303)
        response.set_cookie(COOKIE, variant, max_age=COOKIE_MAX_AGE, samesite="lax")
        return response

    @app.get("/robots.txt", response_class=PlainTextResponse)
    def robots():
        return "User-agent: *\nAllow: /\n" if settings.indexable else "User-agent: *\nDisallow: /\n"

    @app.get("/healthz")
    def healthz():
        return {"ok": True, **catalog.totals()}

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        response.headers.setdefault("X-Frame-Options", "DENY")
        return response

    @app.exception_handler(404)
    def not_found(request: Request, exc):
        return render(request, "404.html", status_code=404)

    if warm:
        threading.Thread(target=catalog.warm, daemon=True, name="warm-cache").start()
    return app
