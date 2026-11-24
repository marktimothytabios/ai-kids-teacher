"""Illustration kit: flat vector scenes drawn with ReportLab.

All drawing happens in an 800 x 800 design space with the origin at the TOP-left, like the
first book. ``Pen`` converts to ReportLab's bottom-left coordinates.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from reportlab.lib.colors import HexColor

S = 800  # design size

DARK = "#2B2D42"
ORANGE = "#FF9F1C"
YELLOW = "#FFD23F"
BLUE = "#4EA8DE"
GREEN = "#8FD18A"
RED = "#E63946"
PINK = "#F28482"
PURPLE = "#A06CD5"
WHITE = "#FFFFFF"


@dataclass(frozen=True)
class Hero:
    name: str
    skin: str
    hair: str
    shirt: str


CAST = [
    Hero("Mia", "#F2C29B", "#6B4226", PINK),
    Hero("Ben", "#C68642", "#2B2D42", BLUE),
    Hero("Zara", "#8D5524", "#1B1B1E", PURPLE),
    Hero("Leo", "#F5CBA7", "#C58B3F", "#52B788"),
]


def hero_for(volume: int, order: int) -> Hero:
    return CAST[(volume + order) % len(CAST)]


class Pen:
    def __init__(self, c):
        self.c = c

    def _fill(self, color, alpha=1.0):
        col = HexColor(color)
        self.c.setFillColor(col)
        self.c.setFillAlpha(alpha)

    def rect(self, x, y, w, h, color, r=0, alpha=1.0):
        self._fill(color, alpha)
        if r:
            self.c.roundRect(x, S - y - h, w, h, r, stroke=0, fill=1)
        else:
            self.c.rect(x, S - y - h, w, h, stroke=0, fill=1)

    def circle(self, x, y, r, color, alpha=1.0):
        self._fill(color, alpha)
        self.c.circle(x, S - y, r, stroke=0, fill=1)

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        self._fill(color, alpha)
        self.c.ellipse(cx - rx, S - cy - ry, cx + rx, S - cy + ry, stroke=0, fill=1)

    def wedge(self, cx, cy, r, start, extent, color):
        """Pie slice; angles in degrees, counter-clockwise from east (y-up like maths)."""
        self._fill(color)
        self.c.wedge(cx - r, S - cy - r, cx + r, S - cy + r, start, extent, stroke=0, fill=1)

    def poly(self, pts, color, alpha=1.0):
        self._fill(color, alpha)
        p = self.c.beginPath()
        p.moveTo(pts[0][0], S - pts[0][1])
        for x, y in pts[1:]:
            p.lineTo(x, S - y)
        p.close()
        self.c.drawPath(p, stroke=0, fill=1)

    def line(self, x1, y1, x2, y2, color, width=8):
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(width)
        self.c.setLineCap(1)
        self.c.line(x1, S - y1, x2, S - y2)

    def curve(self, x1, y1, cx, cy, x2, y2, color, width=6):
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(width)
        self.c.setLineCap(1)
        p = self.c.beginPath()
        p.moveTo(x1, S - y1)
        # quadratic -> cubic
        p.curveTo(x1 + 2 / 3 * (cx - x1), S - (y1 + 2 / 3 * (cy - y1)),
                  x2 + 2 / 3 * (cx - x2), S - (y2 + 2 / 3 * (cy - y2)), x2, S - y2)
        self.c.drawPath(p, stroke=1, fill=0)

    def text(self, x, y, s, font, size, color, anchor="middle"):
        """y is the text baseline."""
        self.c.setFillColor(HexColor(color))
        self.c.setFillAlpha(1)
        self.c.setFont(font, size)
        {"middle": self.c.drawCentredString, "start": self.c.drawString,
         "end": self.c.drawRightString}[anchor](x, S - y, s)


def star(p: Pen, x, y, r, color=YELLOW):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((x + rad * math.cos(a), y + rad * math.sin(a)))
    p.poly(pts, color)


def heart(p: Pen, x, y, size, color=RED):
    r = size * 0.27
    p.circle(x - r, y - size * 0.1, r, color)
    p.circle(x + r, y - size * 0.1, r, color)
    p.poly([(x - size * 0.5, y - size * 0.02), (x + size * 0.5, y - size * 0.02), (x, y + size * 0.5)], color)


def cloud(p: Pen, x, y, s=1.0, color=WHITE):
    p.circle(x, y, 55 * s, color)
    p.circle(x + 65 * s, y + 10 * s, 45 * s, color)
    p.circle(x - 65 * s, y + 15 * s, 40 * s, color)
    p.rect(x - 100 * s, y + 10 * s, 190 * s, 50 * s, color, r=25 * s)


def sun(p: Pen, x, y, r=70):
    for i in range(10):
        a = i * math.pi / 5
        p.line(x + (r + 18) * math.cos(a), y + (r + 18) * math.sin(a),
               x + (r + 45) * math.cos(a), y + (r + 45) * math.sin(a), ORANGE, 11)
    p.circle(x, y, r, YELLOW)
    p.circle(x - r * .3, y - r * .1, 6, DARK)
    p.circle(x + r * .3, y - r * .1, 6, DARK)
    p.circle(x - r * .5, y + r * .2, 9, PINK, 0.7)
    p.circle(x + r * .5, y + r * .2, 9, PINK, 0.7)
    p.curve(x - r * .3, y + r * .25, x, y + r * .6, x + r * .3, y + r * .25, DARK, 6)


def child(p: Pen, x, feet_y, h: Hero, scale=1.0, mood="smile", arm="down"):
    """Kit character. (x, feet_y) is the bottom centre."""
    s = scale
    leg_h, body_h, head_r = 85 * s, 105 * s, 50 * s
    body_top = feet_y - leg_h - body_h
    head_y = body_top - head_r + 8 * s
    for dx in (-17, 17):
        p.line(x + dx * s, feet_y - leg_h, x + dx * s, feet_y - 8 * s, DARK, 15 * s)
    if arm == "up":
        p.line(x + 45 * s, body_top + 22 * s, x + 90 * s, body_top - 45 * s, h.skin, 15 * s)
        p.line(x - 45 * s, body_top + 22 * s, x - 78 * s, body_top + 85 * s, h.skin, 15 * s)
    else:
        p.line(x + 45 * s, body_top + 22 * s, x + 80 * s, body_top + 85 * s, h.skin, 15 * s)
        p.line(x - 45 * s, body_top + 22 * s, x - 80 * s, body_top + 85 * s, h.skin, 15 * s)
    p.rect(x - 50 * s, body_top, 100 * s, body_h, h.shirt, r=28 * s)
    p.circle(x, head_y, head_r, h.skin)
    p.wedge(x, head_y, head_r, 12, 156, h.hair)
    for dx in (-18, 18):
        p.circle(x + dx * s, head_y + 4 * s, 5.5 * s, DARK)
        p.circle(x + dx * 1.45 * s, head_y + 20 * s, 8 * s, PINK, 0.75)
    my = head_y + 24 * s
    if mood == "smile":
        p.curve(x - 14 * s, my - 4 * s, x, my + 14 * s, x + 14 * s, my - 4 * s, DARK, 5 * s)
    elif mood == "sad":
        p.curve(x - 12 * s, my + 8 * s, x, my - 6 * s, x + 12 * s, my + 8 * s, DARK, 5 * s)
    else:  # curious "o"
        p.circle(x, my + 2 * s, 7 * s, DARK)


def ground(p: Pen, top, color=GREEN):
    p.rect(0, top, S, S - top, color)


# ---------------------------------------------------------------- scenes
def sc_day(p, h, _):
    p.rect(0, 0, S, S, "#A8D5F5"); sun(p, 640, 150); cloud(p, 230, 170); cloud(p, 520, 330, .6)
    ground(p, 500); child(p, 330, 520, h, 1.1, "o")


def sc_space(p, h, _):
    p.rect(0, 0, S, S, "#1F2A5C")
    for x, y, r in [(80, 80, 22), (420, 50, 14), (700, 80, 22), (110, 450, 16), (720, 440, 24), (610, 520, 12)]:
        star(p, x, y, r)
    sun(p, 170, 270, 55)
    p.circle(500, 290, 135, BLUE); p.ellipse(440, 240, 55, 35, "#52B788"); p.ellipse(550, 320, 38, 62, "#52B788")
    p.curve(360, 190, 420, 90, 470, 110, WHITE, 7)


def sc_night(p, h, _):
    p.rect(0, 0, S, S, "#28386B")
    for x, y, r in [(120, 100, 24), (680, 90, 22), (150, 400, 16), (640, 430, 26), (280, 490, 12), (520, 60, 14)]:
        star(p, x, y, r)
    p.circle(400, 260, 130, YELLOW); p.circle(470, 220, 118, "#28386B")


def sc_rain(p, h, _):
    p.rect(0, 0, S, S, "#9DB4C8"); cloud(p, 300, 150, 1.3, "#E8EEF3"); cloud(p, 580, 220, .8, "#E8EEF3")
    for i in range(14):
        x = 140 + i * 45; y = 290 + (i % 3) * 40
        p.line(x, y, x - 12, y + 40, BLUE, 8)
    ground(p, 540, "#7FB37C"); child(p, 400, 600, h, 1.0, "o")


def sc_storm(p, h, _):
    p.rect(0, 0, S, S, "#4A5568"); cloud(p, 300, 150, 1.4, "#2D3748"); cloud(p, 560, 200, 1.0, "#2D3748")
    p.poly([(420, 260), (330, 420), (400, 420), (350, 560), (500, 370), (425, 370), (480, 260)], YELLOW)
    ground(p, 590, "#4F7A4D")


def sc_rainbow(p, h, _):
    p.rect(0, 0, S, S, "#BDE0FE")
    cols = [RED, ORANGE, YELLOW, "#52B788", BLUE, PURPLE]
    for i, c in enumerate(cols):
        p.wedge(400, 520, 330 - i * 36, 0, 180, c)
    p.wedge(400, 520, 330 - 6 * 36, 0, 180, "#BDE0FE")
    cloud(p, 130, 460, .6); cloud(p, 680, 460, .6)
    ground(p, 520); child(p, 400, 640, h, 1.0, "smile", "up")


def sc_wind(p, h, _):
    p.rect(0, 0, S, S, "#BDE0FE"); cloud(p, 180, 140, .8)
    for y, w in [(230, 330), (310, 400), (390, 300)]:
        p.curve(80, y, 80 + w / 2, y - 50, 80 + w, y, WHITE, 12)
    p.poly([(600, 120), (660, 210), (600, 300), (540, 210)], RED); p.line(600, 300, 560, 420, DARK, 4)
    ground(p, 520); child(p, 400, 600, h, 1.0, "o")


def sc_snow(p, h, _):
    p.rect(0, 0, S, S, "#DCEBF7")
    for i in range(18):
        p.circle((i * 97) % 760 + 20, (i * 61) % 400 + 20, 7 + i % 3 * 3, WHITE)
    ground(p, 520, WHITE); p.circle(560, 560, 70, WHITE, 1); p.circle(560, 470, 50, WHITE); p.circle(560, 505, 62, "#EEF4FA")
    p.circle(545, 460, 5, DARK); p.circle(575, 460, 5, DARK); p.poly([(560, 472), (600, 480), (560, 486)], ORANGE)
    child(p, 280, 600, h, 1.1, "smile")


def sc_garden(p, h, _):
    p.rect(0, 0, S, S, "#BDE8F7"); sun(p, 680, 120, 55)
    p.rect(120, 300, 36, 230, "#8A5A3C"); p.circle(138, 250, 120, "#52B788"); p.circle(80, 330, 70, "#52B788")
    ground(p, 500, GREEN)
    for x, c in [(300, PINK), (400, YELLOW), (500, PURPLE), (600, RED)]:
        p.line(x, 640, x, 520, "#3E8E5A", 8)
        for k in range(5):
            a = k * 2 * math.pi / 5
            p.circle(x + 22 * math.cos(a), 505 + 22 * math.sin(a), 16, c)
        p.circle(x, 505, 12, YELLOW if c != YELLOW else ORANGE)
    child(p, 380, 760, h, 0.85, "smile")


def sc_sea(p, h, _):
    p.rect(0, 0, S, 400, "#BDE0FE"); sun(p, 650, 130, 55); cloud(p, 200, 130, .7)
    p.rect(0, 380, S, 420, BLUE)
    for y in (450, 540, 640):
        for x in range(0, S, 160):
            p.curve(x + 20, y, x + 80, y - 30, x + 140, y, "#8FCBEE", 8)
    p.poly([(250, 420), (550, 420), (500, 500), (300, 500)], RED); p.line(400, 420, 400, 270, DARK, 8)
    p.poly([(405, 275), (405, 400), (500, 400)], WHITE)
    p.ellipse(180, 630, 50, 28, ORANGE); p.poly([(225, 630), (270, 600), (270, 660)], ORANGE); p.circle(155, 622, 5, DARK)


def sc_home(p, h, _):
    p.rect(0, 0, S, S, "#FFF0D4"); p.rect(0, 540, S, 260, "#E9C99B")
    p.rect(90, 110, 220, 250, "#BDE0FE", r=14); p.line(200, 110, 200, 360, WHITE, 8); p.line(90, 235, 310, 235, WHITE, 8)
    p.ellipse(560, 700, 220, 50, "#F28482"); p.ellipse(560, 700, 150, 30, "#F7B2AE")
    child(p, 480, 700, h, 1.15, "smile")
    p.rect(640, 560, 80, 80, BLUE, r=12); p.rect(656, 576, 48, 12, WHITE, r=6)


def sc_body(p, h, _):
    p.rect(0, 0, S, S, "#FDE8EF"); p.rect(0, 560, S, 240, "#F9C6D9")
    heart(p, 150, 170, 90, "#F28482"); heart(p, 660, 230, 70, "#F28482")
    child(p, 400, 700, h, 1.6, "smile", "up")


def sc_street(p, h, _):
    p.rect(0, 0, S, S, "#DDEAF5"); sun(p, 110, 110, 45)
    p.rect(130, 400, 210, 160, "#F4D35E"); p.poly([(105, 400), (235, 290), (365, 400)], RED)
    p.rect(205, 460, 55, 100, "#8A5A3C"); p.rect(150, 420, 40, 40, "#BDE0FE"); p.rect(290, 420, 40, 40, "#BDE0FE")
    p.rect(560, 230, 130, 330, "#8D99AE")
    for yy in range(250, 540, 50):
        for xx in (575, 615, 655):
            p.rect(xx, yy, 24, 30, YELLOW)
    p.rect(0, 560, S, 240, "#ADB5BD"); p.rect(330, 660, 120, 14, WHITE); p.rect(480, 660, 120, 14, WHITE)
    p.rect(390, 470, 140, 70, YELLOW, r=26); p.rect(420, 440, 80, 50, YELLOW, r=18)
    p.circle(420, 545, 22, DARK); p.circle(500, 545, 22, DARK)


def sc_hearts(p, h, cast):
    p.rect(0, 0, S, S, "#FFD6E0"); p.rect(0, 540, S, 260, "#FFAFCC")
    heart(p, 400, 130, 130); heart(p, 230, 200, 50, "#F28482"); heart(p, 570, 190, 50, "#F28482")
    child(p, 270, 640, h, 1.2, "smile"); child(p, 530, 640, cast[(cast.index(h) + 1) % len(cast)], 1.2, "smile")


def sc_play(p, h, cast):
    p.rect(0, 0, S, S, "#E1F0C8"); ground(p, 500)
    heart(p, 400, 140, 70)
    child(p, 190, 640, h, 1.1, "smile"); child(p, 610, 640, cast[(cast.index(h) + 1) % len(cast)], 1.1, "smile")
    p.circle(400, 600, 48, WHITE)
    for k, c in enumerate([BLUE, YELLOW, RED, ORANGE, "#52B788"]):
        p.wedge(400, 600, 48, k * 72, 72, c)
    p.circle(400, 600, 8, WHITE)


SCENES = {n[3:]: f for n, f in globals().items() if n.startswith("sc_")}


def draw_scene(p: Pen, name: str, hero: Hero) -> None:
    SCENES[name](p, hero, CAST)
