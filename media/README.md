# Site media

## Changing the showreel

Drop your video here as **`reel.mp4`** — overwrite the old one, commit, push. That's it.
No HTML edits needed; `index.html` always points at `media/reel.mp4`.

Then regenerate the poster frame (the still shown before the video loads):

```sh
ffmpeg -y -ss 3 -i reel.mp4 -vframes 1 -vf "scale=1280:-2" -q:v 6 reel-poster.jpg
```

If `reel.mp4` is missing or fails to decode, the site falls back to a
"Watch on YouTube" card, so the page never looks broken.

## Encoding it — use this command

Camera-original footage is **far** too heavy to autoplay on a homepage. Run this
on the master file before committing:

```sh
ffmpeg -y -i SOURCE.mp4 \
  -c:v libx264 -crf 27 -preset slow -profile:v high -level 4.0 -pix_fmt yuv420p \
  -maxrate 7000k -bufsize 14000k \
  -c:a aac -b:a 128k -ac 2 -map 0:v:0 -map 0:a:0 \
  -movflags +faststart \
  reel.mp4
```

Current reel: 1080p, 94s, 4.4 Mbps, 49 MB.

Why these flags:

- **`-movflags +faststart` — the one you must not omit.** It moves the index to
  the front of the file so playback starts immediately. Without it the browser
  downloads the *entire* file before showing a single frame. Verify it landed:
  ```sh
  ffprobe -v error -show_entries format=start_time -of default=noprint_wrappers=1 reel.mp4
  # or check moov comes before mdat:
  ffmpeg -v trace -i reel.mp4 2>&1 | grep -m2 -E "type:'(moov|mdat)'"
  ```
- `-crf 27` — quality knob. Lower = better + bigger. This footage is high-detail
  (foliage, gravel, motion) so it compresses poorly; CRF 23 came out at 104 MB.
  Check the size and adjust.
- `-maxrate/-bufsize` — caps bitrate spikes so playback doesn't stall on slower
  connections.
- `-pix_fmt yuv420p` — required for Safari/iOS. Non-negotiable.
- `-map 0:v:0 -map 0:a:0` — drops extra tracks some converters add.

**Don't use two-pass** unless you keep pass-1 and pass-2 flags identical — a
mismatch makes x264 emit a file with no `moov` atom that looks fine by filesize
and is completely unplayable. Single-pass CRF is safer here.

Always verify before committing:

```sh
ffmpeg -v error -i reel.mp4 -f null /dev/null   # silence = clean decode
```

## Hard limits

The video is served from GitHub Pages, so it lives in git:

- **100 MB** — GitHub's hard per-file limit. Pushes over this are rejected.
  The current 49 MB leaves reasonable headroom.
- **1 GB** — soft repo limit. Every version of the reel you commit counts
  toward it forever, even after replacement. Avoid committing many revisions;
  get it right locally first.
- GitHub Pages allows ~100 GB/month bandwidth, which is far more than this
  site will use.

If the reel starts changing frequently, move it to Cloudflare R2 (free tier,
no egress charges) and point the `<source>` at that URL instead.

## Keep the master elsewhere

Commit only the web-encoded file. The full-resolution original belongs in
Dropbox/cloud storage, not in the repo.
