"""Lay out a book and write the PDF."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from . import kit, spelling, stage
from .content import Book, Story
from .kit import DARK, ORANGE, S, Pen

PAGE_PT = 576  # 8 x 8 inches
K = PAGE_PT / S
CREAM, TIP_BG, TIP_FG, GREY = "#FFF8EC", "#FFE3B3", "#B85C00", "#6B6F80"
FONT, BOLD = "LW-Sans", "LW-Sans-Bold"
FONT_DIRS = [Path(__file__).resolve().parent.parent / "fonts", Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/share/fonts/dejavu")]

GROWN_UP_TIPS = [
    "Read one or two questions at a time. Little ones learn best in short, happy bursts.",
    "Ask first: 'Why do YOU think?' Every guess is a good guess.",
    "Point at the pictures and name things together.",
    "Do the 'Let's try!' activity. Moving, touching and pretending makes it stick.",
    "Answers are simplified on purpose for ages 2-4. As they grow, add more detail.",
    "When they ask a why that isn't here, 'Let's find out together!' is a great answer.",
]


def _register_fonts() -> None:
    if FONT in pdfmetrics.getRegisteredFontNames():
        return
    for d in FONT_DIRS:
        reg, bold = Path(d) / "DejaVuSans.ttf", Path(d) / "DejaVuSans-Bold.ttf"
        if reg.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont(FONT, str(reg)))
            pdfmetrics.registerFont(TTFont(BOLD, str(bold)))
            return
    raise RuntimeError("DejaVuSans fonts not found in ./fonts")


def wrap(text, font, size, width):
    return simpleSplit(text, font, size, width)


class BookBuilder:
    def __init__(self, book: Book, out: Path, variant: str, sample: bool = False,
                 all_books: list[Book] | None = None):
        _register_fonts()
        self.book, self.variant, self.sample = book, variant, sample
        self.all_books = all_books or [book]
        self.stories = book.stories[:3] if sample else book.stories
        self.c = canvas.Canvas(str(out), pagesize=(PAGE_PT, PAGE_PT))
        self.c.setTitle(f"{book.subtitle}")
        self.c.setAuthor("Little Whys")
        self.c.setSubject(f"A read-together book for ages 2-4 ({'US' if variant == 'us' else 'UK'} spelling)")
        self.p = Pen(self.c)
        self.pages = 0

    # ------------------------------------------------------------ helpers
    def t(self, text: str) -> str:
        return spelling.resolve(text, self.variant)

    def page(self, draw):
        self.c.saveState()
        self.c.scale(K, K)
        draw()
        self.c.restoreState()
        self.c.showPage()
        self.pages += 1

    def panel(self, x, y, w, h, color="#FFFFFF", r=60):
        self.p.rect(x, y, w, h, color, r=r)

    def thumb(self, scene, hero, x, y, size, border=10):
        """Scene drawn inside a rounded white frame."""
        c = self.c
        self.p.rect(x - border, y - border, size + 2 * border, size + 2 * border, "#FFFFFF", r=size * .12)
        c.saveState()
        path = c.beginPath()
        path.roundRect(x, S - y - size, size, size, size * .1)
        c.clipPath(path, stroke=0, fill=0)
        c.translate(x, S - y - size)
        k = size / S
        c.scale(k, k)
        stage.draw_scene(self.p, scene, hero)
        c.restoreState()

    def hero(self, story_index: int):
        return kit.hero_for(self.book.volume, story_index)

    # -------------------------------------------------------------- pages
    def cover(self):
        b = self.book
        bg, ground, icons = COVERS.get(b.slug, ("#FFD166", kit.GREEN, ("sun", "cloud")))
        hero = kit.CAST[b.volume % len(kit.CAST)]
        def d():
            self.p.rect(0, 0, S, S, bg); self.p.rect(0, 610, S, 190, ground)
            for x, y, c, sz in [(130, 360, kit.PURPLE, 120), (670, 330, kit.RED, 100)]:
                self.p.text(x, y + sz * .35, "?", BOLD, sz, c)
            for x, name in zip((135, 665), icons):
                stage.ITEMS[name](self.p, x, 640 if name not in stage.FLOAT else 520, 150, 0)
            kit.child(self.p, 400, 665, hero, 1.2, "o", "up")
            self.panel(60, 70, 680, 200)
            self.p.text(400, 175, "Little Whys", BOLD, 92, DARK)
            self.p.text(400, 230, self.t(b.title), BOLD, 32 if len(b.title) < 26 else 27, TIP_FG)
            self.p.text(400, 735, f"{len(b.stories)} big questions for little explorers" if not self.sample
                        else "FREE SAMPLE: the first 3 stories", FONT, 24, DARK)
            self.p.text(400, 770, f"Book {b.volume}  ·  A read-together book for ages 2-4", FONT, 18, DARK)
            if b.status == "draft" and not self.sample:
                self.panel(30, 30, 330, 46, "#E63946", r=20)
                self.p.text(195, 62, f"DRAFT  {len(b.stories)} of {b.target_stories} stories", BOLD, 20, "#FFFFFF")
        self.page(d)

    def grown_up(self):
        def d():
            self.p.rect(0, 0, S, S, CREAM)
            self.p.text(400, 120, "For the grown-up reading this", BOLD, 40, DARK)
            y = 190
            for tip in GROWN_UP_TIPS:
                kit.star(self.p, 88, y + 4, 22, ORANGE)
                for ln in wrap(self.t(tip), FONT, 24, 590):
                    self.p.text(130, y + 10, ln, FONT, 24, DARK, "start"); y += 32
                y += 20
            self.panel(60, 625, 680, 135, TIP_BG, r=30)
            self.p.text(90, 672, "In this book", BOLD, 22, TIP_FG, "start")
            for i, ln in enumerate(wrap(self.t(f"Theme: {self.book.title}. Teaches: {self.book.teaches.lower()}."),
                                        FONT, 21, 620)[:2]):
                self.p.text(90, 708 + i * 28, ln, FONT, 21, DARK, "start")
        self.page(d)

    def contents(self):
        def d():
            self.p.rect(0, 0, S, S, CREAM)
            self.p.text(400, 90, "Our questions", BOLD, 42, DARK)
            self.p.text(400, 130, "Tick each one when you have read it!", FONT, 22, GREY)
            half = 10
            for i, s in enumerate(self.stories):
                col, row = divmod(i, half)
                x, y = 50 + col * 380, 165 + row * 60
                self.p.rect(x, y, 34, 34, "#FFFFFF", r=8); self.p.rect(x + 3, y + 3, 28, 28, "#F5E6CC", r=6)
                lines = wrap(self.t(s.question), FONT, 19, 300)[:2]
                for j, ln in enumerate(lines):
                    self.p.text(x + 50, y + (14 if len(lines) == 2 else 25) + j * 22, ln, FONT, 19, DARK, "start")
        self.page(d)

    def question_page(self, i: int, s: Story):
        hero = self.hero(i)
        def d():
            self.thumb_full(s.scene, hero)
            lines = wrap(self.t(s.question), BOLD, 46, 620)
            size = 46 if len(lines) <= 2 else 38
            lines = wrap(self.t(s.question), BOLD, size, 620)
            h = 60 + len(lines) * (size * 1.25) + 20
            top = S - 40 - h
            self.panel(50, top, 700, h, "#FFFFFF", r=60)
            self.p.circle(400, top, 28, ORANGE)
            self.p.text(400, top + 10, str(i), BOLD, 28, "#FFFFFF")
            for j, ln in enumerate(lines):
                self.p.text(400, top + 62 + size * .75 + j * size * 1.25, ln, BOLD, size, DARK)
            if s.sound:
                self.p.text(400, 90, s.sound, BOLD, 70, ORANGE if s.scene not in ("day", "wind") else kit.RED)
        self.page(d)

    def thumb_full(self, scene, hero):
        stage.draw_scene(self.p, scene, hero)

    def answer_page(self, i: int, s: Story):
        hero = self.hero(i)
        boxes = [("Let's try!", s.lets_try, 21, 27, TIP_BG, TIP_FG)]
        if s.talk_about.strip():
            boxes.append(("Talk about it", s.talk_about, 21, 27, "#DDF0E4", "#2D7A4F"))
        if s.grown_up_corner.strip():
            boxes.append(("Grown-up corner", s.grown_up_corner, 16, 21, "#E8E6F4", "#4B4A8C"))
        def d():
            self.p.rect(0, 0, S, S, CREAM)
            size = {1: 250, 2: 200}.get(len(boxes), 160)
            self.thumb(s.scene, hero, 400 - size / 2, 28, size)
            y = S - 28  # stack the boxes from the bottom
            for label, text, fs, lh, bg, fg in reversed(boxes):
                lines = wrap(self.t(text), FONT, fs, 620)
                h = 62 + (len(lines) - 1) * lh + 22
                y -= h
                self.panel(50, y, 700, h, bg, r=28)
                self.p.text(78, y + 34, label, BOLD, 23 if fs > 16 else 19, fg, "start")
                for j, ln in enumerate(lines):
                    self.p.text(78, y + 64 + j * lh, ln, FONT, fs, DARK, "start")
                y -= 14
            avail_top, avail_bottom = 28 + size + 38, y - 4
            fs = 28
            while fs > 21:
                lines = wrap(self.t(s.answer), FONT, fs, 650)
                if avail_top + len(lines) * fs * 1.32 <= avail_bottom:
                    break
                fs -= 1
            lines = wrap(self.t(s.answer), FONT, fs, 650)
            for j, ln in enumerate(lines):
                self.p.text(75, avail_top + fs + j * fs * 1.32, ln, FONT, fs, DARK, "start")
        self.page(d)

    def recap(self):
        def d():
            self.p.rect(0, 0, S, S, CREAM)
            self.p.text(400, 90, "What we learned", BOLD, 42, DARK)
            self.p.text(400, 130, "Can you remember each answer?", FONT, 22, GREY)
            for i, s in enumerate(self.stories, start=1):
                row, col = divmod(i - 1, 5)
                x, y = 40 + col * 148, 170 + row * 150
                self.thumb(s.scene, self.hero(i), x, y, 118, 6)
                self.p.circle(x + 6, y + 6, 17, ORANGE)
                self.p.text(x + 6, y + 13, str(i), BOLD, 18, "#FFFFFF")
        self.page(d)

    def activity(self):
        def d():
            self.p.rect(0, 0, S, S, "#FFFFFF")
            self.p.text(400, 100, "My Little Whys sticker chart", BOLD, 40, DARK)
            self.p.text(400, 145, self.t("Add a sticker or {color|colour} in a circle after each story!"), FONT, 22, GREY)
            for i in range(1, self.book.target_stories + 1):
                row, col = divmod(i - 1, 5)
                cx, cy = 100 + col * 150, 245 + row * 130
                self.c.setStrokeColorRGB(.3, .3, .3); self.c.setLineWidth(3); self.c.setDash(8, 6)
                self.c.circle(cx, S - cy, 52, stroke=1, fill=0); self.c.setDash()
                self.p.text(cx, cy + 12, str(i), BOLD, 34, "#BBBBBB")
            self.p.text(60, 760, "My favourite why was: " if self.variant == "uk" else "My favorite why was: ",
                        FONT, 22, DARK, "start")
            self.c.setStrokeColorRGB(.3, .3, .3); self.c.setLineWidth(2); self.c.line(330, S - 760, 750, S - 760)
        self.page(d)

    def next_books(self):
        def d():
            self.p.rect(0, 0, S, S, "#FFD166"); self.p.text(400, 110, "More Little Whys", BOLD, 48, DARK)
            self.p.text(400, 150, "Keep asking why!", FONT, 26, TIP_FG)
            y = 220
            for b in self.all_books:
                self.panel(120, y - 30, 560, 46, "#FFFFFF", r=23)
                self.p.text(400, y + 3, f"{b.volume}. {self.t(b.title)}", BOLD, 23 if len(b.title) < 28 else 20, DARK)
                y += 56
        self.page(d)

    def sample_end(self):
        def d():
            self.p.rect(0, 0, S, S, "#FFD166"); kit.child(self.p, 400, 560, kit.CAST[1], 1.3, "smile", "up")
            self.panel(70, 90, 660, 190)
            self.p.text(400, 160, "Want all of the stories?", BOLD, 42, DARK)
            self.p.text(400, 215, f"The full book has {self.book.target_stories} Little Whys.", FONT, 25, TIP_FG)
            self.p.text(400, 255, "Ask a grown-up to get your copy!", FONT, 25, TIP_FG)
        self.page(d)

    def credits(self):
        def d():
            self.p.rect(0, 0, S, S, CREAM)
            self.p.text(400, 140, "Little Whys", BOLD, 50, DARK)
            self.p.text(400, 190, self.t(self.book.subtitle.replace("Little Whys: ", "")), FONT, 28, TIP_FG)
            for j, ln in enumerate([
                "Text and illustrations (c) Little Whys. All rights reserved.",
                "For personal and classroom use. Please do not resell or share online.",
                "You may print this book as many times as you like for your own family.",
                "",
                "Answers are simplified for ages 2-4. Ask a grown-up to help with the activities.",
            ]):
                self.p.text(400, 300 + j * 40, ln, FONT, 20, DARK)
        self.page(d)

    def back_cover(self):
        def d():
            self.p.rect(0, 0, S, S, "#FFD166")
            kit.child(self.p, 400, 600, kit.CAST[2], 1.3, "smile")
            self.panel(80, 120, 640, 170)
            self.p.text(400, 205, "Keep asking WHY!", BOLD, 52, DARK)
            self.p.text(400, 255, "The whole world is waiting to be explored.", FONT, 22, TIP_FG)
        self.page(d)

    def build(self) -> int:
        self.cover(); self.grown_up(); self.contents()
        for i, s in enumerate(self.stories, start=1):
            self.question_page(i, s); self.answer_page(i, s)
        if self.sample:
            self.sample_end()
        else:
            self.recap(); self.activity(); self.next_books(); self.credits()
        self.back_cover()
        self.c.save()
        return self.pages


COVERS = {  # slug: (background, ground, two cover pictures)
    "sky-weather": ("#A8D5F5", kit.GREEN, ("sun", "cloud")),
    "plants-animals": ("#C9F0B8", kit.GREEN, ("flower", "bee")),
    "how-things-work": ("#FFD6A5", "#8FD18A", ("magnet", "bike")),
    "my-body": ("#FDE0EA", "#FFAFCC", ("heart", "hand")),
    "clean-healthy": ("#BDE8F7", "#9AD1E8", ("soap", "toothbrush")),
    "kind-hearts": ("#FFC8DD", "#FFAFCC", ("heart", "gift")),
    "feelings-friends": ("#E1D5FF", "#C9B8F0", ("balloon", "star")),
    "little-mathematicians": ("#FFF1B8", "#F5E6CC", ("block", "clock")),
    "safe-smart": ("#CDE7FF", "#ADB5BD", ("car", "hat")),
    "helpers-world": ("#D8F3DC", "#8FD18A", ("recycle", "house")),
}


def pdf_filename(book: Book, variant: str, sample: bool = False) -> str:
    return f"little-whys-{book.volume:02d}-{book.slug}-{variant}{'-sample' if sample else ''}.pdf"


def build_book(book: Book, out_dir: Path, variant: str, sample: bool = False,
               all_books: list[Book] | None = None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / pdf_filename(book, variant, sample)
    BookBuilder(book, out, variant, sample, all_books).build()
    return out
