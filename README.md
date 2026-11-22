# ReelDeck — one place for the AI-story reels

A small installable web app for five phones. It puts AI-story / AI short-drama reels in one
screen, plays them with the **platform's own player**, keeps a per-phone saved list with a
working-link check, and accepts links straight from the Android share sheet.

**Hosted free:** https://tyniaiworkspace-dev.github.io/reeldeck/
**Home Wi-Fi copy:** http://192.168.8.221:8788 (runs on the PC, `systemctl --user status reeldeck`)

No accounts, no logins, no Tailscale, no downloads, no re-hosting.

## Put it on a phone

1. Open the hosted URL in Chrome.
2. **⋮ → Add to Home screen → Install.** It gets its own icon and opens fullscreen.
3. Scan the QR in a sister's phone if that is easier: `qr-lan.png` (LAN copy).

Each phone keeps its own state — follows, saved list, history. There is nothing to sign into.

## The four tabs

| Tab | What it does |
|---|---|
| **Feed** | Newest videos from Dailymotion. Chips switch genre (AI stories / short drama / AI tales), show only complete stories, and filter to 10 min+. Every card plays inline. |
| **Saved** | **Family picks** — one shared list read from `family.json`, identical on all five phones. **Your list** — only on that phone. Every item shows `works`, `gone`, or `in app`, plus when it was last checked. |
| **Channels** | Follow/unfollow the seeded AI-story channels, or paste any Dailymotion channel link. |
| **Links** | Paste a Facebook / TikTok / Dailymotion / YouTube link, or tap the app tiles. |

## Sharing between the five phones

Three routes, all free:

- **Share sheet → ReelDeck.** In Facebook or TikTok, tap Share → ReelDeck. The link lands in
  the app, opens, and is saved to that phone's list automatically.
- **ReelDeck links.** Every video has a short link like
  `…/reeldeck/#dm/xbyvybi` (`dm` Dailymotion, `fb` Facebook, `tt` TikTok, `yt` YouTube).
  Send it in WhatsApp; it opens straight into the player on any phone.
- **Share my list.** On the Saved tab, "Share my list" builds a single import link. A sister
  opens it, taps **Add**, and gets the whole list (each item is re-checked on arrival).

## Full stories, not fragments

Dailymotion titles carry the only reliable signal, so the app reads them:

- `Part 1/3`, `Part 1/2`, `Episode 2`, `Episodes 1-40` are parsed, and the part marker is
  stripped to form the story's base title.
- Uploads with the same base title are grouped. Long shared titles can group across channels,
  because the same drama is reposted widely; short generic titles stay per channel.
- Each group gets a label: **FULL** (the title says full / complete / all episodes, or it is
  `Part 1/1`), **ALL 3 PARTS** (complete numbered set), **3 PARTS** (set, total unknown), or
  **PART 1/3** (incomplete).
- **Full stories** (on by default) hides every incomplete group, so the feed only offers
  stories you can watch start to finish. Switch it off to see the fragments.
- A multi-part set opens with a parts bar and **Play all**, which advances to the next part
  when the current one ends.

**When a copy is blocked or only a part exists**, the player's **Find the full version** button
searches the cleaned title and lists other uploads, full ones first, longest first. In testing,
one title returned 49 versions with 6 marked FULL, including 2–3 hour complete cuts.

## When the Dailymotion app asks for an email

Dailymotion allows guest viewing in its own terms, but the Android app pushes a sign-in
screen. On Android the player's open button is therefore labelled **Open in Chrome** and
uses an `intent://…package=com.android.chrome` link, which hands the same video page to
Chrome instead of the app. No account is needed there. The button falls back to the normal
link if Chrome is missing.

## Link checking

- **Dailymotion and YouTube** are verified in the browser: title, thumbnail and duration are
  refetched, and a 404 marks the item `gone`.
- **TikTok and Facebook** cannot be verified without a login, so they are labelled `in app`
  instead of pretending they passed.
- "Re-check all" reruns the check on demand, and each card shows how long ago it passed.

## Shared storage (the Google Drive question)

The family picks and the channel list live as two small JSON files in this repo:
`family.json` and `channels.json`. Editing either one changes the app for all five phones on
the next open. That does the job Google Drive would, without OAuth, quota or a login for
anyone. Each sister's personal list stays on her own phone.

## Files

```
index.html            the whole app
manifest.webmanifest  install metadata + Android share target
sw.js                 offline shell + POST /share → ?share= redirect
channels.json         shared channel list and genre chips
family.json           shared "Family picks"
icons/                app icons
qr-lan.png            QR for the LAN copy
serve.sh              python3 -m http.server 8788 (local copy)
```

## Local copy

```bash
systemctl --user status reeldeck     # is it up?
systemctl --user restart reeldeck    # after editing files
./serve.sh                           # foreground alternative
```

## Limits

- Completeness is inferred from titles and part numbers. A fragment whose title carries no
  marker and has no sibling looks complete; **Find the full version** is the escape hatch.
- Dailymotion refuses direct stream URLs through its public API (`stream_h264_url` returns
  403), so there is no custom-player route around a blocked embed. Mirrored uploads are the
  workaround.
- Facebook Reels need a login to embed, so those open in the Facebook app.
- Dailymotion's public API returns about the newest 1,000 matches per search term.
- The "10 min+" chip filters the batch already loaded; reopen the genre chip for a fresh pull.
- No account means no server-side backup: clearing Chrome's site data clears that phone's list.
  Use "Share my list" first if you want a copy.
