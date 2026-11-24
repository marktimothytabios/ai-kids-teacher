"""One-off: port the 50 stories of the first PDF into content/ YAML files.

Usage: python3 -I tools/port_book1.py path/to/Why_Why_Why_Picture_Book.pdf
Already run once; kept so the port is reproducible and reviewable.
"""
import re
import sys
from pathlib import Path

import pypdf
import yaml

ROOT = Path(__file__).resolve().parent.parent

BOOKS = [  # slug, title, teaches, domain, stories from book 1
    ("sky-weather", "Sky, Weather & Seasons", "Curiosity about nature", "science", list(range(1, 12)) + [23]),
    ("plants-animals", "Plants & Animals", "Care for living things", "science", list(range(12, 21))),
    ("how-things-work", "How Things Work", "Cause and effect", "science", [21, 22, 24, 25, 26, 27]),
    ("my-body", "My Amazing Body", "Knowing and loving your body", "body", [34, 35, 36, 37, 38, 39, 41, 42, 43]),
    ("clean-healthy", "Clean, Healthy & Strong", "Cleanliness and good habits", "health", [28, 29, 30, 31, 32, 33, 44, 45]),
    ("kind-hearts", "Kind Hearts", "Kindness, empathy and sharing", "values", [47, 48, 50]),
    ("feelings-friends", "Feelings & Friends", "Naming feelings and making friends", "social-emotional", [40]),
    ("little-mathematicians", "Little Mathematicians", "Practical maths", "maths", []),
    ("safe-smart", "Safe & Smart", "Safety, honesty and listening", "safety", [46]),
    ("helpers-world", "Helpers & Our World", "Community, jobs and caring for Earth", "community", [49]),
]
# Which kit scene each old story uses (see builder/kit.py).
SCENE = {1: "day", 2: "space", 3: "night", 4: "night", 5: "rain", 6: "storm", 7: "rainbow", 8: "wind",
         9: "snow", 10: "snow", 11: "garden", 12: "garden", 13: "garden", 14: "garden", 15: "day",
         16: "sea", 17: "day", 18: "home", 19: "day", 20: "sea", 21: "sea", 22: "sea", 23: "day",
         24: "play", 25: "play", 26: "sea", 27: "street", 28: "home", 29: "home", 30: "home",
         31: "night", 32: "home", 33: "home", 34: "home", 35: "body", 36: "body", 37: "body",
         38: "body", 39: "body", 40: "hearts", 41: "night", 42: "body", 43: "body", 44: "street",
         45: "day", 46: "street", 47: "hearts", 48: "play", 49: "street", 50: "hearts"}
VALUE = {47: "kindness", 48: "sharing", 50: "love", 46: "safety", 45: "self-care", 28: "self-care",
         29: "cleanliness", 30: "cleanliness"}
# British -> {us|uk} markers (source text is British).
FIX = [("cosy", "{cozy|cosy}"), ("colours", "{colors|colours}"), ("Practise", "{Practice|Practise}"), ("Mummy's", "{Mommy's|Mummy's}")]


def mark(t: str) -> str:
    for a, b in FIX:
        t = t.replace(a, b)
    return t


def clean(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def main(pdf: str) -> None:
    r = pypdf.PdfReader(pdf)
    stories = {}
    for n, i in enumerate(range(2, len(r.pages) - 1, 2), start=1):
        q = clean(" ".join(r.pages[i].extract_text().split("\n")[:-2] if False else r.pages[i].extract_text().strip().split("\n")[:-1]))
        sound = ""
        m = re.match(r"^(.*?)\s*(Why .*)$", q)
        if m and m.group(1):
            sound, q = m.group(1).strip(), m.group(2)
        body, _, rest = r.pages[i + 1].extract_text().partition("Let's try!")
        stories[n] = dict(question=q, sound=sound, answer=clean(body), lets_try=clean(rest))
    assert len(stories) == 50, len(stories)

    (ROOT / "content/books").mkdir(parents=True, exist_ok=True)
    for vol, (slug, title, teaches, domain, nums) in enumerate(BOOKS, start=1):
        d = ROOT / f"content/books/{vol:02d}-{slug}"
        (d / "stories").mkdir(parents=True, exist_ok=True)
        book = dict(slug=slug, volume=vol, title=title, subtitle=f"Little Whys: {title}",
                    teaches=teaches, domain=domain, status="draft", target_stories=20)
        (d / "book.yaml").write_text(yaml.safe_dump(book, sort_keys=False, allow_unicode=True))
        for order, n in enumerate(nums, start=1):
            s = stories[n]
            data = dict(id=f"{slug}-{order:02d}", question=mark(s["question"]), answer=mark(s["answer"]),
                        lets_try=mark(s["lets_try"]), talk_about="", grown_up_corner="",
                        tags=dict(domain=domain, value=VALUE.get(n, ""), skill="", activity=""),
                        scene=SCENE[n], source=f"book1-{n:02d}")
            if s["sound"]:
                data["sound"] = s["sound"]
            (d / "stories" / f"{order:02d}.yaml").write_text(
                yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100))
    print("ported", len(stories), "stories")


if __name__ == "__main__":
    main(sys.argv[1])
