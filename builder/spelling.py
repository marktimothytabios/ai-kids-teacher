"""US / British spelling from a single source.

Text marks the differing words inline as ``{us|uk}``, e.g. ``all the {colors|colours}``.
"""
import re

MARK = re.compile(r"\{([^{}|]*)\|([^{}|]*)\}")
VARIANTS = ("us", "uk")

# Words that should never appear outside a {us|uk} marker. Deliberately not "practice/practise",
# which is a noun/verb pair and has to be marked by hand.
US_ONLY = {"color", "colors", "colored", "mom", "mommy", "gray", "favorite", "neighbor", "cozy",
           "center", "pajamas", "flavor", "realize"}
UK_ONLY = {"colour", "colours", "coloured", "mum", "mummy", "grey", "favourite", "neighbour", "cosy",
           "centre", "pyjamas", "flavour", "realise"}


def resolve(text: str, variant: str) -> str:
    if variant not in VARIANTS:
        raise ValueError(f"spelling must be one of {VARIANTS}, got {variant!r}")
    idx = VARIANTS.index(variant) + 1
    out = MARK.sub(lambda m: m.group(idx), text)
    if "{" in out or "}" in out:
        raise ValueError(f"unbalanced spelling marker in: {text!r}")
    return out


def lint(text: str) -> list[str]:
    """Return unmarked spelling-specific words found in ``text``."""
    bare = MARK.sub(" ", text)
    words = {w.lower() for w in re.findall(r"[A-Za-z]+", bare)}
    return sorted(words & (US_ONLY | UK_ONLY))
