# Simple Science Around Us — website (prototype)

Static site for the Simple Science Around Us channel: one page per published Short, six topic pages, a science-kit list and an about/disclosure page. No server, no database, no tracking.

## Structure
- `data/questions.json` — public data of published videos (question, EN/ES text, sources, YouTube ID). Internal pack codes are never written here.
- `data/extras.json` — topic names and colours, "Try it at home" experiments, kit suggestions per topic.
- `assets/` — CSS and a small script (plays the Short in a youtube-nocookie player on click).
- `build.py` — builds the site into `docs/` (`python3 build.py`).
- `docs/` — the built site, served by GitHub Pages.

## Publish on GitHub Pages
1. Create a public repository, e.g. `simplesciencearoundus.github.io` (gives the address https://simplesciencearoundus.github.io) or any name (address https://<user>.github.io/<repo>/).
2. Upload everything in this folder (or `git push`).
3. Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/docs` → Save.
4. Later, a custom domain can be added in the same Pages settings.

## Update
Re-export `data/questions.json` from the factory (read-only), run `python3 build.py`, commit `docs/`.
