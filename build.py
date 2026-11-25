#!/usr/bin/env python3
"""Build the Simple Science Around Us static site into docs/ (GitHub Pages)."""
import json, html, shutil, datetime
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

missing = [s for s in TRY if s not in {q["slug"] for q in QS}]
assert not missing, missing


def page(title, desc, body, depth=0, cls=""):
    up = "../" * depth
    nav = "".join(f'<a href="{up}topics/{t["slug"]}.html">{e(t["name"])}</a>' for t in TOPICS.values())
    soc = " · ".join(f'<a href="{u}">{n}</a>' for n, u in SOCIAL)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css">
</head><body class="{cls}">
<header class="top"><a class="brand" href="{up}index.html">{LOGO}<span>Simple Science<small>Around Us</small></span></a>
<nav class="scroll">{nav}<a href="{up}kits.html" class="kits">Science kits</a></nav></header>
<main>{body}</main>
<footer class="foot"><div><b>Simple Science Around Us</b><p>Short, sourced answers to the everyday "why" questions. New videos every day.</p><p>{soc}</p></div>
<div><p class="disc">Some links on this site may be affiliate links: if you buy through them we may earn a small commission at no extra cost to you. We only suggest products that fit the experiments we show. <a href="{up}about.html">About, disclosure and privacy</a></p></div></footer>
<script src="{up}assets/site.js"></script>
</body></html>"""


LOGO = """<svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#1d4ed8"/><path d="M15 9h10M17 9v9l-7 11a3 3 0 0 0 2.6 4.5h14.8A3 3 0 0 0 30 29l-7-11V9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/><path d="M12.6 27h14.8l1.4 2.4a1.5 1.5 0 0 1-1.3 2.1H12.5a1.5 1.5 0 0 1-1.3-2.1z" fill="#ffc53d"/></svg>"""

HERO = """<svg class="hero-art" viewBox="0 0 560 420" role="img" aria-label="A cold glass with droplets, a sunny window casting a shadow, and sound waves">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe3ff"/><stop offset="1" stop-color="#eaf3ff"/></linearGradient>
<linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".5" stop-color="#d7e8ff" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity=".9"/></linearGradient>
<linearGradient id="wa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa2ff"/><stop offset="1" stop-color="#1d4ed8"/></linearGradient></defs>
<rect x="0" y="0" width="560" height="420" rx="28" fill="url(#sky)"/>
<rect x="300" y="40" width="210" height="170" rx="10" fill="#fff8db" stroke="#ffffff" stroke-width="10"/>
<circle cx="452" cy="96" r="30" fill="#ffc53d"/><g stroke="#ffc53d" stroke-width="5" stroke-linecap="round"><path d="M452 48v-12M452 156v-12M404 96h-12M512 96h-12M418 62l-8-8M494 138l-8-8M418 130l-8 8M494 54l-8 8"/></g>
<path d="M405 40v170M300 125h210" stroke="#ffffff" stroke-width="8"/>
<rect x="0" y="300" width="560" height="120" fill="#f4d8b8"/><rect x="0" y="300" width="560" height="10" fill="#e8c49c"/>
<path d="M150 300 L60 390 L250 390 L250 300 Z" fill="#1b2a4a" opacity=".12"/>
<g class="drops"><path d="M110 110 h120 l-12 190 a8 8 0 0 1 -8 7 h-80 a8 8 0 0 1 -8 -7z" fill="url(#gl)" stroke="#9cc3ff" stroke-width="3"/>
<path d="M118 170 h104 l-8 128 a6 6 0 0 1 -6 5 h-76 a6 6 0 0 1 -6 -5z" fill="url(#wa)" opacity=".85"/>
<rect x="135" y="185" width="34" height="30" rx="6" fill="#e6f2ff" opacity=".9" transform="rotate(-12 152 200)"/>
<rect x="176" y="196" width="30" height="28" rx="6" fill="#e6f2ff" opacity=".85" transform="rotate(10 191 210)"/>
<g fill="#ffffff" stroke="#7fb2ff" stroke-width="1.5"><circle cx="124" cy="140" r="5"/><circle cx="214" cy="150" r="4"/><circle cx="133" cy="238" r="5.5"/><circle cx="208" cy="262" r="4.5"/><circle cx="170" cy="128" r="3.5"/><path d="M226 205 q4 8 0 12 q-4 -4 0 -12z"/></g></g>
<g fill="none" stroke="#8a4fd8" stroke-width="6" stroke-linecap="round" class="waves"><path d="M330 300 q20 -28 0 -56"/><path d="M356 312 q34 -46 0 -92"/><path d="M382 324 q48 -64 0 -128"/></g>
<circle cx="300" cy="272" r="16" fill="#8a4fd8"/>
</svg>"""


def vid(q, big=False):
    url = f"https://www.youtube.com/shorts/{q['video_id']}"
    t = TOPICS.get(q["series"], {"color": "#1d4ed8"})
    return (f'<a class="vid{" big" if big else ""}" href="{url}" data-id="{e(q["video_id"])}" style="--c:{t["color"]}">'
            f'<span class="play" aria-hidden="true"></span><span class="vq">{e(q["question"])}</span>'
            f'<span class="vw">Watch the 1-minute Short</span></a>')


def card(q, up=""):
    t = TOPICS.get(q["series"], {"name": "", "color": "#1d4ed8"})
    tag = '<span class="tryit">Try it at home</span>' if q["slug"] in TRY else ""
    return (f'<a class="qcard" href="{up}q/{q["slug"]}.html" style="--c:{t["color"]}">'
            f'<span class="qt">{e(t["name"])}</span><b>{e(q["question"])}</b>{tag}</a>')


def gear_block(code, up=""):
    items = "".join(f'<li><b>{e(g["name"])}</b><span>{e(g["why"])}</span><em>Age: {e(g["age"])}</em>'
                    f'<span class="soon">Shop link coming soon</span></li>' for g in GEAR.get(code, []))
    return f'<ul class="gear">{items}</ul>'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "q").mkdir(parents=True)
    (OUT / "topics").mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    by = {}
    for q in QS:
        by.setdefault(q["series"], []).append(q)

    # Home
    tiles = "".join(
        f'<a class="topic" href="topics/{t["slug"]}.html" style="--c:{t["color"]}"><b>{e(t["name"])}</b>'
        f'<span>{e(t["blurb"])}</span><em>{len(by.get(c, []))} questions answered</em></a>'
        for c, t in TOPICS.items())
    latest = "".join(card(q) for q in QS[:9])
    tries = "".join(card(q) for q in QS if q["slug"] in TRY)
    body = f"""<section class="hero band"><div class="hero-copy">
<h1>The science hiding in your kitchen, your bathroom and your backyard</h1>
<p class="lead">Why does a cold glass get wet? Why does ice float? Each answer here is a one-minute video plus a short, sourced explanation you can read with your kids.</p>
<p class="cta"><a class="btn" href="#latest">Start with the latest</a><a class="btn alt" href="{CHANNEL}">Watch on YouTube</a></p>
<p class="stat"><b>{len(QS)}</b> questions answered so far, in English with Spanish translations.</p></div>
{HERO}</section>
<section class="band"><h2>Explore by topic</h2><div class="topics">{tiles}</div></section>
<section class="band soft" id="latest"><h2>Latest answers</h2><div class="qgrid">{latest}</div></section>
<section class="band"><h2>Try it at home</h2><p class="sub">Safe, five-minute experiments with things you already have.</p><div class="qgrid">{tries}</div></section>
<section class="band kitband"><div><h2>Want to go further?</h2><p>We are putting together a short list of science kits and tools that match each topic: hygrometers, prisms, tuning forks, simple-machine sets.</p><a class="btn" href="kits.html">See the kit list</a></div></section>"""
    (OUT / "index.html").write_text(page("Simple Science Around Us – everyday science explained",
        "One-minute videos and short, sourced explanations of everyday science questions.", body, 0, "home"), encoding="utf-8")

    # Topics
    for c, t in TOPICS.items():
        qs = by.get(c, [])
        pl = D["playlists"].get(c)
        pll = f'<a class="btn alt" href="https://www.youtube.com/playlist?list={e(pl)}">Play all on YouTube</a>' if pl else ""
        body = f"""<section class="band thead" style="--c:{t['color']}"><p class="crumb"><a href="../index.html">Home</a> / Topic</p>
<h1>{e(t['name'])}</h1><p class="lead">{e(t['blurb'])}</p><p class="cta">{pll}</p></section>
<section class="band"><h2>{len(qs)} questions answered</h2><div class="qgrid">{''.join(card(q, '../') for q in qs)}</div></section>
<section class="band soft"><h2>Tools for exploring {e(t['name'].lower())}</h2>{gear_block(c)}</section>"""
        (OUT / "topics" / f"{t['slug']}.html").write_text(page(f"{t['name']} – Simple Science Around Us", t["blurb"], body, 1), encoding="utf-8")

    # Questions
    for q in QS:
        t = TOPICS[q["series"]]
        s = q["sentences"]
        hook, rest = s[0], s[1:]
        en = "".join(f"<p>{e(x['en'])}</p>" for x in rest)
        es = "".join(f"<p>{e(x['es'])}</p>" for x in s)
        src = "".join(f'<li><a href="{e(x["url"])}" rel="nofollow">{e(x["title"])}</a></li>' for x in q["sources"])
        rel = [r for r in by[q["series"]] if r["slug"] != q["slug"]][:4]
        tr = TRY.get(q["slug"])
        tryb = ""
        if tr:
            tryb = (f'<section class="try"><h2>Try it at home</h2><div class="tcols"><div><h3>You need</h3><ul>'
                    + "".join(f"<li>{e(x)}</li>" for x in tr["need"]) + '</ul></div><div><h3>Steps</h3><ol>'
                    + "".join(f"<li>{e(x)}</li>" for x in tr["steps"]) + f'</ol></div></div>'
                    f'<p><b>What you will see.</b> {e(tr["see"])}</p><p class="safe"><b>Safety.</b> {e(tr["safety"])}</p></section>')
        date = datetime.date.fromisoformat(q["published"][:10]).strftime("%B %-d, %Y")
        body = f"""<article class="band art" style="--c:{t['color']}">
<p class="crumb"><a href="../index.html">Home</a> / <a href="../topics/{t['slug']}.html">{e(t['name'])}</a></p>
<div class="agrid"><div class="acopy"><h1>{e(q['question'])}</h1>
<p class="short"><b>Short answer.</b> {e(q['summary'])}</p>
<p class="hook">{e(hook['en'])}</p>{en}
<details class="es"><summary>Leer en español</summary>{es}</details>
{tryb}
<section class="gearbox"><h2>Tools for this topic</h2>{gear_block(q['series'], '../')}</section>
<section class="srcs"><h2>Sources</h2><ul>{src}</ul><p class="meta">Published {date}. Illustrations in the video are models, not to scale.</p></section>
</div><aside class="aside">{vid(q, True)}</aside></div></article>
<section class="band soft"><h2>More from {e(t['name'])}</h2><div class="qgrid">{''.join(card(r, '../') for r in rel)}</div></section>"""
        (OUT / "q" / f"{q['slug']}.html").write_text(page(f"{q['question']} – Simple Science Around Us", q["summary"][:155], body, 1), encoding="utf-8")

    # Kits
    blocks = "".join(f'<section class="kitsec" style="--c:{t["color"]}"><h2><a href="topics/{t["slug"]}.html">{e(t["name"])}</a></h2>{gear_block(c)}</section>'
                     for c, t in TOPICS.items())
    body = f"""<section class="band thead"><p class="crumb"><a href="index.html">Home</a> / Science kits</p><h1>Science kits and tools by topic</h1>
<p class="lead">Simple, affordable tools that match the questions we answer. Shop links will be added once our partner programs are set up.</p></section>
<section class="band">{blocks}<p class="note">Always check the age rating on the box. Keep small parts, magnets and glass away from young children, and handle anything hot with an adult.</p></section>"""
    (OUT / "kits.html").write_text(page("Science kits by topic – Simple Science Around Us", "Science kits and tools that match each everyday science topic.", body), encoding="utf-8")

    # About
    body = f"""<section class="band thead"><p class="crumb"><a href="index.html">Home</a> / About</p><h1>About Simple Science Around Us</h1></section>
<section class="band prose"><p>Simple Science Around Us answers the everyday questions curious people ask: why a cold glass gets wet, why ice floats, why a straw looks bent. Every answer is a short video with English and Spanish subtitles, plus the explanation and sources on this site.</p>
<h2>How we make the videos</h2><p>Scripts are checked against the sources listed on each page. The narration is AI-generated and the illustrations are simplified models, not to scale.</p>
<h2>Affiliate disclosure</h2><p>Some links on this site may be affiliate links. If you buy through them, we may earn a small commission at no extra cost to you. This never changes our explanations, and we only suggest products that fit the experiments we show.</p>
<h2>Privacy</h2><p>This site does not use accounts, forms or tracking cookies. Videos open on YouTube, or play in a privacy-enhanced YouTube player when you choose to start them.</p>
<h2>Follow</h2><p>{' · '.join(f'<a href="{u}">{n}</a>' for n, u in SOCIAL)}</p></section>"""
    (OUT / "about.html").write_text(page("About – Simple Science Around Us", "About the channel, affiliate disclosure and privacy.", body), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print("built", len(QS), "questions")


if __name__ == "__main__":
    build()
