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
| **Feed** | Newest videos from Dailymotion. Chips switch genre (AI stories / short drama / AI tales) and filter to 10 min+. Every card plays inline. |
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

- Facebook Reels need a login to embed, so those open in the Facebook app.
- Dailymotion's public API returns about the newest 1,000 matches per search term.
- The "10 min+" chip filters the batch already loaded; reopen the genre chip for a fresh pull.
- No account means no server-side backup: clearing Chrome's site data clears that phone's list.
  Use "Share my list" first if you want a copy.
