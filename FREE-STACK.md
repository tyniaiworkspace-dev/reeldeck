# The free stack — what can be cobbled into one working system

Everything below is free tier. The point is not the list; it is that each row does one job, so
several rows can be wired together into something that runs with no server bill and no accounts
for the people using it.

Marks: **VERIFIED** = I probed it from this machine on 2026-11-23. **vendor-stated** = the
provider's published free tier; re-check before you depend on it, because these change.

---

## What ReelDeck already is (the worked example)

Five free pieces already running as one system:

| Job | Piece | Cost |
|---|---|---|
| App front end, HTTPS, installable | GitHub Pages | $0, no card |
| Catalogue build + daily refresh | `catalog.py` on the home box, systemd timer | $0 |
| Video data | Dailymotion public API (keyless, CORS-open) | $0 |
| Full-episode copies | `yt-dlp` + `ffmpeg` on the home box | $0 |
| Throwaway address when a site asks | Guerrilla Mail API (CORS-open, keyless) | $0 |

No account anywhere for the five phones. That is the pattern: **static front end + a home
machine that does the crawling + free APIs for everything else.**

---

## Hosting the front end

| Service | Free tier | Card | Good for |
|---|---|---|---|
| **GitHub Pages** | 1 GB site, ~100 GB/mo, public repo | no | what ReelDeck uses **VERIFIED** |
| **Cloudflare Pages** | unlimited bandwidth, 500 builds/mo | no | same, faster, custom domain |
| **Netlify** | 100 GB/mo, 300 build min | no | forms + functions included |
| **Vercel Hobby** | 100 GB/mo | no | Next.js apps (non-commercial) |
| **Surge.sh** | unlimited simple publishing | no | one-command deploy |
| **Codeberg Pages** | free, no tracking | no | non-GitHub option |
| **Neocities** | 1 GB, 200 GB/mo | no | plain static |

**Free domains:** `*.github.io`, `*.pages.dev`, `*.vercel.app`, `*.netlify.app`; DuckDNS or
afraid.org for a real-looking subdomain; Let's Encrypt for TLS.

## Compute, when the home box is asleep

| Service | Free tier | Card | Note |
|---|---|---|---|
| **Cloudflare Workers** | 100,000 requests/day | no | the one I would use — see *next* below |
| **Deno Deploy** | ~100k requests/day | no | instant HTTPS |
| **Val Town** | generous free | no | script + cron + endpoint in one file |
| **Render** | 750 instance-hours/mo | no | free web service sleeps after 15 min |
| **Koyeb** | 1 free service | no | sleeps |
| **Google Cloud Run** | 2M requests/mo | yes | scales to zero |
| **Oracle Always Free** | 4 ARM cores, 24 GB RAM, 200 GB disk | yes | the biggest free VM anywhere; capacity is often unavailable |
| **Hugging Face Spaces** | 2 vCPU / 16 GB CPU-only | no | sleeps; good for demos |

## Storage

| Service | Free tier | Card | Good for |
|---|---|---|---|
| **Google Drive** | 15 GB (shared with Gmail) | no | what the family already knows |
| **Telegram** | 2 GB per file, effectively unlimited total | no | best free video store — but 2 GB needs a *user* session (Telethon), the plain Bot API caps sends at 50 MB |
| **Cloudflare R2** | 10 GB stored, **zero egress** | no | serving files without a bandwidth bill |
| **Backblaze B2** | 10 GB | no | backup |
| **Hugging Face Hub** | unlimited public repos | no | datasets and model weights |
| **Internet Archive** | unlimited public uploads | no | permanent public copies |
| **Supabase Storage** | 1 GB | no | with a database attached |
| **Firebase Storage** | 5 GB | no | mobile apps |
| **catbox.moe** | 200 MB per file, permanent | no | quick share, no account |
| **0x0.st** | 512 MB, 30 days | no | temporary hand-off |

## Databases and auth

| Service | Free tier | Card |
|---|---|---|
| **Supabase** | 500 MB Postgres + auth + storage + realtime | no |
| **Neon** | 0.5 GB Postgres, autosuspend | no |
| **Turso** | 9 GB SQLite, 1B row reads | no |
| **MongoDB Atlas M0** | 512 MB | no |
| **Upstash Redis** | 10k commands/day | no |
| **PocketBase** | self-hosted single binary, unlimited | n/a |

## Email that receives (aliases, throwaways)

| Service | Free tier | Card | Verified here |
|---|---|---|---|
| **Guerrilla Mail API** | disposable inbox, 1 h (extendable), keyless | no | **VERIFIED** — `Access-Control-Allow-Origin: *`, inbox created and read from a browser, welcome mail rendered |
| **maildrop.cc API** | any `@maildrop.cc` alias, GraphQL, CORS-open | no | **read path VERIFIED** (CORS `*`, empty inbox returned); inbound delivery not proven from this box |
| **mail.tm API** | 40 MB inbox, account created by API | no | account creation **VERIFIED**; **not browser-usable** — responses carry no `Access-Control-Allow-Origin`, so it needs a small proxy |
| **DuckDuckGo Email Protection** | unlimited `@duck.com` aliases, forwards to a real inbox, trackers stripped | no | vendor-stated — the best "peace of mind" option for a family member |
| **Firefox Relay** | 5 aliases | no | vendor-stated |
| **SimpleLogin** | 10 aliases | no | vendor-stated |
| **Cloudflare Email Routing** | unlimited aliases on your own domain | no | vendor-stated |
| **Gmail `+tag`** | unlimited, arrives in the same inbox | no | works; tells you who leaked the address |

Dead as of 2026-11-23 (**VERIFIED**): 1secmail (404), dropmail.me (`legacy_token_disabled`),
mail.gw (no API host), tempmail.plus (no CORS).

## Email that sends

| Service | Free tier | Card |
|---|---|---|
| **Resend** | 100/day, 3,000/mo | no |
| **Brevo** | 300/day | no |
| **Mailjet** | 200/day, 6,000/mo | no |
| **SendGrid** | 100/day | no |
| **SMTP2GO** | 1,000/mo | no |
| **Gmail SMTP** | ~500/day with an app password | no |

## Automation, cron, monitoring

| Service | Free tier |
|---|---|
| **GitHub Actions** | 2,000 min/mo private, unlimited on public repos |
| **Cloudflare Cron Triggers** | with a Worker |
| **cron-job.org** | free scheduled HTTP calls |
| **UptimeRobot** | 50 monitors, 5-minute checks |
| **Healthchecks.io** | 20 checks, alerts when a job stops |

## Media

| Service | Free tier |
|---|---|
| **ffmpeg / yt-dlp** | local, unlimited — what `rip.sh` uses |
| **Cloudinary** | 25 credits/mo (transforms + delivery) |
| **imgbb** | free image hosting |
| **Internet Archive** | free permanent video hosting for public-domain material |

---

## What this unlocks next (and the one thing that needs you)

**1. A Cloudflare Worker proxy — needs a Cloudflare login.**
Two jobs, one Worker, free tier:
- **Play Dailymotion inside the page.** The child HLS manifests and segments send no CORS
  headers, which is why the app can only embed. A Worker that re-serves them with CORS turns
  the embed into a real player with our own controls, resume, and "next part" that works.
  Budget: a 72-minute episode is ~720 segment requests, so 100k/day is ~130 episodes/day —
  far more than five people watch.
- **Relay mail.tm.** It is the nicest throwaway inbox (40 MB, chosen password, 8-day life) and
  it is unusable from a browser only because of the missing CORS header. The same Worker fixes
  that in ten lines.

**2. Telegram as the family's video shelf — needs one login.**
`rip.sh` already produces verified full episodes (~200 MB at `--low`). Uploading them to a
Telegram channel gives the sisters a shelf that plays offline-ish, needs no home network, and
costs nothing. The 2 GB-per-file limit needs a user session (Telethon), not a bot token.

**3. Mirror the catalogue to a second free host.**
Pages + Cloudflare Pages from the same repo. If one is blocked on a school or work network the
other still loads. Costs one more sign-in, no code.

---

## The rule that keeps this free

A free tier is a *job*, not a home. Put each thing where its free limit is far above the actual
load: static files on Pages, files on R2 or Telegram, tiny functions on Workers, mail on an
alias service. The moment one row starts carrying the whole system, its free tier becomes the
bill.
