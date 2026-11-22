# Changelog

Every release gets a version and an entry. Newest first. The version shown at the bottom of the
**Links** tab (`Build x.y.z`) is the version this file's top entry describes.

Format: [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`.
`MINOR` = a new capability, `PATCH` = a fix or a copy change. Dates are AEST.

Entries before 0.7.0 were assembled from the git history on 2026-11-23, when this file was
started; the app had no version number until then.

---

## [0.7.0] — 2026-11-23

### Added
- `CHANGELOG.md` — every future change lands here with a version, a date and its category.
- `APP_VERSION` in the app, exposed as `window.__rd.version` and printed as `Build 0.7.0` in
  the Links tab, so any phone can tell which build it is running.
- Link to this file from the Links tab and from `README.md`.

### Changed
- The "What this runs on" panel now names the build and carries the changelog link.
- `README.md` header carries the version.

### Fixed
- `README.md` still claimed 3,132 stories / 1,371 complete / 3,234 hours after the 0.5.1 crawl.
  It now matches the live catalogue (4,011 / 1,683 / 5,036 h).

---

## [0.6.1] — 2026-11-23

### Changed
- `README.md`: documents the throwaway inbox and points at `FREE-STACK.md`.

---

## [0.6.0] — 2026-11-23

### Added
- **Throwaway inbox** in the Links tab. Creates a disposable address through Guerrilla Mail's
  public API (keyless, `Access-Control-Allow-Origin: *`, no signup). Copy it, read whatever
  arrives in the page, extend it an hour, forget it. Survives reload via `localStorage['rd.box']`.
- Gmail `+tag` and DuckDuckGo `@duck.com` aliases named in the same panel for anyone who wants
  mail to reach a real inbox.
- `FREE-STACK.md` — the free-tier services that can be wired into one system, with the mail
  providers probed rather than assumed (Guerrilla and maildrop.cc browser-safe; mail.tm has no
  CORS; 1secmail, dropmail.me, mail.gw and tempmail.plus dead).

### Fixed
- The email wall had no cure, only a triage card. It now has one.

---

## [0.5.1] — 2026-11-23

### Changed
- Crawl widened from 3 to 8 keyword searches (`full short drama`, `netshort`, `reelshort`,
  `drama eng sub`, `short drama full movie` added).
- Catalogue grew 3,132 → **4,011 stories**, 1,371 → **1,683 complete**, 5,036 hours total.

---

## [0.5.0] — 2026-11-23

### Added
- **Shelf** — the Feed opens as a whole library instead of a shortlist. `catalog.py` crawls the
  keyless Dailymotion API into `catalog.json`; the page loads it first and falls back to live
  search.
- Client-side search over every story, plus All / Complete / 20 min+ / Following chips.
- 48 cards per page with "Load more (N left)".
- `refresh.sh` + `reeldeck-catalog.timer` — the catalogue rebuilds itself daily at 03:17.
- Auto-promotion: channels with ≥5 uploads of 20 min+ and ≥3 hours of long-form join the crawl
  (`channels-auto.json`).

---

## [0.4.0] — 2026-11-23

### Added
- **Save a copy** in the player: hands the source link to the phone's share sheet, so any
  downloader app (YTDLnis, Seal) can keep the whole episode.
- `rip.sh` — saves a link as one verified mp4 at home. `-N 16` parallel fragments (serial ran at
  240 KB/s, parallel at 3–5 MiB/s).
- `--low` profile (~200 MB) as the bulk default.

### Fixed
- Direct stream URLs are refused by Dailymotion's API (403), so a custom player off their CDN
  is not a route; the downloader route is.

---

## [0.3.2] — 2026-11-23

### Added
- Email-prompt triage card (Incognito, switch data, desktop site, another copy) at a time when
  the cause of the prompt was still unknown.

---

## [0.3.1] — 2026-11-23

### Fixed
- Dailymotion links on Android now offer "Open in Chrome" through an `intent://` URL, so the
  site's own app does not take over the link.

---

## [0.3.0] — 2026-11-23

### Added
- **Series engine.** Parses `Part n/m`, `Pt n`, `Episode n` and `Episodes 1-40` from titles and
  groups the parts, so a story is watched in order instead of found piece by piece.
- Completeness labels: FULL, ALL n PARTS, n PARTS, PART n/m. Complete-only filter on by default.
- **Play all** — auto-advances three seconds before each part ends.
- **Find the full version** — searches the cleaned title with `sort=relevance`, filters by word
  overlap, sorts full-first then longest-first.

---

## [0.2.0] — 2026-11-23

### Added
- Saved-list transfer: "Share my list" builds an `#import/…` link; tapping Add merges the items
  and re-checks them.
- Link checking for Dailymotion and YouTube, marking dead ids `gone`. TikTok and Facebook are
  labelled `in app` rather than faked as verified.
- Channels tab with follows and centrally edited `channels.json` / `family.json`.

---

## [0.1.0] — 2026-11-23

### Added
- First working deck: a live feed of AI-story reels from the keyless Dailymotion API, a saved
  list per phone, Android share-target support, resolver links (`#dm/`, `#fb/`, `#tt/`, `#yt/`),
  and install-to-home-screen as a PWA.
- Hosted free on GitHub Pages; a LAN copy runs from the home machine.
