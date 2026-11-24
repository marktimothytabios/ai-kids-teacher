"""Catalogue: loads the books and produces PDFs and preview images on demand, with caching."""
from __future__ import annotations

import os
import tempfile
import threading
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from builder import content, pdf, spelling

ROOT = content.ROOT
PREVIEW_SCALE = 1.0
PREVIEW_PAGES = (0, 3, 4, 9)  # cover, first question, first answer, a story from the middle

DOMAIN_LABELS = {
    "science": "Science", "body": "My body", "health": "Health", "values": "Values",
    "social-emotional": "Feelings", "maths": "Maths", "safety": "Safety", "community": "Community",
}


@dataclass
class StoryView:
    number: int
    question: str
    value: str


@dataclass
class BookView:
    slug: str
    volume: int
    title: str
    teaches: str
    domain_label: str
    story_count: int
    stories: list[StoryView]
    values: list[str]


class Catalog:
    def __init__(self, out_dir: Path | None = None):
        self.out_dir = Path(out_dir) if out_dir else ROOT / "out"
        self.books = [b for b in content.load_all() if b.status == "ready" and b.stories]
        self.by_slug = {b.slug: b for b in self.books}
        self._lock = threading.RLock()

    # ------------------------------------------------------------- views
    def view(self, book: content.Book, variant: str) -> BookView:
        stories = [StoryView(i, spelling.resolve(s.question, variant), s.tags.get("value", ""))
                   for i, s in enumerate(book.stories, start=1)]
        values = [v for v, _ in Counter(s.value for s in stories if s.value).most_common(6)]
        return BookView(book.slug, book.volume, spelling.resolve(book.title, variant), book.teaches,
                        DOMAIN_LABELS.get(book.domain, book.domain.title()), len(stories), stories, values)

    def totals(self) -> dict:
        return {"books": len(self.books), "stories": sum(len(b.stories) for b in self.books)}

    # --------------------------------------------------------------- files
    def _source_mtime(self, book: content.Book) -> float:
        files = list(book.path.rglob("*.yaml")) + list((ROOT / "builder").glob("*.py"))
        return max(f.stat().st_mtime for f in files)

    def pdf_path(self, book: content.Book, variant: str, sample: bool = False) -> Path:
        """Return the PDF, (re)building it if it is missing or older than its sources."""
        target = self.out_dir / pdf.pdf_filename(book, variant, sample)
        with self._lock:
            if target.exists() and target.stat().st_mtime >= self._source_mtime(book):
                return target
            self.out_dir.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=self.out_dir) as tmp:
                built = pdf.build_book(book, Path(tmp), variant, sample, self.books)
                os.replace(built, target)
            return target

    def preview_path(self, book: content.Book, variant: str, page: int) -> Path:
        import pypdfium2 as pdfium

        source = self.pdf_path(book, variant)
        target = self.out_dir / "previews" / f"{book.slug}-{variant}-{page}.png"
        with self._lock:
            if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
                return target
            target.parent.mkdir(parents=True, exist_ok=True)
            doc = pdfium.PdfDocument(str(source))
            try:
                if not 0 <= page < len(doc):
                    raise IndexError(page)
                image = doc[page].render(scale=PREVIEW_SCALE).to_pil()
            finally:
                doc.close()
            tmp = target.with_suffix(".tmp.png")
            image.save(tmp)
            os.replace(tmp, target)
            return target

    def warm(self) -> None:
        """Build every PDF and cover image ahead of time (run in a background thread)."""
        for b in self.books:
            for v in spelling.VARIANTS:
                self.preview_path(b, v, 0)
