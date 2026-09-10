# -*- coding: utf-8 -*-
"""台日 Apple 價差 IG 輪播（1080×1350）。

裝置外觀全以幾何 SVG 自繪——不使用 Apple 官方產品照或商標，避免版權問題。
用法：python3 make_apple_cards.py
輸出：cards/apple/01_cover.png … 08_end.png
"""
import os, json, html, subprocess

W, H = 1080, 1350
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "cards/apple"

# ── 裝置外觀 ──────────────────────────────────────────────
_uid = [0]


def _u():
    _uid[0] += 1
    return f"g{_uid[0]}"


def _defs(body, frame, uid):
    """機身漸層＋外框金屬漸層。"""
    return f'''<defs>
<linearGradient id="{uid}b" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#ffffff" stop-opacity=".16"/>
 <stop offset=".38" stop-color="{body}" stop-opacity="0"/>
 <stop offset="1" stop-color="#000000" stop-opacity=".22"/></linearGradient>
<linearGradient id="{uid}f" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="{frame}"/>
 <stop offset=".14" stop-color="#ffffff" stop-opacity=".55"/>
 <stop offset=".45" stop-color="{frame}"/>
 <stop offset=".9" stop-color="#ffffff" stop-opacity=".35"/>
 <stop offset="1" stop-color="{frame}"/></linearGradient>
<radialGradient id="{uid}l" cx=".35" cy=".3" r=".8">
 <stop offset="0" stop-color="#5b6b82"/><stop offset=".55" stop-color="#141a22"/>
 <stop offset="1" stop-color="#05070a"/></radialGradient>
</defs>'''


def _lens(cx, cy, r, uid):
    """鏡頭：外環→鏡片→反光點。"""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2f2c29" stroke="#565049" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r-5}" fill="url(#{uid}l)"/>'
            f'<circle cx="{cx-r*.28:.1f}" cy="{cy-r*.3:.1f}" r="{r*.22:.1f}" fill="#8fa6c4" opacity=".55"/>')


def iphone_pro(body, frame="#8d8880", h=430):
    """Pro 背面：方形相機平台＋三鏡頭三角排列。"""
    u = _u()
    w = int(h * 200 / 400)
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 200 400" fill="none">{_defs(body, frame, u)}
<rect x="3" y="122" width="5" height="34" rx="2.5" fill="{frame}"/>
<rect x="3" y="170" width="5" height="52" rx="2.5" fill="{frame}"/>
<rect x="192" y="152" width="5" height="62" rx="2.5" fill="{frame}"/>
<rect x="6" y="4" width="188" height="392" rx="44" fill="url(#{u}f)"/>
<rect x="10" y="8" width="180" height="384" rx="40" fill="{body}"/>
<rect x="10" y="8" width="180" height="384" rx="40" fill="url(#{u}b)"/>
<rect x="24" y="24" width="104" height="104" rx="30" fill="{body}" stroke="#ffffff" stroke-opacity=".14" stroke-width="2"/>
{_lens(56, 56, 21, u)}{_lens(100, 56, 21, u)}{_lens(56, 100, 21, u)}
<circle cx="100" cy="98" r="9" fill="#f4e6c4" opacity=".85"/>
<circle cx="100" cy="119" r="5" fill="#1b1815"/>
</svg>'''


def iphone_bar(body, frame="#8d8880", h=430):
    """Air：橫向相機條，單鏡頭。"""
    u = _u()
    w = int(h * 200 / 400)
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 200 400" fill="none">{_defs(body, frame, u)}
<rect x="3" y="122" width="5" height="34" rx="2.5" fill="{frame}"/>
<rect x="3" y="170" width="5" height="52" rx="2.5" fill="{frame}"/>
<rect x="192" y="152" width="5" height="62" rx="2.5" fill="{frame}"/>
<rect x="6" y="4" width="188" height="392" rx="44" fill="url(#{u}f)"/>
<rect x="10" y="8" width="180" height="384" rx="40" fill="{body}"/>
<rect x="10" y="8" width="180" height="384" rx="40" fill="url(#{u}b)"/>
<rect x="22" y="28" width="156" height="54" rx="25" fill="{body}" stroke="#ffffff" stroke-opacity=".14" stroke-width="2"/>
{_lens(56, 55, 20, u)}
<circle cx="116" cy="55" r="8" fill="#f4e6c4" opacity=".8"/>
<circle cx="144" cy="55" r="5" fill="#1b1815"/>
</svg>'''


def watch(body, band="#2f2b28", h=430):
    """Apple Watch：錶帶＋數位錶冠＋側邊按鈕。"""
    u = _u()
    w = int(h * 200 / 400)
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 200 400" fill="none">{_defs(body, body, u)}
<path d="M66 2h68v118H66z" fill="{band}"/>
<path d="M66 282h68v116H66z" fill="{band}"/>
<rect x="58" y="96" width="84" height="30" rx="12" fill="{band}"/>
<rect x="58" y="276" width="84" height="30" rx="12" fill="{band}"/>
<rect x="30" y="104" width="140" height="194" rx="52" fill="url(#{u}f)"/>
<rect x="38" y="112" width="124" height="178" rx="45" fill="#0a0c0f"/>
<rect x="48" y="122" width="104" height="158" rx="38" fill="#12151a"/>
<circle cx="100" cy="176" r="26" fill="none" stroke="#fb923c" stroke-width="7" stroke-linecap="round"
 stroke-dasharray="130 34" transform="rotate(-90 100 176)"/>
<rect x="72" y="222" width="56" height="9" rx="4" fill="#3d444e"/>
<rect x="72" y="242" width="38" height="9" rx="4" fill="#2c323a"/>
<rect x="168" y="150" width="15" height="38" rx="7" fill="{body}" stroke="#ffffff" stroke-opacity=".22" stroke-width="2"/>
<rect x="169" y="204" width="12" height="46" rx="6" fill="{body}" opacity=".85"/>
</svg>'''


def watch_ultra(body="#b9b1a4", band="#3c3a35", h=430):
    """Apple Watch Ultra：鈦金屬平面錶身、左側橘色動作按鈕。"""
    u = _u()
    w = int(h * 200 / 400)
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 200 400" fill="none">{_defs(body, body, u)}
<path d="M62 2h76v122H62z" fill="{band}"/>
<path d="M62 278h76v120H62z" fill="{band}"/>
<rect x="54" y="100" width="92" height="28" rx="10" fill="{band}"/>
<rect x="54" y="274" width="92" height="28" rx="10" fill="{band}"/>
<rect x="22" y="104" width="156" height="196" rx="46" fill="url(#{u}f)"/>
<rect x="30" y="112" width="140" height="180" rx="40" fill="#0a0c0f"/>
<rect x="40" y="122" width="120" height="160" rx="33" fill="#12151a"/>
<circle cx="100" cy="182" r="28" fill="none" stroke="#fb923c" stroke-width="8" stroke-linecap="round"
 stroke-dasharray="140 36" transform="rotate(-90 100 182)"/>
<rect x="70" y="232" width="60" height="10" rx="5" fill="#3d444e"/>
<rect x="70" y="253" width="40" height="10" rx="5" fill="#2c323a"/>
<rect x="12" y="176" width="14" height="48" rx="6" fill="#f97316"/>
<rect x="176" y="150" width="16" height="40" rx="7" fill="{body}" stroke="#ffffff" stroke-opacity=".25" stroke-width="2"/>
<rect x="177" y="206" width="13" height="48" rx="6" fill="{body}" opacity=".85"/>
</svg>'''


def airpods(body="#f4f2ee", h=430, tips=True):
    """AirPods Pro：矽膠耳塞＋耳機柄，左右各一。"""
    u = _u()
    w = int(h * 200 / 400)
    edge, tip, dark = "#cfc9bf", "#e3ded4", "#8f8981"

    def bud(x, y, rot, s):
        return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
                f'<rect x="-14" y="18" width="28" height="112" rx="14" fill="{body}" '
                f'stroke="{edge}" stroke-width="2"/>'
                f'<rect x="-8" y="104" width="16" height="5" rx="2.5" fill="{dark}" opacity=".5"/>'
                f'<circle cx="0" cy="0" r="40" fill="{body}" stroke="{edge}" stroke-width="2"/>'
                f'<ellipse cx="8" cy="6" rx="13" ry="19" fill="{dark}" opacity=".22"/>'
                + (f'<g transform="rotate(-32)">'
                   f'<ellipse cx="0" cy="-38" rx="25" ry="21" fill="{tip}" stroke="{edge}" stroke-width="2"/>'
                   f'<ellipse cx="0" cy="-44" rx="14" ry="10" fill="{dark}"/>'
                   f'<ellipse cx="0" cy="-45" rx="9" ry="6" fill="#4a4540"/></g>' if tips else
                   f'<ellipse cx="-12" cy="-14" rx="17" ry="12" fill="{dark}" opacity=".3" '
                   f'transform="rotate(-32 -12 -14)"/>')
                + f'</g>')
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 200 400" fill="none">'
            f'{bud(128, 128, 14, .78)}{bud(70, 244, -8, .96)}</svg>')


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
.pname{font-size:58px;font-weight:800;letter-spacing:-.02em}
.pspec{margin-top:12px;font-size:30px;color:#a8a29c;display:flex;align-items:center;gap:16px}
.dots{display:flex;gap:10px}
.dots i{width:22px;height:22px;border-radius:50%;display:block;box-shadow:0 0 0 2px rgba(255,255,255,.16)}
.cols{display:flex;gap:52px;align-items:center;margin:44px 0 40px}
.dev{flex:0 0 auto;padding:18px 26px;border-radius:34px;
 background:radial-gradient(ellipse at 50% 45%,rgba(255,255,255,.075),transparent 68%);
 filter:drop-shadow(0 26px 34px rgba(0,0,0,.55))}
.rows{flex:1;display:flex;flex-direction:column;gap:24px}
.r{display:flex;flex-direction:column;gap:6px}
.r s{text-decoration:none;color:#7a736c;font-size:27px;letter-spacing:.04em}
.r b{font-size:44px;font-weight:700;white-space:nowrap}
.r em{font-style:normal;color:#8a837c;font-size:30px;font-weight:400}
.r .hi{color:#fb923c;font-weight:800;font-size:52px}
.verdict{padding:26px 30px;border-radius:16px;font-size:36px;font-weight:800;line-height:1.45}
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
    # 只放 2026/9 發表會的新品，順序照發表順序
    items = [
        ("02_duo", "iPhone Duo", "256GB", iphone_pro("#ece7dd"),
         ["#ece7dd", "#26303c"], "摺疊機・7.6 吋展開"),
        ("03_18pro", "iPhone 18 Pro", "256GB", iphone_pro("#c9a227"),
         ["#c9a227", "#3a3a3c", "#d8d4cd"], "6.3 吋"),
        ("04_18promax", "iPhone 18 Pro Max", "256GB", iphone_pro("#3a3a3c"),
         ["#c9a227", "#3a3a3c", "#d8d4cd"], "6.9 吋"),
        ("05_watch", "Apple Watch Series 12", "42mm 起", watch("#3a3a3c"),
         ["#3a3a3c", "#c9a227", "#d8d4cd"], "42mm／46mm"),
        ("06_ultra", "Apple Watch Ultra 4", "49mm", watch_ultra(),
         ["#b9b1a4", "#3c3a35"], "49mm 鈦金屬"),
        ("07_pods", "AirPods 5", "USB-C 充電盒", airpods(tips=False),
         [], "主動式降噪"),
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

    total = len(items) + 2
    for i, (fn, name, spec, svg, colors, note) in enumerate(items, start=2):
        p = P.get((name, spec))
        if not p: continue
        d_ex = p["twd"] - ex(p)
        v = (f'<div class="verdict v-jp">退稅後日本省 {money(d_ex)}</div>' if d_ex > 0
             else f'<div class="verdict v-tw">台灣便宜 {money(-d_ex)}，不必特地在日本買</div>')
        dots = ("".join(f'<i style="background:{c}"></i>' for c in colors))
        dots = f'<span class="dots">{dots}</span>' if dots else ""
        shot(fn, head_html(PROD, f"{i}／{total}") + f'''<div class="mid">
<div class="pname">{html.escape(name)}</div>
<div class="pspec"><span>{html.escape(spec or note)}</span>{dots}</div>
<div class="cols"><div class="dev">{svg}</div>
<div class="rows">
 <div class="r"><s>日本含稅</s><b>¥{p["jpy"]:,} <em>≈ {money(inc(p))}</em></b></div>
 <div class="r"><s>日本退稅後</s><b class="hi">{money(ex(p))}</b></div>
 <div class="r"><s>台灣售價</s><b>{money(p["twd"])}</b></div>
</div></div>{v}</div>
<div class="site">{site}</div></body></html>''')

    shot(f"{total:02d}_end", head_html(END, f"{total}／{total}") + f'''<div class="mid">
<div class="h">所以到底<br>該在哪裡買？</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>Apple 直營店已不能退稅</b><br>2024/6 起取消旅客免稅，要免稅得去 Bic Camera、Yodobashi</div></div>
 <div class="pt"><i>2</i><div><b>能退稅才有價差</b><br>最多可省 {money(top["twd"]-ex(top))}（{top["name"]} {top["spec"]}）</div></div>
 <div class="pt"><i>3</i><div>{pt3}</div></div>
 <div class="pt"><i>4</i><div><b>保固是區域性的</b><br>日版在台灣可能不受理，需寄回日本</div></div>
</div>
<div class="cta">完整價格表與退稅試算<br>都在個人檔案的連結</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)
    print(f"✅ 產生 {len(made)} 張輪播圖 → {OUT}/  ({W}×{H})")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
