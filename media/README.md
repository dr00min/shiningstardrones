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

`sample-progress-pack.pdf` (9.0 MB) is offered as a download from the homepage.

It is regenerated, not hand-edited. To rebuild it:

```sh
cd /mnt/c/Users/dr00/Dropbox/Claude/drone-delivery-tool
PYTHONPATH=. python3 -m ddt report \
  --task 391a98fc-b36d-4953-8e80-0c398abbcf55 \
  --site "Ramblers Car Park" \
  --client "Demonstration capture — not client work" \
  --date 2026-08-04 --aircraft "DJI Mini 3 Pro" --altitude 40 \
  --company "Shining Star Drones" --accent "#A81B5D" \
  --operator "GBR-OP-335BHXRJHNYT" \
  --contact "info@shiningstardrones.co.uk  ·  +44 7415 502186" \
  --out report.pdf
```

**Do not pass `--baseline`.** It adds an elevation-change page, and Ramblers Car
Park is a validation site where *nothing changed between the two dates* — so that
page can only ever display measurement error. See `CORRECTIONS.md` §5B in the
pipeline repo. A change map goes in the pack only once a site with real change
has been flown twice.

The version that shipped before 2026-08-04 was branded **"Ramblers Aerial"** with
empty Client, Operator and Flight altitude fields. Do not republish that one.

`ramblers-pack-spread.jpg` is pages 1 and 4 of this PDF rendered at scale 2 and
stacked — two A4 landscape pages make an A4 portrait spread. Regenerate it if the
report changes, and keep the `aspect-ratio` in `.r-a4` matching its dimensions.
