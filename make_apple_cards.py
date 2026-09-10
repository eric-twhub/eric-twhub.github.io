# -*- coding: utf-8 -*-
"""台日 Apple 價差 IG 輪播（1080×1350）。

機身以自繪 SVG 輪廓呈現——不使用 Apple 官方產品照，避免版權問題。
用法：python3 make_apple_cards.py
輸出：cards/apple/01_cover.png … 07_end.png
"""
import os, json, html, subprocess, sys

W, H = 1080, 1350
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "cards/apple"

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
.pname{font-size:60px;font-weight:800;letter-spacing:-.02em}
.pspec{margin-top:10px;font-size:30px;color:#a8a29c}
.dev{display:flex;gap:26px;align-items:flex-end;margin:44px 0 40px}
.rows{display:flex;flex-direction:column;gap:14px}
.r{display:flex;align-items:baseline;gap:16px;font-size:34px}
.r s{text-decoration:none;color:#6b6560;width:150px;flex:0 0 auto;font-size:29px}
.r b{font-weight:700}
.r .hi{color:#fb923c;font-weight:800;font-size:42px}
.verdict{margin-top:34px;padding:20px 24px;border-radius:14px;font-size:33px;font-weight:700;line-height:1.5}
.v-tw{background:rgba(251,146,60,.16);color:#fb923c}
.v-jp{background:rgba(45,212,191,.14);color:#2dd4bf}
"""

END = """
.h{font-size:62px;font-weight:800;line-height:1.24;letter-spacing:-.02em}
.pts{margin-top:44px;display:flex;flex-direction:column;gap:26px}
.pt{display:flex;gap:18px;align-items:flex-start;font-size:33px;line-height:1.55}
.pt i{color:#fb923c;font-style:normal;font-weight:800;flex:0 0 auto}
.pt b{font-weight:700}
.cta{margin-top:44px;font-size:34px;color:#fb923c;font-weight:700;line-height:1.5}
"""


def phone_svg(fill, w=132, h=250, notch=True):
    """自繪機身輪廓，非 Apple 官方素材"""
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 132 250">
<rect x="3" y="3" width="126" height="244" rx="26" fill="{fill}" stroke="#3a3532" stroke-width="4"/>
{'<rect x="46" y="14" width="40" height="11" rx="6" fill="#141210" opacity=".55"/>' if notch else ''}
<rect x="16" y="22" width="42" height="46" rx="13" fill="#141210" opacity=".22"/>
</svg>'''


def watch_svg(fill):
    return '''<svg width="118" height="250" viewBox="0 0 118 250">
<rect x="38" y="6" width="42" height="52" rx="14" fill="#2a2624"/>
<rect x="38" y="192" width="42" height="52" rx="14" fill="#2a2624"/>
<rect x="10" y="52" width="98" height="146" rx="30" fill="%s" stroke="#3a3532" stroke-width="4"/>
<rect x="24" y="66" width="70" height="118" rx="22" fill="#141210" opacity=".35"/>
</svg>''' % fill


def pods_svg(fill):
    return '''<svg width="150" height="250" viewBox="0 0 150 250">
<rect x="24" y="86" width="102" height="86" rx="22" fill="%s" stroke="#3a3532" stroke-width="4"/>
<circle cx="75" cy="129" r="5" fill="#141210" opacity=".45"/>
</svg>''' % fill


def head(css, page=None):
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

    # (檔名, 產品名, 取價用 spec, 圖形, 說明)
    items = [
        ("02_duo", "iPhone Duo", "256GB", phone_svg("#e8e4dd") + phone_svg("#26303c"), "星光白色・夜空色"),
        ("03_18pro", "iPhone 18 Pro", "256GB", phone_svg("#c9a227") + phone_svg("#3a3a3c"), "6.3 吋"),
        ("04_18promax", "iPhone 18 Pro Max", "256GB", phone_svg("#c9a227") + phone_svg("#3a3a3c"), "6.9 吋"),
        ("05_air", "iPhone Air", "256GB", phone_svg("#dcd6c8") + phone_svg("#8fb4cc"), "淺金・天藍・雲白・太空黑"),
        ("06_watch", "Apple Watch Series 12", "42mm 起", watch_svg("#3a3a3c") + watch_svg("#c9a227"), "42mm／46mm"),
        ("07_pods", "AirPods Pro 3", "", pods_svg("#e8e4dd"), "主動式降噪"),
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

    iph = [p for p in ap["products"] if p["cat"] == "iPhone"]
    cheap_tw = sum(1 for p in iph if p["twd"] - inc(p) < 0)
    top = max(iph, key=lambda p: p["twd"] - ex(p))

    # 封面
    shot("01_cover", head(COVER) + f'''<div class="mid">
<div class="q">日本買 iPhone<br>真的比較便宜嗎？</div>
<div class="a">在 Apple 直營店買<br>台灣反而便宜</div>
<div class="sub">15 個 iPhone 組合中，<b>{cheap_tw} 個台灣售價較低</b></div>
<div class="swipe">→ 滑看每個新品的實際價差</div></div>
<div class="site">{site}</div></body></html>''')

    total = len(items) + 2
    for i, (fn, name, spec, svg, note) in enumerate(items, start=2):
        p = P.get((name, spec))
        if not p: continue
        d_inc = p["twd"] - inc(p); d_ex = p["twd"] - ex(p)
        v = (f'<div class="verdict v-jp">退稅後日本省 {money(d_ex)}</div>' if d_ex > 0
             else f'<div class="verdict v-tw">台灣便宜 {money(-d_ex)}，不必特地在日本買</div>')
        shot(fn, head(PROD, f"{i}／{total}") + f'''<div class="mid">
<div class="pname">{html.escape(name)}</div>
<div class="pspec">{html.escape(spec or note)}</div>
<div class="dev">{svg}</div>
<div class="rows">
 <div class="r"><s>日本含稅</s><b>¥{p["jpy"]:,}</b><s>≈ {money(inc(p))}</s></div>
 <div class="r"><s>日本退稅後</s><span class="hi">{money(ex(p))}</span></div>
 <div class="r"><s>台灣售價</s><b>{money(p["twd"])}</b></div>
</div>{v}</div>
<div class="site">{site}</div></body></html>''')

    # 結論
    shot(f"{total:02d}_end", head(END, f"{total}／{total}") + f'''<div class="mid">
<div class="h">所以到底<br>該在哪裡買？</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>Apple 直營店已不能退稅</b><br>2024/6 起取消旅客免稅，要免稅得去 Bic Camera、Yodobashi</div></div>
 <div class="pt"><i>2</i><div><b>能退稅才有價差</b><br>最多可省 {money(top["twd"]-ex(top))}（{top["name"]} {top["spec"]}）</div></div>
 <div class="pt"><i>3</i><div><b>Watch 與 AirPods 別買</b><br>連退稅後都是台灣便宜</div></div>
 <div class="pt"><i>4</i><div><b>保固是區域性的</b><br>日版在台灣可能不受理，需寄回日本</div></div>
</div>
<div class="cta">完整價格表與退稅試算<br>都在個人檔案的連結</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)
    print(f"✅ 產生 {len(made)} 張輪播圖 → {OUT}/  ({W}×{H})")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
