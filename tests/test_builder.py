import pytest
import pypdf

from builder import content, pdf, spelling, stage


def test_resolve_both_variants():
    t = "all the {colors|colours} of the rainbow"
    assert spelling.resolve(t, "us") == "all the colors of the rainbow"
    assert spelling.resolve(t, "uk") == "all the colours of the rainbow"


def test_resolve_rejects_bad_variant_and_unbalanced():
    with pytest.raises(ValueError):
        spelling.resolve("x", "au")
    with pytest.raises(ValueError):
        spelling.resolve("a {b} c", "us")


def test_lint_flags_unmarked_only():
    assert spelling.lint("Pick a colour") == ["colour"]
    assert spelling.lint("Pick a {color|colour}") == []


def test_all_content_validates():
    books = content.load_all()
    errors, _ = content.validate(books, stage.scene_ok)
    assert errors == []
    assert len(books) == 10
    assert all(b.status == "ready" and len(b.stories) == 20 for b in books)
    assert sum(len(b.stories) for b in books) == 200


def test_validate_catches_problems():
    s = content.Story(id="a", question="The sky", answer="", lets_try="x", scene="nope")
    b = content.Book("t", 1, "T", "T", "x", "science", "ready", 20, [s], None)
    errors, _ = content.validate([b], stage.scene_ok)
    text = " ".join(errors)
    assert "ready needs 20" in text and "answer is empty" in text and "unknown scene" in text
    assert "must start with" in text


@pytest.mark.parametrize("variant,present,absent", [("us", "colors", "colours"), ("uk", "colours", "colors")])
def test_pdf_spelling(tmp_path, variant, present, absent):
    books = content.load_all()
    out = pdf.build_book(books[0], tmp_path, variant, all_books=books)
    r = pypdf.PdfReader(str(out))
    text = " ".join(p.extract_text() for p in r.pages)
    assert present in text and absent not in text
    assert len(r.pages) == 48


def test_sample_has_three_stories(tmp_path):
    books = content.load_all()
    r = pypdf.PdfReader(str(pdf.build_book(books[0], tmp_path, "us", sample=True, all_books=books)))
    assert len(r.pages) == 3 + 6 + 2


def test_every_book_with_stories_builds(tmp_path):
    books = content.load_all()
    for b in books:
        if b.stories:
            assert pdf.build_book(b, tmp_path, "us", all_books=books).stat().st_size > 10_000


def test_us_and_uk_words_differ(tmp_path):
    books = {b.slug: b for b in content.load_all()}
    texts = {}
    for v in ("us", "uk"):
        r = pypdf.PdfReader(str(pdf.build_book(books["how-things-work"], tmp_path, v)))
        texts[v] = " ".join(p.extract_text() for p in r.pages)
    assert "elevator" in texts["us"] and "elevator" not in texts["uk"]
    assert "lift" in texts["uk"]


def test_every_story_is_complete():
    for b in content.load_all():
        for s in b.stories:
            for field in ("question", "answer", "lets_try", "talk_about", "grown_up_corner"):
                assert getattr(s, field).strip(), (s.id, field)


def test_questions_are_unique():
    qs = [s.question for b in content.load_all() for s in b.stories]
    assert len(qs) == len(set(qs))


def test_stage_scene_parsing():
    assert stage.parse_scene("day") == ("day", None)
    base, toks = stage.parse_scene("kitchen|kid,apple*3,row,cup")
    assert base == "kitchen" and toks == [("kid", 1), ("apple", 3), ("row", 1), ("cup", 1)]
    for bad in ("nope", "kitchen|", "kitchen|unicorn", "nowhere|apple", "kitchen|apple*0", "kitchen|apple*99"):
        assert not stage.scene_ok(bad), bad
