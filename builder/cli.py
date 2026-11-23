"""Command line: python -m builder validate | build <book|all> [--spelling us|uk|both] [--sample]"""
import argparse
import sys
from pathlib import Path

from . import content, kit, pdf

OUT = content.ROOT / "out"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="builder")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate", help="check all content")
    b = sub.add_parser("build", help="build PDF(s)")
    b.add_argument("book", help="book slug, number, or 'all'")
    b.add_argument("--spelling", choices=["us", "uk", "both"], default="both")
    b.add_argument("--sample", action="store_true", help="first 3 stories only")
    b.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)

    books = content.load_all()
    errors, warnings = content.validate(books, set(kit.SCENES))
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    if a.cmd == "validate":
        n = sum(len(x.stories) for x in books)
        print(f"{len(books)} books, {n} stories, {len(errors)} errors, {len(warnings)} warnings")
        return 1 if errors else 0
    if errors:
        return 1
    chosen = books if a.book == "all" else [content.find_book(a.book, books)]
    variants = ["us", "uk"] if a.spelling == "both" else [a.spelling]
    for bk in chosen:
        if not bk.stories:
            print(f"skip {bk.slug}: no stories yet")
            continue
        for v in variants:
            print(pdf.build_book(bk, a.out, v, a.sample, books))
    return 0


if __name__ == "__main__":
    sys.exit(main())
