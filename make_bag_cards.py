# -*- coding: utf-8 -*-
"""廉航行李費圖卡（1080×1350）。

資料同 /japan-flight-baggage/（baggage.json ＋ 票價快取），每張可單獨發。

用法：python3 make_bag_cards.py
輸出：cards/bag/01_cover.png … 05_end.png ＋ posts/japan-baggage.txt
"""
import os, sys, json, html, subprocess

W, H = 1080, 1350
OUT = "cards/bag"
SCAN = "/tmp/scan_all.json"

# 只做本站有足夠一般航空紀錄的三個航點
TARGETS = [("沖繩", {"OKA"}), ("東京", {"TYO", "HND", "NRT"}), ("大阪", {"OSA", "KIX"})]
FSC = {"BR", "CI", "JX", "JL", "NH", "NU", "CX", "KE", "UA", "AE",
       "HX", "MF", "OZ", "FM", "B7", "PR"}
NAME = {"IT": "台灣虎航", "MM": "樂桃航空", "GK": "捷星日本", "TR": "酷航",
        "VZ": "泰越捷航空", "SL": "泰國獅子航空", "FD": "泰國亞洲航空",
        "NQ": "Air Japan", "UO": "香港快運", "TW": "德威航空", "LJ": "真航空",
        "BR": "長榮航空", "CI": "中華航空", "JX": "星宇航空", "JL": "日本航空",
        "NH": "全日空", "NU": "日本越洋航空", "AE": "華信航空", "MF": "廈門航空",
        "B7": "立榮航空", "OZ": "韓亞航空"}


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






def main():
    BG = json.load(open("baggage.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/japan-flight-baggage/"
    REF, TG = BG["ref"], BG["tigerair"]
    RT = REF["per_leg"] * 2

    def money(n): return f"NT${round(n):,}"

    rows = json.load(open(SCAN, encoding="utf-8")) if os.path.exists(SCAN) else []
    cities = []
    for nm, codes in TARGETS:
        f = [r for r in rows if r.get("destination") in codes and r.get("return_at")
             and r.get("price")]
        lcc = sorted([r for r in f if r.get("airline") not in FSC], key=lambda x: x["price"])
        fsc = sorted([r for r in f if r.get("airline") in FSC], key=lambda x: x["price"])
        if lcc and len(fsc) >= 5:
            cities.append((nm, lcc[0], fsc[0]))
    if not cities:
        sys.exit("票價快取不足，無法產生圖卡（先跑 scan_all.py）")

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".bag_tmp.html"); made = []; CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    # ── 1 封面：最便宜的那張票不能帶行李箱 ─────────────────
    nm0, l0, f0 = cities[0]
    a0 = NAME.get(l0["airline"], l0["airline"])
    shot("01_cover", head_html(COVER) + f'''<div class="mid">
<div class="q">{money(l0["price"])} 的{nm0}機票，<br>不能帶行李箱</div>
<div class="a">廉航的最低票價<br>不含託運行李</div>
<div class="cmp">
 <div><b>你看到的價格</b><u>{money(l0["price"])}</u><s>{html.escape(a0)}・只能帶手提</s></div>
 <div><b>帶一個行李箱</b><u>{money(l0["price"] + RT)}</u><s>＋來回 {REF["kg"]}kg {money(RT)}</s></div>
</div>
<div class="sub">廉航的商業模式就是把行李、選位、餐食拆開來賣，讓帳面票價看起來最低。
<b>要比，就要比含行李之後的價格。</b></div>
<div class="swipe">行李費依{html.escape(REF["airline"])}公告費率・查證於 {BG["checked"]}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 加上行李之後，價差縮多少 ────────────────────────
    trs, shrink = "", []
    for nm, l, f in cities:
        gap, gap2 = f["price"] - l["price"], f["price"] - l["price"] - RT
        shrink.append((nm, gap, gap2))
        trs += (f'<tr><td><b>{nm}</b></td>'
                f'<td class="dim">{money(l["price"])}</td>'
                f'<td>{money(l["price"] + RT)}</td>'
                f'<td class="dim">{money(f["price"])}</td>'
                f'<td class="drop">{money(gap)} → <b>{money(gap2)}</b></td></tr>')
    worst = max(shrink, key=lambda x: (x[1] - x[2]) / x[1])
    shot("02_shrink", head_html("") + f'''<div class="mid">
<div class="ttl">加上行李之後，<br>價差縮水多少？</div>
<div class="note">廉航最低票價 ＋ 來回 {REF["kg"]}kg 託運（{money(RT)}），
對照一般航空最低票價</div>
<table><colgroup><col style="width:14%"><col style="width:20%"><col style="width:20%">
<col style="width:20%"><col style="width:26%"></colgroup>
<thead><tr><th>航點</th><th>廉航</th><th>＋行李</th><th>一般航空</th><th>價差變化</th>
</tr></thead><tbody>{trs}</tbody></table>
<div class="kick">{worst[0]}的價差從 {money(worst[1])} 縮到 {money(worst[2])}——
少了 {(worst[1]-worst[2])/worst[1]*100:.0f}%</div>
<div class="unit">行李費以{html.escape(REF["airline"])}公告的 {REF["kg"]}kg 訂票時加購價估算，
各航空不同　·　兩邊都是本站紀錄中的最低價，不是市場最低</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 越晚買越貴 ─────────────────────────────────────
    trs = ""
    for r in TG["rows"]:
        cells = ''.join((f'<td>{money(v)}</td>' if v else '<td class="dim">—</td>')
                        for v in r[1:])
        trs += f'<tr><td><b>{html.escape(r[0])}</b></td>{cells}</tr>'
    r20 = TG["rows"][1]; r15 = TG["rows"][0]; rap = TG["rows"][6]
    shot("03_timing", head_html("") + f'''<div class="mid">
<div class="ttl">行李費，越晚買越貴</div>
<div class="note">{html.escape(REF["airline"])}官方價目表。同樣的重量，
買的時機不同，價格差很多</div>
<table><colgroup><col style="width:32%"><col style="width:17%"><col style="width:17%">
<col style="width:17%"><col style="width:17%"></colgroup>
<thead><tr><th>項目</th>''' + ''.join(f'<th>{html.escape(c)}</th>' for c in TG["cols"]) + f'''
</tr></thead><tbody>{trs}</tbody></table>
<div class="kick">機場才買只能買 15 公斤，要 {money(rap[4])}——
比訂票時買同樣 15 公斤（{money(r15[1])}）貴了將近一倍</div>
<div class="unit">{html.escape(TG["period"])}　·　超重另按每公斤 {money(TG["over_kg"])} 收取<br>
出處：{html.escape(TG["src_name"])}，查證於 {BG["checked"]}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 4 哪些票種含託運 ─────────────────────────────────
    trs = ''.join(
        f'<tr><td><b>{html.escape(f["airline"])}</b>'
        f'<i>{"廉航" if f["cls"] == "lcc" else "一般航空"}</i></td>'
        f'<td class="dim">{html.escape(f["note"])}</td></tr>' for f in BG["fares"])
    shot("04_fares", head_html("") + f'''<div class="mid">
<div class="ttl">買全服務航空<br>就不用擔心行李？</div>
<div class="note">不一定。免費額度常常綁在「訂位艙等」上，促銷票和一般經濟艙可能不同</div>
<table><colgroup><col style="width:28%"><col style="width:72%"></colgroup>
<thead><tr><th>航空公司</th><th>託運行李</th></tr></thead><tbody>{trs}</tbody></table>
<div class="kick">不管買哪一種，訂票前都要看清楚「你買的那個艙等」含多少行李</div>
<div class="unit">只列出本站逐項對過官方頁面的 {len(BG["fares"])} 家。
其餘 {len(BG["unverified"])} 家尚未查證，與其抄第三方整理，不如先空著</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 5 重點 ───────────────────────────────────────────
    shot("05_end", head_html(END) + f'''<div class="mid">
<div class="h">訂廉航之前<br>先想好行李</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>最低票價不含託運</b><br>
  那是「只能帶手提」的價格。要帶行李箱，來回 {REF["kg"]}kg 約 {money(RT)}</div></div>
 <div class="pt"><i>2</i><div><b>訂票時就買最便宜</b><br>
  {REF["kg"]}kg 訂票時 {money(r20[1])}，事後線上 {money(r20[2])}，打客服 {money(r20[3])}</div></div>
 <div class="pt"><i>3</i><div><b>機場才買最貴</b><br>
  只能買 15 公斤且要 {money(rap[4])}，比訂票時買同樣重量貴近一倍</div></div>
 <div class="pt"><i>4</i><div><b>超重比加購貴得多</b><br>
  每公斤 {money(TG["over_kg"])}，超個 3 公斤就超過一整張 {REF["kg"]}kg 行李的錢</div></div>
 <div class="pt"><i>5</i><div><b>全服務航空也要看艙等</b><br>
  免費件數依航線與訂位艙等而定，最便宜的促銷票不一定含兩件</div></div>
</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    L = site
    posts = [
     ("01_cover", f"""{money(l0["price"])} 的{nm0}來回機票——不能帶行李箱。

廉航的最低票價不含託運行李，那是「只能帶手提」的價格。

要帶一個行李箱，加購來回 {REF["kg"]}kg 大約 {money(RT)}，實際是 {money(l0["price"] + RT)}。

這不是什麼陷阱，是廉航的商業模式：把行李、選位、餐食拆開來賣，讓帳面票價看起來最低。

問題在於，大家比價的時候只比了帳面那個數字。

要比，就要比含行李之後的價格。

{L}"""),
     ("02_shrink", f"""「廉航便宜好幾千」——把行李費加回去之後呢？

用本站的即時票價實際算（廉航最低 ＋ 來回 {REF["kg"]}kg 託運 {money(RT)}，對照一般航空最低）：

""" + "\n".join(f"・{nm}　價差 {money(g1)} → {money(g2)}" for nm, g1, g2 in shrink) + f"""

{worst[0]}縮得最兇，少了 {(worst[1]-worst[2])/worst[1]*100:.0f}%。

廉航還是比較便宜，只是沒有帳面上看起來那麼多。如果你本來就只帶手提行李，那廉航的優勢是完整的；要托運，這筆錢一定要算進去。

{L}"""),
     ("03_timing", f"""同一件 {REF["kg"]}kg 託運行李，你什麼時候買，價格差很多。

以{REF["airline"]}公告的費率：

・訂機票時一起買　{money(r20[1])}
・事後到行程管理加購　{money(r20[2])}
・打客服專線　{money(r20[3])}
・機場櫃檯　只能買 15 公斤，{money(rap[4])}

機場才買 15 公斤要 {money(rap[4])}，訂票時買同樣 15 公斤只要 {money(r15[1])}——貴了將近一倍。

超重更狠：每公斤 {money(TG["over_kg"])}。超個 3 公斤，就超過一整張 {REF["kg"]}kg 行李的錢。

訂票那一刻就把重量買足，是最省的做法。

{TG["period"]}
出處：{TG["src_name"]}
{L}"""),
     ("04_fares", f"""「買全服務航空就不用擔心行李」——不一定。

中華航空官網寫明：經濟艙的免費託運件數，依航線與「訂位艙等」而定。最便宜的促銷艙等，和一般經濟艙可能不一樣。

廉航這邊也一樣要看票種：
・台灣虎航：基本票種 tigerlight 不含託運，只有手提 10 公斤
・樂桃：Minimum 不含託運，Standard 與 Standard Plus 各含 1 件

不管買哪一種，訂票前都要確認「你買的那個艙等／票種」實際含多少行李。

本站只列出逐項對過官方頁面的 {len(BG["fares"])} 家，其餘 {len(BG["unverified"])} 家還沒查證就先空著。

{L}"""),
     ("05_end", f"""訂廉航之前，先想好行李：

1　最低票價不含託運
那是「只能帶手提」的價格，來回 {REF["kg"]}kg 約 {money(RT)}

2　訂票時就買最便宜
{REF["kg"]}kg 訂票時 {money(r20[1])}，事後線上 {money(r20[2])}，打客服 {money(r20[3])}

3　機場才買最貴
只能買 15 公斤且要 {money(rap[4])}

4　超重比加購貴得多
每公斤 {money(TG["over_kg"])}，超 3 公斤就超過一整張行李的錢

5　全服務航空也要看艙等
免費件數依訂位艙等而定，促銷票不一定含兩件

{L}"""),
    ]
    os.makedirs("posts", exist_ok=True)
    pf = "posts/japan-baggage.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write(f"廉航行李費圖卡文案（{BG['checked']} 產生）\n每張圖各自獨立，可分開發\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n" + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
