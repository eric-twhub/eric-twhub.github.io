# -*- coding: utf-8 -*-
"""iPhone 持有成本圖卡（1080×1350）。

殘值不用假設：拿收購商今天的公開回收報價，除以該機種當年的
Apple 台灣官方售價，得到實際發生過的折舊，再攤成每月成本。

用法：python3 make_cost_cards.py [--fare 6049]
     --fare 省略時自 /tmp/scan_all.json 取台北飛東京最低來回價
每張都設計成可以單獨發：不編頁碼、標題自帶鉤子、結論寫在卡上，
脫離其他幾張也看得懂。文案另寫到 posts/iphone-cost.txt。

輸出：cards/cost/01_cover.png … 06_end.png ＋ posts/iphone-cost.txt
"""
import os, sys, json, html, datetime, subprocess

W, H = 1080, 1350
OUT = "cards/cost"
SCAN = "/tmp/scan_all.json"
TOKYO = {"TYO", "HND", "NRT"}
TPE = {"TPE", "TSA"}
REFCAP = ("256GB", "128GB", "512GB", "1TB")


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


def tokyo_fare():
    """台北飛東京最低來回含稅價；沒有票價快取時回 None，卡片就不提機票"""
    if not os.path.exists(SCAN):
        return None
    try:
        rows = json.load(open(SCAN, encoding="utf-8"))
    except Exception:
        return None
    ps = [r.get("price", 0) for r in rows
          if r.get("destination") in TOKYO and r.get("origin") in TPE
          and r.get("return_at") and r.get("price")]
    return min(ps) if ps else None


def main():
    fare = None
    if "--fare" in sys.argv:
        fare = int(sys.argv[sys.argv.index("--fare") + 1])
    if fare is None:
        fare = tokyo_fare()

    RS = json.load(open("resale.json", encoding="utf-8"))
    AP = json.load(open("apple.json", encoding="utf-8"))
    R = AP["rate"]["jpy_twd"]
    T = 1 + AP["tax"]["jp_consumption"]
    site = json.load(open("partners.json", encoding="utf-8"))["site"]["url"].rstrip("/") \
           + "/iphone-cost/"
    today = datetime.date.today()

    def money(n): return f"NT${n:,}"

    def yrs(launch):
        d = datetime.date(*map(int, launch.split("-")))
        return max(1, round((today - d).days / 365.25))

    # 殘值率一律取該世代的參考容量，避免不同年份落在不同容量上失去可比性
    RES = {}
    for r in RS["rows"]:
        caps = {c[0]: c for c in r["caps"]}
        spec = next(c for c in REFCAP if c in caps)
        _, lst, res = caps[spec]
        RES.setdefault(r["tier"], {})[yrs(r["launch"])] = {
            "rate": res / lst, "spec": spec, "name": r["name"],
            "launch": r["launch"], "list": lst, "resale": res}

    YRS = sorted({y for t in RES.values() for y in t})
    TIERS = [t for t in ("Pro Max", "Pro", "標準", "Air") if t in RES]

    def rate_of(t, y):
        s = RES.get(t, {}).get(y)
        return s["rate"] if s else None

    def tier_of(n):
        if n.endswith("Pro Max"): return "Pro Max"
        if n.endswith("Pro"): return "Pro"
        if n.endswith("Air"): return "Air"
        if n.replace("iPhone ", "").isdigit(): return "標準"
        return None

    def mcost(twd, t, y):
        rt = rate_of(t, y)
        if rt is None: return None
        keep = round(twd * rt)
        return {"keep": keep, "m": round((twd - keep) / (y * 12))}

    IPH = [p for p in AP["products"] if p["cat"] == "iPhone"]

    def pick(t, spec="256GB"):
        return next((p for p in IPH if p.get("new") and tier_of(p["name"]) == t
                     and p["spec"] == spec), None)

    P, PM = pick("Pro"), pick("Pro Max")

    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".cost_tmp.html")
    made = []
    CH = _chrome()

    def shot(fn, doc):
        open(tmp, "w", encoding="utf-8").write(doc)
        png = os.path.abspath(os.path.join(OUT, fn + ".png"))
        subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--no-sandbox", f"--screenshot={png}", f"--window-size={W},{H}",
                        "--force-device-scale-factor=1", "file://" + tmp],
                       capture_output=True, timeout=90)
        if os.path.exists(png):
            made.append(fn)

    TOTAL = 6
    # 第 2 張的鉤子：最高等級、有資料的最長年數，掉價的絕對金額最有感
    _ht = TIERS[0]
    hero = RES[_ht][max(y for y in RES[_ht] if y <= 3)]

    # ── 1 封面 ───────────────────────────────────────────
    a2, b2 = mcost(P["twd"], "Pro", 2), mcost(PM["twd"], "Pro Max", 2)
    a1c = mcost(P["twd"], "Pro", 1)
    d2 = abs(b2["m"] - a2["m"])
    shot("01_cover", head_html(COVER) + f'''<div class="mid">
<div class="q">iPhone 一個月<br>其實花你多少？</div>
<div class="a">Pro 和 Pro Max<br>每月只差 NT${d2:,}</div>
<div class="cmp">
 <div><b>{html.escape(P["name"])} {P["spec"]}</b><u>NT${a2["m"]:,}</u><s>每月・用兩年</s></div>
 <div><b>{html.escape(PM["name"])} {PM["spec"]}</b><u>NT${b2["m"]:,}</u><s>每月・用兩年</s></div>
</div>
<div class="sub">標價差 {money(PM["twd"] - P["twd"])}，
但 Pro Max 兩年後回收價高 {money(b2["keep"] - a2["keep"])}，<b>把差價吃掉了大半</b></div>
<div class="swipe">殘值不是假設值，是收購商今天的公開報價 ÷ 當年官方售價</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 2 各代實際折舊 ────────────────────────────────────
    rows = ""
    for t in TIERS:
        for y in sorted(RES.get(t, {})):
            d = RES[t][y]
            rows += (f'<tr><td>{html.escape(d["name"])}<i>{d["spec"]}・滿 {y} 年</i></td>'
                     f'<td class="dim">{d["list"]:,}</td>'
                     f'<td class="keep">{d["resale"]:,}</td>'
                     f'<td class="keep">{d["rate"] * 100:.0f}%</td>'
                     f'<td class="drop">−{d["list"] - d["resale"]:,}</td></tr>')
    shot("02_depre", head_html("") + f'''<div class="mid dense">
<div class="ttl">三年後，還值多少？</div>
<div class="note">{money(hero["list"])} 買的 {html.escape(hero["name"])}，
今天收購商收 {money(hero["resale"])}，只剩 {hero["rate"] * 100:.0f}%。<br>
以下是各代的當年官方售價，對照今天的公開回收報價。</div>
<table><colgroup><col style="width:34%"><col style="width:17%">
<col style="width:17%"><col style="width:13%"><col style="width:19%"></colgroup>
<thead><tr><th>機型</th><th>當年售價</th><th>今日回收</th><th>殘值</th><th>掉了</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="unit">單位 NT$　·　資料來源：{html.escape(RS["src_name"])}，查詢於 {RS["updated"]}<br>
每個世代取同一參考容量（優先 256GB）以利對照</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 3 殘值率速查 ──────────────────────────────────────
    def tone(v):
        if v is None: return "background:rgba(255,255,255,.03);color:#4a4642"
        if v >= .6: return "background:rgba(45,212,191,.16);color:#2dd4bf"
        if v >= .45: return "background:rgba(132,204,22,.13);color:#a3e635"
        if v >= .33: return "background:rgba(251,146,60,.15);color:#fb923c"
        return "background:rgba(239,68,68,.15);color:#f87171"

    cells = '<div class="hd l"></div>' + ''.join(f'<div class="hd">滿 {y} 年</div>' for y in YRS)
    for t in TIERS:
        cells += f'<div class="tr">{html.escape(t)}</div>'
        for y in YRS:
            v = rate_of(t, y)
            cells += (f'<div class="cell" style="{tone(v)}">{v * 100:.0f}%</div>' if v
                      else f'<div class="cell na" style="{tone(None)}">—</div>')
    shot("03_matrix", head_html(MATRIX % len(YRS)) + f'''<div class="mid">
<div class="ttl">幾年後還剩幾成？</div>
<div class="note">同一天查到的回收行情，依等級與上市年數整理</div>
<div class="grid">{cells}</div>
<div class="lg">兩件事很清楚：<b>等級越高掉價越慢</b>，而且<b>第一年掉最多</b>。<br>
掉最兇的不是最便宜的機型，是 iPhone Air：滿一年只剩 {rate_of("Air", 1) * 100:.0f}%，
同期 Pro Max 還有 {rate_of("Pro Max", 1) * 100:.0f}%。</div>
<div class="unit">「—」表示目前沒有滿該年數的同級機種可以對照</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 4 在售新機每月成本 ────────────────────────────────
    show = [p for p in IPH if tier_of(p["name"]) and p["spec"] in ("256GB", "512GB")]
    rows = ""
    for p in show:
        t = tier_of(p["name"])
        tds = ""
        for y in YRS:
            m = mcost(p["twd"], t, y)
            tds += f'<td>{m["m"]:,}</td>' if m else '<td class="dim">—</td>'
        rows += (f'<tr><td>{html.escape(p["name"])}<i>{p["spec"]}・{money(p["twd"])}</i></td>'
                 f'{tds}</tr>')
    nod = sorted({p["name"] for p in IPH if not tier_of(p["name"])})
    shot("04_monthly", head_html("") + f'''<div class="mid">
<div class="ttl">在售新機，每月多少？</div>
<div class="note">買價減掉估計回收價，再除以月數</div>
<table><colgroup><col style="width:36%">''' + ''.join(
        '<col style="width:16%">' for _ in YRS) + f'''</colgroup>
<thead><tr><th>機型</th>''' + ''.join(f'<th>用 {y} 年</th>' for y in YRS) + f'''</tr></thead>
<tbody>{rows}</tbody></table>
<div class="kick">用越久越便宜，但一年一換沒你想的貴：
{html.escape(P["name"])} 用一年每月 NT${a1c["m"]:,}，用兩年 NT${a2["m"]:,}</div>
<div class="unit">單位 NT$／月　·　同機型各容量套用同一殘值率，
但大容量實際掉得更兇，大容量那幾列偏樂觀<br>
{html.escape("、".join(nod))} 是全新形態，沒有可比的回收行情，無法推估</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 5 容量加價的殘值 ──────────────────────────────────
    rows, cap_hero = "", None
    for r in RS["rows"]:
        if len(r["caps"]) < 2:
            continue
        s0, l0, v0 = r["caps"][0]
        s1, l1, v1 = r["caps"][-1]
        up, back = l1 - l0, v1 - v0
        # 結論舉例挑加價殘值最慘的一列，且加價金額要夠大才有感
        if up >= 10000 and (cap_hero is None or back / up < cap_hero[5]):
            cap_hero = (r["name"], up, back, yrs(r["launch"]), s1, back / up, s0, v0 / l0)
        rows += (f'<tr><td>{html.escape(r["name"])}<i>{s0} → {s1}・滿 {yrs(r["launch"])} 年</i></td>'
                 f'<td class="dim">＋{up:,}</td><td class="keep">＋{back:,}</td>'
                 f'<td class="drop">{back / up * 100:.0f}%</td>'
                 f'<td class="dim">{v0 / l0 * 100:.0f}%</td></tr>')
    shot("05_capacity", head_html("") + f'''<div class="mid dense">
<div class="ttl">升級容量，最不保值</div>
<div class="note">多付的那筆錢，幾年後回收時還剩多少？</div>
<table><colgroup><col style="width:34%"><col style="width:17%">
<col style="width:17%"><col style="width:16%"><col style="width:16%"></colgroup>
<thead><tr><th>機型</th><th>當年多付</th><th>回收多拿</th>
<th>加價殘值</th><th>整機殘值</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="kick">{html.escape(cap_hero[0])} 多付 {money(cap_hero[1])} 升到 {cap_hero[4]}，
{cap_hero[3]} 年後回收只多拿 {money(cap_hero[2])}</div>
<div class="unit">單位 NT$　·　除了才剛滿一年的 iPhone 17，
加價的殘值率都明顯低於整機，而且放越久差距越大</div></div>
<div class="site">{site}</div></body></html>''')

    # ── 6 重點 ───────────────────────────────────────────
    jex = round(P["jpy"] / T * R)
    sv = P["twd"] - jex
    sv_m = round(sv / 24)
    a1, b1 = mcost(P["twd"], "Pro", 1), mcost(PM["twd"], "Pro Max", 1)
    d1 = b1["m"] - a1["m"]
    hk = RS.get("hike") or {}
    hk_date = "/".join(str(int(x)) if i else x
                       for i, x in enumerate((hk.get("date") or "").split("-")))
    hk_max = max((w - o) for _, o, w in hk.get("items", [(0, 0, 0)]))
    p_jp = (f'<b>為了台日價差專程飛一趟，攤下來是虧的</b><br>'
            f'{html.escape(P["name"])} 在日本免稅買省 {money(sv)}，攤到兩年每月 NT${sv_m:,}'
            + (f'；台北飛東京目前最低 {money(fare)}，攤兩年每月 NT${round(fare / 24):,}'
               if fare else '；一張機票攤下來通常比這個多'))
    shot(f"0{TOTAL}_end", head_html(END) + f'''<div class="mid">
<div class="h">iPhone 怎麼買<br>才划算？5 個重點</div>
<div class="pts">
 <div class="pt"><i>1</i><div><b>買 Pro 的理由不是省錢</b><br>
  和 Pro Max 每月只差 NT${d2:,}；合理的理由是機身輕、好單手操作</div></div>
 <div class="pt"><i>2</i><div><b>iPhone Air 掉價最兇</b><br>
  滿一年只剩 {rate_of("Air", 1) * 100:.0f}%，同期 Pro Max 還有 {rate_of("Pro Max", 1) * 100:.0f}%</div></div>
 <div class="pt"><i>3</i><div><b>容量升級是折舊最快的一筆</b><br>
  整機兩年後還有五成，多付的容量費用通常只剩三成</div></div>
 <div class="pt"><i>4</i><div><b>舊機今年反而漲價</b><br>
  {hk_date} Apple 調高在售舊機售價，最多一款漲 {money(hk_max)}</div></div>
 <div class="pt"><i>5</i><div>{p_jp}</div></div>
</div></div>
<div class="site">{site}</div></body></html>''')

    os.path.exists(tmp) and os.remove(tmp)

    # ── 文案：每張一則，單獨發也成立 ──────────────────────
    L = site
    pm_1 = rate_of("Pro Max", 1) * 100
    air_1 = rate_of("Air", 1) * 100
    posts = [
     ("01_cover", f"""{P["name"]} 和 {PM["name"]}，標價差 {money(PM["twd"] - P["twd"])}。
攤到每月，只差 NT${d2:,}。

・{P["name"]} {P["spec"]}　每月 NT${a2["m"]:,}
・{PM["name"]} {PM["spec"]}　每月 NT${b2["m"]:,}
（都以用兩年、之後賣掉計算）

為什麼？因為 Pro Max 兩年後的回收價高 {money(b2["keep"] - a2["keep"])}，把標價差吃掉了大半。

這裡的殘值不是我假設的——是收購商今天的公開回收報價，除以那支機器當年的官方售價。每個數字都可以自己去對。

所以「買 Pro 比較省」這個理由其實不太成立。要買 Pro，合理的理由是機身輕、好單手操作。

全部機型、1～4 年的試算：
{L}"""),

     ("02_depre", f"""{money(hero["list"])} 買的 {hero["name"]}，今天收購商收 {money(hero["resale"])}。
掉了 {money(hero["list"] - hero["resale"])}，只剩 {hero["rate"] * 100:.0f}%。

這張表把 iPhone 14 Pro 到 17 Pro Max 的「當年官方售價」，對照「今天的公開回收報價」。不是推估，是實際發生過的折舊。

兩件事很清楚：
・等級越高掉價越慢
・第一年掉最多

手機不是消耗品，買價不等於你花掉的錢。真正的成本是買價減掉之後賣掉的價錢——這張表就是在補上後面那一半。

完整試算：
{L}"""),

     ("03_matrix", f"""iPhone 幾年後還剩幾成？用今天的回收行情回推：

（滿 1 年 → 2 年 → 3 年 → 4 年）
・Pro Max　{rate_of("Pro Max", 1) * 100:.0f}% → {rate_of("Pro Max", 2) * 100:.0f}% → {rate_of("Pro Max", 3) * 100:.0f}% → {rate_of("Pro Max", 4) * 100:.0f}%
・Pro　{rate_of("Pro", 1) * 100:.0f}% → {rate_of("Pro", 2) * 100:.0f}% → {rate_of("Pro", 3) * 100:.0f}% → {rate_of("Pro", 4) * 100:.0f}%
・標準　{rate_of("標準", 1) * 100:.0f}% → {rate_of("標準", 2) * 100:.0f}% → {rate_of("標準", 3) * 100:.0f}%
・Air　{air_1:.0f}%（還沒有滿兩年的可比機種）

掉最兇的不是最便宜的機型，是 iPhone Air：滿一年只剩 {air_1:.0f}%，同期 Pro Max 還有 {pm_1:.0f}%。買 Air 多付的那筆設計費，回收時幾乎拿不回來。

（Air 2025 年才上市，還沒有滿兩年的實際行情，所以後面留白，不用推估填補。）

每一格的算法與來源：
{L}"""),

     ("04_monthly", f"""「一年換一次很浪費吧？」

用今天的回收行情算，沒你想的那麼誇張，但也確實最貴：

{P["name"]} {P["spec"]}（{money(P["twd"])}）
・用 1 年　每月 NT${a1c["m"]:,}
・用 2 年　每月 NT${a2["m"]:,}
・用 3 年　每月 NT${mcost(P["twd"], "Pro", 3)["m"]:,}
・用 4 年　每月 NT${mcost(P["twd"], "Pro", 4)["m"]:,}

用越久越便宜的方向沒變，只是差距沒有直覺上那麼大——因為滿一年的機子還有六到七成殘值。

反過來說，持有期越短，高階機種越有利，因為它掉價慢。一年一換的話，Pro Max 的每月成本甚至比 Pro 還低。

各機型各年數的完整表：
{L}"""),

     ("05_capacity", f"""買 iPhone 最不保值的一筆錢，是升級容量。

{cap_hero[0]} 多付 {money(cap_hero[1])} 從 {cap_hero[6]} 升到 {cap_hero[4]}，{cap_hero[3]} 年後回收只多拿 {money(cap_hero[2])}——加價的部分只剩 {cap_hero[5] * 100:.0f}%，同一支機器整機還有 {cap_hero[7] * 100:.0f}%。

其他幾代也一樣：整機兩年後大約還有五成，容量加價通常只剩三成上下，滿三年更低。

不是說不該買大容量，而是如果你正在猶豫「要不要多花錢升一階」，可以把它當成一筆折舊特別快的支出來看。

完整對照：
{L}"""),

     ("06_end", f"""整理一下，iPhone 怎麼買才划算——全部用台灣實際的二手回收行情算：

1　買 Pro 的理由不是省錢
和 Pro Max 每月只差 NT${d2:,}；合理的理由是機身輕、好單手操作

2　iPhone Air 掉價最兇
滿一年只剩 {air_1:.0f}%，同期 Pro Max 還有 {pm_1:.0f}%

3　容量升級是折舊最快的一筆
整機兩年後還有五成，多付的容量費用通常只剩三成

4　舊機今年反而漲價
{hk_date} Apple 調高在售舊機售價，最多一款漲 {money(hk_max)}，「等一等比較便宜」今年不成立

5　為了台日價差專程飛一趟，攤下來是虧的
{P["name"]} 在日本免稅買省 {money(sv)}，攤到兩年每月 NT${sv_m:,}""" +
      (f"；台北飛東京目前最低 {money(fare)}，攤兩年每月 NT${round(fare / 24):,}。本來就要去才順便買。"
       if fare else "；一張機票攤下來通常比這個多。本來就要去才順便買。") + f"""

自己試算：
{L}"""),
    ]
    os.makedirs("posts", exist_ok=True)
    pf = "posts/iphone-cost.txt"
    with open(pf, "w", encoding="utf-8") as f:
        f.write(f"iPhone 持有成本圖卡文案（{RS['updated']} 產生）\n"
                f"每張圖各自獨立，可分開發；順序建議 1→3→5→2→4→6\n")
        for fn, txt in posts:
            f.write("\n" + "=" * 56 + f"\n{fn}.png\n" + "=" * 56 + "\n\n"
                    + txt.strip() + "\n")

    print(f"✅ 產生 {len(made)} 張圖卡 → {OUT}/  ({W}×{H})")
    print(f"   文案 {len(posts)} 則 → {pf}")
    for f in made:
        print("   ", f + ".png")


if __name__ == "__main__":
    main()
