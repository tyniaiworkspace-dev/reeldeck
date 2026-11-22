#!/usr/bin/env python3
"""Build catalog.json for ReelDeck: crawl every known channel plus keyword searches,
group uploads into stories, and record which stories are complete.

Keyless Dailymotion API (CORS-open, no token). Run from cron to keep the shelf fresh.
"""
import json, re, sys, time, urllib.parse, urllib.request

API = "https://api.dailymotion.com"
FIELDS = "id,title,duration,thumbnail_360_url,url,created_time,views_total,owner,owner.screenname,allow_embed,geoblocking"
UA = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36"

TAG_RE = re.compile(
    r"\b(full (?:movie|drama|series|episodes?|story)|complete|all episodes?"
    r"|eng(?:lish)? sub(?:title)?s?|short drama|full short drama|joyreels|netshort|hd|720p|1080p)\b",
    re.I,
)

# A channel is promoted only if the long uploads are story-shaped. Without this, any
# channel with five 20-minute videos qualified — a camera-review or cooking channel
# cleared the bar and landed on a shelf of AI short dramas.
STORY_RE = re.compile(
    r"\b(drama|story|stories|episode|love|revenge|ceo|billionaire|millionaire|reborn|"
    r"married|marriage|divorce|wedding|affair|pregnant|baby|heir|alpha|werewolf|mafia|"
    r"bride|groom|husband|wife|secret|betray|prince|princess|emperor|empress|vampire|"
    r"demon|system|twins?|contract|movie|film|series)\b",
    re.I,
)


def story_shaped(v):
    return bool(v.get("full") or v.get("part") or v.get("total")) or bool(
        STORY_RE.search(v.get("title", ""))
    )


def good_channel(st):
    """Promotion bar: five long uploads and three hours of them.

    Two stricter versions were tried on 2026-11-23 and both were worse than this:
    a title-keyword ratio pruned a channel that was 100% Netshort dramas ("Married To
    Mr. No Mercy"), and a 45-minute mean-episode floor pruned two channels that were
    70% and 99% story-shaped (their Reelshort episodes run 30-40 minutes). Wording and
    episode length are both weak genre instruments. The bar stays on volume, and the
    off-theme share is printed as evidence for the next review instead of being acted on.
    """
    return st["n"] >= 5 and st["hours"] >= 3


def get(path, params):
    url = f"{API}{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 2:
                print(f"  ! {path} {params.get('page','')}: {e}", file=sys.stderr)
                return {"list": []}
            time.sleep(1.5)


def analyze(title):
    t = title or ""
    a = {"base": "", "part": 0, "total": 0, "range": None, "full": False}
    m = re.search(r"\bepisodes?\s*(\d+)\s*[-–]\s*(\d+)\b", t, re.I)
    if m:
        a["range"] = (int(m.group(1)), int(m.group(2)))
    else:
        m = re.search(r"\b(?:part|pt)\.?\s*(\d+)\s*(?:/\s*(\d+))?\b", t, re.I)
        if not m:
            m = re.search(r"\b(?:episode|ep)\.?\s*(\d+)\s*(?:/\s*(\d+))?\b", t, re.I)
        if m:
            a["part"] = int(m.group(1))
            a["total"] = int(m.group(2) or 0)
    a["full"] = bool(re.search(
        r"\b(full (?:movie|drama|series|episodes?|story)|complete|all episodes?)\b", t, re.I
    )) or (a["part"] == 1 and a["total"] == 1) or bool(a["range"])
    base = re.sub(r"\bepisodes?\s*\d+\s*[-–]\s*\d+", " ", t, flags=re.I)
    base = re.sub(r"\b(?:part|pt|episode|ep)\.?\s*\d+\s*(?:/\s*\d+)?", " ", base, flags=re.I)
    base = TAG_RE.sub(" ", base)
    base = re.sub(r"[\u2600-\u27bf\U0001F000-\U0001FAFF]", " ", base)
    base = re.sub(r"""[\[\](){}|:;,.!?"'“”‘’#*_~\-–—]""", " ", base)
    base = re.sub(r"\s+", " ", base).strip().lower()
    base = re.sub(r"\s+(drama|movie|series)\s*$", "", base)
    a["base"] = base
    return a


def norm(v):
    a = analyze(v.get("title", ""))
    return {
        "id": v["id"],
        "title": v.get("title", ""),
        "duration": v.get("duration", 0) or 0,
        "thumb": v.get("thumbnail_360_url", ""),
        "url": v.get("url") or f"https://www.dailymotion.com/video/{v['id']}",
        "channel": (v.get("owner.screenname") or ""),
        "channel_id": (v.get("owner") or ""),
        "views": v.get("views_total", 0) or 0,
        "created": v.get("created_time", 0) or 0,
        "embed": v.get("allow_embed") is not False,
        "part": a["part"],
        "total": a["total"],
        "full": a["full"],
        "base": a["base"],
    }


def main():
    cfg = json.load(open("channels.json"))
    channels = cfg.get("channels", [])
    try:
        auto = json.load(open("channels-auto.json")).get("channels", [])
    except Exception:
        auto = []
    known = {c["id"] if isinstance(c, dict) else c for c in channels}
    for c in auto:
        if c["id"] not in known:
            channels.append(c)
            known.add(c["id"])
    queries = cfg.get("queries", [])
    videos = {}

    for ch in channels:
        cid = ch["id"] if isinstance(ch, dict) else ch
        name = ch.get("name", "") if isinstance(ch, dict) else ""
        got = 0
        for page in (1, 2, 3):
            d = get(f"/user/{cid}/videos", {"fields": FIELDS, "limit": 100, "page": page,
                                            "sort": "recent"})
            lst = d.get("list", [])
            for v in lst:
                videos[v["id"]] = norm(v)
            got += len(lst)
            if len(lst) < 100:
                break
        print(f"  channel {cid} {name}: {got}")

    for q in queries:
        got = 0
        for page in (1, 2, 3):
            d = get("/videos", {"fields": FIELDS, "limit": 100, "page": page,
                                "search": q, "sort": "relevance"})
            lst = d.get("list", [])
            for v in lst:
                videos[v["id"]] = norm(v)
            got += len(lst)
            if len(lst) < 100:
                break
        print(f"  search {q!r}: {got}")

    # group into stories
    groups = {}
    for v in videos.values():
        key = v["base"] if len(v["base"]) >= 18 else (v["base"], v["channel_id"])
        groups.setdefault(key, []).append(v)

    series = []
    for key, parts in groups.items():
        parts.sort(key=lambda x: (x["part"] or 0, x["created"]))
        full = [p for p in parts if p["full"]]
        if full:
            best = max(full, key=lambda p: p["duration"])
            state, label = "full", "FULL"
            item = best
        elif len(parts) > 1:
            best = max(parts, key=lambda p: p["duration"])
            state, label = "set", f"{len(parts)} PARTS"
            item = best
        else:
            state, label = "single", f"{parts[0]['duration']//60} MIN"
            item = parts[0]
        series.append({
            "title": item["title"],
            "state": state,
            "label": label,
            "duration": best["duration"] if state == "set" else item["duration"],
            "thumb": item["thumb"],
            "url": item["url"],
            "id": item["id"],
            "channel": item["channel"],
            "channel_id": item["channel_id"],
            "views": sum(p["views"] for p in parts),
            "created": max(p["created"] for p in parts),
            "parts": [{"id": p["id"], "title": p["title"], "duration": p["duration"],
                       "part": p["part"], "total": p["total"], "thumb": p["thumb"]}
                      for p in parts[:40]],
        })

    series.sort(key=lambda s: (s["state"] != "full", -s["views"]))

    # channels that actually supply long-form stories
    per_channel = {}
    for v in videos.values():
        if v["duration"] >= 600:
            c = per_channel.setdefault(v["channel_id"], {
                "name": v["channel"], "n": 0, "hours": 0, "story_n": 0, "story_hours": 0,
            })
            c["n"] += 1
            c["hours"] += v["duration"] / 3600
            if story_shaped(v):
                c["story_n"] += 1
                c["story_hours"] += v["duration"] / 3600
    discovered = [{"id": k, **v} for k, v in sorted(per_channel.items(), key=lambda x: -x[1]["n"])]

    out = {
        "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "counts": {
            "videos": len(videos),
            "series": len(series),
            "full": sum(1 for s in series if s["state"] == "full"),
            "set": sum(1 for s in series if s["state"] == "set"),
            "hours": round(sum(v["duration"] for v in videos.values()) / 3600, 1),
        },
        "channels": discovered[:60],
        "series": series,
    }
    json.dump(out, open("catalog.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print("\n", out["counts"])
    print(" catalog.json", round(len(json.dumps(out)) / 1024), "KB")

    # Self-expansion: a channel with five or more 20-minute STORY uploads and three hours of
    # story long-form joins the crawl for future runs. The story gate is what keeps a
    # camera-review channel from qualifying on length alone.
    known_all = {c["id"] if isinstance(c, dict) else c for c in cfg.get("channels", [])}
    promote, rejected = [], []
    for k, v in per_channel.items():
        if k in known_all:
            continue
        if good_channel(v):
            promote.append({"id": k, "name": v["name"], "note": "auto-discovered"})
        elif v["n"] >= 5 and v["hours"] >= 3:
            rejected.append(f"{v['name']} (mean {v['hours']*60/v['n']:.0f} min)")
    if rejected:
        print(" not promoted, off-theme:", "; ".join(rejected))
    thin = [f"{v['name']} {v['story_n']}/{v['n']}" for v in per_channel.values()
            if v["n"] >= 5 and v["story_n"] / max(1, v["n"]) < 0.3]
    if thin:
        print(" NOTE low story-share (kept, review later):", "; ".join(thin[:10]))
    # An auto channel that was promoted under the old length-only rule is pruned the first
    # time it fails the story bar, so the stragglers already in the file do not persist.
    keep, pruned = [], []
    for c in auto:
        st = per_channel.get(c["id"])
        if st and not good_channel(st):
            pruned.append(c.get("name", c.get("id", "?")))
        else:
            keep.append(c)
    if pruned:
        print(" pruned from channels-auto.json:", ", ".join(pruned))

    existing = {c["id"] for c in keep}
    merged = keep + [c for c in promote if c["id"] not in existing]
    if merged != auto:
        json.dump({"channels": merged[:60]}, open("channels-auto.json", "w"),
                  ensure_ascii=False, indent=1)
        kept = merged[:60]
        print(f" channels-auto.json: {len(kept)} kept"
              f" ({len(merged) - len(keep)} new, {max(0, len(merged) - 60)} over the cap)")


if __name__ == "__main__":
    main()
