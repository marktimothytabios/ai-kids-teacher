"""Load and validate series content from content/."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import spelling

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
QUESTION_STARTS = ("Why", "How", "What", "Who", "When", "Where")
MAX_SENTENCE_WORDS = 18
MAX_ANSWER_SENTENCES = 6


@dataclass
class Story:
    id: str
    question: str
    answer: str
    lets_try: str
    scene: str
    talk_about: str = ""
    grown_up_corner: str = ""
    sound: str = ""
    tags: dict = field(default_factory=dict)
    source: str = ""


@dataclass
class Book:
    slug: str
    volume: int
    title: str
    subtitle: str
    teaches: str
    domain: str
    status: str
    target_stories: int
    stories: list[Story]
    path: Path


def load_book(path: Path) -> Book:
    meta = yaml.safe_load((path / "book.yaml").read_text())
    stories = []
    for f in sorted((path / "stories").glob("*.yaml")):
        d = yaml.safe_load(f.read_text())
        known = Story.__dataclass_fields__
        stories.append(Story(**{k: v for k, v in d.items() if k in known}))
    return Book(stories=stories, path=path, **{k: meta[k] for k in (
        "slug", "volume", "title", "subtitle", "teaches", "domain", "status", "target_stories")})


def load_all(content: Path = CONTENT) -> list[Book]:
    return [load_book(p) for p in sorted((content / "books").iterdir()) if (p / "book.yaml").exists()]


def find_book(key: str, books: list[Book]) -> Book:
    for b in books:
        if key in (b.slug, str(b.volume), f"{b.volume:02d}"):
            return b
    raise KeyError(f"no book {key!r}; have: {', '.join(b.slug for b in books)}")


def validate(books: list[Book], scene_ok) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors block a build; warnings are advice."""
    errors, warnings = [], []
    seen: set[str] = set()
    for b in books:
        if b.status not in ("draft", "ready"):
            errors.append(f"{b.slug}: status must be draft or ready")
        if b.status == "ready" and len(b.stories) != b.target_stories:
            errors.append(f"{b.slug}: ready needs {b.target_stories} stories, has {len(b.stories)}")
        if len(b.stories) > b.target_stories:
            errors.append(f"{b.slug}: {len(b.stories)} stories is more than {b.target_stories}")
        for s in b.stories:
            where = s.id
            if s.id in seen:
                errors.append(f"{where}: duplicate id")
            seen.add(s.id)
            for name in ("question", "answer", "lets_try"):
                if not str(getattr(s, name)).strip():
                    errors.append(f"{where}: {name} is empty")
            if not scene_ok(s.scene):
                errors.append(f"{where}: unknown scene {s.scene!r}")
            if not s.question.startswith(QUESTION_STARTS) or not s.question.endswith("?"):
                errors.append(f"{where}: question must start with Why/How/What... and end with ?")
            for name in ("question", "answer", "lets_try", "talk_about", "grown_up_corner"):
                text = getattr(s, name)
                try:
                    for v in spelling.VARIANTS:
                        spelling.resolve(text, v)
                except ValueError as e:
                    errors.append(f"{where}: {name}: {e}")
                for w in spelling.lint(text):
                    warnings.append(f"{where}: {name}: unmarked spelling-specific word {w!r}")
            sentences = [x for x in re.split(r"(?<=[.!?])\s+", s.answer.strip()) if x]
            if len(sentences) > MAX_ANSWER_SENTENCES:
                warnings.append(f"{where}: answer has {len(sentences)} sentences (aim for 2-4)")
            for x in sentences:
                if len(x.split()) > MAX_SENTENCE_WORDS:
                    warnings.append(f"{where}: long sentence ({len(x.split())} words): {x[:40]}...")
            if b.status == "ready":
                for name in ("talk_about", "grown_up_corner"):
                    if not getattr(s, name).strip():
                        errors.append(f"{where}: {name} is required in a ready book")
    return errors, warnings
