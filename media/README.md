# Site media

## Where the video lives

**The reel is NOT in this repo.** It's hosted on Cloudflare R2 and referenced by
URL from `index.html`.

This is deliberate. The site deploys as a Cloudflare Worker (`npx wrangler
deploy`), and **Workers reject any single asset over 25 MiB**. A 49 MB reel
committed here fails the build with:

```
✘ [ERROR] Asset too large.
  Cloudflare Workers supports assets with sizes of up to 25 MiB.
```

`.gitignore` blocks `media/*.mp4` so this can't happen again by accident.

Only the poster frame (`reel-poster.jpg`, ~130 KB) lives in the repo.

## Changing the reel

1. Encode it (see below).
2. Upload to the R2 bucket, replacing the existing object.
3. If the filename changed, update the `<source>` URL and the `data-src` on
   `#hero-video` in `index.html` — two places.
4. Regenerate the poster:
   ```sh
   ffmpeg -y -ss 3 -i reel.mp4 -vframes 1 -vf "scale=1280:-2" -q:v 6 reel-poster.jpg
   ```

R2 serves HTTP Range requests, so seeking and the scrub bar work correctly.

## Encoding

```sh
ffmpeg -y -i SOURCE.mp4 \
  -c:v libx264 -crf 27 -preset slow -profile:v high -level 4.0 -pix_fmt yuv420p \
  -maxrate 7000k -bufsize 14000k \
  -c:a aac -b:a 128k -ac 2 -map 0:v:0 -map 0:a:0 \
  -movflags +faststart \
  reel.mp4
```

Current reel: 1080p, 94s, 4.4 Mbps, 49 MB.

Key flags:

- **`-movflags +faststart` — do not omit.** Moves the index to the front so
  playback starts immediately instead of after the whole file downloads.
  Verify it landed (`moov` must precede `mdat`):
  ```sh
  ffmpeg -v trace -i reel.mp4 2>&1 | grep -m2 -E "type:'(moov|mdat)'"
  ```
- `-crf 27` — quality knob, lower = bigger. This footage is high-detail and
  compresses poorly; CRF 23 produced 104 MB.
- `-pix_fmt yuv420p` — required for Safari/iOS.

**Don't use two-pass** unless pass-1 and pass-2 flags match exactly. A mismatch
yields a file with no `moov` atom — plausible filesize, completely unplayable.
Single-pass CRF is safer.

Always verify before uploading:

```sh
ffmpeg -v error -i reel.mp4 -f null /dev/null   # silence = clean decode
```

## Quality reference

Measured against the 49 MB master, a 21.5 MB / 1.85 Mbps encode scored
PSNR 30.3 dB, SSIM 0.887 — visibly softer on foliage and gravel. Fine behind
the hero scrim, noticeable in the showreel player. Don't go below ~4 Mbps for
the full-size player.

## Behaviour if the video is unreachable

The page degrades on its own: the hero falls back to `reel-poster.jpg`, and the
showreel section swaps to a "Watch on YouTube" card. The site never shows a
broken player.

The hero video is also skipped entirely on mobile, `prefers-reduced-motion`,
and data-saver — a large decorative autoplay isn't reasonable over cellular.

## The progress pack sample

`sample-progress-pack.pdf` (15 MB, 6 pages) is offered as a download from the
homepage: cover → orthomosaic → comparison → elevation → capture record → details.

It is regenerated, not hand-edited. To rebuild it:

```sh
cd /mnt/c/Users/dr00/Dropbox/Claude/drone-delivery-tool
PYTHONPATH=. python3 -m ddt report \
  --site-file ramblers-carpark \
  --task 391a98fc-b36d-4953-8e80-0c398abbcf55 \
  --baseline 8bb96451-b6c5-402a-8f24-b3f1cfded2af \
  --no-change-page \
  --site "Ramblers Car Park" \
  --client "Demonstration capture — not client work" \
  --date 2026-08-04 --aircraft "DJI Mini 3 Pro" --altitude 40 \
  --company "Shining Star Drones" --accent "#A81B5D" \
  --operator "GBR-OP-335BHXRJHNYT" \
  --contact "info@shiningstardrones.co.uk  ·  +44 7415 502186" \
  --out report.pdf
```

Three flags carry the whole argument, so don't drop any of them:

- **`--site-file`** pulls visit number, flight reference, weather and the
  measured capture geometry off the Site registry. Without it the cover sheet
  is missing three of the five fields the homepage promises in item 6, and the
  capture-record page does not appear at all.
- **`--baseline`** adds the side-by-side comparison of the two dates — item 5.
- **`--no-change-page`** then drops the elevation-difference map that
  `--baseline` would otherwise also add. Ramblers Car Park is a validation site
  where *nothing changed between the two dates*, so that map can only ever
  display measurement error. See `CORRECTIONS.md` §5B in the pipeline repo. A
  change map goes in the pack only once a site with real change has been flown
  twice. It also keeps the RMS change rows off the details page, which
  `HANDOVER.md` §4 rule 4 forbids quoting.

The version that shipped before 2026-08-04 was branded **"Ramblers Aerial"** with
empty Client, Operator and Flight altitude fields. Do not republish that one.

`ramblers-pack-spread.jpg` is the **first and last** pages of this PDF stacked —
two A4 landscape pages make an A4 portrait spread. Regenerate it if the report
changes, and keep the `aspect-ratio` in `.r-a4` matching its dimensions:

```sh
python3 - <<'PY'
import pypdfium2 as p
from PIL import Image
d = p.PdfDocument("sample-progress-pack.pdf")
W = 1400
imgs = [d[i].render(scale=W / d[0].get_width()).to_pil().convert("RGB")
        for i in (0, len(d) - 1)]
gap = 16
out = Image.new("RGB", (W, sum(i.height for i in imgs) + gap), (255, 255, 255))
y = 0
for im in imgs:
    out.paste(im, (0, y)); y += im.height + gap
out.save("ramblers-pack-spread.jpg", quality=86, optimize=True)
print(out.size)
PY
```

## Orthomosaic widths — regenerate all three together

Each date ships at **1200w, 1800w and 2400w**, wired up with `srcset` on the
homepage and the capability statement. Measured cold load: 2.10 MB -> 0.82 MB on
a phone, 2.10 MB -> 1.32 MB on an iPad Mini.

**Both dates must be resized to the SAME integer pixel size at every width.**
The pipeline renders the two orthophotos onto one shared grid so they are
co-registered pixel for pixel (`HANDOVER.md` 3) -- that is the whole reason the
before/after swipe is honest. Resize them to different sizes and the divider
shows apparent movement that is not real.

```sh
python3 - <<'PY'
from PIL import Image
for d in ("03", "04"):
    im = Image.open(f"ramblers-ortho-2026-08-{d}.jpg")           # 2400 x 1447
    for w, h in ((1200, 724), (1800, 1085)):
        out = im.resize((w, h), Image.LANCZOS).convert("RGB")
        out.save(f"ramblers-ortho-2026-08-{d}-{w}.jpg",
                 quality=84, optimize=True, progressive=True)
PY
```

`sizes` is left at a plain `100vw`, which slightly over-declares the plate's real
width. That is deliberate: over-declaring can only pick a larger candidate,
never too small a one. A phone held in landscape at DPR 3 needs ~1900px and so
still takes the 2400w -- correctly, not as a bug to chase.

## The 3D model was Z-up and had to be corrected

`st-mary-magdalene-building.glb` arrived from the pipeline **lying on its back**.
ODM's textured model is in a local ENU-style frame with **Z up**; `obj2glb`
copies the vertices through without an axis remap, and glTF requires **Y up**.
The file had one node, `{"mesh": 0}`, with no rotation and no matrix, so nothing
corrected it.

Every glTF viewer orbits about Y. With a Z-up model that means dragging **rolls
the building like a clock face** instead of turning it about its own vertical —
you cannot orbit it, and constraining the camera does not help, because the
camera was never the thing that was wrong.

**How to spot it without opening the file:** the vertical axis is the one whose
bounds never cross zero, because it is an elevation above a datum rather than an
offset from a centre. Here Z sat at 54.2..67.7 m while X and Y straddled zero.

Fixed with `scripts/fix_glb_up_axis.py`, which writes a -90 degree X rotation
into the node as a quaternion — mapping `(x, y, z) -> (x, z, -y)` — plus a
translation so the base sits at y=0. Done as a node transform rather than by
rewriting vertices: it costs nothing, leaves the Draco payload untouched, and
works in every viewer instead of relying on `<model-viewer orientation>` and one
viewer's Euler convention.

**This is an upstream bug and will come back on the next model.** Re-run the
script after any re-export:

```sh
python3 scripts/fix_glb_up_axis.py media/<model>.glb --check   # report only
python3 scripts/fix_glb_up_axis.py media/<model>.glb           # patch in place
```

It is safe to re-run — it refuses to touch a node that already carries a
transform, and reports and exits if the model is already Y-up.

The real fix belongs in `obj2glb` / the publish step in the pipeline repo, so
that the deliverable is correct for anyone who consumes it, not just this site.

**It came back, as predicted.** The 2026-08-05 re-export (13,466,712 bytes,
sha256 `4602cf58…`, matching the deliverable manifest) arrived Z-up again, Z at
54.2..67.7 m, and was patched with the same script before being committed.

**That re-export was then rolled back — it has holes in the geometry.** It
shipped in `ee0c08e` and was reverted in the commit that added this paragraph.
The live model is the older 10,840,812-byte one. Do not re-apply the newer file
until the missing parts are fixed upstream.

It is worth recording why it looked like an upgrade, because the same reasoning
will come round again. The re-export repacked the texture as **1002 primitives /
materials / images against the old model's 107**, and on every metric that gets
measured automatically it won —

| | old (live) | rolled-back re-export |
|---|---|---|
| file | 10.3 MiB | 12.8 MiB |
| textures | 107 | 1002 |
| largest texture | 3514x3337 | 302x302 |
| total texels | 58.3 M | 32.0 M |
| decoded GPU memory | ~233 MB | ~128 MB |
| **geometry** | **complete** | **holes** |

The GPU-memory finding is real and still true: the old model's few huge atlases
(one 3514x3337) cost far more decoded to RGBA than their JPEG size suggests, and
a texel count predicts phone memory where a byte count does not. It was simply
not the thing that mattered. A model with missing walls is not improved by being
cheaper to draw, and no amount of load-time instrumentation says so — the
headless check reported `loaded`, zero console errors, and correct bounding-box
dimensions for a model with holes in it, because a hole changes none of those.

So: **a clean load is not a correct model.** The automated checks below are
necessary and not sufficient. Look at the thing, and orbit it — the missing
parts here were not visible from the default camera angle that the verification
screenshot happened to capture.

Verify a re-export by serving a `git archive` checkout and loading it in a real
browser. Check that `getDimensions().y` is the **13.6 m** vertical extent and
not one of the horizontal ones — if y comes back as ~29 m or ~23 m, the axis
patch did not apply. Then spin it through a full rotation and look at it.
