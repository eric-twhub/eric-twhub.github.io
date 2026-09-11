# -*- coding: utf-8 -*-
"""單張主張式貼文圖（1080×1350）。

一張圖只講一件事，適合 Threads／FB 單圖貼文。
目前主題：2026/11/1 日本免稅改制（リファンド方式）。
資料來源：日本觀光廳消費稅免稅店網站。
用法：python3 make_post_card.py
輸出：cards/posts/taxfree-1101.png
"""
import os, json, subprocess

W, H = 1080, 1350
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "cards/posts"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx}
body{background:#141210;color:#f5f2ee;
 font-family:"PingFang TC","Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:70px 68px 60px;position:relative;overflow:hidden}
.glow{position:absolute;width:820px;height:820px;border-radius:50%%;
 background:radial-gradient(circle,rgba(251,146,60,.2),transparent 68%%);top:-340px;right:-300px}
.brand{font-size:25px;letter-spacing:.3em;color:#fb923c;font-weight:700}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.kicker{font-size:29px;color:#fb923c;font-weight:700;letter-spacing:.06em}
.h{margin-top:20px;font-size:78px;font-weight:800;line-height:1.16;letter-spacing:-.03em}
.lede{margin-top:26px;font-size:31px;color:#a8a29c;line-height:1.6}
.rows{margin-top:44px;display:flex;flex-direction:column;gap:16px}
.row{background:rgba(255,255,255,.05);border-radius:18px;padding:26px 30px}
.row.now{border-left:6px solid #5f5a55}
.row.new{border-left:6px solid #fb923c;background:rgba(251,146,60,.11)}
.rt{font-size:27px;font-weight:700;color:#a8a29c;letter-spacing:.04em}
.row.new .rt{color:#fb923c}
.rb{margin-top:12px;font-size:34px;font-weight:700;line-height:1.45}
.rb s{text-decoration:none;color:#8a837c;font-weight:500}
.warn{margin-top:30px;padding:24px 28px;border-radius:16px;
 background:rgba(220,38,38,.14);color:#fca5a5;font-size:29px;font-weight:700;line-height:1.5}
.src{margin-top:24px;font-size:23px;color:#5f5a55;line-height:1.5}
.site{font-size:27px;color:#fb923c;font-weight:700;margin-top:auto}
""" % (W, H)


def main():
    ap = json.load(open("apple.json", encoding="utf-8"))
    R = ap["rate"]["jpy_twd"]
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/apple-japan-price/"

    # 以本次最貴的新機示範要先墊多少稅金
    top = max((p for p in ap["products"] if p.get("new")), key=lambda p: p["jpy"])
    tax_jpy = round(top["jpy"] - top["jpy"] / 1.1)
    tax_twd = round(tax_jpy * R)
    # 一般旅客的量級：消費 10 萬日圓
    ex_jpy = round(100000 - 100000 / 1.1)

    html_str = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<style>{CSS}</style></head><body><div class="glow"></div>
<div class="brand">台日機票速報</div>
<div class="mid">
<div class="kicker">日本免稅制度改制</div>
<div class="h">11/1 起<br>免稅要先付全額</div>
<div class="lede">不是取消免稅，是改成「出境後才退錢」。<br>影響每一個到日本購物的旅客。</div>
<div class="rows">
 <div class="row now"><div class="rt">10/31 前</div>
  <div class="rb">結帳直接扣掉 10%<s>　當場就是免稅價</s></div></div>
 <div class="row new"><div class="rt">11/1 起</div>
  <div class="rb">先付含稅全額 → 出境經海關確認<br>→ 店家事後退還消費稅</div></div>
</div>
<div class="warn">同一筆交易只要有一項沒通過海關查驗，<br>整筆都不算免稅</div>
<div class="src">以 {top["name"]} {top["spec"]} 為例，要先多墊 ¥{tax_jpy:,}（約 NT${tax_twd:,}）；<br>
一般消費 10 萬日圓也要先墊 ¥{ex_jpy:,}。資料來源：日本觀光廳</div>
</div>
<div class="site">{site}</div></body></html>"""

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".post_tmp.html")
    open(tmp, "w", encoding="utf-8").write(html_str)
    png = os.path.abspath(os.path.join(OUT, "taxfree-1101.png"))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={png}", f"--window-size={W},{H}",
                    "--force-device-scale-factor=1", "file://" + tmp],
                   capture_output=True, timeout=90)
    os.path.exists(tmp) and os.remove(tmp)
    print(f"✅ {png}")


if __name__ == "__main__":
    main()
