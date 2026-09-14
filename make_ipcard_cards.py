# -*- coding: utf-8 -*-
"""買 iPhone 刷哪張卡・圖卡（1080×1350）。

資料同 /iphone-card/（apple.json 的台灣售價），每張可單獨發。

用法：python3 make_ipcard_cards.py
輸出：cards/ipcard/01_charge.png … 05_end.png ＋ posts/iphone-card.txt
"""
import os, sys, json, html, subprocess

W, H = 1080, 1350
OUT = "cards/ipcard"


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
body{background:#141210;color:#f5f2ee;
 font-family:"PingFang TC","Noto Sans TC","Noto Sans CJK TC",
 "Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:70px 68px 60px;position:relative;overflow:hidden}
.glow{position:absolute;width:800px;height:800px;border-radius:50%%;
 background:radial-gradient(circle,rgba(251,146,60,.18),transparent 68%%);top:-320px;right:-280px}
.brand{font-size:25px;letter-spacing:.3em;color:#fb923c;font-weight:700}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.site{font-size:27px;color:#fb923c;font-weight:700;margin-top:auto}
.ttl{font-size:54px;font-weight:800;letter-spacing:-.02em;line-height:1.2}
.note{margin-top:14px;font-size:28px;color:#a8a29c;line-height:1.5}
.unit{margin-top:22px;font-size:23px;color:#5f5a55;line-height:1.55}
table{width:100%%;border-collapse:collapse;margin-top:36px;table-layout:fixed;
 font-variant-numeric:tabular-nums;font-feature-settings:"tnum"}
th{font-size:22px;color:#7a736c;font-weight:600;text-align:right;
 padding:0 0 16px;line-height:1.35}
th:first-child{text-align:left}
td{font-size:29px;font-weight:700;text-align:right;padding:15px 0;
 border-top:1px solid rgba(255,255,255,.09)}
td:first-child{text-align:left;font-size:25px;color:#c9c3bc;font-weight:600;line-height:1.3}
td:first-child i{display:block;font-style:normal;font-size:20px;color:#8a837c;
 font-weight:500;margin-top:3px}
td.dim{color:#9c958d;font-weight:600;font-size:26px}
td.keep{color:#2dd4bf}
td.drop{color:#fb923c}
/* 列數多的表格用這組：行高與字級縮一階，12 列才放得進 1350px */
.dense .ttl{font-size:48px}
.dense .note{font-size:26px;margin-top:12px}
.dense table{margin-top:24px}
.dense th{font-size:21px;padding-bottom:12px}
.dense td{font-size:26px;padding:5px 0}
.dense td:first-child{font-size:23px}
.dense td:first-child i{font-size:18px;margin-top:2px}
.dense td.dim{font-size:24px}
.dense .unit{font-size:21px;margin-top:18px}
/* 單張獨立發時，結論要寫在卡上，不能靠下一張補 */
.kick{margin-top:26px;padding:22px 26px;border-radius:16px;
 background:rgba(251,146,60,.14);color:#fb923c;
 font-size:29px;font-weight:800;line-height:1.45}
""" % (W, H)

COVER = """
.q{font-size:76px;font-weight:800;line-height:1.2;letter-spacing:-.02em}
.a{margin-top:40px;font-size:54px;font-weight:800;color:#fb923c;line-height:1.28}
.cmp{margin-top:36px;display:flex;gap:18px}
.cmp div{flex:1;background:rgba(255,255,255,.05);border-radius:16px;padding:24px 26px}
.cmp b{display:block;font-size:26px;color:#a8a29c;font-weight:600}
.cmp u{display:block;text-decoration:none;font-size:52px;font-weight:800;margin-top:10px;
 letter-spacing:-.02em}
.cmp s{text-decoration:none;display:block;font-size:22px;color:#6b6560;margin-top:8px}
.sub{margin-top:30px;font-size:31px;color:#a8a29c;line-height:1.55}
.sub b{color:#f5f2ee;font-weight:700}
.swipe{margin-top:38px;font-size:30px;color:#5f5a55}
"""

MATRIX = """
.grid{margin-top:40px;display:grid;grid-template-columns:1.1fr repeat(%d,1fr);gap:10px}
.hd{font-size:24px;color:#7a736c;font-weight:600;text-align:center;padding:6px 0 10px}
.hd.l{text-align:left}
.tr{font-size:30px;font-weight:700;display:flex;align-items:center;padding-left:4px}
.cell{border-radius:14px;padding:26px 0;text-align:center;font-size:44px;font-weight:800;
 letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.na{color:#4a4642;font-size:34px}
.lg{margin-top:34px;font-size:27px;color:#a8a29c;line-height:1.6}
.lg b{color:#f5f2ee;font-weight:700}
"""

END = """
.h{font-size:62px;font-weight:800;line-height:1.24;letter-spacing:-.02em}
.pts{margin-top:36px;display:flex;flex-direction:column;gap:20px}
.pt{display:flex;gap:18px;align-items:flex-start;font-size:29px;line-height:1.5}
.pt i{color:#fb923c;font-style:normal;font-weight:800;flex:0 0 auto}
.pt b{font-weight:700}
"""


def head_html(css):
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{BASE}{css}</style></head><body><div class="glow"></div>'
            f'<div class="brand">台日機票速報</div>')





C_RATE, R_RATE = 3.3, 1.6          # 示範用的回饋率與資金年報酬
TERMS = (3, 6, 12, 24)


def main():
    AP = json.load(open("apple.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/iphone-card/"
    iph = [p for p in AP["products"] if p["cat"] == "iPhone"]
    demo = (next((p for p in iph if p.get("new") and p["spec"] == "256GB"
                  and p["name"].endswith("Pro")), None) or iph[0])
    P = demo["twd"]

    def money(n): return f"NT${round(n):,}"
    def inst(n): return P * R_RATE / 100 * (n + 1) / 24     # 分期期間留在手上的錢生的利息
    def even(n): return 24 * C_RATE / (n + 1)               # 打平所需年化報酬
    back = P * C_RATE / 100

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".ipcard_tmp.html"); made = []; CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    # ── 1 下單那天切權益沒有用 ────────────────────────────
    shot("01_charge", head_html(COVER) + f'''<div class="mid">
<div class="q">下單那天切權益，<br>其實沒有用</div>
<div class="a">Apple 官網是<br>出貨才請款</div>
<div class="cmp">
 <div><b>下單／預購</b><u>預先授權</u><s>常見一筆 1 元，不是消費</s></div>
 <div><b>出貨</b><u>正式請款</u><s>回饋以這天認列</s></div>
</div>
<div class="sub">台新、國泰這類<b>當日切換權益</b>的卡，要在收到刷卡通知那天
處於正確方案才算數。下單日切了、出貨前切回去，等於白做。</div>
<div class="swipe">出處：Apple 台灣購物協助・付款與安全性</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 回饋看的是哪一天 ───────────────────────────────
    rows = ('<tr><td><b>下單／預購</b></td><td class="dim">取得預先授權，常見 1 元</td>'
            '<td class="drop">不認列</td></tr>'
            '<tr><td><b>出貨</b></td><td class="dim">正式請款，金額入帳</td>'
            '<td class="keep">以這天判定</td></tr>'
            '<tr><td><b>結帳日</b></td><td class="dim">列入當期帳單</td>'
            '<td class="dim">依發卡行週期入帳</td></tr>')
    shot("02_timeline", head_html("") + f'''<div class="mid">
<div class="ttl">回饋看的是哪一天？</div>
<div class="note">Apple 確認訂單時只做預先授權，出貨交付運送人時才向發卡行請款</div>
<table><colgroup><col style="width:26%"><col style="width:44%"><col style="width:30%"></colgroup>
<thead><tr><th>時點</th><th>發生什麼</th><th>對回饋</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="kick">活動寫「9/30 前」指的是請款日——
iPhone Duo 10 月中才開放預購，出貨更晚，短期活動很可能吃不到</div>
<div class="unit">出處：Apple 台灣購物協助・付款與安全性</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 Apple Store 不算「數位」通路 ───────────────────
    ok = ["App Store", "Apple Music", "iCloud", "Apple TV+",
          "Apple Arcade", "Apple One", "iTunes"]
    # 同一欄重複七次「媒體服務」很吵，改成打勾／打叉，對比才看得出來
    rows = ''.join(f'<tr><td>{o}</td><td class="keep">✓ 算</td></tr>' for o in ok)
    rows += ('<tr><td class="drop"><b>Apple Store</b><i>官網、直營店買機器</i></td>'
             '<td class="drop"><b>✗ 不算</b></td></tr>')
    shot("03_channel", head_html("") + f'''<div class="mid">
<div class="ttl">Apple Store<br>不算「數位」通路</div>
<div class="note">以國泰世華 CUBE 卡「玩數位」為例，官方權益說明列得很細</div>
<table><colgroup><col style="width:62%"><col style="width:38%"></colgroup>
<thead><tr><th>通路</th><th>「玩數位」認列</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="kick">官方原文：「⋯⋯不含 Apple Store 之交易」</div>
<div class="unit">看到攻略寫「官網刷某卡有 3.3%」，先去該行的權益說明確認
Apple Store 在不在認列範圍內——這種細節通常寫在條款的括號裡<br>
出處：國泰世華 CUBE 卡權益分級</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 4 分期 0 利率 vs 回饋 ────────────────────────────
    rows = ''.join(
        f'<tr><td><b>{n} 期</b></td><td class="dim">{money(inst(n))}</td>'
        f'<td class="keep">{money(back)}</td>'
        f'<td class="drop">{even(n):.1f}%</td></tr>' for n in TERMS)
    shot("04_installment", head_html("") + f'''<div class="mid">
<div class="ttl">分期 0 利率和回饋，<br>哪個划算？</div>
<div class="note">0 利率分期的價值，就是你留在手上那筆錢能生的利息。
以 {html.escape(demo["name"])} {html.escape(demo["spec"])}（{money(P)}）、
回饋 {C_RATE}%、資金年報酬 {R_RATE}% 試算</div>
<table><colgroup><col style="width:18%"><col style="width:28%">
<col style="width:26%"><col style="width:28%"></colgroup>
<thead><tr><th>期數</th><th>分期的價值</th><th>{C_RATE}% 回饋</th>
<th>要多少報酬才打平</th></tr></thead><tbody>{rows}</tbody></table>
<div class="kick">24 期要打平 {C_RATE}% 回饋，
你的錢得有 {even(24):.1f}% 年化報酬——定存拿不到</div>
<div class="unit">分期價值 ≈ 本金 × 年報酬 × (期數＋1) ÷ 24　·　
打平報酬率 ＝ 24 × 回饋率 ÷ (期數＋1)</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 5 檢查順序 ───────────────────────────────────────
    shot("05_end", head_html(END) + f'''<div class="mid">
<div class="h">買 iPhone 刷卡，<br>照這個順序檢查</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>你的卡在「Apple Store」有沒有加碼</b><br>
  不是看它在「網購」或「數位」有多少。Apple Store 常常被單獨排除</div></div>
 <div class="pt"><i>2</i><div><b>出貨日落在活動期間內嗎</b><br>
  官網出貨才請款，活動以請款日判定；預購熱門機種容易跨過結束日</div></div>
 <div class="pt"><i>3</i><div><b>那天你的權益方案是對的嗎</b><br>
  當日切換型的卡要在收到刷卡通知那天處於正確方案</div></div>
 <div class="pt"><i>4</i><div><b>分期還是一次付清</b><br>
  多數卡二選一。24 期要打平 {C_RATE}% 回饋，資金得有 {even(24):.1f}% 年化報酬</div></div>
 <div class="pt"><i>5</i><div><b>最後才比回饋率</b><br>
  前面幾關沒過，回饋率再高都是 0</div></div>
</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    L = site
    posts = [
     ("01_charge", f"""在 Apple 官網下單那天切換信用卡權益——沒有用。

因為 Apple 官網是**出貨才請款**。

・下單／預購：只取得預先授權，常見是一筆 1 元，不是消費
・出貨：正式請款，回饋以這天認列

所以台新、國泰這類「當日切換權益」的卡，必須在收到刷卡通知那天處於正確方案。下單日切了、出貨前又切回去，等於白做。

很多人照著攻略下單，下個月才發現只拿到基本回饋。

出處：Apple 台灣購物協助・付款與安全性
完整說明：{L}"""),
     ("02_timeline", f"""「這個活動 9/30 前刷卡有加碼」——那你得先知道自己哪天被扣款。

Apple 官網實體商品是出貨才向發卡行請款，回饋活動也多以請款日判定。

・下單／預購　取得預先授權　→ 不認列
・出貨　正式請款　→ 以這天判定
・結帳日　列入當期帳單　→ 依發卡行週期入帳

iPhone Duo 10 月中才開放預購，出貨更晚。想靠 9 月底到期的活動衝回饋，很可能整個撲空。

{L}"""),
     ("03_channel", f"""「Apple 官網刷 CUBE 卡有 3.3%」——這句話是錯的。

國泰世華 CUBE 卡「玩數位」方案的認列範圍，官方權益說明列得很細：App Store、Apple Music、iCloud、Apple TV+、Apple Arcade、Apple One、iTunes 等 Apple 媒體服務的訂閱與購買。

然後有一句：「⋯⋯不含 Apple Store 之交易」。

在官網或直營店買一支手機，不屬於這個通路。

看到攻略寫「官網刷某卡有 X%」，先去該行的權益說明確認 Apple Store 在不在認列範圍內——這種細節通常寫在條款的括號裡。

出處：國泰世華 CUBE 卡權益分級
{L}"""),
     ("04_installment", f"""「分期 0 利率跟回饋只能二選一」——那到底該選哪個？

算得出來。0 利率分期的價值，就是你留在手上那筆錢能生的利息。

以 {demo["name"]} {demo["spec"]}（{money(P)}）、回饋 {C_RATE}%、資金年報酬 {R_RATE}% 算：

・3 期　分期價值 {money(inst(3))}　回饋 {money(back)}
・12 期　分期價值 {money(inst(12))}　回饋 {money(back)}
・24 期　分期價值 {money(inst(24))}　回饋 {money(back)}

要讓 24 期 0 利率贏過 {C_RATE}% 回饋，你的錢得有 {even(24):.1f}% 的年化報酬。定存拿不到。

結論：除非你本來就缺現金週轉，不然拿回饋。分期 0 利率的價值是現金流，不是省錢。

可調參數的試算：{L}"""),
     ("05_end", f"""買 iPhone 刷卡，照這個順序檢查：

1　你的卡在「Apple Store」有沒有加碼
不是看它在「網購」或「數位」有多少

2　出貨日落在活動期間內嗎
官網出貨才請款，活動以請款日判定

3　那天你的權益方案是對的嗎
當日切換型的卡要在收到刷卡通知那天切對

4　分期還是一次付清
24 期要打平 {C_RATE}% 回饋，資金得有 {even(24):.1f}% 年化報酬

5　最後才比回饋率
前面幾關沒過，回饋率再高都是 0

攻略都在比第 5 項，但讓人拿不到回饋的是前面四項。

{L}"""),
    ]
    os.makedirs("posts", exist_ok=True)
    pf = "posts/iphone-card.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write("買 iPhone 刷哪張卡・圖卡文案\n每張圖各自獨立，可分開發\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n" + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
