# -*- coding: utf-8 -*-
"""台日 Apple 價差 IG 輪播（1080×1350）。

每個型號逐容量列出日本含稅價、退稅後換算價、台灣售價與價差。
用法：python3 make_apple_cards.py
輸出：cards/apple/01_cover.png … 08_end.png
"""
import os, json, html, subprocess

W, H = 1080, 1350
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "cards/apple"

# ── 版面 ──────────────────────────────────────────────────
BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx}
body{background:#141210;color:#f5f2ee;
 font-family:"PingFang TC","Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:70px 68px 60px;position:relative;overflow:hidden}
.glow{position:absolute;width:800px;height:800px;border-radius:50%%;
 background:radial-gradient(circle,rgba(251,146,60,.18),transparent 68%%);top:-320px;right:-280px}
.brand{font-size:25px;letter-spacing:.3em;color:#fb923c;font-weight:700}
.pg{position:absolute;top:70px;right:68px;font-size:25px;color:#5f5a55;font-weight:700}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.site{font-size:27px;color:#fb923c;font-weight:700;margin-top:auto}
""" % (W, H)

COVER = """
.q{font-size:76px;font-weight:800;line-height:1.2;letter-spacing:-.02em}
.a{margin-top:44px;font-size:56px;font-weight:800;color:#fb923c;line-height:1.26}
.sub{margin-top:28px;font-size:34px;color:#a8a29c;line-height:1.6}
.sub b{color:#f5f2ee;font-weight:700}
.swipe{margin-top:46px;font-size:30px;color:#5f5a55}
"""

PROD = """
.pname{font-size:56px;font-weight:800;letter-spacing:-.02em}
.pspec{margin-top:12px;font-size:29px;color:#a8a29c}
table{width:100%;border-collapse:collapse;margin-top:44px;table-layout:fixed;
 font-variant-numeric:tabular-nums;font-feature-settings:"tnum"}
th+th,td+td{padding-left:14px}
th{font-size:21px;color:#7a736c;font-weight:600;text-align:right;
 padding:0 0 18px;letter-spacing:.03em;line-height:1.35}
th:first-child{text-align:left}
td{font-size:28px;font-weight:700;text-align:right;padding:19px 0;
 border-top:1px solid rgba(255,255,255,.09)}
td:first-child{text-align:left;font-size:24px;color:#c9c3bc;font-weight:600;
 line-height:1.35;
 padding-right:0;letter-spacing:-.01em}
td:first-child i{display:block;font-style:normal;font-size:21px;
 color:#8a837c;font-weight:500;margin-top:3px}
td.ex{color:#fb923c}
td.jpy{color:#9c958d;font-weight:600}
td.gap{font-weight:600;line-height:1.42;font-size:23px}
td.gap span{display:block;white-space:nowrap}
td.gap s{text-decoration:none;color:#6b6560;margin-right:10px;font-weight:500}
.g-jp{color:#2dd4bf}
.g-tw{color:#fb923c}
.unit{margin-top:20px;font-size:23px;color:#5f5a55;line-height:1.5}
.dates{display:flex;gap:18px;margin-top:22px}
.dates div{flex:1;background:rgba(255,255,255,.045);border-radius:14px;padding:18px 22px}
.dates b{display:block;font-size:24px;color:#a8a29c;font-weight:600;margin-bottom:8px;
 letter-spacing:.05em}
.dates u{display:block;text-decoration:none;font-size:26px;font-weight:700;line-height:1.5}
.dates u s{text-decoration:none;color:#6b6560;font-weight:500;margin-right:8px}
.verdict{margin-top:26px;padding:22px 28px;border-radius:16px;
 font-size:31px;font-weight:800;line-height:1.5}
.v-tw{background:rgba(251,146,60,.16);color:#fb923c}
.v-jp{background:rgba(45,212,191,.14);color:#2dd4bf}
"""

END = """
.h{font-size:62px;font-weight:800;line-height:1.24;letter-spacing:-.02em}
.pts{margin-top:38px;display:flex;flex-direction:column;gap:22px}
.pt{display:flex;gap:18px;align-items:flex-start;font-size:30px;line-height:1.5}
.pt i{color:#fb923c;font-style:normal;font-weight:800;flex:0 0 auto}
.pt b{font-weight:700}
"""


def head_html(css, page=None):
    p = f'<div class="pg">{page}</div>' if page else ''
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{BASE}{css}</style></head><body><div class="glow"></div>'
            f'<div class="brand">台日機票速報</div>{p}')


def main():
    ap = json.load(open("apple.json", encoding="utf-8"))
    R = ap["rate"]["jpy_twd"]; T = 1 + ap["tax"]["jp_consumption"]
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].replace("https://", "")
    P = {(p["name"], p["spec"]): p for p in ap["products"]}

    def money(n): return f"NT${n:,}"
    def inc(p): return round(p["jpy"] * R)
    def ex(p): return round(p["jpy"] / T * R)

    # (檔名, 產品名, 取價 spec, 裝置圖, 機身色, 色名)
    # 每張卡一個型號，逐容量列價。只放 2026/9 發表會的新品
    fams = [
        ("02_duo", "iPhone Duo", "摺疊機・7.6 吋展開", "容量",
         [(c, "iPhone Duo", c) for c in ("256GB", "512GB", "1TB", "2TB")]),
        ("03_18pro", "iPhone 18 Pro", "6.3 吋", "容量",
         [(c, "iPhone 18 Pro", c) for c in ("256GB", "512GB", "1TB", "2TB")]),
        ("04_18promax", "iPhone 18 Pro Max", "6.9 吋", "容量",
         [(c, "iPhone 18 Pro Max", c) for c in ("256GB", "512GB", "1TB", "2TB")]),
        ("05_acc", "Apple Watch ・ AirPods", "本次發表的配件，全部型號", "型號",
         [("Watch S12<i>42mm 起</i>", "Apple Watch Series 12", "42mm 起"),
          ("Watch Ultra 4<i>49mm</i>", "Apple Watch Ultra 4", "49mm"),
          ("AirPods 5<i>USB-C 充電盒</i>", "AirPods 5", "USB-C 充電盒"),
          ("AirPods 5<i>無線充電盒</i>", "AirPods 5", "無線充電盒")]),
    ]

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".apple_tmp.html")
    made = []

    def shot(fn, html_str):
        open(tmp, "w", encoding="utf-8").write(html_str)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    new = [p for p in ap["products"] if p.get("new")]
    iph = [p for p in new if p["cat"] == "iPhone"]
    cheap_tw = sum(1 for p in iph if p["twd"] - inc(p) < 0)
    top = max(iph, key=lambda p: p["twd"] - ex(p))
    pods = [p for p in new if p["cat"] == "AirPods"]
    wat = [p for p in new if p["cat"] == "Apple Watch"]
    w_best = max(wat, key=lambda p: p["twd"] - ex(p))
    w_gap = w_best["twd"] - ex(w_best)
    if all(p["twd"] - ex(p) < 0 for p in pods) and w_gap <= 1500:
        pt3 = (f"<b>配件不值得為它退稅</b><br>AirPods 連退稅後都是台灣便宜；"
               f"Apple Watch 最多也只差 {money(w_gap)}")
    else:
        pt3 = (f"<b>配件價差很小</b><br>AirPods 最多差 "
               f"{money(abs(max(pods, key=lambda p: p['twd'] - ex(p))['twd'] - ex(max(pods, key=lambda p: p['twd'] - ex(p)))))}"
               f"，Apple Watch 最多差 {money(abs(w_gap))}")

    shot("01_cover", head_html(COVER) + f'''<div class="mid">
<div class="q">日本買 iPhone<br>真的比較便宜嗎？</div>
<div class="a">在 Apple 直營店買<br>台灣反而便宜</div>
<div class="sub">{len(iph)} 個新機組合中，<b>{cheap_tw} 個台灣售價較低</b></div>
<div class="swipe">→ 滑看每個新品的實際價差</div></div>
<div class="site">{site}</div></body></html>''')

    total = len(fams) + 2
    DT = ap.get("dates", {})

    def date_block(names):
        d = next((DT[n] for n in names if n in DT), None)
        if not d: return ""
        return (f'<div class="dates">'
                f'<div><b>日本</b><u><s>預約</s>{d["jp_pre"]}</u>'
                f'<u><s>開賣</s>{d["jp_sale"]}</u></div>'
                f'<div><b>台灣</b><u><s>預購</s>{d["tw_pre"]}</u>'
                f'<u><s>開賣</s>{d["tw_sale"]}</u></div></div>')

    for i, (fn, title, note, col1, keys) in enumerate(fams, start=2):
        rows, gaps, gaps_inc = "", [], []
        for lbl, name, spec in keys:
            p = P.get((name, spec))
            if not p: continue
            gi = p["twd"] - inc(p)        # 正 = 直營店含稅價日本較便宜
            g = p["twd"] - ex(p)          # 正 = 退稅後日本較便宜
            gaps.append(g); gaps_inc.append(gi)

            def tag(v, lead):
                c = "g-jp" if v > 0 else "g-tw"
                w = "日本省" if v > 0 else "台灣省"
                return f'<span><s>{lead}</s><b class="{c}">{w} {abs(v):,}</b></span>'

            rows += (f'<tr><td>{lbl}</td>'   # lbl 為本檔內建字串，含 <i> 副標
                     f'<td class="jpy">¥{p["jpy"]:,}</td>'
                     f'<td>{inc(p):,}</td><td class="ex">{ex(p):,}</td>'
                     f'<td>{p["twd"]:,}</td>'
                     f'<td class="gap">{tag(gi, "含稅")}{tag(g, "退稅")}</td></tr>')
        n_jp = sum(1 for g in gaps if g > 0)
        n_tw = sum(1 for g in gaps_inc if g < 0)
        lead = ("在 Apple 直營店買，全部都是台灣便宜" if n_tw == len(gaps_inc) else
                "在 Apple 直營店買，多數是台灣便宜" if n_tw else
                "在 Apple 直營店買，日本比較便宜")
        if n_jp == len(gaps):
            v = (f'<div class="verdict v-jp">{lead}<br>'
                 f'能退稅才反轉，日本最多省 NT${max(gaps):,}</div>')
        elif n_jp == 0:
            v = (f'<div class="verdict v-tw">{lead}<br>'
                 f'連退稅後都還是台灣便宜，最多省 NT${abs(min(gaps)):,}</div>')
        else:
            v = (f'<div class="verdict v-jp">{lead}<br>'
                 f'退稅後部分型號日本較低，最多省 NT${max(gaps):,}</div>')
        shot(fn, head_html(PROD, f"{i}／{total}") + f'''<div class="mid">
<div class="pname">{html.escape(title)}</div>
<div class="pspec">{html.escape(note)}</div>
<table><colgroup><col style="width:19%"><col style="width:16%"><col style="width:14%">
<col style="width:14%"><col style="width:14%"><col style="width:23%"></colgroup>
<thead><tr><th>{col1}</th><th>日本售價<br>日圓</th><th>日本含稅<br>直營店</th>
<th>日本退稅後<br>免稅價</th><th>台灣售價</th><th>價差</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="unit">台幣欄位單位 NT$，日圓依 {R} 換算　·　日本退稅後＝含稅價扣除 10% 消費稅</div>
{date_block([k[1] for k in keys])}
{v}</div>
<div class="site">{site}</div></body></html>''')

    shot(f"{total:02d}_end", head_html(END, f"{total}／{total}") + f'''<div class="mid">
<div class="h">所以到底<br>該在哪裡買？</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>Apple 直營店已不能退稅</b><br>2024/6 起取消旅客免稅，要免稅得去 Bic Camera、Yodobashi</div></div>
 <div class="pt"><i>2</i><div><b>直營店也不能臨櫃買了</b><br>2026/2 起新機須線上下單再取貨，旅客實務上只剩量販店</div></div>
 <div class="pt"><i>3</i><div><b>能退稅才有價差</b><br>最多可省 {money(top["twd"]-ex(top))}（{top["name"]} {top["spec"]}）</div></div>
 <div class="pt"><i>4</i><div>{pt3}</div></div>
 <div class="pt"><i>5</i><div><b>11/1 起免稅要出境才退</b><br>當場先付含稅全額，海關確認後才退還消費稅</div></div>
 <div class="pt"><i>6</i><div><b>保固是區域性的</b><br>日版在台灣可能不受理，需寄回日本</div></div>
</div></div>
<div class="site">{site}/apple-japan-price</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)
    print(f"✅ 產生 {len(made)} 張輪播圖 → {OUT}/  ({W}×{H})")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
