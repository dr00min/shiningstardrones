# Shining Star Drones — Website

Static marketing site for [shiningstardrones.co.uk](https://shiningstardrones.co.uk) — GVC-qualified commercial drone services across West London, Greater London, Buckinghamshire, and the South East.

## What's here

| File | Purpose |
|---|---|
| `index.html` | Landing page (services, showreel, areas, pricing, contact form) |
| `quote-generator.html` | Interactive quote calculator with copy-to-clipboard output |
| `capability-statement.html` | One-page proof artifact for procurement teams |
| `CNAME` | Custom domain mapping for GitHub Pages / Netlify |
| `robots.txt` | Crawler directives |
| `sitemap.xml` | Search-engine sitemap |

The site is **fully static** — no build step, no dependencies. Open `index.html` in a browser to preview locally.

## Editing

This is a vanilla HTML/CSS/JS site. No framework, no bundler. Edit the files directly and push.

- **Copy / pricing changes** → edit `index.html` directly
- **Service list** → search for the `<section class="services">` block
- **Contact form** → swap the `REPLACE_WITH_YOUR_FORM_ID` placeholder in `index.html` with the real Formspree endpoint (see [outreach/inbound_setup.md](../outreach/inbound_setup.md) in the parent pipeline repo)
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
