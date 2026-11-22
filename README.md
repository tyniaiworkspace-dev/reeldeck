# ReelDeck — one place for the AI-story reels

A tiny installable web app (PWA) that puts the family's AI-story / short-drama reels in
one screen, plays them with the **platform's own player**, and opens the native app for
anything that refuses to embed. No downloads, no re-hosting, no accounts.

## Open it on a phone

Same Wi-Fi as this PC:

```
http://192.168.8.221:8788
```

Then in Chrome: **⋮ → Add to Home screen → Install**. It gets its own icon and opens
fullscreen. (That menu item works on plain HTTP; the offline cache only switches on
under HTTPS.)

Away from home, the PC's Tailscale address works if the phone is on the tailnet:

```
http://100.72.81.62:8788
```

## What each tab does

| Tab | What you get |
|---|---|
| **Feed** | Newest videos from Dailymotion. "Following" merges the channels you follow; "All AI stories" searches the topic; "10 min+" filters to the long compilations. |
| **Channels** | Follow/unfollow the curated AI-story channels, or paste any Dailymotion channel link to add one. |
| **Links** | Paste a Facebook reel, TikTok video, Dailymotion or YouTube link and it plays here or opens in the app that owns it. Plus one-tap tiles for the apps they already use, and a local "recently opened" list. |

## Why this shape

- **Dailymotion is the only one with a free, keyless, CORS-enabled API**, so it is the
  live feed. That is also where a lot of the AI-story channels mirror their uploads.
- **TikTok and YouTube embed without a login** — paste a link, it plays inline.
- **Facebook Reels mostly demand a login** to embed, so Facebook links get the
  "Open in app" button instead of a broken black box.
- Everything is a link or an official embed. Nothing is copied, so nothing here is a
  re-host and there is nothing to keep in sync or take down.

## Add or change channels

Channels live in two places:

1. `DEFAULT_CHANNELS` in `index.html` — the six seeded Dailymotion channels
   (`Tales by Jenny`, `KIDS CORNER`, `Ai Video`, `Cartoon Boy`, `ASMR world`, `Meow Media`).
2. Anything added from the **Channels** tab → saved in this phone's `localStorage`
   (`rd.extraChannels`, `rd.follows`).

To change the seed list, edit that array and reload. To start a phone fresh, clear the
site's storage in Chrome settings.

## Run / stop

It runs as a user service:

```bash
systemctl --user status reeldeck     # is it up?
systemctl --user restart reeldeck    # after editing files
systemctl --user disable --now reeldeck
```

Manual run (foreground): `./serve.sh`

## Files

```
index.html            the whole app (UI + logic)
manifest.webmanifest  install metadata
sw.js                 offline shell cache (HTTPS only)
icons/                app icons
serve.sh              python3 -m http.server 8788
```

## Limits worth knowing

- Dailymotion's public API returns roughly the newest 1,000 matches for a search term;
  very deep paging stops there.
- The "10 min+" chip filters the batch already loaded; switch to **All AI stories** to
  pull long compilations.
- Facebook feed enumeration is not available without a logged-in session, so Facebook is
  link-and-open only.
- Thumbnails come from Dailymotion's CDN and can 404 when an upload is removed.
