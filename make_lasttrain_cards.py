# -*- coding: utf-8 -*-
"""機場末班車的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML、版面高度用量的、
寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

時刻表會改點（京急與京成都是 2025-12-13 改正），卡片上印查證日，
改點後要重查 lasttrain.json 再重跑。

用法：python3 make_lasttrain_cards.py
輸出：japan-airport-last-train/cards/lt-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-airport-last-train', 'cards')
SRC = 'lasttrain.json'
E = htm.escape


def fingerprint(d):
    pay = []
    for a in d['airports']:
        pay.append([a['code'], a['name'], a.get('verdict'),
                    [[r.get('name'), r.get('to'), r.get('cut'), r.get('dep_wd'),
                      r.get('dep_hol')] for r in (a.get('rail') or [])],
                    [[b.get('name'), b.get('to'), b.get('cut')]
                     for b in (a.get('bus') or [])]])
    pay.append([d['checked'], d['rule']['steps']])
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
h1{font-size:56px;line-height:1.24;font-weight:800;letter-spacing:-.01em}
h1 em{font-style:normal;color:#c2410c}
.sub{font-size:27px;line-height:1.7;color:#63605c;margin-top:16px}
.legend{font-size:21px;color:#63605c;margin-top:9px;line-height:1.6}
.list{margin-top:24px;flex:1 1 auto;min-height:0}
.hd{display:flex;gap:12px;align-items:flex-end;padding:0 0 9px;
 font-size:20px;color:#8a847c;border-bottom:2px solid #1a1a1a}
.row{display:flex;gap:12px;align-items:baseline;padding:14px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.nm{flex:1 1 auto;font-size:29px;font-weight:700;line-height:1.3}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;line-height:1.55}
.t{flex:0 0 152px;text-align:right;font-size:34px;font-weight:800;
 font-variant-numeric:tabular-nums;white-space:nowrap;color:#c2410c}
.t small{display:block;font-size:19px;font-weight:600;color:#8a847c;margin-top:3px}
.t.late{color:#2f8f4f}
.t.none{color:#b4afa8;font-size:24px;font-weight:500}
.blk{padding:14px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:29px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c2410c;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.7}
.foot{flex:0 0 auto;padding:24px 0 42px;border-top:3px solid #1a1a1a;
 display:flex;justify-content:space-between;align-items:flex-end;margin-top:18px}
.foot b{font-size:28px;font-weight:800;display:block}
.foot span{font-size:22px;color:#63605c;display:block;margin-top:6px}
.pg{font-size:24px;color:#63605c;font-weight:700}
.cover{justify-content:center}
.cover .list{flex:0 0 auto;margin-top:0}
.stat{display:flex;gap:14px;margin-top:36px}
.stat div{flex:1;background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:22px 20px}
.stat b{display:block;font-size:44px;font-weight:800;color:#c2410c;line-height:1.1;
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


TIME = re.compile(r'(\d{1,2}):(\d{2})')


def mins(cut):
    """把 00:08 這種跨夜時刻換成「當日 24 時制」的分鐘數，方便排序。

    有些 cut 寫成「平日 22:07（往京成上野）／土休日 20:38」，取第一個時刻。
    """
    m = TIME.search(str(cut or ''))
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    v = h * 60 + mi
    return v + 24 * 60 if h < 4 else v


def split_cut(cut):
    """回傳（主要時刻, 註記）。

    有些 cut 寫成「平日 00:35／土休日 00:00」。把兩個時刻拆開，
    主欄位放平日、小字放土休日。整串塞進小字會讀成「平日是 00:00」。
    """
    s = str(cut or '')
    ts = TIME.findall(s)
    if not ts:
        return s, ''
    first = f'{ts[0][0]}:{ts[0][1]}'
    if '土休日' in s and len(ts) > 1:
        return first, f'土休日 {ts[1][0]}:{ts[1][1]}'
    m = TIME.search(s)
    return first, (s[:m.start()] + s[m.end():]).strip(' （）／/')


def best_rail(a):
    """最後一班能直接進市區的軌道車。"""
    c = [r for r in (a.get('rail') or []) if mins(r.get('cut')) is not None]
    return max(c, key=lambda r: mins(r['cut'])) if c else None


def best_bus(a):
    c = [b for b in (a.get('bus') or []) if mins(b.get('cut')) is not None]
    return max(c, key=lambda b: mins(b['cut'])) if c else None


def short_bus(name, airport_jp):
    """巴士名含機場名與營運業者，列表上兩者都是重複資訊，拿掉才放得下。"""
    t = re.sub(r'（[^）]*）\s*$', '', str(name or '')).strip()
    for k in (airport_jp, airport_jp.replace('空港', '機場'), '國際線航廈'):
        if k:
            t = t.replace(k, '')
    return re.sub(r'\s{2,}', ' ', t).strip(' →')


def build(d):
    n = 8
    air = d['airports']
    fnote = f'每一列都查官方時刻表，查證於 {d["checked"]}'
    out = []
    ranked = sorted(
        [a for a in air if best_rail(a)],
        key=lambda a: -mins(best_rail(a)['cut']))
    latest, earliest = ranked[0], ranked[-1]

    # ── 1 封面 ──
    cover = ('<div class="kick">紅眼班機落地之後</div>'
             '<h1>問題不在落地時間，<br><em>在末班車</em></h1>'
             f'<div class="sub">{len(air)} 個機場，每一班都查官方時刻表，'
             '不是換乘 App 的即時結果。</div>'
             '<div class="stat">'
             f'<div><b>{E(best_rail(latest)["cut"])}</b>'
             f'<span>最晚<br>{E(latest["name"])}</span></div>'
             f'<div><b>{E(best_rail(earliest)["cut"])}</b>'
             f'<span>最早收班<br>{E(earliest["name"])}</span></div>'
             f'<div><b>{len(air)}</b><span>個機場<br>逐班查證</span></div>'
             f'<div><b>{sum(len(a.get("bus") or []) for a in air)}</b>'
             '<span>條深夜巴士<br>電車來不及時</span></div></div>'
             '<div class="note">真正會卡住人的是兩件事：'
             '末班車常常<b>只開到中途站</b>，'
             '以及便宜的那條線通常<b>比貴的那條線早收班</b>。</div>'
             + foot(1, n, fnote))
    out.append(('lt-01.png', page(cover, 'cover')))

    # ── 2 七個機場的末班 ──
    rows = ('<div class="hd"><div class="nm">機場</div>'
            '<div class="t">最後一班進市區</div></div>')
    for a in ranked:
        r = best_rail(a)
        late = mins(r['cut']) >= 24 * 60
        tm, pre = split_cut(r['cut'])
        rows += (f'<div class="row"><div class="nm">{E(a["name"])}'
                 f'<s>{E(r["name"])}</s></div>'
                 f'<div class="t{" late" if late else ""}">{E(tm)}'
                 + f'<small>{E(pre or str(r.get("to") or ""))}</small>'
                 + '</div></div>')
    for a in air:
        if not best_rail(a):
            rows += (f'<div class="row"><div class="nm">{E(a["name"])}'
                     '<s>沒有直達市區的軌道運輸</s></div>'
                     '<div class="t none">見下</div></div>')
    inner = ('<div class="kick">最後一班能直接進市區的車</div>'
             '<h1>七個機場的<em>末班車</em></h1>'
             '<div class="sub">時刻是發車時刻，不是抵達時刻。'
             '綠色的是跨過午夜還有車。</div>'
             '<div class="legend">「進市區」指不用再轉車就到得了主要車站，'
             '之後的班次多半只開到中途站。'
             '有標「土休日」的，大字是平日、小字是週末與假日。</div>'
             f'<div class="list">{rows}</div>' + foot(2, n, fnote))
    out.append(('lt-02.png', page(inner)))

    # ── 3 怎麼用這張表 ──
    rows = ''.join(
        f'<div class="blk"><b><i>{i:02}</i>{E(s.split("。")[0])}</b>'
        + (f'<s>{E("。".join(s.split("。")[1:]).strip())}</s>'
           if len(s.split('。')) > 1 and s.split('。')[1].strip() else '')
        + '</div>'
        for i, s in enumerate(d['rule']['steps'], 1))
    inner = ('<div class="kick">' + E(d['rule']['title']) + '</div>'
             '<h1>落地到上車，<br><em>要留多久</em></h1>'
             f'<div class="list">{rows}</div>'
             + foot(3, n, fnote))
    out.append(('lt-03.png', page(inner)))

    # ── 4、5、6 各機場細節 ──
    def detail(idx, items):
        rows = ''
        for a in items:
            r, b = best_rail(a), best_bus(a)
            seg = []
            if r:
                seg.append(f'電車末班 {split_cut(r["cut"])[0]}　{r["name"]}')
            if b:
                seg.append(f'深夜巴士 {b.get("name", "")}')
            rows += (f'<div class="blk"><b>{E(a["name"])}'
                     f'<span style="font-weight:500;font-size:22px;color:#8a847c;'
                     f'margin-left:10px">{E(a["city"])}</span></b>'
                     f'<s>{E(a["verdict"])}</s>'
                     + (f'<s style="color:#c2410c;font-weight:600;margin-top:6px">'
                        f'{E("　·　".join(seg))}</s>' if seg else '')
                     + '</div>')
        return ('<div class="kick">落地之後還回得去嗎</div>'
                f'<h1>各機場的<em>實際狀況</em></h1>'
                f'<div class="list">{rows}</div>' + foot(idx, n, fnote))

    out.append(('lt-04.png', page(detail(4, air[:3]))))
    out.append(('lt-05.png', page(detail(5, air[3:5]))))
    out.append(('lt-06.png', page(detail(6, air[5:]))))

    # ── 7 深夜巴士 ──
    rows = ''
    for a in air:
        bs = a.get('bus') or []
        if not bs:
            continue
        for b in bs:
            rr = b.get('runs') or []
            last = max((x for x in rr if mins(x) is not None),
                       key=mins, default=None) if isinstance(rr, list) else None
            rows += (f'<div class="row">'
                     f'<div class="nm">{E(short_bus(b.get("name"), a.get("jp","")))}'
                     f'<s>{E(a["name"])}'
                     + (f'　共 {len(rr)} 班' if isinstance(rr, list) and rr else '')
                     + '</s></div>'
                     + (f'<div class="t">{E(split_cut(last)[0])}<small>末班</small></div>'
                        if last else '<div class="t none">時刻見官網</div>')
                     + '</div>')
    inner = ('<div class="kick">電車來不及的時候</div>'
             '<h1>還有<em>深夜巴士</em></h1>'
             '<div class="sub">巴士通常比電車晚，但班次少、要先確認搭車處。</div>'
             + f'<div class="legend">'
             + (('沒有查到深夜巴士的：'
                 + '、'.join(x['name'] for x in air if not (x.get('bus') or []))
                 + '。') if any(not (x.get('bus') or []) for x in air) else '')
             + '沒有標時刻的那幾條，官網只給 PDF 或未公布。</div>'
             f'<div class="list">{rows}</div>' + foot(7, n, fnote))
    out.append(('lt-07.png', page(inner)))

    # ── 8 還沒查的 ──
    items = d['pending']['items']
    rows = ''.join(
        f'<div class="blk"><b>{E(x["what"])}</b><s>{E(x["why"])}</s></div>'
        for x in items[:5])
    inner = ('<div class="kick">這頁的範圍</div>'
             f'<h1>還沒查到的 <em>{len(items)} 項</em></h1>'
             f'<div class="sub">{E(d["pending"]["_說明"])}</div>'
             '<div class="legend">時刻表會改點，京急與京成都是 2025-12-13 改正。'
             '出發前請以各業者官網為準。</div>'
             f'<div class="list">{rows}</div>' + foot(8, n, fnote))
    out.append(('lt-08.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.blk,.note,.stat,.hd")];'
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
    d = json.load(open(SRC, encoding='utf-8'))
    chrome = _chrome()
    os.makedirs(OUT, exist_ok=True)
    cards = build(d)
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
