# SEO — Shining Star Drones

**Last audit:** 2026-08-07  
**Live origin:** `https://shiningstardrones.co.uk`  
**Source:** this repo (`website/`) · Cloudflare Worker deploy on push to `main`  
**Skill:** pipeline `.grok/skills/seo/` (and `.claude/skills/seo/`) — run `/seo`  
**Auditor:** `python3 ../.grok/skills/seo/scripts/seo_audit.py . --base-url https://shiningstardrones.co.uk --out /tmp/ssd-seo-audit`

This file is the **working backlog + evidence**, not a ranking promise. GSC query data is operator-side; re-rank the list when impressions arrive.

---

## Verdict

**Foundation is strong; packaging and one host rule are weak.**

Honest progress-pack positioning, solid body copy (~1.7k words on home), one H1, good image alts/`srcset`, `LocalBusiness` JSON-LD, clean sitemap, extensionless URLs, capability statement for procurement. Gaps are mostly **technical hygiene + SERP/share tags + thin URL surface** — not a rewrite of the offer.

| Area | /5 | Note |
|------|----|------|
| Crawl & indexation | 3 | www→apex OK; **HTTP apex 200** |
| robots / sitemap | 4 | Valid; CF-managed AI-bot rules on live robots |
| Snippets / social head | 2.5 | Titles long; no canonical; no `og:image` |
| Content & intent | 4.5 | Differentiated, caveated, local |
| IA / internal links | 3 | Three URLs only |
| Media / CWV signals | 4 | Dims, LCP priority, heavy assets gated |
| Schema | 3 | LocalBusiness only; graph incomplete |
| Local readiness | 4 | NAP + areas in text + schema |
| E-E-A-T | 4.5 | GVC, CAA, £10m PL, privacy, accuracy limits |
| Strategic depth | 2.5 | Need real service/proof URLs later |

---

## Already good (do not undo)

- Positioning: progress packs / saved mission / 48h — not generic drone photography
- Single H1 per page; clear H2 outline on home
- Image alts, width/height, `srcset`, hero `fetchpriority="high"`, lazy below fold
- Local entities in copy (Slough, Berks, M4, Bucks, Surrey, Herts, London, Heathrow notes)
- `LocalBusiness` JSON-LD with address, phone, email, `areaServed`, `serviceType`
- Sitemap lists only clean 200 URLs (`/`, `/capability-statement`, `/privacy`)
- HTTPS clean-URL 307s from `.html` / `index.html`
- www → apex 301
- Quote generator removed from public site (was indexable risk)
- Heavy 3D / reel not forced on first paint
- GSC + Cloudflare Web Analytics already on (see session-log 2026-08-05)

---

## TODO — implementation backlog

Track here. Check boxes when shipped and verified live.

### P0 — indexation integrity

- [ ] **HTTP apex → HTTPS 301**  
  Evidence (2026-08-07): `curl -sI http://shiningstardrones.co.uk/` → `200` (no `Location`).  
  `http://www…` already 301s to HTTPS apex.  
  Fix in Cloudflare: Always Use HTTPS / redirect rule covering apex HTTP.  
  Verify: both HTTP hosts return 301 to `https://shiningstardrones.co.uk…`.

### P1 — head tags, social, schema

- [ ] **Self-referential `rel=canonical`** on all three pages  
  - `https://shiningstardrones.co.uk/`  
  - `https://shiningstardrones.co.uk/capability-statement`  
  - `https://shiningstardrones.co.uk/privacy`
- [ ] **`og:image` + dimensions** (absolute HTTPS URL, ~1200×630)  
  Candidate source: Ramblers orthomosaic + wordmark lockup → e.g. `media/og-default.jpg`
- [ ] **Twitter card** `summary_large_image` + title/description/image on all indexable pages
- [ ] **Full OG bundle** on capability-statement + privacy (`og:title`, `og:description`, `og:url`, `og:type`, `og:image`)
- [ ] **Shorten home title** (~50–60 visible chars)  
  Candidate: `Construction progress packs in 48h | Shining Star Drones`
- [ ] **Shorten home meta description** (~140–160 chars)  
  Candidate: `Repeatable drone progress packs from Slough: same mission monthly, orthomosaic + comparison PDF within 48 hours. Visual record, not survey-grade. Berks, Bucks, M4 & London.`
- [ ] **Shorten capability-statement meta description** (currently ~212 chars)
- [ ] **Enrich JSON-LD graph** (only true facts):  
  - `sameAs` → YouTube + LinkedIn (footer already links them)  
  - `image` / `logo`  
  - `WebSite` + `WebPage` with `@id` links  
  - `Service` + `Offer` for progress pack (£400–£650 range already on page)  
  - Optional: `FAQPage` only for visible Q&As; `VideoObject` for showreel  
  Patterns: pipeline `.grok/skills/seo/references/schema-patterns.md`  
  **Do not** invent AggregateRating / fake reviews.

### P2 — polish

- [ ] Optional `lastmod` in `sitemap.xml` when dates are real
- [ ] HSTS after HTTP→HTTPS is solid
- [ ] One honest body sentence for photogrammetry/model intent (no survey-grade overclaim)
- [ ] Re-run static auditor after head-tag pass; paste severity counts below

### P3 — content IA (only with unique substance)

- [ ] `/construction-progress-monitoring` — method, pack, cadence, audiences  
- [ ] `/roof-and-building-inspection` — one-off FM/estates  
- [ ] Case study URL (Ramblers demo or real client when allowed)  
- [ ] Optional film/FPV page so film queries do not dilute homepage  
  No city-doorway clones. Each page: own title, H1, canonical, internal links to `#enquiry`.

### Ops / measurement

- [ ] Confirm CF Web Analytics shows real browser pageviews (if still empty)
- [ ] Optional: Bing Webmaster import from GSC
- [ ] After deploy: GSC URL Inspection on home + capability-statement; sitemap re-submit if needed
- [ ] Share home URL in private chat — confirm OG card image

---

## Live checks (2026-08-07)

| URL | Result |
|-----|--------|
| `https://shiningstardrones.co.uk/` | 200 |
| `https://www.shiningstardrones.co.uk/` | 301 → apex |
| `http://shiningstardrones.co.uk/` | **200 — fix** |
| `http://www…` | 301 → HTTPS apex |
| `/*.html` / `/index.html` | 307 → clean paths |
| `/robots.txt` | 200 (repo + CF managed bot rules) |
| `/sitemap.xml` | 200, three locs |

### Static auditor snapshot

| Page | Title len | Desc len | Canonical | og:image | JSON-LD |
|------|-----------|----------|-----------|----------|---------|
| `index.html` | 81 | 246 | missing | missing | LocalBusiness |
| `capability-statement.html` | 42 | 212 | missing | missing | none |
| `privacy.html` | 36 | 158 | missing | missing | none |

Severity (static only): **P0 0 · P1 6 · P2 12 · P3 0** — plus live HTTP P0 above.

### Keyword posture (home body, approx)

progress 10 · orthomosaic 7 · slough 8 · berkshire 7 · survey 13 (mostly disclaimers) · monthly 5 · 48 hour 5 · drone 5 · construction 2 · photogrammetry 0

---

## Fix order (when implementing)

1. Cloudflare HTTP → HTTPS  
2. Canonical + OG image + Twitter + tighter title/description  
3. Schema graph  
4. Re-audit script + live curl matrix  
5. New URLs only after money page packaging is done  

**Claims discipline:** SEO edits must not invent accuracy, insurance, rates, or service scope. Caveats stay. Soften for CTR only if the factual claim remains true.

---

## Related

- Site README: `README.md`
- Privacy / analytics disclosure: `privacy.html`
- YouTube channel SEO (separate): pipeline `outreach/youtube_optimisation.md`
- Redesign history: pipeline `refactor/11-website-redesign.md`
- Skill + checklist: pipeline `.grok/skills/seo/`
