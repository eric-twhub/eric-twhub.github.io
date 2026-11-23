"""換日圓現鈔 vs 刷卡 短影音（15 秒、直式 1080×1920、動態字卡＋手繪貼紙＋原創配樂）。

數字不在這裡寫死：直接讀線上 /japan-yen-exchange/「換現金真的比較省嗎」那張表
（各付款方式相對即期中價的成本）和表下方的牌告日期、即期中價；
「花 ¥10,000 多付多少」用頁上的中價與百分比當場算。
畫面、動畫、配樂沿用 make_transit_video_v2（同一套 render(t)、破關風配樂）。
用法：python3 make_yen_video.py [輸出資料夾]
需要 Chrome、Playwright（Python）、numpy、ffmpeg。
"""
import html as htm
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
import urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else 'cards/threads/短影音-換日幣'
sys.argv = sys.argv[:1]  # 下面 import 的交通卡產生器也會讀 argv，避免它把輸出資料夾當成自己的
import make_transit_video_v2 as V  # noqa: E402

URL = 'https://jptripcard.com/japan-yen-exchange/'
W, H, FPS, DUR = V.W, V.H, V.FPS, V.DUR
BEAT = V.BEAT


def _txt(s):
    return htm.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s))).strip()


def _section(s, title):
    i = s.find(title + '</h2>')
    if i < 0:
        sys.exit(f'線上頁面找不到「{title}」那一段')
    j = s.find('<h2', i + 10)
    return s[i:j if j > 0 else len(s)]


def fetch():
    s = urllib.request.urlopen(urllib.request.Request(URL), timeout=30).read().decode('utf-8')
    sec = _section(s, '換現金真的比較省嗎')
    tb = sec[sec.find('<tbody>'):sec.find('</tbody>')]
    rows = []
    for r in re.findall(r'<tr>(.*?)</tr>', tb, re.S):
        td = re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)
        m = re.search(r'[＋+]\s*([\d.]+)%', _txt(td[2]))
        rows.append({'name': _txt(td[0]), 'basis': _txt(td[1]), 'pct': float(m.group(1)),
                     'pct_s': m.group(1)})
    disc = _txt(sec[sec.find('<p class="disc">'):sec.find('</p>', sec.find('<p class="disc">'))])
    m = re.search(r'(\d{4})-(\d\d)-(\d\d) 的牌告計算（即期中價 ([\d.]+)）', disc)
    card_assume = '假設約等於即期中價' in disc
    tl = _txt(sec[sec.find('<div class="tldr">'):])
    cash_m = re.search(r'日本仍有(.+?)，完全不帶現金會卡住', tl)
    # 「用台幣帳戶在外幣 ATM 領日圓」是多數人最划算的一條；四種管道表裡臨櫃寫最貴
    atm = _section(s, '用台幣帳戶在外幣 ATM 領日圓')
    ways = _section(s, '四種管道，怎麼挑')
    atm_best = '多數人最划算的一條' in _txt(atm)
    counter_worst = bool(re.search(r'臨櫃直接換.*?最貴', _txt(ways)))
    reward = '真正的差距在回饋' in tl and '現金沒有回饋' in tl
    # 為什麼現鈔比較貴：頁上「先搞懂現金匯率和即期匯率」那段的原因
    why = re.search(r'因為銀行要承擔(.+?成本)', _txt(_section(s, '先搞懂現金匯率和即期匯率')))
    if not (len(rows) == 3 and m and card_assume and cash_m and atm_best and counter_worst and reward and why):
        sys.exit('線上頁面的格式或說法和預期不同，請先看頁面再改解析')
    mid = float(m.group(4))
    for r in rows:
        r['extra'] = round(10000 * mid * r['pct'] / 100)
        b = r['basis']
        r['why'] = ('用銀行的即期賣出匯率' if b == '即期賣出' else
                    f'用現金賣出匯率，含{why.group(1)}' if b == '現金賣出' else b)
    items = [x for x in re.split(r'、|與', cash_m.group(1)) if x]
    return {'rows': rows, 'mid': m.group(4), 'date': f'{int(m.group(2))}/{int(m.group(3))}',
            'date_full': f'{m.group(1)}-{m.group(2)}-{m.group(3)}', 'cash_items': items}


EXTRA_CSS = r"""
#num{font-size:250px;top:880px}
#num small{font-size:110px;margin:0 4px}
#h1{font-size:96px;top:720px}
.rw{height:210px}
.nm{font-size:56px;top:0}
.br{top:82px;height:66px;border-radius:33px}
.vl{top:76px;font-size:66px}
.amt{position:absolute;left:122px;top:158px;font-size:32px;line-height:1.45;font-weight:700;color:#8a6a55;white-space:nowrap}
.amt .w{color:#5a3d2b}
.amt b{color:#5a3d2b}
.rw.g .amt b{color:#e8553e}
#crown{width:auto}
#crown span{display:inline-block;background:#e8553e;color:#fff;border:5px solid #5a3d2b;border-radius:18px;
 padding:4px 18px;font-size:44px;transform:rotate(8deg)}
#base{font-size:46px;color:#5a3d2b;line-height:1.45;border-top:4px dashed #ead9c4;padding-top:26px}
#base em{font-style:normal;color:#e8553e}
.cp{padding:22px 36px}
.cp b{font-size:60px;font-weight:400}
#reg{top:1230px}
#reg div.t{font-size:48px}
#srch{font-size:50px}
"""


def build_html(d):
    e = htm.escape
    rows = sorted(d['rows'], key=lambda r: -r['pct'])  # 最貴的放第一列（最後揭曉）
    if '現鈔' not in rows[0]['name']:
        sys.exit(f'最貴的已經不是換現鈔（是 {rows[0]["name"]}），開場文案要改')
    top = rows[0]
    rnd = random.Random(7)
    cols = ['#e8553e', '#ffe48a', '#9fd3c7', '#f6a5ad', '#6bb38a', '#a5c8f0']

    def burst(n, x, y):
        out = []
        for _ in range(n):
            ang = rnd.uniform(-math.pi, 0)
            sp = rnd.uniform(500, 1300)
            out.append({'x': x, 'y': y, 'vx': math.cos(ang) * sp, 'vy': math.sin(ang) * sp - 200,
                        'r': rnd.uniform(0, 360), 'vr': rnd.uniform(-720, 720),
                        'f': rnd.uniform(6, 16), 'c': rnd.choice(cols)})
        return out

    y0, rh = 450, 270
    mx = max(r['pct'] for r in rows)
    wrow = [{'save': r['pct'], 'w': max(80, round(r['pct'] / mx * 480))} for r in rows]
    n = len(rows)
    rowT = [0] * n
    for k, i in enumerate(range(n - 1, 0, -1)):
        rowT[i] = V.T_RANK + (1 + k) * BEAT
    rowT[0] = V.T_RANK + 5 * BEAT - 0.45  # 多停一拍再揭曉最貴的，衝擊落在拍點上
    cf1 = burst(36, 540, 1000)
    cf2 = burst(30, 700, y0 + 100)
    items = d['cash_items']
    D = {'L': V.T_LAND, 'R': V.T_RANK, 'C': V.T_CAP, 'E': V.T_END, 'top': top['pct'], 'rows': wrow,
         'rowT': rowT, 'rowY0': y0, 'caps': items, 'cf1': cf1, 'cf2': cf2}

    def cfdivs(g, tag):
        return ''.join(f'<div class="cf" id="{tag}{i}" style="background:{c["c"]}"></div>' for i, c in enumerate(g))

    s1 = (f'<div id="s1" class="sc">'
          f'<div id="k1" class="ab"><span class="pill hn">去日本前要先換日幣嗎？</span></div>'
          f'<div id="st1c" class="ab stk sh">{V._svg("phone")}</div>'
          f'<div id="st1" class="ab stk sh">{V._svg("yen")}</div>'
          f'<div id="st1b" class="ab stk sh">{V._svg("card")}</div>'
          f'<div id="h1" class="ab hn">換現鈔其實最貴</div>'
          f'<div id="num" class="ab hn"><small>＋</small><span id="nv">0</span><small>%</small></div>'
          f'<div id="sub1" class="ab">比刷卡、電支掃碼都高</div>'
          f'<div id="q1" class="ab"><span class="hn">花 ¥10,000 差多少？</span></div>'
          f'{cfdivs(cf1, "a")}</div>')
    rw = ''
    for i, r in enumerate(rows):
        rw += (f'<div id="r{i}" class="ab rw{" g" if i == 0 else ""}" style="top:{y0 + i * rh}px">'
               f'<div class="rk hn">{i + 1}</div><div class="nm">{e(r["name"])}</div>'
               f'<div class="br" style="width:{wrow[i]["w"]}px"></div>'
               f'<div class="vl hn"><small>＋</small><i>0</i><small>%</small></div>'
               f'<div class="amt"><div class="w">{e(r["why"])}</div>'
               f'<div>花 ¥10,000 比中價多付約 <b>NT${r["extra"]}</b></div></div></div>')
    s2 = (f'<div id="s2" class="sc">'
          f'<div id="t2" class="ab hn">付日圓的成本<br><em>哪種最貴</em></div>{rw}'
          f'<div id="crown" class="ab"><span class="hn">最貴</span></div>'
          f'<div id="base" class="ab hn" style="top:{y0 + n * rh + 10}px">'
          f'<em>真正的差距在刷卡回饋</em><br>現金沒有回饋</div>'
          f'{cfdivs(cf2, "b")}</div>')
    cp = ''.join(f'<div id="cp{i}" class="ab cp" style="top:{430 + i * 175}px"><b class="hn">{e(x)}</b></div>'
                 for i, x in enumerate(items))
    s3 = (f'<div id="s3" class="sc"><div id="stamp" class="ab"><span class="hn">但現金還是要帶</span></div>{cp}'
          f'<div id="reg" class="ab"><div class="stk sh">{V._svg("shop")}</div>'
          f'<div class="t hn">要換現金：台幣帳戶<br>到外幣 ATM 領最划算<br><em>臨櫃換最貴</em></div></div></div>')
    s4 = (f'<div id="s4" class="sc"><div id="st4" class="ab stk sh">{V._svg("plane-fuji")}</div>'
          f'<div id="brand" class="ab hn">日本旅遊小卡</div>'
          f'<div id="url" class="ab"><span class="hn">jptripcard.com</span></div>'
          f'<div id="srch" class="ab">各銀行外幣 ATM 減碼比較</div>'
          f'<div id="tiny" class="ab">{e(d["date"])} 臺灣銀行牌告試算（即期中價 {e(d["mid"])}）<br>'
          f'卡組織匯率假設約等於中價，實際可能再高一點<br>匯率隨時變動，以各銀行公告為準</div></div>')
    # 沿用交通卡 v2 的 render(t)；數字改成兩位小數
    js_cf = 'for(const [g,p] of [["cf1","a"],["cf2","b"]]) D[g].forEach((c,i)=>c.el=document.getElementById(p+i));'
    js = V.JS + "\nfunction fmt(n){return n.toFixed(2)}\n"
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Huninn&display=swap" rel="stylesheet">'
            f'<style>{V.CSS}{EXTRA_CSS}</style></head><body><div id="bg"></div><div id="burst"></div>'
            f'{s1}{s2}{s3}{s4}<div id="wipe"></div>'
            f'<script>window.D={json.dumps(D, ensure_ascii=False)};{js_cf}{js}</script></body></html>'), rowT, items


def main():
    from playwright.sync_api import sync_playwright
    d = fetch()
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src, rowT, items = build_html(d)
    sty = os.environ.get('MUSIC', 'game')
    if sty not in V.STYLES:
        sys.exit(f'沒有這種配樂：{sty}，可用 {list(V.STYLES)}')
    keep = os.environ.get('KEEP_FRAMES')
    mp4 = os.path.join(OUT, f'yen-exchange-15s-{sty}.mp4')
    with tempfile.TemporaryDirectory() as tmp:
        hf = os.path.join(tmp, 'v.html')
        open(hf, 'w', encoding='utf-8').write(src)
        wav = os.path.join(tmp, 'm.wav')
        V.STYLES[sty](wav, rowT, len(items))
        ff = subprocess.Popen(
            ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
             '-c:v', 'png', '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4],
            stdin=subprocess.PIPE)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=V.base._chrome())
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
            pg.goto('file://' + hf)
            pg.evaluate('document.fonts.ready')
            if not pg.evaluate('document.fonts.check(\'40px "Huninn"\')'):
                sys.exit('Huninn 字型沒有載入（需要網路連到 Google Fonts）')
            for f in range(int(DUR * FPS)):
                t = f / FPS
                pg.evaluate(f'render({t})')
                png = pg.screenshot(type='png')
                ff.stdin.write(png)
                if keep and any(abs(t - float(x)) < .5 / FPS for x in keep.split(',')):
                    open(os.path.join(V.keep_dir(), f'{t:05.2f}.png'), 'wb').write(png)
            b.close()
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit('ffmpeg 合成失敗')
    r = sorted(d['rows'], key=lambda x: -x['pct'])
    print(mp4)
    print(f'{d["date_full"]} 牌告、中價 {d["mid"]}；' + '、'.join(f'{x["name"]} +{x["pct_s"]}%（¥10,000 多付 NT${x["extra"]}）' for x in r))


if __name__ == '__main__':
    main()
