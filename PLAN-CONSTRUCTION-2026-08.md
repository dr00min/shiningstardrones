# Construction repositioning plan — 2026-08-07

**Source:** external market review (construction budget lines, competitor procurement
records, site critique). **Status:** plan only, nothing implemented.
**Convention:** same as `SEO.md` — working backlog with checkboxes and evidence, not a
promise. Tick items only when the change is live and verified.

---

## The one-line verdict

The site sells a **visual record** and disqualifies itself, loudly and repeatedly, from
the **earthworks / cut-and-fill** budget — which is the largest recurring construction
spend. That honesty is an asset and must not be undone. But it means the offer competes
against a site manager with a phone, a £1–2k/yr fixed time-lapse camera, and
OpenSpace-style 360 walkthroughs already on many sites, **and the page never answers
"why not just get the site engineer to fly a Mavic?"** That unanswered question is the
thing killing the sale.

Everything below is sequenced against that.

---

## Ordering rule — read before picking anything up

**The binding constraint is not the website. It is that no construction client has ever
seen this and reacted** (`NEEDLE.md` gate 5, count 0). The review says the same thing in
its own words: *"Get one live site free in exchange for a named case study and a reference
call — that's the first move, ahead of everything else."*

So:

- **Phase 0 runs first and in parallel with everything.** It is phone calls and one
  insurance form, not code.
- **Phase 1 is the only website work that should happen before a named prospect exists.**
  It is ~1 day, needs no new evidence, and removes the objections that make a call go dead.
- **Phases 2–4 are gated on evidence.** Each item states its gate. Do not write a claim
  onto the site before its gate is met — the site's credibility is currently its single
  strongest asset and one unbacked accreditation badge destroys it.

If a session is about to start Phase 2+ while gate 5 is still 0, that is displacement
activity. Say so and go back to Phase 0.

---

## Phase 0 — Evidence acquisition (no website work)

Nothing here is a code change. All of it gates something later.

- [ ] **P0.1 — Professional indemnity insurance.** *The single biggest omission on the
  site.* PL is stated; PI is absent. If a PM makes a programme or valuation decision off a
  pack, PI is exactly what procurement asks for, and its absence ends a PQQ. Get quotes
  (Coverdrone / Moonrock / Hiscox all write UAV PI), decide the limit against what a
  contractor's supply-chain form typically demands, bind it. **Gates P2.1 and most of
  Phase 3.** Do not put a number on the site until the certificate exists.
- [ ] **P0.2 — One live construction site, flown free, in exchange for a named case study
  and a reference call.** Not a favour — a trade, stated as one. This is the only item
  that unlocks P2.2, and construction buys on reference. Target from P0.5.
- [ ] **P0.3 — Written data position.** Three short paragraphs, currently absent
  everywhere: **retention** (how long imagery is held, where, deletion on request),
  **IP / licence** (who owns the pack, what the client may do with it, what may be used as
  a portfolio reference), and **GDPR on operatives visible in frame** (lawful basis,
  face/plate handling, how a site inducts it). Lands in `privacy.html` + a summary row on
  the capability statement. **Gates P2.3.**
- [ ] **P0.4 — Decide sole trader vs limited company.** A company number is requested on
  most supply-chain forms and its absence is friction at every PQQ. Cost is small; the
  decision is the operator's. **Gates P3.2 (Constructionline/CHAS both ask).**
- [ ] **P0.5 — Live-site prospecting list.** Not head-office procurement. Pull approved
  **major** applications from the **Slough, Maidenhead (RBWM), Reading, Bracknell Forest
  and Windsor** planning portals — these name the developer *and* the contractor. Filter
  to sites inside the 1-hour travel radius that are visibly in groundworks or
  superstructure. Target the **site PM** (discretionary spend) or a **QS on a job already
  in dispute**. Merge into `prospects-live.html`, which already exists and holds call
  state. **This is the real work.**

---

## Phase 1 — Website changes needing no new evidence (~1 day, ship together)

**IMPLEMENTED 2026-08-07 except P1.5.** Built, tag-balance checked on all four pages, and
rendered locally in a browser. Not yet committed or pushed — review the diff first.

All in `index.html` unless stated. None of these assert anything not already true.

- [x] **P1.1 — Answer "why not get the site engineer to fly a Mavic?"** New section,
  placed immediately after the pricing table, before *What this kit will and won't tell
  you*. This is the highest-value single change on the page. The honest answer is already
  demonstrable from the repo and nobody else on a local search result can make it:
  - **The saved mission.** Month three is comparable to month one because it is the *same
    flight*, not a similar one — line spacing reproduced to 2 cm across dates, verified
    from the flown EXIF, not asserted. A hand-flown Mavic produces a different geometry
    every visit and the comparison is worthless.
  - **Alignment to a baseline.** Each visit is georeferenced against the first, which is
    what makes an overlay legal. Without it, GPS drift moves the whole map between dates.
  - **The stated error, with percentiles.** A number the site engineer cannot give you,
    and a QS in a dispute needs the number, not the picture.
  - **It is not their job.** Someone else carries the CAA authorisation, the RAMS, the
    £10m PL, the airspace check and the induction — and it does not come off the site
    team's week.
  Keep it to four short rows. Do not make it defensive.
  **As built:** new numbered section 05, placed between the pricing table and the accuracy
  section, using the existing `deflist` pattern. Four rows as planned, plus a right-hand
  column that concedes the opposite case out loud — *"if all you need is a picture of the
  site this week, someone on site with a drone is cheaper and faster, and you should do
  that."* Conceding it is what makes the rest credible. Everything after it renumbered;
  the enquiry section stays 07 because the film section left at the same time.
- [x] **P1.2 — Re-clock the delivery promise.** "48 hours" is a *capability*; the *promise*
  should be a calendar the buyer already keeps. Change the hero and the spec strip to
  **"on your desk by the 3rd working day of the month — before your progress meeting"**,
  and demote 48 h to a single spec row ("48 h from a successful flight"). 5 occurrences of
  `48 hours` in `index.html` today; the hero one is the one that matters.
  **As built:** hero, `<title>`, meta description, `og:description` and the `LocalBusiness`
  JSON-LD description all now lead with the third working day. The hero spec card changed
  from *Turnaround / 48 hours* to *On your desk / 3rd working day*, with "48 h from a flight"
  as its subline — so the capability is still stated, just not sold as the promise. Pack
  item 07 and the section tag follow. `48 hour` now appears **once** in `index.html`,
  down from five.
- [x] **P1.3 — Cut "Who this is for" from six rows to two.** Six segments for a one-pilot
  operation reads as none. Keep **Main contractor / PM** (lead) and **QS / commercial**
  (second door — this is where dispute urgency lives, so do not drop it). Delete
  Groundworks, Survey practice, Quarry ops and FM & estates from the home page; move them
  to a single line at the foot of the capability statement ("also undertaken, quoted per
  job"). Keeps the offer, loses the "will fly anything for anyone" signal.
  **As built:** the home page keeps Main contractor / PM and QS / commercial. The other four
  moved to `capability-statement.html` under "who the monthly pack is built for / also worked
  with, quoted per job", with the quarry caveat about audited volumes carried over intact. A
  short line on the home page says two is deliberate and links to the statement — so nothing
  looks dropped.
- [x] **P1.4 — Delivery / integration line.** Costs nothing and separates this from a
  photographer: *"the pack lands in your Procore, Autodesk Construction Cloud, SharePoint
  or Dropbox folder — not as an attachment in my email."* Add as a row in *What's in a
  progress pack* and a field on the enquiry form. Currently zero occurrences of any of
  those four names on the site.
  **As built:** a "Where it lands is your choice" paragraph beside the pack list naming
  Procore, Autodesk Construction Cloud, SharePoint and Dropbox, plus a **"Where the pack
  should land"** field on the enquiry form. Watch the markup here — the pack section is a
  two-column grid and a bare `<p>` sibling becomes a third grid child, which pushed the
  pack-spread plate out of column two. Caught in the browser, fixed by wrapping the list and
  the paragraph in one `<div>`.
- [ ] **P1.5 — Substitution arithmetic. NOT BUILT — blocked on figures, deliberately.**
  The buyer will not do the comparison; do it for them. A three-row block under pricing:
  what a topo visit costs, what a scaffold or MEWP costs for a façade look, what a half-day
  of a site manager's time costs — against £400–£650/month.
  **Held back because no sourced figures exist for any of the three.** An invented
  comparison is worse than none: the accuracy section two blocks below is the site's
  strongest credibility asset precisely because every number in it was measured, and a
  made-up cost table sitting above it poisons that. This repo's own rule is to mark an
  unsourced commercial claim `[ASSUMED]` rather than assert it.
  **To unblock, one of:** the operator supplies real quotes seen in the field; or a
  sourced desk pass on UK topographic survey day rates, MEWP/scaffold hire and site
  management costs, each cited on the page.
- [x] **P1.6 — Move the film section to its own URL.** FPV rates and a YouTube reel on the
  same page as a progress pack tells a commercial manager to price the operator as a
  videographer. Cut section 06 out of `index.html` into `film.html`; leave one line in the
  footer ("brand film and FPV — see film"). Nav, `sitemap.xml`, canonical and the SEO
  backlog all need the new URL. **Do not delete the content** — it is where the business
  started and it still sells.
  **As built:** `film.html` is a new self-contained page — its own trimmed stylesheet using
  the same tokens, its own theme toggle sharing the `ssd-theme` key, masthead and footer
  matching the home page, and a "looking for the survey side?" block routing back. Follows
  the pattern `capability-statement.html` already set: no shared stylesheet, because the
  site has no build step. `index.html` keeps a one-line comment where the section was,
  recording *why* it moved, and the footer links to it. The hero's "see the reel" link now
  points at `/film`.
- [x] **P1.7 — Housekeeping that follows from 1.6.** `sitemap.xml` gains `/film`;
  canonicals added to all four pages (home, film, capability statement, privacy) — `SEO.md`
  had flagged "no canonical" as a 2.5/5 weakness. URL surface goes from three to four,
  against the same file's "three URLs only" note. **Still to do: re-run the SEO audit script
  and update the `SEO.md` scorecard.**

---

## Phase 2 — Gated on Phase 0 evidence

- [ ] **P2.1 — Add professional indemnity to the compliance block.** *Gate: P0.1 bound.*
  One row beside the existing PL row, limit stated, certificate on request. Also add to
  `capability-statement.html`.
- [ ] **P2.2 — A named case study page.** *Gate: P0.2 delivered and permission in writing.*
  One live site: what was flown, the cadence, what the pack was used for, and a named
  reference willing to take a call. This is worth more than every other item on this list
  combined, and it is the one thing the site cannot fake. Until it exists the portfolio is
  *"a car park and a church"* — which is exactly how a contractor will read it.
- [ ] **P2.3 — Data retention, IP and GDPR block.** *Gate: P0.3 written.* Into
  `privacy.html`, summarised on the capability statement.
- [ ] **P2.4 — Company number on the capability statement.** *Gate: P0.4 decided.*

---

## Phase 3 — Procurement readiness (weeks, and only once a real prospect asks)

Tier 1 supply chains are entered through these. Do not chase them speculatively — chase
them the first time a prospect's form demands one, then keep the badge.

- [ ] **P3.1 — CDM statement + CSCS.** A one-paragraph position on where a visiting
  surveyor sits under CDM 2015, plus the appropriate CSCS route for a visitor/professional.
  Cheap, and asked for at induction constantly.
- [ ] **P3.2 — Register with Constructionline and/or CHAS** (SafeContractor and Achilles as
  alternates). *Gate: P0.1 + P0.4.* These are the doors into tier 1 supply chains and none
  is currently mentioned on the site.
- [ ] **P3.3 — ISO 9001 / 45001, or a stated equivalent.** Full certification is
  disproportionate for a sole operator; a written, honest "equivalent practice" statement
  is not, and is usually accepted at this scale. Say which it is — never imply the badge.
- [ ] **P3.4 — Cyber Essentials.** Cheap, increasingly mandatory in public-sector and tier 1
  supply chains, and directly relevant because the deliverable is data.

---

## Phase 4 — Strategic (changes the offer, not the copy)

- [ ] **P4.1 — C2-class RTK aircraft (Mavic 3 Enterprise).** *The review's highest-ROI
  recommendation, and it is correct in direction:* it moves the business out of the small
  visual-record budget and into the **earthworks / cut-and-fill** budget, which is the
  largest recurring line and where the housebuilder relationships sit. **But its
  arithmetic — "three sites over six months pays for it" — is only true if three sites
  exist, and today zero do.** Gate this on the **first paying recurring client**, not on
  the plan. Until then the pricing table's existing *hired kit · POA* rows for topo and
  stockpile volumes are the honest and sufficient answer.
  When it does land, it forces a rewrite of the accuracy section, a new accuracy statement
  with ground control, and a second preset — that is a project, not a page edit.
- [ ] **P4.2 — Framework / tender route.** Public frameworks under CPV 79961200 are real,
  recurring and winnable by SMEs — the review cites a 24-month Fife Council drone survey
  framework (£279,575–£304,245 range of offers) and an Ordnance Survey UAV award of
  £1,092,200 to an SME, where all 10 tenders received were from SMEs. Set a Find a Tender
  alert now (free, zero effort); bid nothing until P0.1, P2.2 and Phase 3 exist, because
  a PQQ without PI and a reference is a wasted week.

---

## What the competitors prove, and what to copy

| Who | What they actually sell | The transferable lesson |
|---|---|---|
| **Drone Surveying Ltd** — names Taylor Wimpey, Barratt Redrow, Bellway, Miller Homes, Vistry | Not flights: a portal + mobile app, live checks, measurements in minutes | **They sell a replacement for a surveyor, not a survey.** The recurring product *is* the software layer |
| **Kemp Engineering & Surveys** — Balfour Beatty, BAM, Costain, Kier, Tilbury Douglas | A survey practice that *added* drone | Credibility came from the survey business, not the aircraft |
| **Sensat** — mapped 120 miles of the M25 for Balfour Beatty's Connect Plus | Platform | Data capture is the wedge; the platform is the business |

**Nobody wins by owning a drone.** The winning categories are a survey business, a
recurring reporting product with software, or a framework position. *"Drone pilot"* is the
losing category — and note that this repo already has the beginnings of the second one
(`ddt viewer`, the site registry, the saved mission, `publish_site.py`). That is the asset
to lean on, and P1.1 is where it first becomes visible to a buyer.

---

## Explicitly NOT doing, and why

- **Not softening the accuracy statement.** The percentiles, the heavy-tail note and the
  refusal to price hired kit as owned kit are the strongest credibility assets on the site
  and the review says so too. They stay exactly as they are.
- **Not deleting "48 hours"** — demoting it. It is a genuine capability and a real
  differentiator against a monthly-report competitor; it is just the wrong *headline*.
- **Not cutting to literally one segment.** The review names two that pay recurring money
  (PM and QS/commercial) and then says cut to one. Lead with **one** (Main contractor / PM)
  and keep **QS / commercial** as the second door — same buyer chain, and the QS is the one
  with a live dispute and therefore urgency. Cutting the other four is the actual win.
- **Not buying the RTK aircraft yet.** See P4.1 — right call, wrong order.
- **Not claiming any accreditation, insurance or certification before it is held.** Every
  Phase 2–3 item carries a gate for exactly this reason.

---

## Coordination note

The website lives in a **separate Claude Code session** from the `drone-delivery-tool`
processing repo. Two things carry across and will bite:

1. **`deliverables/st-mary-magdalene/` currently holds the REJECTED ultra church model**
   (13,466,712 B, visible mesh gaps); the good one is at `…​.prev` (10,841,060 B) and is
   what the live site serves. **A re-sync from `deliverables/` puts the gappy model back on
   the live site.** Roll back before syncing — the command is in that repo's `CLAUDE.md`.
2. Deliverable paths and the `manifest.json` schema are contracted in that repo's
   `HANDOVER.md`. Anything on this list that changes what the site displays should be
   checked against it.
