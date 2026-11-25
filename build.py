#!/usr/bin/env python3
"""Build the Simple Science Around Us static site into docs/ (served by GitHub Pages)."""
import json, html, shutil, datetime, re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
D = json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))
X = json.loads((ROOT / "data/extras.json").read_text(encoding="utf-8"))
TOPICS, GEAR, TRY = X["topics"], X["gear"], X["try"]
QS = sorted(D["questions"], key=lambda q: q["published"], reverse=True)
CHANNEL = "https://www.youtube.com/channel/UCeI7TSO4NyU83jbTScY5X0Q"
SOCIAL = [("YouTube", CHANNEL), ("TikTok", "https://www.tiktok.com/@simplesciencearoundus"),
          ("Instagram", "https://www.instagram.com/simplesciencearoundus/"),
          ("Facebook", "https://www.facebook.com/1515255428327941")]
e = html.escape
assert all(s in {q["slug"] for q in QS} for s in TRY)

# One simple line-icon per topic, used for topic chips and product tiles.
ICON = {
    "S01": '<path d="M24 6c6 8 12 15 12 22a12 12 0 0 1-24 0c0-7 6-14 12-22z"/>',
    "S02": '<path d="M20 8a4 4 0 0 1 8 0v18a8 8 0 1 1-8 0z"/><path d="M24 18v14"/>',
    "S03": '<path d="M17 6h14M19 6v12L9 36a3 3 0 0 0 3 4h24a3 3 0 0 0 3-4L29 18V6"/><path d="M14 30h20"/>',
    "S04": '<path d="M24 6 40 38H8z"/><path d="M4 22h12M30 24l14-6M31 28l14 2"/>',
    "S05": '<path d="M8 19h7l9-8v26l-9-8H8z"/><path d="M31 17a9 9 0 0 1 0 14M36 12a16 16 0 0 1 0 24"/>',
    "S06": '<path d="M6 34h36"/><path d="M10 30 38 14"/><path d="M22 34l2-12 2 12"/><circle cx="12" cy="26" r="4"/>',
}


def icon(code, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true">{ICON[code]}</svg>'


def thumb(q):
    return f"https://i.ytimg.com/vi/{q['video_id']}/hqdefault.jpg"


def one_liner(q):
    s = q["sentences"][-1]["en"].strip()
    s = re.sub(r"^(So|That's why)\s*,?\s*", "", s)
    return s[0].upper() + s[1:]


LOGO = """<svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#1d4ed8"/><path d="M15 9h10M17 9v9l-7 11a3 3 0 0 0 2.6 4.5h14.8A3 3 0 0 0 30 29l-7-11V9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/><path d="M12.6 27h14.8l1.4 2.4a1.5 1.5 0 0 1-1.3 2.1H12.5a1.5 1.5 0 0 1-1.3-2.1z" fill="#ffc53d"/></svg>"""


def page(title, desc, body, depth=0, cls="", og=None):
    up = "../" * depth
    soc = "".join(f'<a href="{u}">{n}</a>' for n, u in SOCIAL)
    ogimg = f'<meta property="og:image" content="{og}">' if og else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">{ogimg}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css">
</head><body class="{cls}">
<header class="top"><a class="brand" href="{up}index.html">{LOGO}<span>Simple Science</span></a>
<nav><a href="{up}index.html#watch">Watch</a><a href="{up}index.html#try">Try it</a><a class="shop" href="{up}kits.html">Shop kits</a></nav></header>
<main>{body}</main>
<footer class="foot"><div class="fs">{soc}</div>
<p>Some links may be affiliate links: we may earn a small commission at no extra cost to you. <a href="{up}about.html">About &amp; disclosure</a></p></footer>
<script src="{up}assets/site.js"></script>
</body></html>"""


def chips(up="", active=None):
    out = []
    for c, t in TOPICS.items():
        on = ' aria-current="page"' if c == active else ""
        out.append(f'<a class="chip" style="--c:{t["color"]}" href="{up}topics/{t["slug"]}.html"{on}>{icon(c)}{e(t["name"])}</a>')
    return '<nav class="chips" aria-label="Topics">' + "".join(out) + "</nav>"


def vcard(q, up="", big=False):
    t = TOPICS[q["series"]]
    tag = '<span class="badge">Try it</span>' if q["slug"] in TRY else ""
    return (f'<a class="vc{" vbig" if big else ""}" href="{up}q/{q["slug"]}.html" style="--c:{t["color"]}">'
            f'<span class="vimg"><img src="{thumb(q)}" alt="" loading="lazy" onerror="this.remove()"><span class="pl" aria-hidden="true"></span>{tag}</span>'
            f'<span class="vq">{e(q["question"])}</span></a>')


def pcard(g, code, up=""):
    t = TOPICS[code]
    return (f'<div class="pc" style="--c:{t["color"]}"><div class="pimg">{icon(code, "pic")}</div>'
            f'<b>{e(g["name"])}</b><span class="age">Ages {e(g["age"].replace("All ages with an adult", "all, with an adult"))}</span>'
            f'<span class="buy" aria-disabled="true">Shop link soon</span></div>')


def rail(inner, cls="rail"):
    return f'<div class="{cls}" tabindex="0">{inner}</div>'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "q").mkdir(parents=True)
    (OUT / "topics").mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    by = {}
    for q in QS:
        by.setdefault(q["series"], []).append(q)
    tries = [q for q in QS if q["slug"] in TRY]

    # Home
    allgear = "".join(pcard(g, c) for c in TOPICS for g in GEAR[c][:1])
    body = f"""<section class="hero"><div class="hcopy"><h1>Everyday science<br>in 60 seconds</h1>
<p>Short videos that explain the things you see every day.</p>
<a class="btn" href="#watch">Start watching</a></div>
<div class="hrail">{''.join(vcard(q, big=True) for q in QS[:6])}</div></section>
{chips()}
<section class="sec" id="watch"><div class="sh"><h2>New this week</h2><a href="{CHANNEL}">See all on YouTube</a></div>
<div class="grid">{''.join(vcard(q) for q in QS[:12])}</div></section>
<section class="sec band-sun" id="try"><div class="sh"><h2>Try it at home</h2><span>5 minutes · no special gear</span></div>
{rail(''.join(vcard(q) for q in tries))}</section>
<section class="sec"><div class="sh"><h2>Shop the experiment</h2><a href="kits.html">All kits</a></div>
{rail(allgear, 'rail prail')}</section>
<section class="sec"><div class="sh"><h2>More to watch</h2></div><div class="grid">{''.join(vcard(q) for q in QS[12:])}</div></section>"""
    (OUT / "index.html").write_text(page("Simple Science Around Us – everyday science in 60 seconds",
        "Short videos that explain everyday science: why ice floats, why a cold glass gets wet, and more.", body,
        og=thumb(QS[0])), encoding="utf-8")

    # Topics
    for c, t in TOPICS.items():
        qs = by.get(c, [])
        pl = D["playlists"].get(c)
        pll = f'<a class="btn ghost" href="https://www.youtube.com/playlist?list={e(pl)}">Play all</a>' if pl else ""
        body = f"""<section class="thead" style="--c:{t['color']}">{icon(c, 'tic')}<div><h1>{e(t['name'])}</h1><p>{len(qs)} videos</p></div>{pll}</section>
{chips('../', c)}
<section class="sec"><div class="grid">{''.join(vcard(q, '../') for q in qs)}</div></section>
<section class="sec"><div class="sh"><h2>Shop this topic</h2></div>{rail(''.join(pcard(g, c) for g in GEAR[c]), 'rail prail')}</section>"""
        (OUT / "topics" / f"{t['slug']}.html").write_text(page(f"{t['name']} – Simple Science Around Us", t["blurb"], body, 1,
            og=thumb(qs[0]) if qs else None), encoding="utf-8")

    # Questions
    for i, q in enumerate(QS):
        t = TOPICS[q["series"]]
        rel = [r for r in by[q["series"]] if r["slug"] != q["slug"]]
        nxt = rel[0] if rel else QS[(i + 1) % len(QS)]
        tr = TRY.get(q["slug"])
        tryb = ""
        if tr:
            steps = "".join(f'<li><span>{n}</span>{e(s)}</li>' for n, s in enumerate(tr["steps"], 1))
            need = " · ".join(e(x) for x in tr["need"])
            tryb = (f'<section class="try"><h2>Try it at home</h2><p class="need"><b>You need</b> {need}</p>'
                    f'<ol class="steps">{steps}</ol><p class="see"><b>What happens</b> {e(tr["see"].split(". ")[0])}.</p>'
                    f'<p class="safe">{e(tr["safety"])}</p></section>')
        en = "".join(f"<p>{e(x['en'])}</p>" for x in q["sentences"])
        es = "".join(f"<p>{e(x['es'])}</p>" for x in q["sentences"])
        src = "".join(f'<li><a href="{e(x["url"])}" rel="nofollow">{e(x["title"])}</a></li>' for x in q["sources"])
        body = f"""<article class="qp" style="--c:{t['color']}">
<div class="player"><button class="vid" data-id="{e(q['video_id'])}" aria-label="Play video: {e(q['question'])}"><img src="{thumb(q)}" alt="" onerror="this.remove()"><span class="pl" aria-hidden="true"></span></button></div>
<div class="qside"><a class="tp" href="../topics/{t['slug']}.html">{icon(q['series'])}{e(t['name'])}</a>
<h1>{e(q['question'])}</h1>
<p class="ans">{e(one_liner(q))}</p>
{tryb}
<section class="kit"><h2>Get the kit</h2>{rail(''.join(pcard(g, q['series'], '../') for g in GEAR[q['series']]), 'rail prail')}</section>
<details class="more"><summary>Read the full explanation</summary><div>{en}<h3>En español</h3>{es}<h3>Sources</h3><ul>{src}</ul>
<p class="meta">Illustrations in the video are models, not to scale. AI-generated narration.</p></div></details>
</div></article>
<section class="sec"><div class="sh"><h2>Watch next</h2></div>{rail(''.join(vcard(r, '../') for r in (rel + [x for x in QS if x['series'] != q['series']])[:10]))}</section>
<a class="nextbar" href="{nxt['slug']}.html" style="--c:{TOPICS[nxt['series']]['color']}"><span>Next</span><b>{e(nxt['question'])}</b></a>"""
        (OUT / "q" / f"{q['slug']}.html").write_text(page(f"{q['question']} – Simple Science Around Us", one_liner(q), body, 1, "qpage", og=thumb(q)), encoding="utf-8")

    # Kits
    blocks = "".join(f'<section class="sec"><div class="sh"><h2><a href="topics/{t["slug"]}.html">{e(t["name"])}</a></h2></div>'
                     f'<div class="pgrid">{"".join(pcard(g, c) for g in GEAR[c])}</div></section>' for c, t in TOPICS.items())
    body = f"""<section class="thead" style="--c:#1d4ed8"><div><h1>Science kits</h1><p>Tools that match our videos. Shop links coming soon.</p></div></section>
{chips()}{blocks}<p class="note">Check the age rating on the box. Keep small parts, magnets and glass away from young children.</p>"""
    (OUT / "kits.html").write_text(page("Science kits – Simple Science Around Us", "Science kits and tools that match each everyday science topic.", body), encoding="utf-8")

    # About
    body = f"""<section class="thead" style="--c:#1d4ed8"><div><h1>About</h1></div></section>
<section class="sec prose"><p>Simple Science Around Us answers everyday "why" questions in one-minute videos with English and Spanish subtitles. Scripts are checked against the sources listed on each page. Narration is AI-generated and illustrations are simplified models.</p>
<h2>Affiliate disclosure</h2><p>Some links on this site may be affiliate links. If you buy through them, we may earn a small commission at no extra cost to you. We only suggest products that fit the experiments we show.</p>
<h2>Privacy</h2><p>No accounts, forms or tracking cookies. Videos play in YouTube's privacy-enhanced player only when you press play.</p></section>"""
    (OUT / "about.html").write_text(page("About – Simple Science Around Us", "About the channel, affiliate disclosure and privacy.", body), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print("built", len(QS), "questions")


if __name__ == "__main__":
    build()
