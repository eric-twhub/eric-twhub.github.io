# -*- coding: utf-8 -*-
"""旅日信用卡圖卡（1080×1350）。

資料同 /japan-credit-card/（cards.json），不另外維護一份數字。
每張都設計成可以單獨發：不編頁碼、標題自帶鉤子、結論寫在卡上。

用法：python3 make_card_cards.py
輸出：cards/card/01_fx.png … 06_end.png ＋ posts/japan-card.txt
"""
import os, sys, json, html, subprocess

W, H = 1080, 1350
OUT = "cards/card"


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
    CD = json.load(open("cards.json", encoding="utf-8"))
    AP = json.load(open("apple.json", encoding="utf-8"))
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/japan-credit-card/"
    cards = CD["cards"]
    FX = CD["fx_fee"]["typical"]
    MID = AP["rate"].get("jpy_twd_mid") or AP["rate"]["jpy_twd"]
    MP = CD["mpay"]; BOT = MP["bot"]

    def money(n): return f"NT${round(n):,}"
    def bill(jpy): return jpy * MID * (1 + FX / 100)

    def tiers(c, mode):
        return [t for t in c["tiers"] if t["scope"] == mode or t["scope"] == "any"]

    def back(c, jpy, mode="shop"):
        b = bill(jpy); v = c["base"] / 100 * b
        for t in tiers(c, mode):
            x = t["rate"] / 100 * b
            v += min(x, t["cap"]) if t["cap"] else x
        return v

    def hit(c, mode="shop"):
        ts = [t for t in tiers(c, mode) if t["cap"]]
        return round(min(t["cap"] / (t["rate"] / 100) for t in ts)) if ts else 0

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".card_tmp.html"); made = []; CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                        f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png): made.append(fn)

    # ── 1 匯率：免手續費實際省多少 ─────────────────────────
    mid = (BOT["spot_buy"] + BOT["spot_sell"]) / 2
    c_spot = (BOT["spot_sell"] / mid - 1) * 100
    c_cash = (BOT["cash_sell"] / mid - 1) * 100
    save = FX - c_spot
    lo, hi = min(c["total"] for c in cards), max(c["total"] for c in cards)
    shot("01_fx", head_html(COVER) + f'''<div class="mid">
<div class="q">「電支免 {FX}%<br>海外手續費」</div>
<div class="a">實際只省 {save:.1f} 個百分點</div>
<div class="cmp">
 <div><b>電支・即期賣出</b><u>＋{c_spot:.2f}%</u><s>{BOT["spot_sell"]}</s></div>
 <div><b>信用卡・含手續費</b><u>＋{FX:.2f}%</u><s>卡組織匯率＋{FX}%</s></div>
</div>
<div class="sub">因為電支的換匯用的是銀行牌告<b>賣出價</b>，本身就比即期中價
（{mid:.4f}）高 {c_spot:.2f}%。大家只比有沒有收手續費，沒比換匯用哪個價。</div>
<div class="swipe">臺灣銀行牌告匯率・{BOT["date"]} 查詢</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 三種付款方式的實際成本 ──────────────────────────
    rows = (f'<tr><td><b>電支</b><i>用即期賣出價</i></td><td class="dim">{BOT["spot_sell"]}</td>'
            f'<td class="keep">＋{c_spot:.2f}%</td></tr>'
            f'<tr><td><b>信用卡</b><i>卡組織匯率 ＋ {FX}% 手續費</i></td><td class="dim">—</td>'
            f'<td>＋{FX:.2f}%</td></tr>'
            f'<tr><td><b>電支</b><i>用現金賣出價</i></td><td class="dim">{BOT["cash_sell"]}</td>'
            f'<td class="drop">＋{c_cash:.2f}%</td></tr>')
    shot("02_cost", head_html("") + f'''<div class="mid">
<div class="ttl">哪一種付款最便宜？</div>
<div class="note">把換匯與手續費一起算，換成「相對即期中價（{mid:.4f}）的成本」</div>
<table><colgroup><col style="width:50%"><col style="width:25%"><col style="width:25%"></colgroup>
<thead><tr><th>付款方式</th><th>今日匯率</th><th>成本</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="kick">用現金賣出價的那幾家，成本比信用卡還高 {abs(FX - c_cash):.2f} 個百分點——
免了手續費，卻在匯率上輸回去</div>
<div class="unit">臺灣銀行牌告匯率，{BOT["date"]} 查詢　·　
卡組織匯率無法事先查詢，此處假設約等於即期中價</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 疊加？其實是二選一 ──────────────────────────────
    rows = ''.join(
        f'<tr><td><b>{html.escape(a["name"])}</b></td>'
        + (f'<td class="keep">可綁指定卡</td>' if a["card"] else '<td class="drop">不能綁卡</td>')
        + f'<td class="dim">{html.escape(a["card_note"])}</td></tr>' for a in MP["apps"])
    n_no = sum(1 for a in MP["apps"] if not a["card"])
    shot("03_stack", head_html("") + f'''<div class="mid">
<div class="ttl">「行動支付疊加回饋」<br>其實疊不起來</div>
<div class="note">{len(MP["apps"])} 家台灣電支裡，有 {n_no} 家在境外根本不收信用卡</div>
<table><colgroup><col style="width:26%"><col style="width:22%"><col style="width:52%"></colgroup>
<thead><tr><th>電子支付</th><th>境外綁卡</th><th>可用的付款來源</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="kick">走電支＝放棄你那張卡的海外加碼。
省下零點幾個百分點，放棄好幾個百分點</div>
<div class="unit">查證於 {MP["checked"]}　·　街口一列有實測報導佐證，其餘為第三方整理</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 4 刷到多少就到頂 ─────────────────────────────────
    top = sorted(cards, key=lambda c: -c["total"])[:8]
    rows = ''.join(
        f'<tr><td><b>{html.escape(c["name"])}</b></td><td class="keep">{c["total"]}%</td>'
        + (f'<td>{money(hit(c))}</td>' if hit(c) else '<td class="dim">無上限</td>')
        + f'<td class="dim">{c["base"]}%</td></tr>' for c in top)
    shot("04_caps", head_html("") + f'''<div class="mid">
<div class="ttl">刷到多少，加碼就沒了？</div>
<div class="note">帳面回饋都是多層加碼疊出來的，而且各有上限。
真正該看的是「刷到多少到頂」</div>
<table><colgroup><col style="width:42%"><col style="width:16%">
<col style="width:24%"><col style="width:18%"></colgroup>
<thead><tr><th>卡片</th><th>帳面最高</th><th>刷到這裡到頂</th><th>之後只剩</th>
</tr></thead><tbody>{rows}</tbody></table>
<div class="kick">買一支 iPhone，多數卡的加碼第一筆就用完</div>
<div class="unit">單位為台幣帳單金額　·　查證於 {CD["checked"]}，共收錄 {len(cards)} 張卡</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 5 11/1 免稅新制之後，回饋會變多嗎 ────────────────
    Y = 100000; Y2 = round(Y * 1.1)
    ds = []
    rows = ''
    for c in sorted(cards, key=lambda x: -x["total"])[:6]:
        o, n = round(back(c, Y)), round(back(c, Y2))
        ds.append(n - o)
        rows += (f'<tr><td><b>{html.escape(c["name"])}</b></td>'
                 f'<td class="dim">{money(o)}</td><td>{money(n)}</td>'
                 f'<td class="keep">＋{money(n-o)}</td></tr>')
    prepaid = round(bill(Y2) - bill(Y))
    shot("05_taxfree", head_html("") + f'''<div class="mid">
<div class="ttl">11/1 之後刷含稅價，<br>回饋會變多嗎？</div>
<div class="note">免稅改成出境後才退，店裡要先付含稅全額。
同一件稅前 ¥{Y:,} 的商品，刷的金額變成 ¥{Y2:,}</div>
<table><colgroup><col style="width:40%"><col style="width:20%">
<col style="width:20%"><col style="width:20%"></colgroup>
<thead><tr><th>卡片</th><th>刷 ¥{Y:,}</th><th>刷 ¥{Y2:,}</th><th>差額</th>
</tr></thead><tbody>{rows}</tbody></table>
<div class="kick">多拿 {money(min(ds))}～{money(max(ds))}，
卻要先墊 {money(prepaid)} 的稅金等出境才拿得回來</div>
<div class="unit">加碼多半早就觸頂，多刷的 10% 只算得到基本回饋　·　
匯率 {MID} 並加計 {FX}% 國外交易手續費</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 6 重點 ───────────────────────────────────────────
    best = max(cards, key=lambda c: c["total"])
    shot("06_end", head_html(END) + f'''<div class="mid">
<div class="h">在日本刷卡<br>五個常被搞錯的點</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>帳面最高回饋幾乎拿不到</b><br>
  {html.escape(best["name"])} 的 {best["total"]}% 是多層加碼全部成立的數字，每層各有條件與上限</div></div>
 <div class="pt"><i>2</i><div><b>看「刷到多少到頂」比看%重要</b><br>
  加碼上限換算下來多半是一萬多元，買一支 iPhone 第一筆就用完</div></div>
 <div class="pt"><i>3</i><div><b>電支免手續費只省 {save:.1f} 個百分點</b><br>
  換匯用的是銀行牌告賣出價，本身就含價差</div></div>
 <div class="pt"><i>4</i><div><b>電支多半不能綁卡</b><br>
  {n_no}／{len(MP["apps"])} 家境外只收銀行帳戶，走電支就拿不到卡的海外加碼</div></div>
 <div class="pt"><i>5</i><div><b>結帳一律選日圓</b><br>
  選台幣是 DCC，匯率通常差 3–5%，而且多數海外加碼要求以外幣結帳</div></div>
</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    L = site
    posts = [
     ("01_fx", f"""「用台灣的電支在日本付款，免 {FX}% 海外交易手續費。」

這句話沒錯，但省下來的比你以為的少很多。

因為大家只比「有沒有收手續費」，沒比「換匯用哪個價」。電支是用銀行牌告的賣出價換匯，那個價本身就含價差。

以 {BOT["date"]} 臺灣銀行牌告（即期中價 {mid:.4f}）換算成實際成本：

・電支（即期賣出 {BOT["spot_sell"]}）　＋{c_spot:.2f}%
・信用卡（卡組織匯率＋{FX}%）　＋{FX:.2f}%
・電支（現金賣出 {BOT["cash_sell"]}）　＋{c_cash:.2f}%

免手續費實際只省 {save:.1f} 個百分點。而用現金賣出價的那幾家，成本比信用卡還高。

完整比較：
{L}"""),
     ("02_cost", f"""在日本付款，哪一種最便宜？

把換匯和手續費一起算，全部換成「相對即期中價的成本」才比得出來：

・電支（即期賣出）　＋{c_spot:.2f}%
・信用卡　＋{FX:.2f}%
・電支（現金賣出）　＋{c_cash:.2f}%

用現金賣出價的電支，成本比刷卡還高 {abs(FX - c_cash):.2f} 個百分點——免了手續費，在匯率上輸回去。

但這些都是零點幾個百分點的事。真正的差距在回饋：旅日信用卡的海外加碼是 {lo}%～{hi}%，大一個量級。

所以別為了免手續費放棄海外加碼。

{L}"""),
     ("03_stack", f"""「行動支付疊加信用卡回饋」——多數情況疊不起來。

台灣有 {len(MP["apps"])} 家電支可以在日本的 PayPay 特約店掃碼，其中 {n_no} 家在境外根本不收信用卡：

・街口支付：只能用街口帳戶或銀行帳戶
・全盈+Pay、一卡通：只能綁銀行帳戶
・全支付、玉山 Wallet、台新 Pay+：可綁指定卡

所以這不是疊加，是二選一。走電支就等於放棄那張卡的海外加碼。

省下零點幾個百分點的手續費，放棄好幾個百分點的回饋——大額消費幾乎一定是刷卡贏。

{L}"""),
     ("04_caps", f"""看到「日本最高回饋 {best["total"]}%」先別急。

那是多層加碼全部同時成立的數字，而且每一層各有上限。真正該問的是：**刷到多少，加碼就沒了？**

換算成台幣帳單金額，多數卡的加碼上限落在一萬多元。買一支 iPhone，第一筆就用完，之後只剩基本回饋。

本站把 {len(cards)} 張旅日卡的上限全部換算成「刷到多少到頂」，附發卡行官方來源，查證於 {CD["checked"]}。

{L}"""),
     ("05_taxfree", f"""11/1 起日本免稅改成「出境後才退錢」，店裡要先付含稅全額。

刷的金額多了 10%，回饋基數跟著變大——聽起來是好事？算給你看。

同一件稅前 ¥{Y:,} 的商品，回饋最高的 6 張卡多拿到的是 {money(min(ds))}～{money(max(ds))}。

而你要先墊 {money(prepaid)} 的稅金，等出境經海關確認後才拿得回來。

為什麼差這麼少？因為加碼多半早就觸頂了，多刷的那 10% 只算得到基本回饋。

還有兩點沒人講：加碼上限是台幣金額不會變，含稅後同樣額度只夠買原本約 91% 的東西；而退稅如果選擇退回原卡，回饋還可能被回沖。

{L}"""),
     ("06_end", f"""在日本刷卡，五個常被搞錯的點：

1　帳面最高回饋幾乎拿不到
{best["name"]} 的 {best["total"]}% 是多層加碼全部成立的數字

2　看「刷到多少到頂」比看 % 重要
加碼上限換算下來多半是一萬多元

3　電支免手續費只省 {save:.1f} 個百分點
換匯用的是銀行牌告賣出價，本身就含價差

4　電支多半不能綁卡
{n_no}／{len(MP["apps"])} 家境外只收銀行帳戶

5　結帳一律選日圓
選台幣是 DCC，匯率通常差 3–5%

{len(cards)} 張卡的完整比較與試算：
{L}"""),
    ]
    os.makedirs("posts", exist_ok=True)
    pf = "posts/japan-card.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write(f"旅日信用卡圖卡文案（{CD['checked']} 產生）\n每張圖各自獨立，可分開發\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n" + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    for f in made: print("   ", f + ".png")


if __name__ == "__main__":
    main()
