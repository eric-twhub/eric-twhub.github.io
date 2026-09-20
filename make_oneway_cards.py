# -*- coding: utf-8 -*-
"""單程 vs 來回圖卡（1080×1350）。

資料在 oneway.json——台北→福岡，同一組查詢參數，一天一天實查。
每張可單獨發。

用法：python3 make_oneway_cards.py
輸出：cards/oneway/01_cover.png … 05_end.png ＋ posts/oneway.txt
"""
import os, sys, json, html, subprocess, statistics

W, H = 1080, 1350
OUT = "cards/oneway"


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
body{background:#16120f;color:#f6f2ee;
 font-family:"PingFang TC","Noto Sans TC","Noto Sans CJK TC",
 "Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:70px 68px 60px;position:relative;overflow:hidden}
.glow{position:absolute;width:820px;height:820px;border-radius:50%%;
 background:radial-gradient(circle,rgba(244,114,182,.15),transparent 68%%);top:-330px;right:-290px}
.brand{font-size:25px;letter-spacing:.3em;color:#f472b6;font-weight:700}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.site{font-size:27px;color:#f472b6;font-weight:700;margin-top:auto}
.ttl{font-size:54px;font-weight:800;letter-spacing:-.02em;line-height:1.2}
.note{margin-top:14px;font-size:28px;color:#a49a92;line-height:1.5}
.unit{margin-top:22px;font-size:23px;color:#615850;line-height:1.55}
table{width:100%%;border-collapse:collapse;margin-top:30px;table-layout:fixed;
 font-variant-numeric:tabular-nums;font-feature-settings:"tnum"}
th{font-size:22px;color:#867c74;font-weight:600;text-align:right;
 padding:0 0 14px;line-height:1.35}
th:first-child{text-align:left}
td{font-size:29px;font-weight:700;text-align:right;padding:13px 0;
 border-top:1px solid rgba(255,255,255,.09)}
td:first-child{text-align:left;font-size:25px;color:#cbc2ba;font-weight:600;line-height:1.3}
td.dim{color:#a49a92;font-weight:600;font-size:26px}
td.hi{color:#f472b6}
tr.best td{background:rgba(244,114,182,.18)}
/* 十五列：行高與字級再縮一階才進得了 1350px */
.dense .ttl{font-size:46px}
.dense .note{font-size:25px;margin-top:10px}
.dense table{margin-top:18px}
.dense th{font-size:20px;padding-bottom:10px}
.dense td{font-size:25px;padding:3px 0}
.dense td:first-child{font-size:22px}
.dense td.dim{font-size:23px}
.dense .unit{font-size:20px;margin-top:14px}
.dense .kick{margin-top:16px;font-size:26px;padding:16px 22px}
/* 單張獨立發時，結論要寫在卡上，不能靠下一張補 */
.kick{margin-top:24px;padding:22px 26px;border-radius:16px;
 background:rgba(244,114,182,.14);color:#f472b6;
 font-size:29px;font-weight:800;line-height:1.45}
"""% (W, H)

COVER = """
.q{font-size:74px;font-weight:800;line-height:1.2;letter-spacing:-.02em}
.a{margin-top:36px;font-size:54px;font-weight:800;color:#f472b6;line-height:1.28}
.cmp{margin-top:34px;display:flex;gap:18px}
.cmp div{flex:1;background:rgba(255,255,255,.05);border-radius:16px;padding:24px 26px}
.cmp b{display:block;font-size:26px;color:#a49a92;font-weight:600}
.cmp u{display:block;text-decoration:none;font-size:50px;font-weight:800;margin-top:10px;
 letter-spacing:-.02em}
.cmp s{text-decoration:none;display:block;font-size:22px;color:#726860;margin-top:8px}
.sub{margin-top:28px;font-size:31px;color:#a49a92;line-height:1.55}
.sub b{color:#f6f2ee;font-weight:700}
.swipe{margin-top:34px;font-size:29px;color:#615850}
"""

STAT = """
.big{margin-top:44px;display:flex;gap:18px}
.big div{flex:1;background:rgba(255,255,255,.05);border-radius:18px;padding:30px 24px;
 text-align:center}
.big b{display:block;font-size:25px;color:#a49a92;font-weight:600}
.big u{display:block;text-decoration:none;font-size:66px;font-weight:800;margin-top:12px;
 letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.mid2{margin-top:36px;font-size:31px;color:#a49a92;line-height:1.6}
.mid2 b{color:#f6f2ee;font-weight:700}
"""

TAX = """
.rows{margin-top:34px}
.r{background:rgba(255,255,255,.05);border-radius:16px;padding:24px 28px;
 display:flex;align-items:center;gap:22px;margin-top:18px}
.r .l{flex:1}
.r b{display:block;font-size:31px;font-weight:800;line-height:1.3}
.r s{text-decoration:none;display:block;margin-top:7px;font-size:23px;
 color:#a49a92;line-height:1.45}
.r u{text-decoration:none;font-size:44px;font-weight:800;letter-spacing:-.02em;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.r i{font-style:normal;display:block;font-size:20px;color:#726860;margin-top:5px;
 text-align:right;white-space:nowrap}
.r i del{color:#726860}
"""

LIST = """
.pts{margin-top:38px;display:flex;flex-direction:column;gap:24px}
.pt{background:rgba(255,255,255,.05);border-radius:18px;padding:26px 30px}
.pt b{display:block;font-size:33px;font-weight:800;line-height:1.35}
.pt s{text-decoration:none;display:block;margin-top:11px;font-size:27px;
 color:#a49a92;line-height:1.5}
.pt i{font-style:normal;color:#f472b6;font-weight:800;margin-right:10px}
"""

END = """
.h{font-size:60px;font-weight:800;line-height:1.24;letter-spacing:-.02em}
.pts{margin-top:34px;display:flex;flex-direction:column;gap:22px}
.pt{display:flex;gap:18px;align-items:flex-start;font-size:29px;line-height:1.5}
.pt i{color:#f472b6;font-style:normal;font-weight:800;flex:0 0 auto}
.pt b{font-weight:700}
"""


def head_html(css, cls=""):
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{BASE}{css}</style></head><body class="{cls}">'
            f'<div class="glow"></div><div class="brand">台日機票速報</div>')


def main():
    D = json.load(open("oneway.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/fukuoka/"
    CK, RT, TG = D["checked"], D["route"], D["trigger"]
    CC = D["method"]["cabin_compare"]

    def money(n): return f"NT${n:,}"
    def md(s): return s.replace("-", "/").lstrip("0")

    rows = []
    for r in D["rows"]:
        cands = [x for x in (r["rt5"], r["rt7"]) if x]
        lo = min(cands)
        rows.append({**r, "rt": lo, "x": lo / r["ow"]})

    xs = [r["x"] for r in rows]
    lo_x, hi_x, med = min(xs), max(xs), statistics.median(xs)
    under2 = sum(1 for x in xs if x < 2)
    best = min(rows, key=lambda r: r["rt"])
    cheap_ow = min(rows, key=lambda r: r["ow"])

    # 貼文的數字心算兩倍 vs 實際查到的最低來回
    claim = int("".join(c for c in TG["claim"] if c.isdigit())[-4:])
    guess = claim * 2
    gap = best["rt"] - guess

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".ow_tmp.html"); made = []; CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    # ── 1 封面：那是單程 ─────────────────────────────────
    shot("01_cover", head_html(COVER) + f'''<div class="mid">
<div class="q">「直飛含稅<br>{claim:,}」——那是單程</div>
<div class="a">來回不是乘以二</div>
<div class="cmp">
 <div><b>你心裡算的來回</b><u>{money(guess)}</u><s>{claim:,} × 2</s></div>
 <div><b>實際查到最低來回</b><u style="color:#f472b6">{money(best["rt"])}</u>
  <s>{md(best["dep"])} 出發・同航線同平台</s></div>
</div>
<div class="sub">差 {money(gap)}，<b>低估了 {gap/guess*100:.0f}%</b>。
而這還是這半個月裡最便宜的一天。</div>
<div class="swipe">{html.escape(RT)}・Trip.com・查證於 {CK}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 一天一天比 ─────────────────────────────────────
    trs = ""
    for r in rows:
        trs += (f'<tr class="{"best" if r is best else ""}">'
                f'<td><b>{md(r["dep"])}</b></td>'
                f'<td class="dim">{r["ow"]:,}</td>'
                f'<td>{r["rt"]:,}</td>'
                f'<td class="hi">{r["x"]:.2f} 倍</td></tr>')
    shot("02_table", head_html("", "dense") + f'''<div class="mid">
<div class="ttl">同一天出發，<br>單程與來回一天一天比</div>
<div class="note">{html.escape(RT)}，{html.escape(D["method"]["cabin"])}，
來回取 5 晚與 7 晚較低者</div>
<table><colgroup><col style="width:22%"><col style="width:26%"><col style="width:26%">
<col style="width:26%"></colgroup>
<thead><tr><th>出發日</th><th>單程</th><th>來回</th><th>來回 ÷ 單程</th>
</tr></thead><tbody>{trs}</tbody></table>
<div class="kick">十五天裡只有 {under2} 天低於 2 倍，中位數是 {med:.2f} 倍</div>
<div class="unit">單位為新台幣含稅。價格每天變動，這是 {CK} 的快照，不是保證<br>
粉色那列是這半個月來回最便宜的一天</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 倍數到底是多少 ─────────────────────────────────
    shot("03_ratio", head_html(STAT) + f'''<div class="mid">
<div class="ttl">「單程 ×2」<br>猜得準嗎？</div>
<div class="note">把上一張的十五天全部算成倍數，分布是這樣</div>
<div class="big">
 <div><b>最低</b><u>{lo_x:.2f}</u></div>
 <div><b>中位數</b><u style="color:#f472b6">{med:.2f}</u></div>
 <div><b>最高</b><u>{hi_x:.2f}</u></div>
</div>
<div class="mid2">十五天裡<b>只有 {under2} 天</b>的來回低於單程的兩倍。
有一半的日子在 <b>{med:.2f} 倍以上</b>，最貴的那天接近三倍。<br><br>
所以看到單程價格心算乘以二，<b>多數時候會低估兩成到四成</b>。</div>
<div class="unit">{html.escape(RT)}・{html.escape(D["gate"])}・查證於 {CK}<br>
倍數＝當日最低來回 ÷ 當日最低單程，兩者用同一組查詢參數</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 4 怎麼看出是單程 ─────────────────────────────────
    pts = ''.join(
        f'<div class="pt"><b><i>{i}</i>{html.escape(t["t"])}</b>'
        f'<s>{html.escape(t["b"])}</s></div>'
        for i, t in enumerate(D["tells"], 1))
    shot("04_tell", head_html(LIST) + f'''<div class="mid">
<div class="ttl">怎麼一眼看出<br>報的是單程？</div>
<div class="note">{html.escape(TG["note"])}</div>
{pts}</div>
<div class="site">{site}</div></body></html>''')

    # ── 5 先做三件事 ─────────────────────────────────────
    BG = D["baggage_example"]
    shot("05_end", head_html(END) + f'''<div class="mid">
<div class="h">看到機票特價貼文，<br>先做三件事</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>先確認是單程還是來回</b><br>
  網址裡只有一個日期、或參數是 triptype=0，那就是單程</div></div>
 <div class="pt"><i>2</i><div><b>自己查同一天的來回，不要乘以二</b><br>
  這條線十五天裡只有 {under2} 天低於 2 倍，中位數 {med:.2f} 倍</div></div>
 <div class="pt"><i>3</i><div><b>看含不含託運行李</b><br>
  {md(BG["date"])} 最便宜的單程是{html.escape(BG["cheapest"]["air"])} {money(BG["cheapest"]["price"])}，
  {html.escape(BG["cheapest"]["bag"])}；{html.escape(BG["with_bag"]["air"])} {money(BG["with_bag"]["price"])}
  但{html.escape(BG["with_bag"]["bag"])}</div></div>
</div>
<div class="unit">價格每天變動。上面的數字是 {CK} 在 {html.escape(D["gate"])} 實際查到的，
你看到這則的時候請自己再查一次</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 6 「未稅價」是怎麼把數字講小的 ─────────────────
    AA = D.get("airasia")
    if AA:
        # 變數不要叫 rows——外層的 rows 是每日票價，後面的文案還要用
        _ar = ''.join(
            f'<div class="r"><div class="l"><b>{html.escape(r["route"])}</b>'
            f'<s>{html.escape(r["air"])}・{html.escape(r["leg"])}<br>'
            f'{html.escape(r["note"])}</s></div>'
            f'<div><u style="color:'
            + ("#34d399" if r["flag"] == "win" else "#f472b6" if r["flag"] == "lo" else "#f6f2ee")
            + f'">{money(r["price"])}</u>'
            f'<i>{html.escape(r["src"])}含稅'
            + (f'・<del>{money(r["was"])}</del> {html.escape(r["off"])}' if r.get("was") else '')
            + '</i></div></div>'
            for r in AA["rows"])
        shot("06_tax", head_html(TAX) + f'''<div class="mid">
<div class="ttl">「{AA["claim"]:,} 元起」<br>——那是<span style="color:#f472b6">未稅</span>價</div>
<div class="note">亞航秋季促銷。同一天（{md(AA["sample_date"])}）在能真的訂票的地方查到的是：</div>
{_ar}
<div class="kick">{html.escape(AA["kicker"])}</div>
<div class="unit">他附的連結是 Trip.com 的亞航航空公司頁，那頁自己寫「價格包括所有費用」——
{AA["claim"]:,} 在那個連結上永遠看不到<br>
查證於 {AA["checked"]}・價格每天變動</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    L = site
    tbl = "\n".join(f"・{md(r['dep'])}　單程 {money(r['ow'])}　來回 {money(r['rt'])}　{r['x']:.2f} 倍"
                    for r in rows)
    posts = [
     ("01_cover", f"""看到「台北-福岡 直飛含稅 {claim:,}」，先別急著心算來回 {money(guess)}。

那是單程。

貼文附的 Trip.com 連結裡參數是 triptype=0，日曆上只有一個出發日期，沒有回程——連結本身就寫著單程。

同一條航線、同一個平台、同樣經濟艙，我把接下來半個月一天一天查過：最便宜的來回是 {md(best['dep'])} 出發的 {money(best['rt'])}。

比心算的 {money(guess)} 多了 {money(gap)}，低估 {gap/guess*100:.0f}%。而且這已經是最便宜的一天。

這不是有人在騙你，單程票價本來就是這樣報。問題在於我們會拿它跟記憶中的來回價比。

{RT}・{D['gate']}・查證於 {CK}
{L}"""),
     ("02_table", f"""台北飛福岡，同一天出發，單程與來回一天一天比（經濟艙，來回取 5 晚與 7 晚較低者）：

{tbl}

十五天裡只有 {under2} 天的來回低於單程的兩倍，中位數是 {med:.2f} 倍。

{md(best['dep'])} 是這半個月來回最便宜的一天，{money(best['rt'])}。剛好也是單程最便宜的那天（{money(cheap_ow['ow'])}）——但這是巧合，不是規律，其他日子兩者對不上。

價格每天變動，這是 {CK} 的快照，不是保證。自己查一次最準。

{L}"""),
     ("03_ratio", f"""「單程 ×2 就是來回」——這個心算猜得準嗎？

把台北→福岡接下來半個月的十五天全部算成倍數：

・最低 {lo_x:.2f} 倍
・中位數 {med:.2f} 倍
・最高 {hi_x:.2f} 倍

十五天裡只有 {under2} 天低於兩倍。有一半的日子在 {med:.2f} 倍以上，最貴的那天接近三倍。

所以看到單程價格乘以二，多數時候會低估兩成到四成。

原因不難理解：便宜的單程是單向的庫存出清，湊成來回要另外買回程，而回程沒有在出清。

倍數＝當日最低來回 ÷ 當日最低單程，兩者用同一組查詢參數（{D['method']['cabin']}，1 位成人）。

{D['gate']}・查證於 {CK}
{L}"""),
     ("04_tell", f"""怎麼一眼看出機票特價貼文報的是單程？三個檢查點：

""" + "\n\n".join(f"{i}　{t['t']}\n{t['b']}" for i, t in enumerate(D["tells"], 1)) + f"""

{TG['note']}

順帶一提，查價的時候參數要一致。同樣是 {md(CC['date'])} {RT}，用「經濟艙」查是 {money(CC['y'])}，用「經濟艙／豪華經濟艙」查是 {money(CC['ys'])}。比較倍數時兩邊參數不同，算出來的數字就沒有意義。

{L}"""),
     ("05_end", f"""看到機票特價貼文，先做三件事：

1　先確認是單程還是來回
網址裡只有一個日期、或參數是 triptype=0，那就是單程

2　自己查同一天的來回，不要乘以二
台北→福岡這條線，十五天裡只有 {under2} 天低於 2 倍，中位數 {med:.2f} 倍

3　看含不含託運行李
{md(BG['date'])} 最便宜的單程是{BG['cheapest']['air']} {money(BG['cheapest']['price'])}，{BG['cheapest']['bag']}；
{BG['with_bag']['air']} {money(BG['with_bag']['price'])} 但{BG['with_bag']['bag']}

價格每天變動。上面的數字是 {CK} 實際查到的，你看到這則的時候請自己再查一次。

{L}"""),
    ]
    if AA:
        _rl = "\n".join(
            f"・{r['route']}　{money(r['price'])}（{r['src']}含稅"
            + (f"，原價 {money(r['was'])} {r['off']}" if r.get('was') else "")
            + f"）\n　　{r['air']}・{r['leg']}\n　　{r['note']}"
            for r in AA["rows"])
        posts.append(("06_tax", f"""亞航秋季促銷的貼文寫：「台北出發 大阪｜福岡｜札幌｜沖繩……最低 {AA['claim']:,} 元起（單程未稅價）」。

未稅。那不是你要付的錢。

同一天（{md(AA['sample_date'])}），在能真的訂票的地方查到的是：

{_rl}

{AA['kicker']}

還有一件事：{AA['missing']}

而那則貼文附的 Trip.com 連結，其實不是任何一條航線的搜尋結果，是 Trip.com 的亞航航空公司頁。那一頁自己寫著「價格包括所有費用（含稅金、燃油費、行李費），無任何隱藏費用」——所以 {AA['claim']:,} 這個數字，在他給你的那個連結上永遠看不到。

促銷是真的，折扣也是真的。只是「起」跟「未稅」這兩個字，各自把數字講小了一次。

查證於 {AA['checked']}。價格每天變動，請自己再查一次。
{L}"""))
    os.makedirs("posts", exist_ok=True)
    pf = "posts/oneway.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write(f"單程 vs 來回圖卡文案（{CK} 產生）\n每張圖各自獨立，可分開發\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n" + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    print(f"   倍數 {lo_x:.2f}–{hi_x:.2f}，中位數 {med:.2f}，低於 2 倍 {under2}/{len(rows)} 天")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
