# Shining Star Drones — Website

Static marketing site for [shiningstardrones.co.uk](https://shiningstardrones.co.uk) — GVC-qualified construction progress monitoring and aerial site records from Slough across Berkshire, Bucks, the M4 corridor, and Greater London.

## What's here

| File | Purpose |
|---|---|
| `index.html` | Landing page (services, showreel, areas, pricing, contact form) |
| `capability-statement.html` | One-page proof artifact for procurement teams |
| `CNAME` | Vestigial. The live site is a Cloudflare Worker, not GitHub Pages. |
| `robots.txt` | Crawler directives |
| `sitemap.xml` | Search-engine sitemap |

**`quote-generator.html` was removed from this repo on 2026-08-04 and must not come
back.** It is an internal pricing calculator — it exposes the rate card, assistant and
travel costs, multi-site multipliers and deposit terms, it carried a "Manual Price
Override" control, and it was branded "Shining Star Media" rather than "Shining Star
Drones". Nothing linked to it, but it was listed in `sitemap.xml` with no `noindex`, so
it was reachable and indexable. It now lives at `quotes/quote-generator.html` in the
pipeline repo.

The site is **fully static** — no build step, no dependencies. Open `index.html` in a browser to preview locally.

## Editing

This is a vanilla HTML/CSS/JS site. No framework, no bundler. Edit the files directly and push.

- **Copy / pricing changes** → edit `index.html` directly
- **Service list** → search for the `<section class="services">` block
- **Contact form** → Formspree endpoint is set to `https://formspree.io/f/mbdeaqgg`. Submissions go to `info@shiningstardrones.co.uk`. Verify the form works by submitting a test message after deploy.
- **LocalBusiness JSON-LD** → search for `"@type": "LocalBusiness"` in `index.html`

## Deployment

The site is set up to deploy to either **GitHub Pages** (free) or **Netlify** (free tier with form handling). Both work with the current file layout.

### Option A — GitHub Pages

1. Settings → Pages → Source: `main` branch, root
2. Custom domain: `shiningstardrones.co.uk`
3. DNS: see `docs/dns.md` (when added)

### Option B — Netlify

1. New site → Import from Git → select this repo
2. Build command: *(none — leave blank)*
3. Publish directory: `.` (root)
4. Custom domain: `shiningstardrones.co.uk`
5. Enable Forms for the contact form to work without Formspree

### Option C — Cloudflare Pages (current host)

1. Cloudflare dashboard → **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**
2. Select `dr00min/shiningstardrones` → **Begin setup**
3. Project name: `shining-star-drones`
4. Production branch: `main`
5. Framework preset: **None**
6. Build command: *(empty)*
7. Build output directory: `/` (root)
8. **Custom domains** tab → add `shiningstardrones.co.uk` — Cloudflare handles DNS + SSL automatically
9. Staging URL: `https://shining-star-drones.pages.dev` (visit first to verify deploy)

## Local preview

```bash
# From the website/ directory
python3 -m http.server 8080
# Visit http://localhost:8080
```

## Asset notes

- All imagery is embedded or external (YouTube iframes)
- No build artefacts, no `node_modules`
- See `capability-statement.html` for the one-page "leave behind" for procurement teams

## License

© Shining Star Drones. All rights reserved.
