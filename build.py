#!/usr/bin/env python3
"""Builds the Maintlytics website: each page in pages/ gets the shared header and footer, into public/.

    python3 build.py

Edit SITE below for the company name, email and domain once you have them. Upload the public/ folder to any web host.
"""
import pathlib, re, shutil, datetime

SITE = {
    "company": "Maintlytics",                 # shown in the footer and legal pages
    "email": "chad@czahner.com",              # contact address
    "domain": "https://maintlytics.com",      # used for share links
}

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"          # the finished site (GitHub Pages serves this folder)
NAV = [("index.html", "Home"), ("features.html", "Features"), ("pricing.html", "Pricing"), ("faq.html", "FAQ"), ("download.html", "Download")]
# links leave out ".html" (maintlytics.com/features): GitHub Pages serves features.html for /features
LINK = lambda page: "/" if page == "index.html" else "/" + page[:-5]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{domain}/img/overview.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/site.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><img src="/img/icon.png" alt="">Maintlytics</a>
  <button class="menu" aria-label="Menu" onclick="document.querySelector('.nav').classList.toggle('open')">Menu</button>
  <nav class="nav">{nav}<a class="btn gold" href="/contact">Book a demo</a></nav>
</div></header>
<main>
"""

FOOT = """</main>
<footer><div class="wrap">
  <div class="cols">
    <div><a class="brand" href="/"><img src="/img/icon.png" alt="">Maintlytics</a>
      <p class="muted" style="margin-top:12px;font-size:15px">Maintenance KPIs, planning and reliability for plants that run on a CMMS.</p></div>
    <div><h4>Product</h4><a href="/features">Features</a><a href="/pricing">Pricing</a><a href="/faq">FAQ</a><a href="/download">Download</a></div>
    <div><h4>Company</h4><a href="/contact">Book a demo</a><a href="mailto:{email}">{email}</a></div>
    <div><h4>Legal</h4><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div>
  </div>
  <div class="fine"><span>© {year} {company}.</span>
    <button class="theme" onclick="toggleTheme()">Light / dark</button></div>
</div></footer>
<div class="lb" onclick="this.classList.remove('on')"><img alt=""></div>
<script>
// screenshots open full size; the theme choice is remembered on this device
document.querySelectorAll('.shot img, .devices img').forEach(i => i.addEventListener('click', () => {{ const l = document.querySelector('.lb'); l.querySelector('img').src = i.src; l.classList.add('on') }}));
function toggleTheme() {{ const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; r.dataset.theme = dark ? 'light' : 'dark'; try {{ localStorage.setItem('theme', r.dataset.theme) }} catch (e) {{}} }}
try {{ const t = localStorage.getItem('theme'); if (t) document.documentElement.dataset.theme = t }} catch (e) {{}}
</script>
</body>
</html>
"""


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "site.css", OUT / "site.css")
    shutil.copytree(ROOT / "img", OUT / "img")
    (OUT / "CNAME").write_text("maintlytics.com\n")          # GitHub Pages: the site's domain
    (OUT / ".nojekyll").write_text("")                      # serve the files as they are
    for extra in (ROOT / "static").glob("*"):               # pages kept as they are (the App Store support page)
        shutil.copy(extra, OUT / extra.name)
    for page in sorted((ROOT / "pages").glob("*.html")):
        text = page.read_text()
        m = re.match(r"<!--\s*title:\s*(.*?)\n\s*desc:\s*(.*?)\s*-->\n", text, re.S)
        title, desc = (m.group(1).strip(), m.group(2).strip()) if m else ("Maintlytics", "")
        body = text[m.end():] if m else text
        nav = "".join(f'<a href="{LINK(href)}"{" class=\"on\"" if href == page.name else ""}>{label}</a>' for href, label in NAV)
        html = HEAD.format(title=title, desc=desc, nav=nav, **SITE) + body + FOOT.format(year=datetime.date.today().year, **SITE)
        for k, v in SITE.items():
            html = html.replace("{{" + k + "}}", v)
        (OUT / page.name).write_text(html)
        print("built", page.name)


if __name__ == "__main__":
    build()
