# Maintlytics website

Sales site for Maintlytics. Plain HTML and CSS, no build tools beyond Python 3 (already on every Mac).

- `pages/` — each page's content (edit these)
- `site.css` — the look (navy and gold, light and dark)
- `img/` — screenshots of the app's made-up demo plant, and the icon
- `build.py` — adds the shared header and footer and writes the finished site to `docs/`
- `docs/` — the finished site: upload this folder to any web host

## Preview

```bash
cd "/Users/chadz/PMWare Data/Website" && python3 build.py && python3 -m http.server 8090 --bind 127.0.0.1 --directory docs
```

Then open http://127.0.0.1:8090 (this Mac only).

## Before going live

1. Set the company name, email and domain at the top of `build.py`, then run it again.
2. Fill in prices in `pages/pricing.html` (they show "$—" and "Prices to be set").
3. Connect the demo form in `pages/contact.html` to a form service or email.
4. Have Privacy and Terms reviewed.
5. Upload `docs/` to the host (Netlify, Cloudflare Pages, GitHub Pages or any web host) and point the domain at it.
