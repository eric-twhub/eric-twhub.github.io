# -*- coding: utf-8 -*-
"""由 posts/deals.json 產生 IG 圖卡（1080×1350，直式）

用法：
    python3 gen.py && python3 make_cards.py
輸出：
    cards/YYYY-MM-DD/<slug>.png
"""
import json, os, html, subprocess, shutil, datetime, sys

W, H = 1080, 1350
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "cards"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx}
body{background:#141210;color:#f5f2ee;
 font-family:"PingFang TC","Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:76px 72px 64px;position:relative;overflow:hidden}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.glow{position:absolute;width:760px;height:760px;border-radius:50%%;
 background:radial-gradient(circle,rgba(251,146,60,.20),transparent 68%%);
 top:-300px;right:-260px}
.brand{font-size:27px;letter-spacing:.32em;color:#fb923c;font-weight:700}
.brand span{color:#6b6560;letter-spacing:.06em;font-weight:400;margin-left:14px;font-size:23px}
.route{font-size:88px;font-weight:800;line-height:1.14;letter-spacing:-.02em}
.route i{font-style:normal;color:#fb923c;margin:0 20px}
.via{margin-top:20px;font-size:40px;color:#a8a29c;font-weight:600}
.price{margin-top:52px;font-size:172px;font-weight:800;line-height:.94;
 letter-spacing:-.045em;color:#fb923c}
.price small{font-size:58px;margin-right:10px;font-weight:700}
.unit{margin-top:22px;font-size:34px;color:#a8a29c;letter-spacing:.05em}
.badge{display:inline-block;margin-top:44px;background:#fb923c;color:#141210;
 font-size:31px;font-weight:800;padding:15px 32px;border-radius:14px}
.meta{border-top:2px solid #2b2724;padding-top:40px}
.row{display:flex;align-items:baseline;gap:20px;font-size:38px;margin-bottom:20px}
.row b{font-weight:700}
.row s{text-decoration:none;color:#6b6560}
.dates{font-size:44px;font-weight:700;letter-spacing:.01em}
.foot{margin-top:36px;display:flex;justify-content:space-between;align-items:flex-end;gap:20px}
.site{font-size:29px;color:#fb923c;font-weight:700}
.note{font-size:22px;color:#5f5a55;text-align:right;line-height:1.55}
""" % (W, H)


def _md(s):
    """2026-09-13 → 9/13"""
    try:
        y, m, dd = s.split("-")
        return f"{int(m)}/{int(dd)}"
    except Exception:
        return s


def card_html(d, site):
    trip = "總計" if d["cls"] == "transfer" else "來回含稅"
    yr = d["dep"][:4]
    dates = _md(d["dep"]) + ("　–　" + _md(d["ret"]) if d.get("ret") else "")
    reason = d["reasons"][0] if d.get("reasons") else ""
    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="glow"></div>
<div class="brand">台日機票速報</div>
<div class="mid">
<div class="route">{html.escape(d['o'])}<i>→</i>{html.escape(d['c'])}</div>
{f'<div class="via">經 {html.escape(d["via"])} 轉乘</div>' if d.get('via') else ''}
<div class="price"><small>NT$</small>{d['price']:,}</div>
<div class="unit">{trip}．單人{'．含機票與國內交通' if d['cls']=='transfer' else ''}</div>
<div><span class="badge">{html.escape(reason)}</span></div>
</div>
<div class="meta">
  <div class="row"><s>{'方案' if d['cls']=='transfer' else '航空'}</s><b>{html.escape(d['air'])}</b><s>·</s><b>{html.escape(d['stops'])}</b></div>
  <div class="row"><s>日期</s><span class="dates">{dates}</span><s>{yr} 年</s></div>
  <div class="foot">
    <div class="site">{site}</div>
    <div class="note">票價含稅，隨時可能變動<br>實際價格請以訂票平台為準</div>
  </div>
</div>
</body></html>"""


def main():
    # 查證後校正：python3 make_cards.py --slug 2026-09-10-taipei-tokyo --price 6699
    # 快取價常低於訂票平台實際售價，發文一律以查證看到的價格為準
    fix_slug = fix_price = None
    if "--slug" in sys.argv:
        fix_slug = sys.argv[sys.argv.index("--slug") + 1]
    if "--price" in sys.argv:
        fix_price = int(sys.argv[sys.argv.index("--price") + 1])

    if not os.path.exists("posts/deals.json"):
        sys.exit("找不到 posts/deals.json，請先執行 python3 gen.py")
    if not os.path.exists(CHROME):
        sys.exit(f"找不到 Chrome：{CHROME}")

    deals = json.load(open("posts/deals.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].replace("https://", "")
    day = datetime.date.today().isoformat()
    outdir = os.path.join(OUT, day)
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.abspath(".card_tmp.html")

    if fix_slug:
        deals = [d for d in deals if d["slug"] == fix_slug]
        if not deals:
            sys.exit(f"找不到 slug：{fix_slug}")
        if fix_price:
            d = deals[0]
            old = d["price"]
            d["price"] = fix_price
            if d.get("med"):
                pct = round((1 - fix_price / d["med"]) * 100)
                d["reasons"] = [f"低於本站近期紀錄中位價 {pct}%"] if pct >= 15 else \
                               [f"{'廉航' if d['cls']=='lcc' else '一般航空'}直飛來回含稅"]
            print(f"   校正價格：NT${old:,} → NT${fix_price:,}")

    made = []
    for d in deals:
        open(tmp, "w", encoding="utf-8").write(card_html(d, site))
        png = os.path.abspath(os.path.join(outdir, d["slug"] + ".png"))
        r = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             f"--screenshot={png}", f"--window-size={W},{H}",
             "--force-device-scale-factor=1", "file://" + tmp],
            capture_output=True, timeout=90)
        if os.path.exists(png):
            made.append((d["slug"], os.path.getsize(png)))
        else:
            print("  ⚠️ 失敗:", d["slug"], r.stderr.decode()[:120])
    os.path.exists(tmp) and os.remove(tmp)

    print(f"✅ 產生 {len(made)} 張圖卡 → {outdir}/  ({W}×{H})")
    for s, sz in made[:5]:
        print(f"   {s}.png  {sz//1024} KB")
    if len(made) > 5:
        print(f"   …另外 {len(made)-5} 張")


if __name__ == "__main__":
    main()
