"""Stage scenes: a background plus kids and items laid out on the floor.

A scene spec is either a classic scene name from ``kit.SCENES`` ("day") or
``"background|token,token*3"``, e.g. ``"kitchen|kid,apple*3,cup"``:

* ``kid`` / ``kid2`` / ``kids``  (optionally ``kid:sad`` or ``kid:o``) put the cast on the floor
* any item name from ``ITEMS`` (``apple*3`` draws three)
"""
from __future__ import annotations

import math

from .kit import (BLUE, CAST, DARK, GREEN, ORANGE, PINK, PURPLE, RED, SCENES, WHITE, YELLOW,
                  Hero, Pen, S, child, cloud, ground, heart, star, sun)

COLS = [RED, BLUE, YELLOW, "#52B788", ORANGE, PURPLE]
TAN = "#D9A066"
BROWN = "#8A5A3C"
LEAF = "#52B788"


def it_apple(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 44 * u, 42 * u, RED); p.line(x, b - 84 * u, x + 4 * u, b - 100 * u, BROWN, 5 * u)
    p.ellipse(x + 14 * u, b - 92 * u, 14 * u, 7 * u, LEAF)


def it_orange(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 42 * u, 42 * u, ORANGE); p.circle(x, b - 82 * u, 6 * u, LEAF)


def it_banana(p, x, b, s, i=0):
    u = s / 100
    p.curve(x - 45 * u, b - 62 * u, x, b + 4 * u, x + 45 * u, b - 66 * u, YELLOW, 22 * u)


def it_carrot(p, x, b, s, i=0):
    u = s / 100
    p.poly([(x - 20 * u, b - 85 * u), (x + 20 * u, b - 85 * u), (x, b)], ORANGE)
    for dx in (-10, 0, 10):
        p.line(x + dx * u, b - 85 * u, x + dx * 1.6 * u, b - 108 * u, LEAF, 6 * u)


def it_cookie(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 40 * u, 40 * u, TAN)
    for dx, dy in [(-16, -52), (14, -58), (4, -34), (-18, -26), (20, -28)]:
        p.circle(x + dx * u, b + dy * u, 5 * u, BROWN)


def it_cake(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 48 * u, b - 48 * u, 96 * u, 48 * u, "#F4A261", r=8 * u)
    p.rect(x - 48 * u, b - 58 * u, 96 * u, 20 * u, WHITE, r=10 * u); p.rect(x - 4 * u, b - 84 * u, 8 * u, 26 * u, RED)
    p.ellipse(x, b - 92 * u, 6 * u, 10 * u, YELLOW)


def it_cup(p, x, b, s, i=0):
    u = s / 100
    p.curve(x + 28 * u, b - 48 * u, x + 64 * u, b - 32 * u, x + 28 * u, b - 14 * u, BLUE, 8 * u)
    p.rect(x - 32 * u, b - 62 * u, 62 * u, 62 * u, BLUE, r=10 * u); p.rect(x - 32 * u, b - 62 * u, 62 * u, 16 * u, "#8FCBEE", r=8 * u)


def it_plate(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 16 * u, 56 * u, 16 * u, WHITE); p.ellipse(x, b - 18 * u, 36 * u, 9 * u, "#E8EEF3")


def it_bowl(p, x, b, s, i=0):
    u = s / 100
    p.wedge(x, b - 50 * u, 46 * u, 180, 180, "#F4A261"); p.ellipse(x, b - 50 * u, 46 * u, 8 * u, "#FFD6A5")


def it_spoon(p, x, b, s, i=0):
    u = s / 100
    p.line(x, b - 55 * u, x, b, "#ADB5BD", 8 * u); p.ellipse(x, b - 72 * u, 18 * u, 26 * u, "#ADB5BD")


def it_milk(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 30 * u, b - 80 * u, 60 * u, 80 * u, WHITE, r=6 * u)
    p.rect(x - 30 * u, b - 56 * u, 60 * u, 30 * u, BLUE)
    p.poly([(x - 30 * u, b - 80 * u), (x, b - 100 * u), (x + 30 * u, b - 80 * u)], "#E8EEF3")


def it_ball(p, x, b, s, i=0):
    u = s / 100
    for k, c in enumerate([BLUE, YELLOW, RED, ORANGE, LEAF]):
        p.wedge(x, b - 42 * u, 42 * u, k * 72, 72, c)
    p.circle(x, b - 42 * u, 7 * u, WHITE)


def it_block(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 38 * u, b - 76 * u, 76 * u, 76 * u, COLS[i % 6], r=8 * u)
    p.rect(x - 22 * u, b - 60 * u, 44 * u, 44 * u, WHITE, r=6 * u, alpha=.35)


def it_duck(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 28 * u, 44 * u, 28 * u, YELLOW); p.circle(x + 22 * u, b - 66 * u, 22 * u, YELLOW)
    p.poly([(x + 40 * u, b - 64 * u), (x + 62 * u, b - 58 * u), (x + 40 * u, b - 52 * u)], ORANGE)
    p.circle(x + 28 * u, b - 72 * u, 4 * u, DARK)


def it_fish(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 40 * u, 42 * u, 26 * u, ORANGE)
    p.poly([(x + 36 * u, b - 40 * u), (x + 66 * u, b - 62 * u), (x + 66 * u, b - 18 * u)], ORANGE)
    p.circle(x - 22 * u, b - 46 * u, 5 * u, DARK)


def it_cat(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 28 * u, 36 * u, 28 * u, "#F4A261"); p.circle(x, b - 70 * u, 30 * u, "#F4A261")
    p.poly([(x - 28 * u, b - 84 * u), (x - 22 * u, b - 112 * u), (x - 4 * u, b - 94 * u)], "#F4A261")
    p.poly([(x + 28 * u, b - 84 * u), (x + 22 * u, b - 112 * u), (x + 4 * u, b - 94 * u)], "#F4A261")
    for dx in (-11, 11):
        p.circle(x + dx * u, b - 74 * u, 4 * u, DARK)
    p.circle(x, b - 62 * u, 4 * u, PINK)


def it_dog(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 28 * u, 38 * u, 28 * u, TAN); p.circle(x, b - 70 * u, 30 * u, TAN)
    p.ellipse(x - 30 * u, b - 66 * u, 11 * u, 22 * u, BROWN); p.ellipse(x + 30 * u, b - 66 * u, 11 * u, 22 * u, BROWN)
    for dx in (-11, 11):
        p.circle(x + dx * u, b - 74 * u, 4 * u, DARK)
    p.circle(x, b - 60 * u, 6 * u, DARK)


def it_bird(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 36 * u, 40 * u, 28 * u, BLUE); p.circle(x + 30 * u, b - 62 * u, 18 * u, BLUE)
    p.poly([(x + 46 * u, b - 64 * u), (x + 66 * u, b - 58 * u), (x + 46 * u, b - 54 * u)], ORANGE)
    p.ellipse(x - 6 * u, b - 38 * u, 22 * u, 12 * u, "#2F7FB5"); p.circle(x + 34 * u, b - 66 * u, 3.5 * u, DARK)


def it_bee(p, x, b, s, i=0):
    u = s / 100
    p.circle(x - 10 * u, b - 76 * u, 18 * u, "#DDF0FF"); p.circle(x + 14 * u, b - 76 * u, 18 * u, "#DDF0FF")
    p.ellipse(x, b - 40 * u, 38 * u, 28 * u, YELLOW)
    for dx in (-14, 4, 20):
        p.rect(x + dx * u - 4 * u, b - 64 * u, 8 * u, 48 * u, DARK, r=3 * u)
    p.circle(x - 34 * u, b - 44 * u, 4 * u, DARK)


def it_butterfly(p, x, b, s, i=0):
    u = s / 100
    for dx, dy, c in [(-26, -66, PURPLE), (26, -66, PURPLE), (-20, -30, PINK), (20, -30, PINK)]:
        p.ellipse(x + dx * u, b + dy * u, 24 * u, 22 * u, c)
    p.rect(x - 4 * u, b - 84 * u, 8 * u, 72 * u, DARK, r=4 * u)


def it_flower(p, x, b, s, i=0):
    u = s / 100
    p.line(x, b, x, b - 62 * u, "#3E8E5A", 7 * u)
    col = COLS[(i + 1) % 6] if COLS[(i + 1) % 6] != YELLOW else PINK
    for k in range(6):
        a = k * math.pi / 3
        p.circle(x + 20 * u * math.cos(a), b - 74 * u + 20 * u * math.sin(a), 15 * u, col)
    p.circle(x, b - 74 * u, 12 * u, YELLOW)


def it_tree(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 10 * u, b - 55 * u, 20 * u, 55 * u, BROWN); p.circle(x, b - 76 * u, 40 * u, LEAF)


def it_leaf(p, x, b, s, i=0):
    u = s / 100
    p.poly([(x, b - 92 * u), (x + 36 * u, b - 52 * u), (x, b - 6 * u), (x - 36 * u, b - 52 * u)], ORANGE if i % 2 else LEAF)
    p.line(x, b - 88 * u, x, b - 10 * u, WHITE, 3 * u)


def it_star(p, x, b, s, i=0):
    star(p, x, b - 48 * s / 100, 48 * s / 100)


def it_heart(p, x, b, s, i=0):
    heart(p, x, b - 52 * s / 100, 92 * s / 100)


def it_circle(p, x, b, s, i=0):
    p.circle(x, b - 46 * s / 100, 46 * s / 100, COLS[i % 6])


def it_square(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 42 * u, b - 84 * u, 84 * u, 84 * u, COLS[(i + 1) % 6], r=6 * u)


def it_triangle(p, x, b, s, i=0):
    u = s / 100
    p.poly([(x - 50 * u, b), (x + 50 * u, b), (x, b - 86 * u)], COLS[(i + 2) % 6])


def it_rectangle(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 56 * u, b - 66 * u, 112 * u, 66 * u, COLS[(i + 3) % 6], r=6 * u)


def it_toothbrush(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 7 * u, b - 62 * u, 14 * u, 62 * u, BLUE, r=7 * u); p.rect(x - 13 * u, b - 104 * u, 26 * u, 46 * u, WHITE, r=6 * u)
    for dy in (-98, -84, -70):
        p.rect(x - 9 * u, b + dy * u, 18 * u, 8 * u, LEAF, r=3 * u)


def it_tooth(p, x, b, s, i=0):
    u = s / 100
    p.circle(x - 20 * u, b - 62 * u, 26 * u, WHITE); p.circle(x + 20 * u, b - 62 * u, 26 * u, WHITE)
    p.rect(x - 38 * u, b - 62 * u, 76 * u, 38 * u, WHITE); p.rect(x - 32 * u, b - 30 * u, 24 * u, 30 * u, WHITE, r=10 * u)
    p.rect(x + 8 * u, b - 30 * u, 24 * u, 30 * u, WHITE, r=10 * u)
    p.circle(x - 10 * u, b - 64 * u, 4 * u, DARK); p.circle(x + 10 * u, b - 64 * u, 4 * u, DARK)


def it_soap(p, x, b, s, i=0):
    u = s / 100
    for dx, dy, r in [(-22, -30, 28), (20, -48, 22), (4, -84, 16), (30, -18, 14)]:
        p.circle(x + dx * u, b + dy * u, r * u, "#BDE0FE", .7)
        p.circle(x + (dx - r * .3) * u, b + (dy - r * .3) * u, r * .22 * u, WHITE)


def it_towel(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 34 * u, b - 90 * u, 68 * u, 90 * u, PINK, r=6 * u)
    for dy in (-70, -50):
        p.rect(x - 34 * u, b + dy * u, 68 * u, 8 * u, WHITE)


def it_bin(p, x, b, s, i=0):
    u = s / 100
    p.poly([(x - 36 * u, b - 74 * u), (x + 36 * u, b - 74 * u), (x + 28 * u, b), (x - 28 * u, b)], LEAF)
    p.rect(x - 42 * u, b - 88 * u, 84 * u, 16 * u, "#3E8E5A", r=6 * u)


def it_book(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 40 * u, b - 80 * u, 80 * u, 80 * u, COLS[i % 6], r=6 * u)
    p.rect(x - 30 * u, b - 70 * u, 64 * u, 60 * u, WHITE, r=3 * u); p.rect(x - 40 * u, b - 80 * u, 12 * u, 80 * u, DARK, r=4 * u, alpha=.25)


def it_shoe(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 46 * u, b - 14 * u, 92 * u, 14 * u, DARK, r=6 * u)
    p.poly([(x - 40 * u, b - 14 * u), (x - 40 * u, b - 56 * u), (x - 8 * u, b - 56 * u), (x + 46 * u, b - 14 * u)], BLUE)
    p.circle(x - 4 * u, b - 36 * u, 4 * u, WHITE)


def it_sock(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 22 * u, b - 86 * u, 44 * u, 66 * u, PURPLE, r=10 * u); p.ellipse(x + 8 * u, b - 20 * u, 38 * u, 20 * u, PURPLE)
    p.rect(x - 22 * u, b - 86 * u, 44 * u, 12 * u, WHITE, r=4 * u)


def it_hat(p, x, b, s, i=0):
    u = s / 100
    p.wedge(x, b - 22 * u, 40 * u, 0, 180, YELLOW); p.ellipse(x, b - 22 * u, 62 * u, 12 * u, YELLOW)
    p.rect(x - 40 * u, b - 30 * u, 80 * u, 8 * u, RED)


def it_bed(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 60 * u, b - 56 * u, 120 * u, 56 * u, BROWN, r=8 * u); p.rect(x - 54 * u, b - 52 * u, 108 * u, 30 * u, WHITE, r=8 * u)
    p.rect(x - 14 * u, b - 52 * u, 68 * u, 30 * u, BLUE, r=8 * u); p.rect(x - 52 * u, b - 76 * u, 34 * u, 22 * u, "#E8EEF3", r=10 * u)


def it_clock(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 48 * u, 48 * u, DARK); p.circle(x, b - 48 * u, 41 * u, WHITE)
    p.line(x, b - 48 * u, x, b - 78 * u, DARK, 5 * u); p.line(x, b - 48 * u, x + 22 * u, b - 38 * u, RED, 5 * u)
    p.circle(x, b - 48 * u, 4 * u, DARK)


def it_coin(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 40 * u, 40 * u, "#F4C430"); p.circle(x, b - 40 * u, 31 * u, "#FFE17D")
    p.text(x, b - 28 * u, "1", "Helvetica-Bold", 44 * u, "#B8860B")


def it_car(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 56 * u, b - 52 * u, 112 * u, 36 * u, COLS[i % 6], r=14 * u); p.rect(x - 32 * u, b - 76 * u, 64 * u, 34 * u, COLS[i % 6], r=12 * u)
    p.rect(x - 24 * u, b - 70 * u, 20 * u, 20 * u, "#DDF0FF"); p.rect(x + 2 * u, b - 70 * u, 20 * u, 20 * u, "#DDF0FF")
    p.circle(x - 30 * u, b - 14 * u, 15 * u, DARK); p.circle(x + 30 * u, b - 14 * u, 15 * u, DARK)


def it_bus(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 64 * u, b - 76 * u, 128 * u, 58 * u, ORANGE, r=12 * u)
    for dx in (-48, -20, 8, 36):
        p.rect(x + dx * u, b - 68 * u, 22 * u, 22 * u, "#DDF0FF")
    p.circle(x - 38 * u, b - 16 * u, 15 * u, DARK); p.circle(x + 38 * u, b - 16 * u, 15 * u, DARK)


def it_house(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 42 * u, b - 58 * u, 84 * u, 58 * u, YELLOW); p.poly([(x - 52 * u, b - 58 * u), (x, b - 100 * u), (x + 52 * u, b - 58 * u)], RED)
    p.rect(x - 9 * u, b - 34 * u, 18 * u, 34 * u, BROWN)


def it_drop(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 32 * u, 30 * u, BLUE); p.poly([(x - 28 * u, b - 42 * u), (x + 28 * u, b - 42 * u), (x, b - 94 * u)], BLUE)


def it_bandage(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 56 * u, b - 52 * u, 112 * u, 38 * u, "#F2C29B", r=19 * u); p.rect(x - 20 * u, b - 52 * u, 40 * u, 38 * u, "#E0A97C")


def it_lightbulb(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 62 * u, 32 * u, YELLOW); p.rect(x - 16 * u, b - 34 * u, 32 * u, 28 * u, "#ADB5BD", r=5 * u)
    for a in (-60, 0, 60):
        r = math.radians(a - 90)
        p.line(x + 42 * u * math.cos(r), b - 62 * u + 42 * u * math.sin(r),
               x + 58 * u * math.cos(r), b - 62 * u + 58 * u * math.sin(r), ORANGE, 5 * u)


def it_recycle(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 48 * u, 48 * u, LEAF)
    for k in range(3):
        a = math.radians(-90 + k * 120)
        cx, cy = x + 26 * u * math.cos(a), b - 48 * u + 26 * u * math.sin(a)
        p.poly([(cx + 16 * u * math.cos(a + 2.1), cy + 16 * u * math.sin(a + 2.1)),
                (cx + 16 * u * math.cos(a - 2.1), cy + 16 * u * math.sin(a - 2.1)),
                (cx + 20 * u * math.cos(a), cy + 20 * u * math.sin(a))], WHITE)


def it_teddy(p, x, b, s, i=0):
    u = s / 100
    p.circle(x - 24 * u, b - 92 * u, 12 * u, BROWN); p.circle(x + 24 * u, b - 92 * u, 12 * u, BROWN)
    p.ellipse(x, b - 36 * u, 34 * u, 36 * u, BROWN); p.circle(x, b - 76 * u, 28 * u, BROWN); p.ellipse(x, b - 66 * u, 12 * u, 9 * u, TAN)
    p.circle(x - 10 * u, b - 82 * u, 3.5 * u, DARK); p.circle(x + 10 * u, b - 82 * u, 3.5 * u, DARK); p.circle(x, b - 70 * u, 4 * u, DARK)


def it_balloon(p, x, b, s, i=0):
    u = s / 100
    p.line(x, b - 56 * u, x + 6 * u, b, "#ADB5BD", 3 * u); p.ellipse(x, b - 76 * u, 30 * u, 38 * u, COLS[i % 6])


def it_gift(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 40 * u, b - 66 * u, 80 * u, 66 * u, COLS[i % 6], r=6 * u); p.rect(x - 6 * u, b - 66 * u, 12 * u, 66 * u, WHITE)
    p.circle(x - 12 * u, b - 76 * u, 12 * u, WHITE); p.circle(x + 12 * u, b - 76 * u, 12 * u, WHITE)


def it_door(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 34 * u, b - 100 * u, 68 * u, 100 * u, BROWN, r=8 * u); p.circle(x + 20 * u, b - 48 * u, 5 * u, YELLOW)


def it_pencil(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 11 * u, b - 84 * u, 22 * u, 66 * u, YELLOW); p.poly([(x - 11 * u, b - 18 * u), (x + 11 * u, b - 18 * u), (x, b)], TAN)
    p.rect(x - 11 * u, b - 100 * u, 22 * u, 16 * u, PINK, r=4 * u)


def it_crayon(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 11 * u, b - 76 * u, 22 * u, 76 * u, COLS[i % 6], r=4 * u)
    p.poly([(x - 11 * u, b - 76 * u), (x + 11 * u, b - 76 * u), (x, b - 96 * u)], COLS[i % 6])


def it_hand(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 36 * u, 34 * u, 32 * u, "#F2C29B")
    for k, dx in enumerate((-30, -15, 0, 15, 30)):
        h = 52 + (8 if k in (1, 2, 3) else 0)
        p.line(x + dx * u, b - 44 * u, x + dx * 1.15 * u, b - h * u - 40 * u, "#F2C29B", 13 * u)


def it_eye(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 38 * u, 50 * u, 30 * u, WHITE); p.circle(x, b - 38 * u, 20 * u, BLUE); p.circle(x, b - 38 * u, 9 * u, DARK)


def it_tap(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 8 * u, b - 96 * u, 16 * u, 56 * u, "#ADB5BD"); p.rect(x - 8 * u, b - 96 * u, 54 * u, 16 * u, "#ADB5BD", r=6 * u)
    p.circle(x + 38 * u, b - 28 * u, 8 * u, BLUE); p.circle(x + 38 * u, b - 8 * u, 6 * u, BLUE)


def it_cloud(p, x, b, s, i=0):
    cloud(p, x, b - 50 * s / 100, s / 120)


def it_sun(p, x, b, s, i=0):
    sun(p, x, b - 56 * s / 100, 34 * s / 100)


def it_moon(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 50 * u, 44 * u, YELLOW); p.circle(x + 18 * u, b - 58 * u, 38 * u, "#28386B")


def it_umbrella(p, x, b, s, i=0):
    u = s / 100
    p.line(x, b - 60 * u, x, b - 8 * u, DARK, 5 * u); p.curve(x, b - 8 * u, x + 4 * u, b + 6 * u, x + 16 * u, b - 6 * u, DARK, 5 * u)
    p.wedge(x, b - 60 * u, 52 * u, 0, 180, RED); p.line(x, b - 112 * u, x, b - 60 * u, "#FFFFFF", 3 * u, )


def it_puddle(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 10 * u, 62 * u, 14 * u, "#8FCBEE"); p.ellipse(x - 14 * u, b - 12 * u, 24 * u, 5 * u, WHITE, .6)


def it_mitten(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 28 * u, b - 84 * u, 56 * u, 74 * u, RED, r=26 * u); p.ellipse(x - 32 * u, b - 46 * u, 12 * u, 20 * u, RED)
    p.rect(x - 28 * u, b - 28 * u, 56 * u, 18 * u, WHITE, r=6 * u)


def it_coat(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 38 * u, b - 88 * u, 76 * u, 88 * u, COLS[i % 6], r=14 * u)
    p.line(x - 38 * u, b - 76 * u, x - 56 * u, b - 30 * u, COLS[i % 6], 22 * u); p.line(x + 38 * u, b - 76 * u, x + 56 * u, b - 30 * u, COLS[i % 6], 22 * u)
    p.line(x, b - 88 * u, x, b, WHITE, 4 * u)
    for dy in (-60, -40, -20):
        p.circle(x + 10 * u, b + dy * u, 3 * u, WHITE)


def it_snowflake(p, x, b, s, i=0):
    u = s / 100
    for k in range(3):
        a = k * math.pi / 3
        p.line(x - 44 * u * math.cos(a), b - 48 * u - 44 * u * math.sin(a), x + 44 * u * math.cos(a), b - 48 * u + 44 * u * math.sin(a), "#7FB8E0", 7 * u)


def it_egg(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 40 * u, 28 * u, 38 * u, "#FBE3C4"); p.ellipse(x - 8 * u, b - 52 * u, 6 * u, 10 * u, WHITE, .6)


def it_chicken(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 36 * u, 40 * u, 32 * u, WHITE); p.circle(x + 28 * u, b - 70 * u, 18 * u, WHITE)
    p.circle(x + 26 * u, b - 92 * u, 7 * u, RED); p.circle(x + 36 * u, b - 90 * u, 6 * u, RED)
    p.poly([(x + 44 * u, b - 72 * u), (x + 62 * u, b - 66 * u), (x + 44 * u, b - 62 * u)], ORANGE); p.circle(x + 32 * u, b - 74 * u, 3.5 * u, DARK)
    p.line(x - 6 * u, b - 6 * u, x - 6 * u, b, ORANGE, 5 * u); p.line(x + 10 * u, b - 6 * u, x + 10 * u, b, ORANGE, 5 * u)


def it_cow(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 52 * u, b - 74 * u, 100 * u, 52 * u, WHITE, r=14 * u)
    for dx in (-36, -8, 24, 42):
        p.rect(x + dx * u - 5 * u, b - 24 * u, 10 * u, 24 * u, DARK, r=3 * u)
    p.circle(x - 22 * u, b - 56 * u, 12 * u, DARK); p.circle(x + 14 * u, b - 46 * u, 10 * u, DARK)
    p.rect(x + 36 * u, b - 96 * u, 36 * u, 38 * u, WHITE, r=12 * u); p.rect(x + 44 * u, b - 70 * u, 26 * u, 14 * u, PINK, r=6 * u)
    p.circle(x + 46 * u, b - 84 * u, 3.5 * u, DARK)


def it_worm(p, x, b, s, i=0):
    u = s / 100
    p.curve(x - 50 * u, b - 20 * u, x - 25 * u, b - 56 * u, x, b - 20 * u, PINK, 14 * u); p.curve(x, b - 20 * u, x + 25 * u, b + 16 * u, x + 50 * u, b - 20 * u, PINK, 14 * u)
    p.circle(x + 50 * u, b - 22 * u, 3 * u, DARK)


def it_spider(p, x, b, s, i=0):
    u = s / 100
    for k in range(4):
        dy = -30 + k * 14
        p.line(x - 12 * u, b - 46 * u, x - 52 * u, b + dy * u - 40 * u, DARK, 4 * u); p.line(x + 12 * u, b - 46 * u, x + 52 * u, b + dy * u - 40 * u, DARK, 4 * u)
    p.circle(x, b - 46 * u, 20 * u, DARK); p.circle(x, b - 70 * u, 12 * u, DARK)


def it_snail(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 10 * u, 56 * u, 12 * u, TAN); p.circle(x - 6 * u, b - 44 * u, 36 * u, "#C97B4A"); p.circle(x - 6 * u, b - 44 * u, 22 * u, "#E0A06E")
    p.circle(x - 6 * u, b - 44 * u, 9 * u, "#C97B4A"); p.line(x + 46 * u, b - 14 * u, x + 54 * u, b - 46 * u, TAN, 6 * u); p.circle(x + 54 * u, b - 48 * u, 5 * u, DARK)


def it_giraffe(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 18 * u, b - 120 * u, 26 * u, 80 * u, YELLOW, r=10 * u); p.ellipse(x, b - 36 * u, 34 * u, 24 * u, YELLOW)
    p.ellipse(x + 8 * u, b - 124 * u, 26 * u, 16 * u, YELLOW)
    for dx in (-22, 22):
        p.rect(x + dx * u - 4 * u, b - 24 * u, 8 * u, 24 * u, YELLOW)
    for dx, dy in [(-4, -90), (2, -66), (-14, -40), (16, -36)]:
        p.circle(x + dx * u, b + dy * u, 5 * u, "#C97B4A")
    p.circle(x + 16 * u, b - 128 * u, 3 * u, DARK)


def it_elephant(p, x, b, s, i=0):
    u = s / 100
    g = "#ADB5BD"
    p.ellipse(x - 10 * u, b - 46 * u, 46 * u, 34 * u, g); p.circle(x + 36 * u, b - 62 * u, 26 * u, g)
    p.curve(x + 54 * u, b - 52 * u, x + 70 * u, b - 14 * u, x + 54 * u, b - 8 * u, g, 12 * u); p.ellipse(x + 20 * u, b - 62 * u, 14 * u, 20 * u, "#8D99AE")
    p.circle(x + 42 * u, b - 68 * u, 3.5 * u, DARK)
    for dx in (-36, 6):
        p.rect(x + dx * u - 6 * u, b - 24 * u, 14 * u, 24 * u, g, r=4 * u)


def it_owl(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 44 * u, 36 * u, 44 * u, BROWN); p.ellipse(x, b - 36 * u, 22 * u, 28 * u, TAN)
    for dx in (-14, 14):
        p.circle(x + dx * u, b - 62 * u, 13 * u, WHITE); p.circle(x + dx * u, b - 62 * u, 6 * u, DARK)
    p.poly([(x - 5 * u, b - 52 * u), (x + 5 * u, b - 52 * u), (x, b - 42 * u)], ORANGE)
    p.poly([(x - 30 * u, b - 84 * u), (x - 20 * u, b - 96 * u), (x - 12 * u, b - 84 * u)], BROWN); p.poly([(x + 30 * u, b - 84 * u), (x + 20 * u, b - 96 * u), (x + 12 * u, b - 84 * u)], BROWN)


def it_bear(p, x, b, s, i=0):
    u = s / 100
    br = "#6B4226"
    p.circle(x - 24 * u, b - 92 * u, 12 * u, br); p.circle(x + 24 * u, b - 92 * u, 12 * u, br)
    p.ellipse(x, b - 36 * u, 38 * u, 36 * u, br); p.circle(x, b - 76 * u, 28 * u, br); p.ellipse(x, b - 66 * u, 13 * u, 10 * u, TAN)
    p.circle(x - 10 * u, b - 82 * u, 3.5 * u, DARK); p.circle(x + 10 * u, b - 82 * u, 3.5 * u, DARK); p.circle(x, b - 70 * u, 4 * u, DARK)


def it_caterpillar(p, x, b, s, i=0):
    u = s / 100
    for k in range(5):
        p.circle(x - 48 * u + k * 24 * u, b - 24 * u - (6 * u if k % 2 else 0), 16 * u, LEAF if k else "#3E8E5A")
    p.circle(x + 54 * u, b - 28 * u, 4 * u, DARK)


def it_sprout(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 8 * u, 52 * u, 12 * u, BROWN); p.line(x, b - 10 * u, x, b - 62 * u, "#3E8E5A", 7 * u)
    p.ellipse(x - 20 * u, b - 66 * u, 20 * u, 10 * u, LEAF); p.ellipse(x + 20 * u, b - 74 * u, 20 * u, 10 * u, LEAF)


def it_seed(p, x, b, s, i=0):
    u = s / 100
    for dx, dy in [(-22, -18), (4, -26), (24, -12)]:
        p.ellipse(x + dx * u, b + dy * u, 10 * u, 16 * u, BROWN)


def it_bike(p, x, b, s, i=0):
    u = s / 100
    for dx in (-40, 40):
        p.circle(x + dx * u, b - 32 * u, 32 * u, DARK); p.circle(x + dx * u, b - 32 * u, 26 * u, "#FFF8EC")
    p.line(x - 40 * u, b - 32 * u, x - 6 * u, b - 70 * u, RED, 6 * u); p.line(x - 6 * u, b - 70 * u, x + 40 * u, b - 32 * u, RED, 6 * u)
    p.line(x - 40 * u, b - 32 * u, x + 4 * u, b - 32 * u, RED, 6 * u); p.line(x + 4 * u, b - 32 * u, x - 6 * u, b - 70 * u, RED, 6 * u)
    p.line(x + 28 * u, b - 76 * u, x + 40 * u, b - 32 * u, DARK, 5 * u); p.line(x + 22 * u, b - 78 * u, x + 38 * u, b - 76 * u, DARK, 5 * u)


def it_plane(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 50 * u, 62 * u, 16 * u, WHITE); p.poly([(x - 10 * u, b - 52 * u), (x + 14 * u, b - 52 * u), (x - 22 * u, b - 92 * u)], "#ADB5BD")
    p.poly([(x - 10 * u, b - 48 * u), (x + 14 * u, b - 48 * u), (x - 22 * u, b - 10 * u)], "#ADB5BD")
    p.poly([(x - 56 * u, b - 54 * u), (x - 44 * u, b - 54 * u), (x - 54 * u, b - 76 * u)], BLUE)
    for dx in (-8, 8, 24, 38):
        p.circle(x + dx * u, b - 52 * u, 3.5 * u, BLUE)


def it_seesaw(p, x, b, s, i=0):
    u = s / 100
    p.poly([(x - 14 * u, b), (x + 14 * u, b), (x, b - 34 * u)], "#ADB5BD")
    p.poly([(x - 62 * u, b - 52 * u), (x - 58 * u, b - 64 * u), (x + 62 * u, b - 24 * u), (x + 58 * u, b - 12 * u)], ORANGE)
    p.circle(x - 56 * u, b - 74 * u, 9 * u, BLUE); p.circle(x + 56 * u, b - 8 * u, 0.1, BLUE)


def it_magnet(p, x, b, s, i=0):
    u = s / 100
    p.line(x - 34 * u, b - 78 * u, x - 34 * u, b - 46 * u, RED, 24 * u); p.line(x + 34 * u, b - 78 * u, x + 34 * u, b - 46 * u, RED, 24 * u)
    p.curve(x - 34 * u, b - 46 * u, x, b + 30 * u, x + 34 * u, b - 46 * u, RED, 24 * u)
    p.rect(x - 46 * u, b - 98 * u, 24 * u, 20 * u, "#ADB5BD"); p.rect(x + 22 * u, b - 98 * u, 24 * u, 20 * u, "#ADB5BD")


def it_battery(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 14 * u, b - 96 * u, 28 * u, 14 * u, "#ADB5BD", r=3 * u); p.rect(x - 24 * u, b - 84 * u, 48 * u, 84 * u, DARK, r=8 * u)
    p.rect(x - 24 * u, b - 60 * u, 48 * u, 24 * u, ORANGE); p.text(x, b - 40 * u, "+", "Helvetica-Bold", 26 * u, WHITE)


def it_mirror(p, x, b, s, i=0):
    u = s / 100
    p.ellipse(x, b - 52 * u, 42 * u, 52 * u, BROWN); p.ellipse(x, b - 52 * u, 34 * u, 44 * u, "#DDF0FF"); p.line(x - 14 * u, b - 76 * u, x - 4 * u, b - 92 * u, WHITE, 6 * u)


def it_tissue(p, x, b, s, i=0):
    u = s / 100
    p.poly([(x - 8 * u, b - 48 * u), (x + 20 * u, b - 48 * u), (x + 34 * u, b - 98 * u), (x - 2 * u, b - 84 * u)], WHITE)
    p.rect(x - 44 * u, b - 52 * u, 88 * u, 52 * u, BLUE, r=8 * u); p.rect(x - 22 * u, b - 52 * u, 44 * u, 8 * u, DARK, alpha=.35)


def it_comb(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 46 * u, b - 74 * u, 92 * u, 22 * u, PURPLE, r=8 * u)
    for k in range(9):
        p.line(x - 40 * u + k * 10 * u, b - 52 * u, x - 40 * u + k * 10 * u, b - 18 * u, PURPLE, 5 * u)


def it_laundry(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 44 * u, b - 92 * u, 88 * u, 92 * u, WHITE, r=10 * u); p.circle(x, b - 44 * u, 28 * u, "#ADB5BD"); p.circle(x, b - 44 * u, 22 * u, BLUE)
    p.circle(x - 28 * u, b - 76 * u, 5 * u, RED); p.circle(x - 14 * u, b - 76 * u, 5 * u, YELLOW)


def it_bread(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 52 * u, b - 56 * u, 104 * u, 56 * u, TAN, r=26 * u)
    for dx in (-26, 0, 26):
        p.line(x + dx * u - 6 * u, b - 44 * u, x + dx * u + 6 * u, b - 24 * u, "#B87333", 5 * u)


def it_firetruck(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 64 * u, b - 64 * u, 128 * u, 44 * u, RED, r=8 * u); p.rect(x + 22 * u, b - 84 * u, 42 * u, 36 * u, RED, r=8 * u)
    p.rect(x + 34 * u, b - 78 * u, 22 * u, 20 * u, "#DDF0FF")
    p.line(x - 56 * u, b - 76 * u, x + 8 * u, b - 76 * u, "#ADB5BD", 6 * u)
    p.circle(x - 36 * u, b - 18 * u, 15 * u, DARK); p.circle(x + 38 * u, b - 18 * u, 15 * u, DARK)


def it_letter(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 50 * u, b - 74 * u, 100 * u, 70 * u, WHITE, r=6 * u)
    p.line(x - 50 * u, b - 74 * u, x, b - 38 * u, "#ADB5BD", 4 * u); p.line(x + 50 * u, b - 74 * u, x, b - 38 * u, "#ADB5BD", 4 * u)
    p.rect(x + 22 * u, b - 68 * u, 22 * u, 22 * u, RED, r=4 * u)


def it_mailbox(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 6 * u, b - 40 * u, 12 * u, 40 * u, BROWN); p.rect(x - 40 * u, b - 84 * u, 80 * u, 50 * u, BLUE, r=22 * u)
    p.rect(x + 34 * u, b - 98 * u, 8 * u, 38 * u, RED)


def it_ruler(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 60 * u, b - 36 * u, 120 * u, 36 * u, YELLOW, r=4 * u)
    for k in range(11):
        p.line(x - 54 * u + k * 10.8 * u, b - 36 * u, x - 54 * u + k * 10.8 * u, b - (20 if k % 2 == 0 else 10) * u - 6 * u, DARK, 2.5 * u)


def it_hammer(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 7 * u, b - 84 * u, 14 * u, 84 * u, BROWN, r=4 * u); p.rect(x - 36 * u, b - 100 * u, 72 * u, 24 * u, "#ADB5BD", r=6 * u)


def it_medicine(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 26 * u, b - 76 * u, 52 * u, 76 * u, "#E8B77A", r=8 * u); p.rect(x - 22 * u, b - 92 * u, 44 * u, 20 * u, WHITE, r=5 * u)
    p.rect(x - 20 * u, b - 56 * u, 40 * u, 28 * u, WHITE, r=3 * u)


def it_rainbow(p, x, b, s, i=0):
    u = s / 100
    for k, c in enumerate([RED, ORANGE, YELLOW, LEAF, BLUE]):
        p.wedge(x, b - 10 * u, (56 - k * 9) * u, 0, 180, c)
    p.wedge(x, b - 10 * u, 11 * u, 0, 180, "#FFF8EC")


def it_fireworks(p, x, b, s, i=0):
    u = s / 100
    for k in range(8):
        a = k * math.pi / 4
        p.line(x + 14 * u * math.cos(a), b - 56 * u + 14 * u * math.sin(a), x + 44 * u * math.cos(a), b - 56 * u + 44 * u * math.sin(a), COLS[(i + k) % 6], 6 * u)


def it_candle(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 9 * u, b - 56 * u, 18 * u, 56 * u, BLUE, r=3 * u); p.ellipse(x, b - 70 * u, 7 * u, 12 * u, YELLOW)


def it_basket(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 46 * u, b - 52 * u, 92 * u, 52 * u, "#C9A27A", r=12 * u); p.curve(x - 40 * u, b - 52 * u, x, b - 120 * u, x + 40 * u, b - 52 * u, "#B8895A", 7 * u)
    for dx in (-24, 0, 24):
        p.line(x + dx * u, b - 48 * u, x + dx * u, b - 6 * u, "#B8895A", 4 * u)


def it_speech(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 52 * u, b - 84 * u, 104 * u, 64 * u, WHITE, r=26 * u); p.poly([(x - 22 * u, b - 24 * u), (x - 4 * u, b - 24 * u), (x - 30 * u, b - 2 * u)], WHITE)
    for dx in (-24, 0, 24):
        p.circle(x + dx * u, b - 52 * u, 6 * u, DARK)


def it_globe(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 50 * u, 48 * u, BLUE); p.ellipse(x - 14 * u, b - 62 * u, 20 * u, 14 * u, LEAF); p.ellipse(x + 16 * u, b - 36 * u, 14 * u, 22 * u, LEAF)


def it_bubble(p, x, b, s, i=0):
    u = s / 100
    p.circle(x, b - 46 * u, 44 * u, "#BDE0FE", .55); p.circle(x - 16 * u, b - 62 * u, 8 * u, WHITE)


def it_toy_train(p, x, b, s, i=0):
    u = s / 100
    p.rect(x - 52 * u, b - 48 * u, 70 * u, 34 * u, RED, r=8 * u); p.rect(x + 14 * u, b - 64 * u, 36 * u, 50 * u, BLUE, r=8 * u)
    for dx in (-34, -4, 30):
        p.circle(x + dx * u, b - 12 * u, 11 * u, DARK)



ITEMS = {n[3:]: f for n, f in globals().items() if n.startswith("it_")}


# ------------------------------------------------------------ backgrounds
def _sky(p, top="#A8D5F5"):
    p.rect(0, 0, S, S, top); sun(p, 660, 130, 52); cloud(p, 220, 150, .8); ground(p, 500, GREEN)


def bg_sky(p):
    _sky(p)


def bg_park(p):
    _sky(p); p.rect(60, 330, 24, 170, BROWN); p.circle(72, 300, 70, LEAF)


def bg_night(p):
    p.rect(0, 0, S, S, "#28386B")
    for x, y, r in [(100, 90, 20), (330, 60, 14), (560, 110, 22), (700, 60, 14), (210, 220, 12), (660, 260, 16)]:
        star(p, x, y, r)
    p.rect(0, 520, S, 280, "#2F5D50")


def bg_kitchen(p):
    p.rect(0, 0, S, S, "#FFF0D4"); p.rect(80, 90, 200, 200, "#BDE0FE", r=12); p.line(180, 90, 180, 290, WHITE, 8)
    p.rect(0, 400, S, 70, "#C9A27A"); p.rect(0, 470, S, 330, "#E9C99B")


def bg_bath(p):
    p.rect(0, 0, S, S, "#D8F0F7")
    for x in range(0, S, 100):
        p.line(x, 0, x, 500, WHITE, 3)
    for y in range(0, 500, 100):
        p.line(0, y, S, y, WHITE, 3)
    p.rect(0, 500, S, 300, "#BFE3EE")


def bg_bedroom(p):
    p.rect(0, 0, S, S, "#E8E1FF"); p.rect(540, 80, 190, 220, "#28386B", r=14)
    p.circle(620, 160, 34, YELLOW); star(p, 680, 240, 14); p.rect(0, 500, S, 300, "#C9B8F0")


def bg_shop(p):
    p.rect(0, 0, S, S, "#FFF3C4")
    for k in range(8):
        p.rect(k * 100, 0, 100, 90, RED if k % 2 == 0 else WHITE)
    p.rect(0, 500, S, 300, "#E7C873")


def bg_plain(p):
    p.rect(0, 0, S, S, "#FFF8EC"); p.rect(0, 520, S, 280, "#F5E6CC")


def bg_water(p):
    p.rect(0, 0, S, 330, "#BDE0FE"); sun(p, 650, 120, 48); p.rect(0, 330, S, 470, BLUE)
    for y in (400, 520, 640):
        for x in range(0, S, 160):
            p.curve(x + 20, y, x + 80, y - 26, x + 140, y, "#8FCBEE", 8)


def bg_snow(p):
    p.rect(0, 0, S, S, "#DCEBF7"); ground(p, 520, WHITE)
    for i in range(16):
        p.circle((i * 97) % 760 + 20, (i * 61) % 400 + 20, 6 + i % 3 * 3, WHITE)


def bg_rainy(p):
    p.rect(0, 0, S, S, "#9DB4C8"); cloud(p, 300, 140, 1.3, "#E8EEF3"); cloud(p, 580, 210, .8, "#E8EEF3")
    for i in range(12):
        p.line(150 + i * 50, 300 + (i % 3) * 40, 138 + i * 50, 340 + (i % 3) * 40, BLUE, 7)
    ground(p, 540, "#7FB37C")


def bg_hearts(p):
    p.rect(0, 0, S, S, "#FFD6E0"); p.rect(0, 540, S, 260, "#FFAFCC")
    heart(p, 140, 120, 60, "#F28482"); heart(p, 660, 150, 80, "#F28482"); heart(p, 400, 70, 44, "#F28482")


def bg_play(p):
    p.rect(0, 0, S, S, "#E1F0C8"); ground(p, 500); sun(p, 680, 110, 44)


def bg_street(p):
    p.rect(0, 0, S, S, "#DDEAF5"); sun(p, 110, 110, 45)
    p.rect(110, 300, 210, 160, "#F4D35E"); p.poly([(85, 300), (215, 190), (345, 300)], RED)
    p.rect(185, 360, 55, 100, BROWN); p.rect(130, 320, 40, 40, "#BDE0FE"); p.rect(270, 320, 40, 40, "#BDE0FE")
    p.rect(560, 130, 130, 330, "#8D99AE")
    for yy in range(150, 440, 50):
        for xx in (575, 615, 655):
            p.rect(xx, yy, 24, 30, YELLOW)
    p.rect(0, 460, S, 130, "#CED4DA"); p.rect(0, 590, S, 210, "#ADB5BD")
    for x in range(40, S, 200):
        p.rect(x, 680, 110, 12, WHITE)


BGS = {n[3:]: f for n, f in globals().items() if n.startswith("bg_")}
FLOOR = {}  # per-background override; default keeps items above the question panel (y < 560)
DEFAULT_FLOOR = 555
KID_TOKENS = ("kid", "kid2", "kids")
ROW = "row"  # starts a new row of items (for showing groups side by side)
FLOAT = {"cloud", "sun", "moon", "fireworks", "rainbow"}  # drawn up in the sky


def parse_scene(spec: str):
    """'kitchen|kid,apple*3' -> ('kitchen', [('kid', 1), ('apple', 3)]); classic names -> (name, None)."""
    if "|" not in spec:
        if spec not in SCENES:
            raise ValueError(f"unknown scene {spec!r}")
        return spec, None
    base, _, rest = spec.partition("|")
    if base not in BGS:
        raise ValueError(f"unknown background {base!r}")
    toks = []
    for part in [t.strip() for t in rest.split(",") if t.strip()]:
        full, _, n = part.partition("*")
        name = full.split(":")[0]
        if name not in ITEMS and name not in KID_TOKENS and name != ROW:
            raise ValueError(f"unknown item {name!r}")
        count = int(n) if n else 1
        if not 1 <= count <= 12:
            raise ValueError(f"bad count in {part!r}")
        toks.append((full, count))
    if not toks:
        raise ValueError(f"stage scene {spec!r} has nothing on it")
    return base, toks


def scene_ok(spec: str) -> bool:
    try:
        parse_scene(spec)
        return True
    except (ValueError, AttributeError):
        return False


def draw_scene(p: Pen, spec: str, hero: Hero) -> None:
    base, toks = parse_scene(spec)
    if toks is None:
        SCENES[base](p, hero, CAST)
        return
    BGS[base](p)
    floor = FLOOR.get(base, DEFAULT_FLOOR)
    other = CAST[(CAST.index(hero) + 1) % len(CAST)]
    kids, groups = [], [[]]
    for full, count in toks:
        kind, _, mood = full.partition(":")
        if kind == "kid":
            kids.append((hero, mood or "smile"))
        elif kind == "kid2":
            kids.append((other, mood or "smile"))
        elif kind == "kids":
            kids += [(hero, mood or "smile"), (other, mood or "smile")]
        elif kind == ROW:
            groups.append([])
        else:
            groups[-1] += [kind] * count
    groups = [g for g in groups if g]
    if len(groups) == 1 and len(groups[0]) > 6:  # split a long run evenly into rows of at most 6
        n = len(groups[0]); rows = -(-n // 6); per = -(-n // rows)
        groups = [groups[0][i:i + per] for i in range(0, n, per)]
    xs = {1: [210], 2: [160, 330]}.get(len(kids), [])
    for (h, mood), kx in zip(kids, xs):
        child(p, kx, floor, h, 1.0, mood)
    left = 80 if not kids else (450 if len(kids) == 1 else 520)
    if not groups:
        return
    rows = len(groups)
    widest = max(len(g) for g in groups)
    region = (S - 50) - left
    size = min((200 if widest <= 2 else 165 if widest <= 4 else 140) if rows == 1 else 115, region / widest * .85)
    k = 0
    for r, row in enumerate(groups):
        by = floor - (rows - 1 - r) * (size + 40)
        for c, name in enumerate(row):
            cx = left + region / 2 + (c - (len(row) - 1) / 2) * region / widest
            ITEMS[name](p, cx, 300 + (k % 2) * 50 if name in FLOAT else by, size, k)
            k += 1
