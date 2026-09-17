# -*- coding: utf-8 -*-
"""雪具託運圖卡（1080×1350）。

資料同 /japan-ski-baggage/（ski.json），每張可單獨發。

刻意不放票價：這組是冬季前就要發的規則卡，票價會過期而規則不會。
要配票價請另外用當天的 posts/YYYY-MM-DD.txt，並先在 Trip.com 對過。

用法：python3 make_ski_cards.py
輸出：cards/ski/01_cover.png … 05_end.png ＋ posts/japan-ski.txt
"""
import os, sys, json, html, subprocess

W, H = 1080, 1350
OUT = "cards/ski"
BAG = "150–170"          # 市售雪板袋常見長度，頁面與圖卡共用同一組說法


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
body{background:#0f1417;color:#f2f5f6;
 font-family:"PingFang TC","Noto Sans TC","Noto Sans CJK TC",
 "Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:70px 68px 60px;position:relative;overflow:hidden}
.glow{position:absolute;width:820px;height:820px;border-radius:50%%;
 background:radial-gradient(circle,rgba(56,189,248,.16),transparent 68%%);top:-330px;right:-290px}
.brand{font-size:25px;letter-spacing:.3em;color:#38bdf8;font-weight:700}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.site{font-size:27px;color:#38bdf8;font-weight:700;margin-top:auto}
.ttl{font-size:54px;font-weight:800;letter-spacing:-.02em;line-height:1.2}
.note{margin-top:14px;font-size:28px;color:#9aa5ab;line-height:1.5}
.unit{margin-top:22px;font-size:23px;color:#5a646a;line-height:1.55}
table{width:100%%;border-collapse:collapse;margin-top:34px;table-layout:fixed;
 font-variant-numeric:tabular-nums;font-feature-settings:"tnum"}
th{font-size:22px;color:#77828a;font-weight:600;text-align:right;
 padding:0 0 16px;line-height:1.35}
th:first-child{text-align:left}
td{font-size:29px;font-weight:700;text-align:right;padding:15px 0;
 border-top:1px solid rgba(255,255,255,.09)}
td:first-child{text-align:left;font-size:25px;color:#c4ccd1;font-weight:600;line-height:1.3}
td:first-child i{display:block;font-style:normal;font-size:20px;color:#7d878e;
 font-weight:500;margin-top:3px}
td.dim{color:#98a1a7;font-weight:600;font-size:26px}
td.na{color:#5a646a;font-weight:600;font-size:25px}
td.tight{color:#38bdf8}
td.roomy{color:#34d399}
td small{display:block;font-size:19px;color:#7d878e;font-weight:500;margin-top:3px}
/* 九列的表格：行高與字級縮一階才進得了 1350px */
.dense .ttl{font-size:48px}
.dense .note{font-size:26px;margin-top:12px}
.dense table{margin-top:22px}
.dense th{font-size:21px;padding-bottom:12px}
.dense td{font-size:27px;padding:7px 0}
.dense td:first-child{font-size:23px}
.dense td:first-child i{font-size:18px;margin-top:2px}
.dense td.dim{font-size:24px}
.dense td.na{font-size:23px}
.dense td small{font-size:18px}
.dense .unit{font-size:21px;margin-top:18px}
/* 單張獨立發時，結論要寫在卡上，不能靠下一張補 */
.kick{margin-top:24px;padding:22px 26px;border-radius:16px;
 background:rgba(56,189,248,.14);color:#38bdf8;
 font-size:29px;font-weight:800;line-height:1.45}
.dense .kick{margin-top:20px;font-size:27px;padding:18px 24px}
"""% (W, H)

COVER = """
.q{font-size:74px;font-weight:800;line-height:1.2;letter-spacing:-.02em}
.a{margin-top:38px;font-size:54px;font-weight:800;color:#38bdf8;line-height:1.28}
.cmp{margin-top:36px;display:flex;gap:18px}
.cmp div{flex:1;background:rgba(255,255,255,.05);border-radius:16px;padding:24px 26px}
.cmp b{display:block;font-size:26px;color:#9aa5ab;font-weight:600}
.cmp u{display:block;text-decoration:none;font-size:52px;font-weight:800;margin-top:10px;
 letter-spacing:-.02em}
.cmp s{text-decoration:none;display:block;font-size:22px;color:#69737a;margin-top:8px}
.sub{margin-top:30px;font-size:31px;color:#9aa5ab;line-height:1.55}
.sub b{color:#f2f5f6;font-weight:700}
.swipe{margin-top:36px;font-size:29px;color:#5a646a}
"""

TRAPS = """
.pts{margin-top:38px;display:flex;flex-direction:column;gap:26px}
.pt{background:rgba(255,255,255,.05);border-radius:18px;padding:28px 30px}
.pt b{display:block;font-size:34px;font-weight:800;line-height:1.35}
.pt s{text-decoration:none;display:block;margin-top:12px;font-size:27px;
 color:#9aa5ab;line-height:1.5}
.pt i{font-style:normal;color:#38bdf8;font-weight:800;margin-right:10px}
"""

END = """
.h{font-size:62px;font-weight:800;line-height:1.24;letter-spacing:-.02em}
.pts{margin-top:36px;display:flex;flex-direction:column;gap:20px}
.pt{display:flex;gap:18px;align-items:flex-start;font-size:29px;line-height:1.5}
.pt i{color:#38bdf8;font-style:normal;font-weight:800;flex:0 0 auto}
.pt b{font-weight:700}
"""


def head_html(css, cls=""):
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{BASE}{css}</style></head><body class="{cls}">'
            f'<div class="glow"></div><div class="brand">台日機票速報</div>')


def main():
    SK = json.load(open("ski.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/japan-ski-baggage/"
    AL, TR, CK = SK["airlines"], SK["traps"], SK["checked"]

    def by(n): return next(a for a in AL if a["name"] == n)

    # 門檻低於一般板袋長度的那幾家，是整組圖卡的主角
    tight = sorted([a for a in AL if a["side_cm"] and a["side_cm"] < 150],
                   key=lambda a: a["side_cm"])
    roomy = [a for a in AL if a["side_cm"] and a["side_cm"] >= 150]
    low = tight[0]
    assert tight and roomy, "ski.json 的 side_cm 分布有變，圖卡文案要重寫"

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".ski_tmp.html"); made = []; CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    # ── 1 封面：卡住你的是長度，不是重量 ───────────────────
    shot("01_cover", head_html(COVER) + f'''<div class="mid">
<div class="q">雪板被拒載，<br>多半不是因為太重</div>
<div class="a">是因為單邊太長</div>
<div class="cmp">
 <div><b>你的雪板袋</b><u>{BAG}</u><s>市售板袋常見長度（公分）</s></div>
 <div><b>{html.escape(low["name"])}的門檻</b><u style="color:#38bdf8">{low["side_cm"]}</u>
  <s>{html.escape(low["side_short"])}（公分）</s></div>
</div>
<div class="sub">{len(AL)} 家航空裡，有 {len(tight)} 家的單邊門檻低於板袋長度。
<b>多數人只記得加購重量，結果被長度卡住。</b></div>
<div class="swipe">九家官網條款逐項查證於 {CK}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 九家單邊長度對照 ───────────────────────────────
    order = (sorted([a for a in AL if a["side_cm"]], key=lambda a: a["side_cm"])
             + sorted([a for a in AL if not a["side_cm"]], key=lambda a: a["total_cm"] or 0))
    trs = ""
    for a in order:
        if a["side_cm"]:
            cls = "roomy" if a["side_cm"] >= 150 else "tight"
            cell = (f'<td class="{cls}">{a["side_cm"]} 公分'
                    f'<small>{html.escape(a.get("side_short", ""))}</small></td>')
        else:
            cell = '<td class="na">未列</td>'
        # 203 是業界通例，低於它的（酷航 158）是自成一格的坑，要標出來
        tcls = "tight" if (a["total_cm"] or 999) < 203 else "dim"
        trs += (f'<tr><td><b>{html.escape(a["name"])}</b>'
                f'<i>{"廉航" if a["cls"] == "lcc" else "一般航空"}</i></td>'
                f'<td class="{tcls}">{a["total_cm"] or "—"}</td>{cell}</tr>')
    shot("02_sides", head_html("", "dense") + f'''<div class="mid">
<div class="ttl">九家航空的<br>單邊長度門檻</div>
<div class="note">由低到高。市售雪板袋多半 {BAG} 公分，比一比就知道誰會卡住你</div>
<table><colgroup><col style="width:34%"><col style="width:22%"><col style="width:44%">
</colgroup><thead><tr><th>航空公司</th><th>總尺寸（公分）</th><th>單邊長度上限</th>
</tr></thead><tbody>{trs}</tbody></table>
<div class="kick">裝得下 {BAG} 公分板袋、又不必先打電話的，九家裡只有{html.escape(roomy[0]["name"])}</div>
<div class="unit">總尺寸為長＋寬＋高。「未列」是官網沒有單獨的單邊限制，改以總尺寸計費——
酷航的 158 公分是本表最緊的總尺寸，一片 160 公分的板單邊就超了<br>
逐項對過各航空官網原文，查證於 {CK}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 三個會多付錢的地方 ─────────────────────────────
    pts = ''.join(
        f'<div class="pt"><b><i>{i}</i>{html.escape(t["title"])}</b>'
        f'<s>{html.escape(t["short"])}<br>依據：{html.escape(t["who"])}官網條款</s></div>'
        for i, t in enumerate(TR, 1))
    shot("03_traps", head_html(TRAPS) + f'''<div class="mid">
<div class="ttl">三個會讓你<br>多付錢的地方</div>
<div class="note">尺寸過了還是可能被加錢，而且三條都寫在官網條款裡</div>
{pts}</div>
<div class="site">{site}</div></body></html>''')

    # ── 4 誰要先打電話、誰要另外付錢 ─────────────────────
    trs = ''.join(
        f'<tr><td><b>{html.escape(a["name"])}</b>'
        f'<i>{"廉航" if a["cls"] == "lcc" else "一般航空"}</i></td>'
        f'<td class="dim">{html.escape(a["call_short"])}</td>'
        f'<td class="dim">{html.escape(a["fee_short"])}'
        + (f'<small>{html.escape(a["fee_note"])}</small>' if a.get("fee_note") else '')
        + '</td></tr>' for a in AL)
    pay = [a for a in AL if a.get("fee_note")]
    shot("04_call", head_html("", "dense") + f'''<div class="mid">
<div class="ttl">要先打電話嗎？<br>要另外付錢嗎？</div>
<div class="note">雪具多半計入你原本的託運額度，但有兩家是另外一筆錢</div>
<table><colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%">
</colgroup><thead><tr><th>航空公司</th><th>事先申請</th><th>超尺寸的錢</th>
</tr></thead><tbody>{trs}</tbody></table>
<div class="kick">{"、".join(html.escape(a["name"]) for a in pay)}的超尺寸費是託運額度以外的錢——
買足重量還是要再付一筆</div>
<div class="unit">沒先問而現場被拒載，機票錢不會退給你<br>
逐項對過各航空官網原文，查證於 {CK}</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 5 重點 ───────────────────────────────────────────
    shot("05_end", head_html(END) + f'''<div class="mid">
<div class="h">訂雪季機票前<br>先確認這五件事</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>先量板袋，再看重量</b><br>
  板袋多半 {BAG} 公分，而 {len(tight)} 家的單邊門檻在這之下，最低只有 {low["side_cm"]} 公分</div></div>
 <div class="pt"><i>2</i><div><b>雪具通常計入原本的額度</b><br>
  不是另外一筆——但捷星日本與樂桃的超尺寸費是額度以外再付</div></div>
 <div class="pt"><i>3</i><div><b>板袋裡不要塞雪衣</b><br>
  長榮與華航都寫明，內含非運動用品時整袋視為一般行李加收超尺寸費</div></div>
 <div class="pt"><i>4</i><div><b>板、靴、杖裝在同一個袋子</b><br>
  全日空明寫分開包裝會各自計一次超額費，華航則依實際件數收費</div></div>
 <div class="pt"><i>5</i><div><b>要先申請的，趁訂票就問</b><br>
  星宇起飛前 24 小時、長榮 48 小時；沒先問而被拒載，機票錢不會退</div></div>
</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    L, mm, gk = site, by("樂桃航空"), by("捷星日本")
    tl = "\n".join(f"・{a['name']}　{a['side_cm']} 公分（{a['side_short']}）" for a in tight)
    posts = [
     ("01_cover", f"""雪板被航空公司拒載，多半不是因為太重，是因為單邊太長。

市售雪板袋常見長度是 {BAG} 公分。而各家的單邊門檻：

{tl}

九家裡有 {len(tight)} 家的門檻低於板袋長度。

多數人加購行李時只盯著重量，20 公斤、30 公斤買好買滿，然後在櫃檯被長度卡住。

規則都寫在官網，只是沒人會特地去看。

九家條款逐項查證於 {CK}
{L}"""),
     ("02_sides", f"""帶雪具飛日本，九家航空的單邊長度門檻（由低到高）：

""" + "\n".join(
        (f"・{a['name']}　{a['side_cm']} 公分（{a['side_short']}）" if a["side_cm"]
         else f"・{a['name']}　未列單邊限制，總尺寸 {a['total_cm']} 公分")
        for a in order) + f"""

市售板袋 {BAG} 公分。裝得下又不必先打電話的，九家裡只有{roomy[0]['name']}——它的深度上限是 {roomy[0]['side_cm']} 公分。

{low['name']}那條最容易漏掉：{low['side_short']}時單邊只有 {low['side_cm']} 公分，比廉航還低。

「未列」不等於沒限制，是官網沒有單獨的單邊條款，改以總尺寸計費。

逐項對過官網原文，查證於 {CK}
{L}"""),
     ("03_traps", f"""尺寸過了，還是可能被加錢。三個都寫在官網條款裡：

""" + "\n\n".join(f"{i}　{t['title']}\n{t['short']}（{t['who']}）"
                  for i, t in enumerate(TR, 1)) + f"""

第一條最多人中：板袋空間大，順手就把雪衣雪褲塞進去。長榮與華航的條款用詞幾乎一樣——內含非運動用物品，整袋視為一般行李。

板袋只放板、靴、杖，衣服放行李箱。

查證於 {CK}
{L}"""),
     ("04_call", f"""雪具要不要先打電話？要不要另外付錢？九家整理：

""" + "\n".join(
        f"・{a['name']}　{a['call_short']}｜{a['fee_short']}"
        + (f"（{a['fee_note']}）" if a.get("fee_note") else "") for a in AL) + f"""

大部分航空的雪具是「計入你原本買的託運額度」，不是另外一筆。

例外是{gk['name']}與{mm['name']}：超尺寸費是額度以外再付的錢。{gk['name']}寫得最白——這筆費用「不包括行李的重量，並且是託運行李限額以外支付的額外費用」。也就是說，你還得另外買足夠的重量。

要先申請的那幾家，趁訂票的時候一起問完。沒先問而現場被拒載，機票錢不會退給你。

查證於 {CK}
{L}"""),
     ("05_end", f"""訂雪季機票前，先確認這五件事：

1　先量板袋，再看重量
板袋多半 {BAG} 公分，{len(tight)} 家的單邊門檻在這之下，最低 {low['side_cm']} 公分

2　雪具通常計入原本的額度
不是另外一筆——但{gk['name']}與{mm['name']}的超尺寸費要額度以外再付

3　板袋裡不要塞雪衣
內含非運動用品時，整袋被視為一般行李加收超尺寸費

4　板、靴、杖裝在同一個袋子
分開包裝會各自計一次超額費

5　要先申請的，趁訂票就問
星宇起飛前 24 小時、長榮 48 小時，沒先問被拒載機票錢不退

雪季 12 月開始，但行李額度是訂票那一刻決定的。

九家條款逐項查證於 {CK}
{L}"""),
    ]
    os.makedirs("posts", exist_ok=True)
    pf = "posts/japan-ski.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write(f"雪具託運圖卡文案（{CK} 產生）\n每張圖各自獨立，可分開發\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n" + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
