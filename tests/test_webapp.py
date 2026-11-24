import pytest
from fastapi.testclient import TestClient

from webapp.app import Settings, create_app


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    return TestClient(create_app(out_dir=tmp_path_factory.mktemp("out")))


def test_home_lists_all_books(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.text.count('class="card"') == 10
    assert "Kind Hearts" in r.text and "200</strong> stories" in r.text


def test_book_page(client):
    r = client.get("/books/kind-hearts")
    assert r.status_code == 200
    assert "Why do we say sorry?" in r.text
    assert "/books/kind-hearts/download/us" in r.text


def test_download_pdf_both_spellings(client):
    for variant in ("us", "uk"):
        r = client.get(f"/books/sky-weather/download/{variant}")
        assert r.status_code == 200
        assert r.headers["content-type"] == "application/pdf"
        assert r.content.startswith(b"%PDF")
        assert f"-{variant}.pdf" in r.headers["content-disposition"]


def test_sample_is_smaller_than_book(client):
    full = client.get("/books/sky-weather/download/us").content
    sample = client.get("/books/sky-weather/download/us?sample=true").content
    assert sample.startswith(b"%PDF") and len(sample) < len(full)


def test_unknown_book_or_spelling_is_404(client):
    assert client.get("/books/nope").status_code == 404
    assert "Why can" in client.get("/books/nope").text
    assert client.get("/books/sky-weather/download/au").status_code == 404
    assert client.get("/previews/nope/us/0.png").status_code == 404


def test_previews_only_for_allowed_pages(client):
    ok = client.get("/previews/sky-weather/us/0.png")
    assert ok.status_code == 200 and ok.content.startswith(b"\x89PNG")
    assert client.get("/previews/sky-weather/us/30.png").status_code == 404
    assert client.get("/previews/sky-weather/us/-1.png").status_code == 404


def test_spelling_cookie_and_switch(client):
    c = TestClient(client.app)
    r = c.get("/set-spelling/uk?next=/books/my-body", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/books/my-body"
    page = c.get("/books/my-body")
    assert 'lang="en-GB"' in page.text and "/download/uk" in page.text


def test_switch_rejects_open_redirect(client):
    r = client.get("/set-spelling/us?next=//evil.example", follow_redirects=False)
    assert r.headers["location"] == "/"
    r = client.get("/set-spelling/us?next=https://evil.example", follow_redirects=False)
    assert r.headers["location"] == "/"


def test_browser_language_picks_uk(client):
    r = TestClient(client.app).get("/", headers={"accept-language": "en-GB,en;q=0.9"})
    assert 'lang="en-GB"' in r.text


def test_static_pages(client):
    for path in ("/parents", "/about", "/healthz", "/static/style.css"):
        assert client.get(path).status_code == 200, path


def test_download_hook_blocks_paid_books(tmp_path):
    paid = TestClient(create_app(out_dir=tmp_path, settings=Settings(free=False)))
    assert paid.get("/books/sky-weather/download/us").status_code == 402
    assert paid.get("/books/sky-weather/download/us?sample=true").status_code == 200
    assert "not available" in paid.get("/books/sky-weather").text


def test_hidden_from_search_engines_by_default(client):
    assert 'name="robots"' in client.get("/").text
    assert "Disallow: /" in client.get("/robots.txt").text


def test_can_allow_indexing(tmp_path):
    c = TestClient(create_app(out_dir=tmp_path, settings=Settings(indexable=True)))
    assert 'name="robots"' not in c.get("/").text
    assert "Allow: /" in c.get("/robots.txt").text


def test_about_tells_the_story_in_both_spellings(client):
    us = client.get("/about?spelling=us").text
    uk = client.get("/about?spelling=uk").text
    assert "Psalm" in us and "Psalm" in uk
    assert "realize" in us and "judgment" in us and "realise" not in us
    assert "realise" in uk and "judgement" in uk and "realize" not in uk


def test_reader_page(client):
    r = client.get("/books/kind-hearts/read?spelling=us")
    assert r.status_code == 200
    assert 'data-total="48"' in r.text and 'data-page="1"' in r.text
    assert "/books/kind-hearts/pages/us/1.webp" in r.text
    assert "Download PDF to print" in r.text


def test_reader_clamps_page_number(client):
    assert 'data-page="48"' in client.get("/books/kind-hearts/read?page=999").text
    assert 'data-page="1"' in client.get("/books/kind-hearts/read?page=-5").text


def test_reader_page_images(client):
    r = client.get("/books/kind-hearts/pages/us/4.webp")
    assert r.status_code == 200 and r.headers["content-type"] == "image/webp"
    assert r.content[:4] == b"RIFF" and r.content[8:12] == b"WEBP"
    assert client.get("/books/kind-hearts/pages/us/0.webp").status_code == 404
    assert client.get("/books/kind-hearts/pages/us/49.webp").status_code == 404
    assert client.get("/books/kind-hearts/pages/au/1.webp").status_code == 404
    assert client.get("/books/nope/pages/us/1.webp").status_code == 404


def test_reader_text_alternatives(client):
    page = client.get("/books/kind-hearts/read?page=4&spelling=us").text
    assert "Why do we say please and thank you?" in page  # as image description and in the jump list


def test_book_page_offers_reader(client):
    assert "/books/kind-hearts/read" in client.get("/books/kind-hearts").text


def test_paid_mode_keeps_only_the_preview_open(tmp_path):
    paid = TestClient(create_app(out_dir=tmp_path, settings=Settings(free=False)))
    assert paid.get("/books/kind-hearts/pages/us/9.webp").status_code == 200
    assert paid.get("/books/kind-hearts/pages/us/10.webp").status_code == 402
    page = paid.get("/books/kind-hearts/read?page=10&spelling=us").text
    assert "end of the free preview" in page
    assert "pages/us/10.webp" not in page
    assert "Download PDF to print" not in page
    import json
    alts = json.loads(page.split('id="alts">')[1].split("</script>")[0])
    assert len(alts) == 48 and all(alts[:9]) and not any(alts[9:])  # text of locked pages is not sent
