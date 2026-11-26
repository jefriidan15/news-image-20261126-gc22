#!/usr/bin/env python3
"""news-image-20261126: one image summing up Thursday 26 November 2026.

Pure stdlib (zlib + struct only): paints a broadsheet front page at
1024x1024 with a hand-written 5x7 bitmap font, then writes entry.png.
No network, no timestamps, no randomness, so two runs write
byte-identical files.

Lead story: Houthi strikes on Saudi Arabia's Ras Tanura refinery and
Riyadh push Brent crude past $94. Also covered: US tariffs on 14
partners, Ukraine's air-base strike, Kim's tactical-nuke order, the
birthright-citizenship block, Pakistan's first astronaut, and the death
of Duran Duran guitarist Andy Taylor.
"""
import hashlib
import os
import struct
import sys
import zlib

W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (22, 22, 22)
NAVY = (18, 28, 54)
NAVY2 = (26, 40, 76)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
GREY = (110, 104, 92)
GREY_DK = (74, 70, 66)
DUSK_TOP = (233, 116, 54)
DUSK_MID = (122, 62, 110)
DUSK_LOW = (44, 26, 64)
SEA = (16, 32, 58)
TOWER = (26, 18, 32)
BRACE = (52, 40, 58)
FLAME = (242, 163, 82)
FLAME_HOT = (255, 214, 90)
SUN = (255, 190, 90)
SMOKE = (120, 112, 128)
TEAL = (18, 110, 110)
PURPLE = (96, 52, 130)
BLUE = (32, 96, 145)

# 5x7 bitmap font, '#' on, '.' off. Lowercase maps to uppercase.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", "01100", "01100"),
    ",": (".....", ".....", ".....", ".....", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "01110", ".....", ".....", "....."),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "!": ("00100", "00100", "00100", "00100", "00100", ".....", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", ".....", "00100"),
    ":": (".....", "01100", "01100", ".....", "01100", "01100", "....."),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": (".....", "00100", "00100", "01110", "00100", "00100", "....."),
    "=": (".....", ".....", "11111", ".....", "11111", ".....", "....."),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(x, 0), max(y, 0)
        x1, y1 = min(x + w, self.w), min(y + h, self.h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            self.px[base:(base + (x1 - x0) * 3)] = bytes(c) * (x1 - x0)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5)
            self.rect(cx - dx, yy, dx * 2 + 1, 1, c)

    def triangle(self, cx, top, base_y, half, c):
        # Isosceles triangle, apex at (cx, top), base at base_y.
        for yy in range(top, base_y + 1):
            t = (yy - top) / max(base_y - top, 1)
            hw = max(int(half * t), 0)
            self.rect(cx - hw, yy, hw * 2 + 1, 1, c)

    def vgrad(self, x, y, w, h, top, mid, bot):
        # Two-stop vertical gradient: top -> mid -> bot.
        for yy in range(y, y + h):
            t = (yy - y) / max(h - 1, 1)
            if t < 0.5:
                a, b, u = top, mid, t * 2
            else:
                a, b, u = mid, bot, (t - 0.5) * 2
            c = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
            self.rect(x, yy, w, 1, c)


def char_w(scale):
    return 6 * scale


def text_w(s, scale):
    return len(s) * char_w(scale) - scale


def draw_text(cv, x, y, s, scale, color):
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "1":
                    cv.rect(cx + col * scale, y + row * scale,
                            scale, scale, color)
        cx += char_w(scale)
    return cx


def wrap(s, scale, max_w):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    words = s.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(cv, x, y, s, scale, color, max_w, leading=None):
    lh = (7 * scale) + (leading if leading is not None else scale)
    for i, line in enumerate(wrap(s, scale, max_w)):
        draw_text(cv, x, y + i * lh, line, scale, color)
    return y + len(wrap(s, scale, max_w)) * lh


# --- lead scene: refinery at dusk -------------------------------------

def draw_lead(cv, y0, y1):
    cv.vgrad(0, y0, W, y1 - y0, DUSK_TOP, DUSK_MID, DUSK_LOW)
    # Low sun behind the plant, right of centre.
    cv.disc(830, 300, 48, SUN)
    cv.disc(830, 300, 34, FLAME)
    # Flare stacks with flames (right side, clear of the headline).
    for sx, sh in ((640, 250), (920, 220)):
        cv.rect(sx, y1 - 48 - sh, 10, sh + 48, TOWER)
        cv.triangle(sx + 5, y1 - 48 - sh - 34, y1 - 48 - sh, 13, FLAME)
        cv.triangle(sx + 5, y1 - 48 - sh - 20, y1 - 48 - sh, 7, FLAME_HOT)
        cv.disc(sx + 5, y1 - 48 - sh - 30, 6, FLAME_HOT)
    # Distillation towers, left and centre.
    for tx, tw, th in ((90, 46, 150), (180, 34, 205), (250, 40, 130),
                       (330, 30, 175), (420, 52, 160), (500, 36, 110)):
        cv.rect(tx, y1 - 48 - th, tw, th + 48, TOWER)
        # Cross-bracing.
        for k in range(4):
            yy = y1 - 48 - th + 18 + k * 34
            cv.hline(tx, yy, tw, BRACE)
        cv.rect(tx + tw // 2 - 4, y1 - 48 - th - 12, 8, 12, TOWER)
    # Storage tanks.
    for tx, tw, th in ((560, 70, 62), (300, 90, 70)):
        cv.rect(tx, y1 - 48 - th, tw, th + 48, TOWER)
        cv.rect(tx, y1 - 48 - th - 8, tw, 8, BRACE)
    # Lit windows on the towers.
    for wx, wy in ((100, 400), (150, 430), (190, 360), (260, 420),
                   (340, 380), (430, 400), (510, 440), (570, 450)):
        cv.rect(wx, wy, 7, 9, GOLD_LT)
    # Smoke puffs above two stacks.
    for sx, sy in ((645, 190), (925, 215), (660, 165)):
        cv.disc(sx, sy, 12, SMOKE)
        cv.disc(sx + 14, sy - 8, 9, SMOKE)
    # Sea with shimmer at the foot of the plant.
    cv.rect(0, y1 - 48, W, 48, SEA)
    for sx, sy, sw in ((60, y1 - 38, 90), (300, y1 - 30, 130),
                       (620, y1 - 40, 80), (760, y1 - 26, 150),
                       (180, y1 - 18, 70), (480, y1 - 12, 110)):
        cv.rect(sx, sy, sw, 2, FLAME)
    for sx, sy, sw in ((140, y1 - 34, 60), (420, y1 - 22, 90),
                       (840, y1 - 36, 70)):
        cv.rect(sx, sy, sw, 2, FLAME_HOT)


# --- page layout -------------------------------------------------------

STORIES = [
    ("TARIFFS", RED,
     "US TARIFFS ON 14 PARTNERS",
     "China hit hardest; markets fall"),
    ("UKRAINE", BLUE,
     "UKRAINE STRIKES AIR BASE",
     "Five planes damaged in strike"),
    ("N KOREA", NAVY2,
     "KIM ORDERS MORE NUKES",
     "Pyongyang widens deployment"),
    ("US COURT", GREY_DK,
     "BIRTHRIGHT ORDER BLOCKED",
     "Second judge halts Trump curbs"),
    ("SPACE", TEAL,
     "PAKISTAN'S FIRST ASTRONAUT",
     "China flies guest to Tiangong"),
    ("MUSIC", PURPLE,
     "ANDY TAYLOR DIES AT 65",
     "Duran Duran guitarist mourned"),
]


def draw_page(cv):
    # Masthead.
    cv.rect(0, 0, W, 92, NAVY)
    draw_text(cv, 32, 20, "THE WORLD IN ONE IMAGE", 4, WHITE)
    draw_text(cv, 32, 58, "THURSDAY 26 NOVEMBER 2026", 2, GOLD_LT)
    cv.rect(0, 92, W, 4, GOLD)

    # Lead scene + headline.
    draw_lead(cv, 96, 548)
    draw_text(cv, 40, 122, "HOUTHIS HIT", 5, WHITE)
    draw_text(cv, 40, 168, "SAUDI REFINERY", 5, WHITE)
    draw_text(cv, 40, 222, "BRENT CRUDE TOPS $94", 3, GOLD_LT)
    draw_text(cv, 40, 252, "RAS TANURA AND RIYADH TARGETED", 2, WHITE)

    # Ticker strip.
    cv.rect(0, 548, W, 48, INK)
    draw_text(cv, 32, 566, "BRENT $94.20 UP | US TARIFFS HIT 14 | "
              "UKRAINE AIR BASE HIT | KIM ORDERS NUKES", 2, GOLD_LT)

    # Story grid: 2 columns x 3 rows.
    for i, (tag, color, head, summ) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = 16 + col * 504
        y = 612 + row * 112
        cv.rect(x, y, 488, 104, PAPER)
        cv.rect(x, y, 488, 3, color)
        cv.rect(x, y, 3, 104, color)
        # Tag chip.
        cv.rect(x + 14, y + 14, 118, 26, color)
        draw_text(cv, x + 22, y + 19, tag, 2, WHITE)
        draw_text(cv, x + 14, y + 50, head, 3, INK)
        draw_text(cv, x + 14, y + 80, summ, 2, GREY)

    # Footer.
    cv.rect(0, 952, W, 72, NAVY)
    draw_text(cv, 32, 966, "ALSO: LEBANON PLANS SECOND AIRPORT | SUDAN DRONE "
              "STRIKES KILL 19", 2, WHITE)
    draw_text(cv, 32, 992, "GAZA STRIKE KILLS HAMAS OFFICIAL | BANGLADESH "
              "GARMENT PAY UP 36%", 2, GOLD_LT)


# --- PNG writer (deterministic: no time chunks) ------------------------

def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw.extend(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return png


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    cv = Canvas(W, H, PAPER)
    draw_page(cv)
    path = os.path.join(outdir, "entry.png")
    data = write_png(cv, path)
    print("wrote %s %d bytes sha256=%s" %
          (path, len(data), hashlib.sha256(data).hexdigest()))
    # Read-back check: decode dimensions from the IHDR we wrote.
    with open(path, "rb") as f:
        head = f.read(33)
    w, h = struct.unpack(">II", head[16:24])
    assert (w, h) == (1024, 1024), "bad size %dx%d" % (w, h)
    assert len(data) <= 1024 * 1024, "over 1 MiB"
    print("entry.png OK: 1024x1024, %d bytes" % len(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
