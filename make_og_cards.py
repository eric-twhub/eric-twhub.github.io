# -*- coding: utf-8 -*-
"""社群分享縮圖（og:image，1200×630）。

背景刻意用純色色塊不用漸層：同一張圖漸層版 118 KB、純色版 45 KB，
四十幾張的差距是 5.2 MB 對 2.2 MB，而 repo 每天都在 commit。

分享到 Threads、LINE、Facebook 時沒有預覽圖的話只會是一張純文字卡片。
這支依 gen.py 產出的 og-manifest.json，幫每個內容頁做一張。

票價頁不產：它們的標題每天帶著當日最低價，每天重產只會讓 repo
一直長出二進位檔，那些統一用 og/default.png。

只重產標題有變的那幾張，所以平常跑起來幾乎不花時間。

用法：python3 make_og_cards.py [--force]
輸出：og/<slug>.png、og/default.png
"""
import json, os, sys, subprocess, hashlib, shutil
import html as htm

W, H = 1200, 630
OUT = "og"
MANIFEST = "og-manifest.json"
STATE = os.path.join(OUT, ".hash.json")


def _chrome():
    """依序找可用的 Chrome：環境變數 → macOS 路徑 → Linux 常見指令"""
    c = os.environ.get("CHROME")
    if c and os.path.exists(c):
        return c
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac):
        return mac
    for n in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
        p = shutil.which(n)
        if p:
            return p
    sys.exit("找不到 Chrome，請設定 CHROME 環境變數")


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx}
body{background:#141210;color:#f5f2ee;
 font-family:"Noto Sans CJK TC","Noto Sans TC","PingFang TC","Heiti TC",sans-serif;
 display:flex;flex-direction:column;justify-content:space-between;
 padding:64px 72px;position:relative;overflow:hidden}
.glow{position:absolute;width:470px;height:470px;border-radius:50%%;
 background:#1f1a15;top:-210px;right:-150px}
.glow2{position:absolute;width:200px;height:200px;border-radius:50%%;
 background:#2b2118;top:-70px;right:-40px}
.brand{font-size:24px;letter-spacing:.34em;color:#fb923c;font-weight:700;position:relative}
.h{font-size:%dpx;font-weight:800;line-height:1.22;letter-spacing:-.02em;
 position:relative;max-width:1020px}
.foot{display:flex;align-items:center;gap:18px;position:relative}
.bar{width:54px;height:5px;background:#fb923c;border-radius:3px}
.site{font-size:25px;color:#8a837c;letter-spacing:.02em}
"""


def page(h1, site):
    # 標題越長字級越小，避免長標題溢出版面
    n = len(h1)
    size = 76 if n <= 18 else 66 if n <= 26 else 56 if n <= 34 else 48
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS % (W, H, size)}</style></head><body>'
            f'<div class="glow"></div><div class="glow2"></div>'
            f'<div class="brand">台日機票速報</div>'
            f'<div class="h">{htm.escape(h1)}</div>'
            f'<div class="foot"><span class="bar"></span>'
            f'<span class="site">{htm.escape(site)}</span></div>'
            f'</body></html>')


def shot(chrome, html_str, png):
    tmp = os.path.abspath(".og_tmp.html")
    open(tmp, "w", encoding="utf-8").write(html_str)
    cmd = [chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
           f"--screenshot={os.path.abspath(png)}", f"--window-size={W},{H}",
           "--force-device-scale-factor=1"]
    if sys.platform.startswith("linux"):
        cmd += ["--no-sandbox", "--disable-dev-shm-usage"]
    subprocess.run(cmd + ["file://" + tmp], capture_output=True, timeout=90)
    os.path.exists(tmp) and os.remove(tmp)
    return os.path.exists(png)


def main():
    force = "--force" in sys.argv
    if not os.path.exists(MANIFEST):
        sys.exit(f"找不到 {MANIFEST}，請先跑 gen.py")
    M = json.load(open(MANIFEST, encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"]
    site = site.replace("https://", "").replace("http://", "").rstrip("/")

    os.makedirs(OUT, exist_ok=True)
    old = {}
    if os.path.exists(STATE) and not force:
        try:
            old = json.load(open(STATE, encoding="utf-8"))
        except Exception:
            old = {}

    chrome = _chrome()
    new, made, kept, failed = {}, [], 0, []

    jobs = [(i["slug"], i["h1"] or i["title"]) for i in M["items"]]
    jobs.append(("default", "台灣飛日本，今天的票價與行前要知道的事"))

    for slug, h1 in jobs:
        key = hashlib.sha1(h1.encode("utf-8")).hexdigest()[:16]
        png = os.path.join(OUT, f"{slug}.png")
        if old.get(slug) == key and os.path.exists(png):
            new[slug] = key; kept += 1; continue
        if shot(chrome, page(h1, site), png):
            new[slug] = key; made.append(slug)
        else:
            failed.append(slug)

    json.dump(new, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"✅ og 圖卡：新產 {len(made)} 張、沿用 {kept} 張 → {OUT}/")
    for s in made[:12]:
        print(f"   {s}.png  {os.path.getsize(os.path.join(OUT, s + '.png')) // 1024} KB")
    if len(made) > 12:
        print(f"   …另外 {len(made) - 12} 張")
    if failed:
        print(f"   ⚠ 產生失敗：{failed}")
        sys.exit(1)


if __name__ == "__main__":
    main()
