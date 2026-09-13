# -*- coding: utf-8 -*-
"""每日最低價月曆圖卡（1080×1350）。

一眼看出「哪天便宜、哪天貴」——同一個月的價差常常是兩倍以上，
用文字講很無感，做成月曆就一目了然。

資料來自票價快取，並非每天都有紀錄；覆蓋率不足的城市不產卡，
缺資料的日子留白，不以鄰近日期推估填補。

用法：python3 make_calendar_cards.py [--days 42] [--min-cov 0.5]
輸出：cards/calendar/<slug>.png
"""
import json, os, sys, datetime, subprocess, collections
from zoneinfo import ZoneInfo

W, H = 1080, 1350
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
OUT = "cards/calendar"
SCAN = "/tmp/scan_all.json"
TODAY = datetime.datetime.now(ZoneInfo("Asia/Taipei")).date()
WD = ["一", "二", "三", "四", "五", "六", "日"]

# 想產卡的城市：前綴比對 _dname，因為資料裡是「東京・羽田」「東京・成田」
TARGETS = [
    ("tokyo", "東京", "東京"), ("okinawa", "沖繩", "沖繩"),
    ("osaka", "大阪", "大阪"), ("fukuoka", "福岡", "福岡"),
    ("kobe", "神戶", "神戶"), ("nagoya", "名古屋", "名古屋"),
]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx}
body{background:#141210;color:#f5f2ee;
 font-family:"PingFang TC","Noto Sans TC","Noto Sans CJK TC",
 "Hiragino Sans GB","Heiti TC",sans-serif;
 display:flex;flex-direction:column;padding:64px 56px 52px;position:relative;overflow:hidden}
.glow{position:absolute;width:780px;height:780px;border-radius:50%%;
 background:radial-gradient(circle,rgba(251,146,60,.18),transparent 68%%);top:-320px;right:-280px}
.brand{font-size:25px;letter-spacing:.3em;color:#fb923c;font-weight:700}
.route{margin-top:22px;font-size:62px;font-weight:800;letter-spacing:-.02em;line-height:1.15}
.route i{font-style:normal;color:#fb923c;margin:0 14px}
.sub{margin-top:12px;font-size:28px;color:#a8a29c}
.wk{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:30px}
.wk span{text-align:center;font-size:23px;color:#6b6560;font-weight:600}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:10px}
.c{border-radius:12px;padding:12px 4px 11px;text-align:center;min-height:92px;
 display:flex;flex-direction:column;justify-content:center;gap:5px}
.c u{text-decoration:none;font-size:27px;font-weight:700;line-height:1}
.c b{font-size:23px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums}
.c s{text-decoration:none;font-size:20px;color:#57524d}
.lo{background:#0f766e;color:#e6fffb}
.lo u,.lo b{color:#fff}
.mid{background:rgba(15,118,110,.28);color:#8fded4}
.hi{background:rgba(255,255,255,.05);color:#b8b2ab}
.high{background:rgba(127,29,29,.34);color:#f2a9a9}
.high u,.high b{color:#ffd9d9}
.top{background:#7f1d1d;color:#fecaca}
.top u,.top b{color:#fff}
.na{background:rgba(255,255,255,.025);color:#3f3a36}
.pad{background:none}
.legend{display:flex;gap:16px;margin-top:22px;font-size:21px;color:#8a837c;flex-wrap:wrap}
.legend i{font-style:normal;display:inline-block;width:18px;height:18px;border-radius:5px;
 margin-right:7px;vertical-align:-3px}
.note{margin-top:auto;padding-top:20px;font-size:22px;color:#5f5a55;line-height:1.55}
.site{margin-top:14px;font-size:26px;color:#fb923c;font-weight:700}
""" % (W, H)


def load():
    if not os.path.exists(SCAN):
        sys.exit(f"找不到 {SCAN}（需先執行 scan_all.py）")
    return json.load(open(SCAN, encoding="utf-8"))


def daily_min(rows, days):
    """每日最低價；沒有紀錄的日期不填補，直接留空。"""
    by = collections.defaultdict(list)
    for r in rows:
        by[r["departure_at"][:10]].append(r["price"])
    out = {}
    for i in range(days):
        d = (TODAY + datetime.timedelta(days=i)).isoformat()
        if by.get(d):
            out[d] = min(by[d])
    return out


def build(slug, name, prices, days):
    vals = sorted(prices.values())
    lo, hi = vals[0], vals[-1]
    q1 = vals[len(vals) // 4]
    q3 = vals[len(vals) * 3 // 4]

    def cls(v):
        if v == hi: return "top"
        if v == lo: return "lo"
        if v <= q1: return "mid"
        if v >= q3: return "high"      # 偏貴要和「一般」分開，否則整排看起來一樣
        return "hi"

    start = TODAY - datetime.timedelta(days=TODAY.weekday())   # 從本週一排起
    cells = ""
    d = start
    end = TODAY + datetime.timedelta(days=days)
    while d < end:
        k = d.isoformat()
        if d < TODAY:
            cells += '<div class="c pad"></div>'
        elif k in prices:
            v = prices[k]
            cells += (f'<div class="c {cls(v)}"><u>{d.day}</u>'
                      f'<b>{v//1000},{v%1000:03d}</b></div>')
        else:
            cells += f'<div class="c na"><u>{d.day}</u><s>—</s></div>'
        d += datetime.timedelta(days=1)

    span = f"{TODAY.month}/{TODAY.day} – {(end-datetime.timedelta(days=1)).month}/{(end-datetime.timedelta(days=1)).day}"
    cheap_day = [k for k, v in prices.items() if v == lo][0]
    cd = datetime.date.fromisoformat(cheap_day)
    ratio = hi / lo

    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<style>{CSS}</style></head><body><div class="glow"></div>
<div class="brand">台日機票速報</div>
<div class="route">台灣<i>→</i>{name}</div>
<div class="sub">{span} 每日最低來回含稅　·　最貴是最便宜的 {ratio:.1f} 倍</div>
<div class="wk">{''.join(f'<span>{w}</span>' for w in WD)}</div>
<div class="cal">{cells}</div>
<div class="legend">
 <span><i style="background:#0f766e"></i>最便宜　{cd.month}/{cd.day} NT${lo:,}</span>
 <span><i style="background:rgba(15,118,110,.28)"></i>偏低</span>
 <span><i style="background:rgba(255,255,255,.05)"></i>一般</span>
 <span><i style="background:rgba(127,29,29,.34)"></i>偏貴</span>
 <span><i style="background:#7f1d1d"></i>最貴 NT${hi:,}</span>
 <span><i style="background:rgba(255,255,255,.025)"></i>無紀錄</span>
</div>
<div class="note">價格為單人來回含稅的近期最低紀錄，僅供比較各日期高低，
非即時可訂價；標「—」的日期目前沒有紀錄，不代表沒有航班。</div>
<div class="site">eric-twhub.github.io</div>
</body></html>"""


def main():
    days = 42
    min_cov = 0.5
    for i, a in enumerate(sys.argv):
        if a == "--days": days = int(sys.argv[i + 1])
        if a == "--min-cov": min_cov = float(sys.argv[i + 1])

    chrome = _chrome()
    data = load()
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.abspath(".cal_tmp.html")
    made, skipped = [], []

    for slug, name, prefix in TARGETS:
        rows = [x for x in data
                if str(x.get("_dname", "")).startswith(prefix) and x.get("return_at")]
        if not rows:
            skipped.append((name, "無資料")); continue
        prices = daily_min(rows, days)
        cov = len(prices) / days
        if cov < min_cov:
            skipped.append((name, f"覆蓋率 {cov*100:.0f}%")); continue

        open(tmp, "w", encoding="utf-8").write(build(slug, name, prices, days))
        png = os.path.abspath(os.path.join(OUT, f"{slug}.png"))
        cmd = [chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
               f"--screenshot={png}", f"--window-size={W},{H}",
               "--force-device-scale-factor=1"]
        if sys.platform.startswith("linux"):
            cmd += ["--no-sandbox", "--disable-dev-shm-usage"]
        subprocess.run(cmd + ["file://" + tmp], capture_output=True, timeout=90)
        if os.path.exists(png):
            made.append((name, len(prices), days, min(prices.values()), max(prices.values())))

    os.path.exists(tmp) and os.remove(tmp)
    print(f"✅ 產生 {len(made)} 張月曆卡 → {OUT}/")
    for n, c, d, lo, hi in made:
        print(f"   {n}　{c}/{d} 天有紀錄　NT${lo:,} – NT${hi:,}（{hi/lo:.1f} 倍）")
    for n, why in skipped:
        print(f"   ⏭  {n} 未產出（{why}）")


if __name__ == "__main__":
    main()
