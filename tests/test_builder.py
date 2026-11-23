import pytest
import pypdf

from builder import content, kit, pdf, spelling


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
    errors, _ = content.validate(books, set(kit.SCENES))
    assert errors == []
    assert len(books) == 10
    assert sum(len(b.stories) for b in books) == 50


def test_validate_catches_problems():
    s = content.Story(id="a", question="The sky", answer="", lets_try="x", scene="nope")
    b = content.Book("t", 1, "T", "T", "x", "science", "ready", 20, [s], None)
    errors, _ = content.validate([b], set(kit.SCENES))
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
    assert len(r.pages) == 3 + 2 * len(books[0].stories) + 5


def test_sample_has_three_stories(tmp_path):
    books = content.load_all()
    r = pypdf.PdfReader(str(pdf.build_book(books[0], tmp_path, "us", sample=True, all_books=books)))
    assert len(r.pages) == 3 + 6 + 2


def test_every_book_with_stories_builds(tmp_path):
    books = content.load_all()
    for b in books:
        if b.stories:
            assert pdf.build_book(b, tmp_path, "us", all_books=books).stat().st_size > 10_000
