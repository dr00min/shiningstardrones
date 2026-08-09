#!/usr/bin/env python3
"""Build the site's Open Graph cards, 1200x630.

Run from the repo root:

    python3 scripts/make_og_cards.py

Writes media/og-default.jpg and media/og-accuracy-study.jpg.

Why a script and not a one-off export: the cards carry live facts (the accuracy
figures, the rate band, the delivery promise). When one of those changes on the
site it has to change here too, and hand-editing a JPEG guarantees it will not.

The base image is the real Ramblers orthomosaic. Type is the site's own three
faces, fetched as variable TTFs from the Google Fonts repo into /tmp on first
run — PIL cannot read the woff2 files the CSS uses.
"""
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
MARGIN = 62

INK = (14, 21, 25)
PAPER = (253, 254, 252)
MAGENTA = (228, 88, 154)      # the dark-theme magenta: the card is always dark
MUTED = (154, 166, 174)

GF = "https://raw.githubusercontent.com/google/fonts/main/"
FONTS = {
    "an": (GF + "ofl/archivonarrow/ArchivoNarrow%5Bwght%5D.ttf", "/tmp/ssd-archivonarrow.ttf"),
    "ps": (GF + "ofl/publicsans/PublicSans%5Bwght%5D.ttf", "/tmp/ssd-publicsans.ttf"),
    "rm": (GF + "ofl/robotomono/RobotoMono%5Bwght%5D.ttf", "/tmp/ssd-robotomono.ttf"),
}


def fetch_fonts():
    for url, path in FONTS.values():
        if not os.path.exists(path) or os.path.getsize(path) < 20000:
            print("fetching " + os.path.basename(path))
            urllib.request.urlretrieve(url, path)
    return {k: p for k, (_, p) in FONTS.items()}


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([weight])   # these are variable fonts
    except Exception:
        pass
    return f


def tracked(draw, xy, text, f, fill, tracking):
    """PIL has no letter-spacing, and the brand's mono labels live on it."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def base(src, zoom=0.78):
    im = Image.open(src).convert("RGB")
    # Centre-crop to 1200:630. `zoom` pulls in past the survey boundary — the
    # orthomosaic has black nodata wedges at its corners, and a full-frame crop
    # puts one of them behind the headline where it reads as a rendering fault.
    tw, th = im.width, int(im.width * H / W)
    if th > im.height:
        th, tw = im.height, int(im.height * W / H)
    tw, th = int(tw * zoom), int(th * zoom)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    im = im.crop((left, top, left + tw, top + th)).resize((W, H), Image.LANCZOS)

    # Flat scrim plus a left-weighted gradient: the text block sits on the left,
    # and a single flat layer heavy enough for it kills the whole image.
    im = Image.blend(im, Image.new("RGB", (W, H), INK), 0.60)
    grad = Image.new("L", (W, 1))
    for x in range(W):
        grad.putpixel((x, 0), int(150 * max(0.0, 1 - (x / (W * 0.86)) ** 1.5)))
    return Image.composite(Image.new("RGB", (W, H), INK), im,
                           grad.resize((W, H), Image.BILINEAR))


def ticks(d):
    """The corner registration marks used on every plate on the site."""
    t, o = 26, 26
    for (x, y, dx, dy) in ((o, o, 1, 1), (W - o, o, -1, 1),
                           (o, H - o, 1, -1), (W - o, H - o, -1, -1)):
        d.line([(x, y), (x + dx * t, y)], fill=MAGENTA, width=2)
        d.line([(x, y), (x, y + dy * t)], fill=MAGENTA, width=2)


def card(f, src, out, eyebrow, head, stand, figs,
         url="shiningstardrones.co.uk"):
    im = base(src)
    d = ImageDraw.Draw(im)
    ticks(d)

    f_eye = font(f["rm"], 17, 500)
    f_h = font(f["an"], 62, 600)
    f_st = font(f["ps"], 22, 300)
    f_val = font(f["an"], 40, 600)
    f_lab = font(f["rm"], 14, 400)
    f_url = font(f["rm"], 16, 500)

    x = MARGIN
    tracked(d, (x, 60), eyebrow, f_eye, MAGENTA, 2.6)

    y = 104
    for line in head:
        d.text((x, y), line, font=f_h, fill=PAPER)
        y += 66

    y += 22
    for line in stand:
        d.text((x, y), line, font=f_st, fill=(214, 221, 217))
        y += 32

    d.line([(x, 444), (W - MARGIN, 444)], fill=(70, 84, 92), width=1)

    fx = x
    for value, label in figs:
        d.text((fx, 466), value, font=f_val, fill=PAPER)
        tracked(d, (fx + 2, 520), label, f_lab, MUTED, 1.6)
        fx += max(d.textlength(value, font=f_val),
                  d.textlength(label, font=f_lab) + 1.6 * len(label)) + 56

    # Right-aligned, so it never crowds the last figure label.
    u = url.upper()
    uw = sum(d.textlength(c, font=f_url) + 2.2 for c in u) - 2.2
    tracked(d, (W - MARGIN - uw, H - 72), u, f_url, MUTED, 2.2)

    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    print("%s  %d KB" % (out, os.path.getsize(out) // 1024))


if __name__ == "__main__":
    root = (sys.argv[1] if len(sys.argv) > 1 else ".").rstrip("/")
    f = fetch_fonts()
    ortho = root + "/media/ramblers-ortho-2026-08-03.jpg"

    # Figures must match the article. See articles/how-accurate-is-a-sub-250g-drone.html
    card(
        f, ortho, root + "/media/og-accuracy-study.jpg",
        "FIELD NOTE  ·  MEASUREMENT",
        ["How accurate is a sub-250 g", "drone, really?"],
        ["The same site, flown twice, 24 hours apart, with nothing changed",
         "between the flights — so everything the model reported was error."],
        [("0.24 m", "90% AGREEMENT"), ("0.033 m", "SCATTER, HARDSTANDING"),
         ("2.7×", "VOLUME OVER-READ")],
    )

    # Figures must match the homepage spec row.
    card(
        f, ortho, root + "/media/og-default.jpg",
        "CONSTRUCTION PROGRESS MONITORING  ·  SLOUGH",
        ["The same flight,", "every month."],
        ["Orthomosaic, labelled stills and a month-to-month comparison —",
         "on your desk by the third working day, before your progress meeting."],
        [("3rd working day", "OF THE MONTH"), ("£400–£650", "PER SITE, PER MONTH"),
         ("GVC", "CAA AUTHORISED · £10m PL")],
    )
