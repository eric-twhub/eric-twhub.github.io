# -*- coding: utf-8 -*-
"""札幌雪季機票圖卡（1080×1350）。

資料在 sapporo.json（Trip.com 實查）＋ ski.json（各航空雪具條款）。
每張可單獨發。

票價會過期。發之前一定要重查，對不上就重跑這支。

用法：python3 make_sapporo_cards.py
輸出：cards/sapporo/01_cover.png … 05_end.png ＋ posts/sapporo.txt
"""
import os, sys, json, html, subprocess

W, H = 1080, 1350
OUT = "cards/sapporo"


def _chrome():
    """依序找可用的 Chrome：環境變數 → macOS 路徑 → Linux 常見指令"""
    import shutil
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


BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx}
body{background:#0d1620;color:#eef4f8;
 font-family:"PingFang TC","Noto Sans TC","Noto Sans CJK TC",
 "Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:70px 68px 60px;position:relative;overflow:hidden}
.glow{position:absolute;width:840px;height:840px;border-radius:50%%;
 background:radial-gradient(circle,rgba(125,211,252,.15),transparent 68%%);top:-340px;right:-300px}
.brand{font-size:25px;letter-spacing:.3em;color:#7dd3fc;font-weight:700}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.site{font-size:27px;color:#7dd3fc;font-weight:700;margin-top:auto}
.ttl{font-size:52px;font-weight:800;letter-spacing:-.02em;line-height:1.2}
.note{margin-top:14px;font-size:28px;color:#94a6b4;line-height:1.5}
.unit{margin-top:22px;font-size:23px;color:#5a6875;line-height:1.55}
table{width:100%%;border-collapse:collapse;margin-top:28px;table-layout:fixed;
 font-variant-numeric:tabular-nums;font-feature-settings:"tnum"}
th{font-size:22px;color:#7f8e9c;font-weight:600;text-align:right;
 padding:0 0 14px;line-height:1.35}
th:first-child{text-align:left}
td{font-size:28px;font-weight:700;text-align:right;padding:13px 0;
 border-top:1px solid rgba(255,255,255,.09)}
td:first-child{text-align:left;font-size:25px;color:#c6d2dc;font-weight:600;line-height:1.3}
td:first-child i{display:block;font-style:normal;font-size:20px;color:#7f8e9c;
 font-weight:500;margin-top:3px}
td.dim{color:#94a6b4;font-weight:600;font-size:25px;text-align:left;line-height:1.35;
 padding-left:22px}
td.lo{color:#34d399}
td.hi{color:#fb7185}
td.tight{color:#fb7185}
td.fee{color:#fbbf24}
td.ok{color:#34d399}
td small{display:block;font-size:19px;color:#7f8e9c;font-weight:500;margin-top:3px}
.dense .ttl{font-size:46px}
.dense .note{font-size:25px;margin-top:10px}
.dense table{margin-top:20px}
.dense th{font-size:20px;padding-bottom:10px}
.dense td{font-size:25px;padding:10px 0}
.dense td:first-child{font-size:23px}
/* .dense td 的 padding 和 td.dim 同權重又寫在後面，會把左邊距洗掉，要再指定一次 */
.dense td.dim{font-size:21px;padding-left:22px}
.dense td small{font-size:18px}
.dense .unit{font-size:20px;margin-top:16px}
.dense .kick{margin-top:18px;font-size:26px;padding:17px 22px}
/* 單張獨立發時，結論要寫在卡上，不能靠下一張補 */
.kick{margin-top:24px;padding:22px 26px;border-radius:16px;
 background:rgba(125,211,252,.13);color:#7dd3fc;
 font-size:29px;font-weight:800;line-height:1.45}
"""% (W, H)

COVER = """
.q{font-size:70px;font-weight:800;line-height:1.22;letter-spacing:-.02em}
.a{margin-top:34px;font-size:50px;font-weight:800;color:#7dd3fc;line-height:1.28}
.cmp{margin-top:34px;display:flex;gap:18px}
.cmp div{flex:1;background:rgba(255,255,255,.05);border-radius:16px;padding:24px 26px}
.cmp b{display:block;font-size:26px;color:#94a6b4;font-weight:600}
.cmp u{display:block;text-decoration:none;font-size:48px;font-weight:800;margin-top:10px;
 letter-spacing:-.02em}
.cmp s{text-decoration:none;display:block;font-size:22px;color:#6b7885;margin-top:8px}
.sub{margin-top:28px;font-size:30px;color:#94a6b4;line-height:1.55}
.sub b{color:#eef4f8;font-weight:700}
.swipe{margin-top:32px;font-size:28px;color:#5a6875}
"""

SPLIT = """
.two{margin-top:40px;display:flex;flex-direction:column;gap:22px}
.row{background:rgba(255,255,255,.05);border-radius:18px;padding:28px 30px}
.row b{display:block;font-size:31px;font-weight:800;line-height:1.35}
.row u{display:block;text-decoration:none;font-size:46px;font-weight:800;margin-top:10px;
 letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.row s{text-decoration:none;display:block;margin-top:9px;font-size:26px;
 color:#94a6b4;line-height:1.5}
"""

END = """
.h{font-size:58px;font-weight:800;line-height:1.24;letter-spacing:-.02em}
.pts{margin-top:34px;display:flex;flex-direction:column;gap:22px}
.pt{display:flex;gap:18px;align-items:flex-start;font-size:29px;line-height:1.5}
.pt i{color:#7dd3fc;font-style:normal;font-weight:800;flex:0 0 auto}
.pt b{font-weight:700}
"""


def head_html(css, cls=""):
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{BASE}{css}</style></head><body class="{cls}">'
            f'<div class="glow"></div><div class="brand">台日機票速報</div>')


def main():
    D = json.load(open("sapporo.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/sapporo/"
    CK, RT, SM = D["checked"], D["route"], D["sample"]

    def money(n): return f"NT${n:,}"
    def md(s): return s.replace("-", "/").lstrip("0")

    daily = {k: v for k, v in D["daily"].items() if v}
    # 視窗的最低／最高由每日資料算出來，不手打，避免改了資料忘了改文案
    wins = []
    for w in D["windows"]:
        ks = [k for k in D["daily"]
              if (w["from"] <= k <= w["to"]) or
                 (w["from"] > w["to"] and (k >= w["from"] or k <= w["to"]))]
        vs = [(k, daily[k]) for k in ks if k in daily]
        lo = min(vs, key=lambda x: x[1]); hi = max(vs, key=lambda x: x[1])
        wins.append({**w, "lo": lo, "hi": hi, "n": len(vs)})

    gmin = min(daily.items(), key=lambda x: x[1])
    gmax = max(daily.items(), key=lambda x: x[1])
    cheap_win = min(wins, key=lambda w: w["lo"][1])
    direct = D["direct"]
    d0 = SM["rows"][0]                       # 最便宜的直飛
    bagged = next(r for r in SM["rows"] if r["flag"] == "ok")   # 最便宜且含行李

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".sap_tmp.html"); made = []; CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    # ── 1 封面：最便宜的直飛帶不了雪板 ───────────────────
    shot("01_cover", head_html(COVER) + f'''<div class="mid">
<div class="q">札幌雪季最便宜的<br>直飛，帶不了雪板</div>
<div class="a">{html.escape(d0["air"])} {money(d0["price"])}</div>
<div class="cmp">
 <div><b>票價（來回含稅）</b><u style="color:#34d399">{money(d0["price"])}</u>
  <s>{html.escape(d0["leg"])}</s></div>
 <div><b>雪具託運</b><u style="color:#fb7185">158</u>
  <s>總尺寸上限（公分），運動器材沒放寬</s></div>
</div>
<div class="sub">市售雪板袋 150–170 公分。<b>158 是長寬高相加</b>——
一片板單邊就吃掉整個額度。</div>
<div class="swipe">{html.escape(RT)}・{md(SM["dep"])} 出發 7 晚・Trip.com {CK}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 什麼時候最便宜 ─────────────────────────────────
    trs = ""
    for w in wins:
        best = w is cheap_win
        trs += (f'<tr><td><b>{html.escape(w["label"])}</b>'
                f'<i>{md(w["from"])}–{md(w["to"])}</i></td>'
                f'<td class="{"lo" if best else ""}">{w["lo"][1]:,}'
                f'<small>{md(w["lo"][0])}</small></td>'
                f'<td class="{"hi" if w["hi"][1] == gmax[1] else ""}">{w["hi"][1]:,}'
                f'<small>{md(w["hi"][0])}</small></td></tr>')
    shot("02_when", head_html("", "dense") + f'''<div class="mid">
<div class="ttl">12 月和 1 月，<br>什麼時候最便宜？</div>
<div class="note">{html.escape(RT)}，來回含稅，經濟艙，出發日 ＋ {D["method"]["nights"]} 晚</div>
<table><colgroup><col style="width:42%"><col style="width:29%"><col style="width:29%">
</colgroup><thead><tr><th>期間</th><th>最低</th><th>最高</th></tr></thead>
<tbody>{trs}</tbody></table>
<div class="kick">{md(gmin[0])} 的 {money(gmin[1])} 和 {md(gmax[0])} 的 {money(gmax[1])}——
同一條航線同樣 7 晚，差 {money(gmax[1]-gmin[1])}</div>
<div class="unit">每日價格取自 Trip.com 來回日曆，是該日期組合的最低價，多數含轉機<br>
價格每天變動，這是 {CK} 的快照，不是保證</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 日曆上的最低價是轉機 ───────────────────────────
    c = SM["cheapest"]
    shot("03_direct", head_html(SPLIT) + f'''<div class="mid">
<div class="ttl">日曆上那個最低價，<br>多半不是直飛</div>
<div class="note">{md(SM["dep"])} 出發、{md(SM["ret"])} 回，同一組日期</div>
<div class="two">
 <div class="row"><b>日曆上的最低價</b><u style="color:#fb7185">{money(c["price"])}</u>
  <s>{html.escape(c["air"])}・{html.escape(c["route"])}<br>
  總時長 {html.escape(c["dur"])}，{html.escape(c["note"])}</s></div>
 <div class="row"><b>真正的直飛最低</b><u style="color:#34d399">{money(d0["price"])}</u>
  <s>{html.escape(d0["air"])}・{html.escape(d0["leg"])}</s></div>
</div>
<div class="kick">差 {money(d0["price"]-c["price"])}，換掉 12 小時的大阪機場</div>
<div class="unit">帶雪具的人尤其要注意：轉機等於多一次行李進出與尺寸審查<br>
{html.escape(RT)}・Trip.com・查證於 {CK}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 4 票價 × 雪具規則 × 行李 ────────────────────────
    trs = ''.join(
        f'<tr><td><b>{html.escape(r["air"])}</b>'
        f'<i>{html.escape(r["leg"].split("（")[0])}</i></td>'
        f'<td>{r["price"]:,}</td>'
        f'<td class="dim {r["flag"]}">{html.escape(r["ski"])}'
        f'<small>{html.escape(r["bag"])}</small></td></tr>' for r in SM["rows"])
    shot("04_bags", head_html("", "dense") + f'''<div class="mid">
<div class="ttl">同一天出發，<br>便宜的票雪具過不了</div>
<div class="note">{md(SM["dep"])} 出發 {md(SM["ret"])} 回。票價由低到高，右欄是各家的雪具門檻</div>
<table><colgroup><col style="width:27%"><col style="width:22%"><col style="width:51%">
</colgroup><thead><tr><th>航空公司</th><th>來回含稅</th><th>雪具與託運</th>
</tr></thead><tbody>{trs}</tbody></table>
<div class="kick">最便宜的直飛和最便宜「雪具帶得了又含行李」的差 
{money(bagged["price"]-d0["price"])}</div>
<div class="unit">雪具條款逐項對過各航空官網，詳見本站雪具託運頁<br>
票價為 {CK} 在 Trip.com 查到，每天變動</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 5 三件事 ─────────────────────────────────────────
    shot("05_end", head_html(END) + f'''<div class="mid">
<div class="h">訂札幌雪季機票，<br>先想清楚三件事</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>最便宜的日子，雪還沒來</b><br>
  {html.escape(cheap_win["label"])}最低 {money(cheap_win["lo"][1])}，但北海道要到 12 月下旬才穩定。
  一月中（{md(D["snow"]["balance"])} 前後）是雪與價格的平衡點</div></div>
 <div class="pt"><i>2</i><div><b>日曆價不等於直飛價</b><br>
  {md(SM["dep"])} 日曆最低 {money(SM["cheapest"]["price"])} 是大阪停 12 小時；
  直飛要 {money(d0["price"])}，一月中的直飛更要 {money(direct["01-13"])}</div></div>
 <div class="pt"><i>3</i><div><b>先確認雪具上不上得了</b><br>
  {html.escape(d0["air"])}總尺寸只有 158 公分、不含託運；
  {html.escape(bagged["air"])} {money(bagged["price"])} 才是{html.escape(bagged["bag"])}又收得了雪具</div></div>
</div>
<div class="unit">票價每天變動。上面的數字是 {CK} 在 Trip.com 實際查到的，
你看到這則的時候請自己再查一次</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    L = site
    wl = "\n".join(
        f"・{w['label']}（{md(w['from'])}–{md(w['to'])}）　{money(w['lo'][1])} – {money(w['hi'][1])}"
        for w in wins)
    rl = "\n".join(f"・{r['air']}　{money(r['price'])}　{r['leg']}\n　　雪具：{r['ski']}／{r['bag']}"
                   for r in SM["rows"])
    posts = [
     ("01_cover", f"""札幌雪季最便宜的直飛，是{d0['air']} {money(d0['price'])}（{md(SM['dep'])} 出發 7 晚，來回含稅）。

但如果你要帶雪板，這張票可能用不了。

{d0['air']}的託運行李總尺寸上限是 158 公分——注意是**長寬高相加**。市售雪板袋 150–170 公分，光是單邊就吃掉整個額度，而且官網對運動器材沒有另外放寬。

同一天含 23 公斤託運、雪具也收得了的是{bagged['air']} {money(bagged['price'])}，差 {money(bagged['price']-d0['price'])}。

便宜的票和帶得了雪具的票，在這條線上幾乎是兩回事。

{RT}・Trip.com・查證於 {CK}
{L}"""),
     ("02_when", f"""台北飛札幌，12 月和 1 月什麼時候最便宜？（來回含稅，經濟艙，出發日 ＋ 7 晚）

{wl}

最低是 {md(gmin[0])} 的 {money(gmin[1])}，最高是 {md(gmax[0])} 的 {money(gmax[1])}——同一條航線同樣 7 晚，差 {money(gmax[1]-gmin[1])}。

聖誕跨年那段沒有便宜的日子，整段都在一萬五以上。想省錢又要有雪，一月中是比較實際的選擇。

每日價格取自 Trip.com 的來回日曆，是該日期組合的最低價，多數含轉機。價格每天變動，這是 {CK} 的快照。

{L}"""),
     ("03_direct", f"""查機票日曆看到「{money(SM['cheapest']['price'])}」，先別急著開心。

{md(SM['dep'])} 出發、{md(SM['ret'])} 回，日曆上最低的那張是{SM['cheapest']['air']}——{SM['cheapest']['route']}，總時長 {SM['cheapest']['dur']}，{SM['cheapest']['note']}。

真正的直飛最低是{d0['air']} {money(d0['price'])}，{d0['leg']}。

差 {money(d0['price']-SM['cheapest']['price'])}，換掉 12 小時的大阪機場。

帶雪具的人尤其要算這筆：轉機等於多一次行李進出與尺寸審查，而雪板袋本來就是最容易被卡的那一件。

{RT}・Trip.com・查證於 {CK}
{L}"""),
     ("04_bags", f"""台北→札幌，{md(SM['dep'])} 出發 {md(SM['ret'])} 回，同一組日期下各航空的票價與雪具規則：

{rl}

最便宜的直飛（{d0['air']} {money(d0['price'])}）總尺寸只有 158 公分，運動器材沒放寬；最便宜「雪具帶得了又含託運」的是{bagged['air']} {money(bagged['price'])}——差 {money(bagged['price']-d0['price'])}。

這就是雪季訂票最容易踩的坑：比價只比票面，結果選到一張雪板上不去的票。

雪具條款逐項對過各航空官網，查證於 {CK}；票價當天變動，發文時請自行再查。

{L}"""),
     ("05_end", f"""訂札幌雪季機票，先想清楚三件事：

1　最便宜的日子，雪還沒來
{cheap_win['label']}最低 {money(cheap_win['lo'][1])}，但北海道要到 12 月下旬才進入穩定雪期。一月中（{md(D['snow']['balance'])} 前後）是雪況與價格的平衡點

2　日曆價不等於直飛價
{md(SM['dep'])} 日曆最低 {money(SM['cheapest']['price'])} 是大阪停 12 小時；直飛要 {money(d0['price'])}，一月中的直飛更要 {money(direct['01-13'])}

3　先確認雪具上不上得了
{d0['air']}總尺寸只有 158 公分、不含託運；{bagged['air']} {money(bagged['price'])} 才是{bagged['bag']}又收得了雪具

票價每天變動。上面的數字是 {CK} 在 Trip.com 實際查到的，你看到這則的時候請自己再查一次。

{L}"""),
    ]
    os.makedirs("posts", exist_ok=True)
    pf = "posts/sapporo.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write(f"札幌雪季機票圖卡文案（{CK} 產生）\n每張圖各自獨立，可分開發\n"
                f"※ 票價會過期，發之前一定要重查\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n" + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    print(f"   全期最低 {money(gmin[1])}（{md(gmin[0])}）·"
          f" 最高 {money(gmax[1])}（{md(gmax[0])}）")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
