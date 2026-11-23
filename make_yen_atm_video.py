"""換日幣現鈔怎麼換最省 短影音（15 秒、直式 1080×1920、動態字卡＋手繪貼紙＋原創配樂）。

數字不在這裡寫死：直接讀線上 /japan-yen-exchange/ 的
「四種管道，怎麼挑」表（臨櫃手續費範圍）、「用台幣帳戶在外幣 ATM 領日圓」減碼表（元／日圓、出鈔面額、備註）、
「換現金真的比較省嗎」表（現鈔相對中價的成本）與「出國前要先開通」那段；
「¥10,000 少付多少」「要領到多少才超過最低收費」用頁上的減碼、百分比與中價當場算。官網沒寫的銀行照實標「官網沒寫」，不當成 0、不從表裡拿掉。
畫面、動畫、配樂沿用 make_transit_video_v2。
用法：python3 make_yen_atm_video.py [輸出資料夾]
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
sys.argv = sys.argv[:1]
import make_yen_video as Y  # noqa: E402  （也會帶進 make_transit_video_v2）

V = Y.V
W, H, FPS, DUR = V.W, V.H, V.FPS, V.DUR
BEAT = V.BEAT
_txt, _section = Y._txt, Y._section


def fetch():
    base = Y.fetch()  # 牌告日期、中價、各付款方式相對中價的成本（含格式檢查）
    s = urllib.request.urlopen(urllib.request.Request(Y.URL), timeout=30).read().decode('utf-8')
    atm = _section(s, '用台幣帳戶在外幣 ATM 領日圓')
    tb = atm[atm.find('<tbody>'):atm.find('</tbody>')]
    banks = []
    for r in re.findall(r'<tr>(.*?)</tr>', tb, re.S):
        td = re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)
        cut = _txt(td[1])
        den = _txt(td[2])
        banks.append({'name': _txt(td[0]),
                      'cut': float(cut) if re.fullmatch(r'[\d.]+', cut) else None,
                      'den': den if re.fullmatch(r'[\d,]+', den) else None,
                      'note': _txt(td[3])})
    notes = ' '.join(b['note'] for b in banks)
    lim = re.search(r'他行卡單筆上限約 ([\d.]+ 萬元)', notes)
    not24 = '不是 24 小時' in notes
    ways = _section(s, '四種管道，怎麼挑')
    cf = re.search(r'臨櫃直接換</b></td><td[^>]*>[^<]*</td><td[^>]*>[^<]*?(\d+) 到 (\d+) 元', ways)
    airport = '機場分行還會再加收' in _txt(ways)
    atm_free = re.search(r'外幣 ATM，用台幣帳戶扣款</b></td><td[^>]*>[^<]*</td><td[^>]*>免手續費', ways)
    go = _section(s, '出國前要先開通，這件事不能到日本再弄')
    four = _section(s, '到日本才領現金：費用是四層，不是一層')
    pre = '要另外申請跨國提款功能' in _txt(go)
    known = [b for b in banks if b['cut'] is not None]
    cash = [r for r in base['rows'] if r['basis'] == '現金賣出']
    spot = [r for r in base['rows'] if r['basis'] == '即期賣出']
    # 外幣帳戶領鈔的匯差手續費最低收費（「最低收費會咬人」那段＋四種管道表）
    mn = re.search(r'匯差手續費多數銀行最低收 (\d+) 元', _txt(ways))
    mn_row = re.search(r'線上換匯進外幣帳戶，再用外幣 ATM 領鈔</b></td><td[^>]*>[^<]*</td><td[^>]*>匯差手續費，最低 (\d+) 元', ways)
    if not (len(banks) >= 5 and known and lim and not24 and cf and airport and atm_free and pre
            and '四層' in _txt(four) and cash and spot and mn and mn_row and mn.group(1) == mn_row.group(1)):
        sys.exit('線上頁面的格式或說法和預期不同，請先看頁面再改解析')
    mid = float(base['mid'])
    top = max(b['cut'] for b in known)
    cash_extra = 10000 * mid * cash[0]['pct'] / 100          # 現鈔（現金賣出）比中價多付
    for b in banks:
        b['save'] = round(10000 * b['cut']) if b['cut'] is not None else None
    dens = sorted({int(b['den'].replace(',', '')) for b in banks if b['den']})
    min_fee = int(mn.group(1))
    # 全額收匯差的銀行：價差 × 金額 超過最低收費才不吃虧。價差＝現金賣出－即期賣出，
    # 用頁上兩個百分比（各自四捨五入到 0.01%）和中價估算；誤差範圍算出來的「萬」不一致就不放
    gap = lambda dp: 10000 * mid * (cash[0]['pct'] - spot[0]['pct'] + dp) / 100  # 每 ¥10,000 的價差
    be = [min_fee / gap(dp) * 10000 for dp in (-.01, 0, .01)]
    be_man = round(be[1] / 10000) if len({round(x / 10000) for x in be}) == 1 else None
    return {'date': base['date'], 'date_full': base['date_full'], 'mid': base['mid'], 'banks': banks,
            'top_cut': top, 'top_save': round(10000 * top),
            'cash_extra': round(cash_extra), 'atm_extra': round(cash_extra - 10000 * top),
            'counter_fee': (int(cf.group(1)), int(cf.group(2))),
            'gap_max': round(10000 * top) + int(cf.group(2)),
            'limit': lim.group(1), 'dens': dens, 'min_fee': min_fee, 'be_man': be_man,
            'gap10k': round(gap(0))}


EXTRA_CSS = r"""
#num{font-size:260px;top:880px}
#num small{font-size:110px;margin-right:6px}
#h1{font-size:88px;top:730px}
#sub1{font-size:40px;top:1175px;line-height:1.5}
#t2{font-size:64px}
#q1{top:1330px}
#q1 span{font-size:50px;line-height:1.3;padding:12px 36px}
.rw{height:120px}
.rk{top:10px;width:84px;height:84px;line-height:72px;font-size:48px}
.rw.u .rk{border-style:dashed;color:#b9a48f}
.nm{font-size:44px;top:2px;left:110px}
.nm small{font-size:30px;font-weight:700;color:#8a6a55;margin-left:12px}
.nm .tie{display:inline-block;background:#e8553e;color:#fff;border:4px solid #5a3d2b;border-radius:14px;
 padding:0 12px;font-size:32px;margin-left:12px;transform:rotate(6deg);font-family:"Huninn",sans-serif;font-weight:400}
.br{left:110px;top:64px;height:44px;border-radius:22px}
.vl{top:56px;font-size:46px}
.vl small{font-size:30px}
.rw.u .br,.rw.u .vl i{display:none}
.rw.u .vl{color:#b9a48f;font-family:"PingFang TC",sans-serif;font-size:36px;font-weight:700;top:64px}
#crown{display:none}
#base{font-size:40px;line-height:1.5;border-top:4px dashed #ead9c4;padding-top:20px}
#base em{font-style:normal;color:#e8553e}
.cp{padding:14px 32px}
.cp b{font-size:46px;font-weight:400;line-height:1.3}
.cp s{font-size:32px;margin-top:2px}
#reg{top:1240px}
#reg div.t{font-size:44px;line-height:1.35}
#srch{font-size:48px}
#tiny{font-size:30px}
"""


def build_html(d):
    e = htm.escape
    banks = d['banks']
    # 有數字的照減碼由大到小（同分照頁面順序），官網沒寫的放最後
    known = sorted([b for b in banks if b['cut'] is not None], key=lambda b: -b['cut'])
    unknown = [b for b in banks if b['cut'] is None]
    rows = known + unknown
    rnd = random.Random(7)
    cols = ['#e8553e', '#ffe48a', '#9fd3c7', '#f6a5ad', '#6bb38a', '#a5c8f0']

    def burst(n, x, y):
        return [{'x': x, 'y': y, 'vx': math.cos(a) * sp, 'vy': math.sin(a) * sp - 200,
                 'r': rnd.uniform(0, 360), 'vr': rnd.uniform(-720, 720), 'f': rnd.uniform(6, 16),
                 'c': rnd.choice(cols)}
                for a, sp in ((rnd.uniform(-math.pi, 0), rnd.uniform(500, 1300)) for _ in range(n))]

    y0, rh = 410, 120
    mx = d['top_save'] or 1
    wrow = [{'save': (b['save'] or 0), 'w': (max(40, round(b['save'] / mx * 440)) if b['save'] else 0)}
            for b in rows]
    n = len(rows)
    rowT = [0] * n
    for k, i in enumerate(range(n - 1, 0, -1)):
        rowT[i] = V.T_RANK + BEAT * (1 + .75 * k)
    rowT[0] = V.T_RANK + 8 * BEAT - 0.45  # 第一名最後揭曉，衝擊落在拍點上
    # 名次：同分同名次；官網沒寫的不給名次
    ranks, prev, rk = [], None, 0
    for k, b in enumerate(rows):
        if b['cut'] is None:
            ranks.append('?')
            continue
        if b['cut'] != prev:
            rk, prev = k + 1, b['cut']
        ranks.append(str(rk))
    cf1 = burst(36, 540, 1000)
    cf2 = burst(30, 700, y0 + 60)
    items = [
        ('他行卡單筆上限', f'約 {d["limit"]}'),
        ('出鈔面額固定', '／'.join(f'{x:,}' for x in d['dens']) + ' 日圓為單位'),
        ('部分機台不是 24 小時', '設在分行營業廳內'),
        ('臨櫃換最貴', f'沒有減碼，還收 {d["counter_fee"][0]}～{d["counter_fee"][1]} 元'),
        (f'外幣帳戶領鈔最低收 {d["min_fee"]} 元', '小額最吃虧'),
    ]
    D = {'L': V.T_LAND, 'R': V.T_RANK, 'C': V.T_CAP, 'E': V.T_END, 'top': d['min_fee'], 'rows': wrow,
         'rowT': rowT, 'rowY0': y0, 'caps': items, 'cf1': cf1, 'cf2': cf2}

    def cfdivs(g, tag):
        return ''.join(f'<div class="cf" id="{tag}{i}" style="background:{c["c"]}"></div>' for i, c in enumerate(g))

    s1 = (f'<div id="s1" class="sc">'
          f'<div id="k1" class="ab"><span class="pill hn">換日幣現鈔，哪裡換最省？</span></div>'
          f'<div id="st1c" class="ab stk sh">{V._svg("receipt")}</div>'
          f'<div id="st1" class="ab stk sh">{V._svg("yen")}</div>'
          f'<div id="st1b" class="ab stk sh">{V._svg("shop")}</div>'
          f'<div id="h1" class="ab hn">外幣帳戶領 ¥10,000</div>'
          f'<div id="num" class="ab hn"><small>NT$</small><span id="nv">0</span></div>'
          f'<div id="sub1" class="ab">手續費最低就收這麼多（價差只有約 NT${d["gap10k"]}）<br>'
          + (f'要領到約 ¥{d["be_man"]} 萬才超過最低收費' if d['be_man'] else '小額領最吃虧') + '</div>'
          f'<div id="q1" class="ab"><span class="hn">台幣帳戶直接在外幣 ATM 領<br>免手續費還有減碼</span></div>'
          f'{cfdivs(cf1, "a")}</div>')
    rw = ''
    for i, b in enumerate(rows):
        cls = ' g' if b['cut'] == d['top_cut'] else (' u' if b['cut'] is None else '')
        den = f'<small>{e(b["den"])} 面額</small>' if b['den'] else '<small>面額官網沒寫</small>'
        tie = '<span class="tie">最省</span>' if b['cut'] == d['top_cut'] else ''
        val = ('<small>省 NT$</small><i>0</i>' if b['cut'] is not None
               else '<i>0</i>減碼官網沒寫')
        rw += (f'<div id="r{i}" class="ab rw{cls}" style="top:{y0 + i * rh}px">'
               f'<div class="rk hn">{ranks[i]}</div><div class="nm">{e(b["name"])}{tie}{den}</div>'
               f'<div class="br" style="width:{wrow[i]["w"]}px"></div>'
               f'<div class="vl hn">{val}</div></div>')
    s2 = (f'<div id="s2" class="sc">'
          f'<div id="t2" class="ab hn">外幣 ATM 領 ¥10,000<br><em>哪家減碼最多</em></div>{rw}'
          f'<div id="crown" class="ab"></div>'
          f'<div id="base" class="ab" style="top:{y0 + n * rh + 6}px">台幣帳戶扣款、免手續費，以減碼最多的算<br>'
          f'<em>現鈔比中價多付約 NT${d["cash_extra"]} → NT${d["atm_extra"]}</em></div>'
          f'{cfdivs(cf2, "b")}</div>')
    cp = ''.join(f'<div id="cp{i}" class="ab cp" style="top:{420 + i * 160}px"><b class="hn">{e(a)}</b>'
                 f'<s>{e(b)}</s></div>' for i, (a, b) in enumerate(items))
    s3 = (f'<div id="s3" class="sc"><div id="stamp" class="ab"><span class="hn">但要注意</span></div>{cp}'
          f'<div id="reg" class="ab"><div class="stk sh">{V._svg("plane")}</div>'
          f'<div class="t hn">想到日本再領？<br><em>出國前要先開通跨國提款</em><br>費用還有四層</div></div></div>')
    s4 = (f'<div id="s4" class="sc"><div id="st4" class="ab stk sh">{V._svg("plane-fuji")}</div>'
          f'<div id="brand" class="ab hn">日本旅遊小卡</div>'
          f'<div id="url" class="ab"><span class="hn">jptripcard.com</span></div>'
          f'<div id="srch" class="ab">各銀行減碼、臨櫃手續費比較</div>'
          f'<div id="tiny" class="ab">減碼與面額依各行官網整理，「官網沒寫」不代表沒有或不收費<br>'
          f'{e(d["date"])} 臺灣銀行牌告試算（即期中價 {e(d["mid"])}）'
          + ('；「約 ¥' + str(d['be_man']) + ' 萬」以全額收匯差估算，各行自己的牌告不同' if d['be_man'] else '')
          + '<br>以各銀行公告為準</div></div>')
    js_cf = 'for(const [g,p] of [["cf1","a"],["cf2","b"]]) D[g].forEach((c,i)=>c.el=document.getElementById(p+i));'
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Huninn&display=swap" rel="stylesheet">'
            f'<style>{V.CSS}{EXTRA_CSS}</style></head><body><div id="bg"></div><div id="burst"></div>'
            f'{s1}{s2}{s3}{s4}<div id="wipe"></div>'
            f'<script>window.D={json.dumps(D, ensure_ascii=False)};{js_cf}{V.JS}</script></body></html>'), rowT, items


def main():
    from playwright.sync_api import sync_playwright
    d = fetch()
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data-atm.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src, rowT, items = build_html(d)
    sty = os.environ.get('MUSIC', 'game')
    if sty not in V.STYLES:
        sys.exit(f'沒有這種配樂：{sty}，可用 {list(V.STYLES)}')
    keep = os.environ.get('KEEP_FRAMES')
    mp4 = os.path.join(OUT, f'yen-atm-15s-{sty}.mp4')
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
    print(mp4)
    print(f'外幣帳戶領鈔最低收 NT${d["min_fee"]}（¥10,000 價差約 NT${d["gap10k"]}，約 ¥{d["be_man"]} 萬才超過）；現鈔 NT${d["cash_extra"]} → ATM NT${d["atm_extra"]}；' +
          '、'.join(f'{b["name"]} {b["cut"] if b["cut"] is not None else "官網沒寫"}' for b in d['banks']))


if __name__ == '__main__':
    main()
