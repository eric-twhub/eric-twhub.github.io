# -*- coding: utf-8 -*-
"""三國連假與請假試算的分享圖卡（1080×1350，4:5）。

資料不是直接讀 holidays.json，而是讀 gen.py 產出的
japan-holiday-calendar/cards-data.json。原因有兩個：
請假試算是八十幾行的邏輯，票價價差又要有當日的 scan 資料才算得出來，
在這裡重寫一次一定會和頁面漂移。

票價那一張是**當日快照**，數字每天都會變（2026-09-28 當天，
「只有日本連假」就從 -7% 變成 +4%），所以卡片上會把產生時間印出來，
指紋也刻意不涵蓋票價，否則每天都會跳過期警告。

用法：python3 make_holiday_cards.py
輸出：japan-holiday-calendar/cards/hol-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib, datetime
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-holiday-calendar', 'cards')
SRC = os.path.join('japan-holiday-calendar', 'cards-data.json')
E = htm.escape
CN = {'jp': '日本', 'tw': '台灣', 'cn': '中國'}


def fingerprint(d):
    """只涵蓋行事曆算出來的東西，不含票價。

    票價是當日快照，天天都不一樣，放進指紋只會讓建置每天都喊過期。
    """
    pay = [[p['name'], p['base'], p['from'], p['to'],
            sorted((str(k), v['tot']) for k, v in p['opts'].items())]
           for p in d['leave']]
    pay.append([[o['start'], o['end'], o['days'], o['countries']] for o in d['overlaps']])
    pay.append([[k, [[r['start'], r['end'], r['days']] for r in v]]
                for k, v in sorted(d['runs'].items())])
    pay.append([d['checked']])
    return hashlib.sha1(json.dumps(pay, ensure_ascii=False,
                                   sort_keys=True).encode('utf-8')).hexdigest()[:12]


def _chrome():
    c = os.environ.get('CHROME')
    if c and os.path.exists(c):
        return c
    mac = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(mac):
        return mac
    for n in ('google-chrome', 'google-chrome-stable', 'chromium-browser', 'chromium'):
        p = shutil.which(n)
        if p:
            return p
    sys.exit('找不到 Chrome，請設定 CHROME 環境變數')


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;
 font-family:"Noto Sans CJK TC","Noto Sans TC","PingFang TC","Hiragino Sans",
 "Heiti TC",sans-serif;
 background:#f7f7f5;color:#1a1a1a;-webkit-font-smoothing:antialiased}
.card{width:1080px;height:1350px;padding:58px 64px 0;display:flex;flex-direction:column;
 background:#f7f7f5}
.kick{font-size:26px;color:#c2410c;font-weight:700;letter-spacing:.06em;margin-bottom:14px}
h1{font-size:58px;line-height:1.24;font-weight:800;letter-spacing:-.01em}
h1 em{font-style:normal;color:#c2410c}
.sub{font-size:27px;line-height:1.7;color:#63605c;margin-top:16px}
.legend{font-size:21px;color:#63605c;margin-top:9px;line-height:1.6}
.list{margin-top:24px;flex:1 1 auto;min-height:0}
.hd{display:flex;gap:12px;align-items:flex-end;padding:0 0 9px;
 font-size:20px;color:#8a847c;border-bottom:2px solid #1a1a1a}
.row{display:flex;gap:12px;align-items:baseline;padding:13px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.nm{flex:1 1 auto;font-size:29px;font-weight:700;line-height:1.28;letter-spacing:-.01em}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;letter-spacing:0}
.d{flex:0 0 74px;text-align:center;font-size:27px;font-weight:700;
 font-variant-numeric:tabular-nums}
.d small{display:block;font-size:17px;font-weight:600;color:#8a847c;margin-top:2px}
.d.up{color:#c2410c}
.big{flex:0 0 118px;text-align:right;font-size:32px;font-weight:800;color:#c2410c;
 font-variant-numeric:tabular-nums}
.big small{font-size:20px;font-weight:600;color:#8a847c;margin-left:3px}
.who{flex:0 0 150px;text-align:right;font-size:25px;font-weight:700;color:#c4563a;
 white-space:nowrap}
.pct{flex:0 0 124px;text-align:right;font-size:30px;font-weight:800;
 font-variant-numeric:tabular-nums}
.pct.up{color:#c4563a}.pct.flat{color:#63605c}
.med{flex:0 0 154px;text-align:right;font-size:27px;font-weight:700;
 font-variant-numeric:tabular-nums}
.med small{display:block;font-size:19px;font-weight:500;color:#8a847c;margin-top:2px}
.foot{flex:0 0 auto;padding:24px 0 42px;border-top:3px solid #1a1a1a;
 display:flex;justify-content:space-between;align-items:flex-end;margin-top:18px}
.foot b{font-size:28px;font-weight:800;display:block}
.foot span{font-size:22px;color:#63605c;display:block;margin-top:6px}
.pg{font-size:24px;color:#63605c;font-weight:700}
.cover{justify-content:center}
.cover .list{flex:0 0 auto;margin-top:0}
.stat{display:flex;gap:14px;margin-top:36px}
.stat div{flex:1;background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:22px 20px}
.stat b{display:block;font-size:46px;font-weight:800;color:#c2410c;line-height:1.1;
 font-variant-numeric:tabular-nums}
.stat span{display:block;font-size:22px;color:#63605c;margin-top:8px;line-height:1.5}
.note{margin-top:34px;background:#fff;border:1px solid #e5e3de;border-left:7px solid #c2410c;
 border-radius:14px;padding:26px 28px;font-size:25px;line-height:1.75}
"""


def page(inner, cls=''):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS}</style></head><body><div class="card {cls}">{inner}</div>'
            '</body></html>')


def foot(i, n, note):
    return ('<div class="foot"><div><b>eric-twhub.github.io</b>'
            f'<span>{E(note)}</span></div>'
            f'<div class="pg">{i} / {n}</div></div>')


def md(d):
    return f'{int(d[5:7])}/{int(d[8:10])}'


def money(v):
    return f'NT${v:,}'


def build(d, today):
    n = 8
    lv = [p for p in d['leave'] if p['to'] >= today]
    ov = [o for o in d['overlaps'] if o['end'] >= today]
    fare = d['fare']
    cal_note = f'官方行事曆查證於 {d["checked"]}'
    out = []

    def best1(p):
        o = p['opts'].get('1') or p['opts'].get(1)
        return o['tot'] if o else p['base']

    # ── 1 封面 ──
    top = max(lv, key=lambda p: best1(p) - p['base']) if lv else None
    tw_pct = jp_pct = None
    if fare:
        for r in fare['rows']:
            if r['label'] == '只有台灣連假' and r['pct'] is not None:
                tw_pct = r['pct']
            if r['label'] == '只有日本連假' and r['pct'] is not None:
                jp_pct = r['pct']
    cover = ('<div class="kick">台灣・日本・中國</div>'
             '<h1>該避開的是<em>台灣的連假</em>，<br>不是日本的</h1>'
             '<div class="sub">用行政院人事行政總處與日本內閣府的官方行事曆逐日計算，'
             '請假排法不是手打的表。</div>'
             '<div class="stat">'
             f'<div><b>{len(ov)}</b><span>段三國撞期<br>還沒過</span></div>'
             f'<div><b>{len(lv)}</b><span>個台灣假期<br>可以排</span></div>'
             + (f'<div><b>+{tw_pct:.0f}%</b><span>台灣連假出發<br>機票中位價</span></div>'
                if tw_pct is not None else '')
             + (f'<div><b>{jp_pct:+.0f}%</b><span>只有日本連假<br>影響小得多</span></div>'
                if jp_pct is not None else '')
             + '</div>'
             + (f'<div class="note">投報率最高的一段是 {top["from"][:4]} 年的'
                f'<b>{E(top["name"])}</b>（{md(top["from"])}）：'
                f'本來只有 {top["base"]} 天，請 1 天假就變成 {best1(top)} 天。</div>'
                if top else '')
             + foot(1, n, cal_note))
    out.append(('hol-01.png', page(cover, 'cover')))

    # ── 2 價差實算 ──
    if fare:
        rows = ('<div class="hd"><div class="nm">出發日</div>'
                '<div class="med">中位票價</div><div class="pct">價差</div></div>'
                f'<div class="row"><div class="nm">平常日<s>{fare["base_n"]} 筆</s></div>'
                f'<div class="med">{money(fare["base_median"])}</div>'
                '<div class="pct flat">基準</div></div>')
        for r in fare['rows']:
            if r['median'] is None:
                rows += (f'<div class="row"><div class="nm">{E(r["label"])}'
                         f'<s>{r["n"]} 筆</s></div>'
                         '<div class="med">—</div>'
                         '<div class="pct flat">樣本不足</div></div>')
                continue
            rows += (f'<div class="row"><div class="nm">{E(r["label"])}'
                     f'<s>{r["n"]} 筆</s></div>'
                     f'<div class="med">{money(r["median"])}</div>'
                     f'<div class="pct {"up" if r["pct"] > 0 else "flat"}">'
                     f'{r["pct"]:+.0f}%</div></div>')
        inner = ('<div class="kick">不是引用別人的統計</div>'
                 '<h1>台灣飛日本，<em>連假貴多少</em></h1>'
                 '<div class="sub">用本站當天抓到的票價，依「出發日」分組取中位數。</div>'
                 '<div class="legend">這是單日快照，不是長期統計，'
                 f'隔天重算數字就會變。產生於 {E(d["generated"])}。'
                 '樣本少於 10 筆的分組不給數字。</div>'
                 f'<div class="list">{rows}</div>'
                 + foot(2, n, f'票價快照 {E(d["generated"])}'))
        out.append(('hol-02.png', page(inner)))

    # ── 3 撞期 ──
    rows = ''
    for o in ov:
        who = '＋'.join(CN[c] for c in o['countries'])
        left = (datetime.date.fromisoformat(o['start'])
                - datetime.date.fromisoformat(today)).days
        rows += (f'<div class="row"><div class="nm">{md(o["start"])}–{md(o["end"])}'
                 f'<s>{o["start"][:4]}　{E("、".join(o["names"]))}</s></div>'
                 f'<div class="who">{E(who)}</div>'
                 f'<div class="d">{o["days"]}<small>天</small></div>'
                 f'<div class="d">{max(left, 0)}<small>天後</small></div></div>')
    inner = ('<div class="kick">兩國以上同時放長假</div>'
             f'<h1>接下來會<em>撞期</em>的 {len(ov)} 段</h1>'
             '<div class="sub">同一天有兩個以上國家在放三天以上的連假，'
             '機票與住宿會一起被推上去。</div>'
             '<div class="legend">單純的週六日不算，那不會造成額外的需求高峰。</div>'
             f'<div class="list">{rows}</div>' + foot(3, n, cal_note))
    out.append(('hol-03.png', page(inner)))

    # ── 4 請 1 天休最多 ──
    rank = sorted(lv, key=lambda p: (-(best1(p) - p['base']), p['from']))[:8]
    rows = ('<div class="hd"><div class="nm">假期</div>'
            '<div class="d">本來</div><div class="big">請 1 天</div></div>')
    for p in rank:
        rows += (f'<div class="row"><div class="nm">{E(p["name"])}'
                 f'<s>{p["from"][:4]}　{md(p["from"])}–{md(p["to"])}</s></div>'
                 f'<div class="d">{p["base"]}<small>天</small></div>'
                 f'<div class="big">{best1(p)}<small>天</small></div></div>')
    inner = ('<div class="kick">投報率最高的一天</div>'
             '<h1>只請 <em>1 天</em>，能休幾天</h1>'
             '<div class="sub">依「多出來的天數」排序。'
             '同樣請一天假，有的假期只多一天，有的多好幾天。</div>'
             '<div class="legend">同名的假期每年都有，日期那行有標年份，別看錯。</div>'
             f'<div class="list">{rows}</div>' + foot(4, n, cal_note))
    out.append(('hol-04.png', page(inner)))

    # ── 5、6 完整請假試算 ──
    def lv_card(idx, part, items):
        rows = ('<div class="hd"><div class="nm">假期</div>'
                '<div class="d">本來</div><div class="d">請1</div>'
                '<div class="d">請2</div><div class="d">請3</div>'
                '<div class="d">請4</div></div>')
        for p in items:
            cells = ''
            for L in ('1', '2', '3', '4'):
                o = p['opts'].get(L)
                tot = o['tot'] if o else None
                good = tot is not None and tot >= p['base'] + int(L) + 2
                cells += (f'<div class="d{" up" if good else ""}">'
                          + (str(tot) if tot else '—') + '</div>')
            rows += (f'<div class="row"><div class="nm">{E(p["name"])}'
                     f'<s>{p["from"][:4]}　{md(p["from"])}–{md(p["to"])}</s></div>'
                     f'<div class="d">{p["base"]}</div>{cells}</div>')
        return ('<div class="kick">請幾天，連休幾天</div>'
                f'<h1>完整排法 <em>{part}</em></h1>'
                '<div class="sub">橫著看就知道多請一天划不划算。單位都是天。</div>'
                '<div class="legend">橘色是「多請的那幾天換到更多連休」的排法，'
                '也就是投報率高的。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, n, cal_note))

    half = (len(lv) + 1) // 2
    out.append(('hol-05.png', page(lv_card(5, '①', lv[:half]))))
    out.append(('hol-06.png', page(lv_card(6, '②', lv[half:]))))

    # ── 7、8 各國的連假 ──
    def runs_card(idx, key, title, sub):
        rs = [r for r in d['runs'].get(key, []) if r['end'] >= today][:9]
        rows = ('<div class="hd"><div class="nm">日期</div>'
                '<div class="d">天數</div></div>')
        for r in rs:
            nm = '、'.join(r['names']) if r['names'] else '純週末'
            rows += (f'<div class="row"><div class="nm">'
                     f'{md(r["start"])}–{md(r["end"])}'
                     f'<s>{r["start"][:4]}　{E(nm)}</s></div>'
                     f'<div class="d">{r["days"]}<small>天</small></div></div>')
        return ('<div class="kick">接下來的連假</div>'
                f'<h1>{title}</h1>'
                f'<div class="sub">{sub}</div>'
                f'<div class="list">{rows}</div>' + foot(idx, n, cal_note))

    out.append(('hol-07.png', page(runs_card(
        7, 'jp', '<em>日本</em>接下來的連假',
        '日本放假影響的是你到了之後的住宿與國內交通，不是機票。'))))
    out.append(('hol-08.png', page(runs_card(
        8, 'tw', '<em>台灣</em>接下來的連假',
        '這才是機票漲價的主因。想省機票，先避開這幾段。'))))
    return out


def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.note,.stat,.hd")];'
        'const b=it.length?Math.max(...it.map(e=>e.getBoundingClientRect().bottom)):0;'
        'return{gap:Math.round(f-b)}})())</script></body>'))
    r = subprocess.run([chrome, '--headless', '--disable-gpu', '--dump-dom',
                        '--virtual-time-budget=1500', f'file://{os.path.abspath(probe)}'],
                       capture_output=True, text=True, timeout=60)
    m = re.search(r'<title>(\{.*?\})</title>', r.stdout)
    if not m:
        print(f'   ! {name} 量不到版面，略過檢查')
        return
    gap = json.loads(htm.unescape(m.group(1)))['gap']
    if gap < 0:
        sys.exit(f'{name}：內容超出頁尾 {-gap}px，會被切掉。請減少筆數或縮小字級')
    print(f'   {name}  底部餘裕 {gap}px')


def main():
    if not os.path.exists(SRC):
        sys.exit(f'找不到 {SRC}。那是 gen.py 產生的，先跑過建置（或 git pull）再來。')
    d = json.load(open(SRC, encoding='utf-8'))
    if not d.get('fare'):
        print('   注意：資料檔裡沒有票價（本機跑 gen.py 沒有 scan 資料），'
              '價差那張會略過。要完整的八張請先 git pull 取 CI 產生的版本。')
    chrome = _chrome()
    os.makedirs(OUT, exist_ok=True)
    cards = build(d, datetime.date.today().isoformat())
    with tempfile.TemporaryDirectory() as tmp:
        for name, src in cards:
            check(chrome, tmp, name, src)
            f = os.path.join(tmp, name + '.html')
            open(f, 'w', encoding='utf-8').write(src)
            png = os.path.join(OUT, name)
            subprocess.run([chrome, '--headless', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', f'--window-size={W},{H}',
                            f'--screenshot={os.path.abspath(png)}',
                            f'file://{os.path.abspath(f)}'],
                           capture_output=True, timeout=90)
            if not os.path.exists(png):
                sys.exit(f'{name} 沒有產生出來')
    open(os.path.join(OUT, 'stamp.txt'), 'w').write(fingerprint(d))
    print(f'完成 {len(cards)} 張，輸出到 {OUT}/')


if __name__ == '__main__':
    main()
