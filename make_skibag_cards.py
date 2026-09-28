# -*- coding: utf-8 -*-
"""雪具託運規則的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML、版面高度用量的、
寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

用法：python3 make_skibag_cards.py
輸出：japan-ski-baggage/cards/bag-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-ski-baggage', 'cards')
SRC = 'ski.json'
E = htm.escape
BAG_LO, BAG_HI = 150, 170       # 市售雪板袋的常見長度
SCALE = 240                     # 條圖的滿格公分數，樂桃 230 要放得下


def fingerprint(d):
    pay = [[a.get(k) for k in ('name', 'code', 'cls', 'total_cm', 'side_cm',
                               'max_kg', 'call_short', 'fee_short', 'side_short')]
           for a in d['airlines']]
    pay.append([[t['title'], t['short']] for t in d['traps']])
    pay.append([d['checked'], d['pending']])
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
.row{display:flex;gap:12px;align-items:baseline;padding:14px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.nm{flex:1 1 auto;font-size:30px;font-weight:700;line-height:1.28}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px}
.v{flex:0 0 132px;text-align:right;font-size:26px;color:#63605c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.v b{color:#1a1a1a}
.side{flex:0 0 168px;text-align:right;font-size:28px;font-weight:800;
 font-variant-numeric:tabular-nums;white-space:nowrap;color:#c4563a}
.side.ok{color:#2f8f4f}
.side.none{color:#b4afa8;font-weight:500;font-size:23px}
.side small{display:block;font-size:18px;font-weight:500;color:#8a847c;margin-top:3px}
/* 長度條圖 */
.brow{padding:13px 0;border-bottom:1px solid #e5e3de}
.brow:last-child{border-bottom:0}
.brow b{display:block;font-size:27px;margin-bottom:8px}
.brow b i{font-style:normal;font-size:21px;color:#8a847c;font-weight:500;margin-left:10px}
.bar{position:relative;height:30px;background:#e9e6e1;border-radius:5px}
.bar u{position:absolute;left:0;top:0;bottom:0;border-radius:5px;text-decoration:none}
.bar em{position:absolute;top:-4px;bottom:-4px;border-left:3px dashed #1a1a1a;
 font-style:normal}
.bar span{position:absolute;right:10px;top:0;line-height:30px;font-size:19px;
 font-weight:700;color:#1a1a1a}
.tight u{background:#d9633f}.roomy u{background:#3f8f5f}
.blk{padding:15px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:30px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c4563a;margin-right:10px}
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


def build(d):
    n = 8
    air = d['airlines']
    lcc = [a for a in air if a['cls'] == 'lcc']
    fsc = [a for a in air if a['cls'] == 'fsc']
    sided = [a for a in air if a['side_cm']]
    lo = min(sided, key=lambda a: a['side_cm'])
    fnote = f'九家航空的條款逐項對過官網，查證於 {d["checked"]}'
    out = []

    # ── 1 封面 ──
    tight = [a for a in sided if a['side_cm'] < BAG_LO]
    cover = ('<div class="kick">帶雪具去日本</div>'
             '<h1>卡住你的是<em>單邊長度</em>，<br>不是重量</h1>'
             f'<div class="sub">{len(air)} 家航空的條款逐項對過官網原文。'
             f'市售雪板袋多半 {BAG_LO}–{BAG_HI} 公分。</div>'
             '<div class="stat">'
             f'<div><b>{lo["side_cm"]}</b><span>公分<br>門檻最低（{E(lo["name"])}）</span></div>'
             f'<div><b>{len(tight)}</b><span>家的單邊門檻<br>裝不下一般板袋</span></div>'
             f'<div><b>{BAG_LO}–{BAG_HI}</b><span>公分<br>市售板袋長度</span></div>'
             f'<div><b>{len(air)}</b><span>家<br>逐條查證</span></div></div>'
             f'<div class="note">雪具幾乎都是<b>計入你原本的託運額度</b>，不是另外一筆。'
             f'買足重量之外，還要確認尺寸過得了。'
             f'{E(lo["name"])}在 737 機材寫明單邊超過 {lo["side_cm"]} 公分就要事先聯繫。</div>'
             + foot(1, n, fnote))
    out.append(('bag-01.png', page(cover, 'cover')))

    # ── 2 單邊長度條圖 ──
    rows = ''
    for a in sorted(sided, key=lambda a: a['side_cm']):
        w = min(a['side_cm'], SCALE) / SCALE * 100
        roomy = a['side_cm'] >= BAG_HI
        rows += (f'<div class="brow {"roomy" if roomy else "tight"}">'
                 f'<b>{E(a["name"])}<i>{E(a.get("side_short") or "單邊上限")}</i></b>'
                 f'<div class="bar"><u style="width:{w:.1f}%"></u>'
                 f'<em style="left:{BAG_LO / SCALE * 100:.1f}%"></em>'
                 f'<span>{a["side_cm"]} cm</span></div></div>')
    inner = ('<div class="kick">板袋放不放得進去</div>'
             '<h1>單邊長度上限 <em>vs</em> 板袋</h1>'
             f'<div class="sub">虛線是市售板袋的下限 {BAG_LO} 公分。'
             '條沒有超過虛線的，板袋就過不了。</div>'
             '<div class="legend">只有四家在官網寫明單邊上限，其餘幾家用總尺寸計價，'
             '見下一張。</div>'
             f'<div class="list">{rows}</div>' + foot(2, n, fnote))
    out.append(('bag-02.png', page(inner)))

    # ── 3、4 各家對照 ──
    def air_card(idx, title, items, sub):
        rows = ('<div class="hd"><div class="nm">航空公司</div>'
                '<div class="v">總尺寸</div><div class="v">重量</div>'
                '<div class="side">單邊上限</div></div>')
        for a in items:
            if a['side_cm']:
                cls = 'ok' if a['side_cm'] >= BAG_HI else ''
                sd = (f'<div class="side {cls}">{a["side_cm"]} cm'
                      + (f'<small>{E(a["side_short"])}</small>'
                         if a.get('side_short') else '') + '</div>')
            else:
                sd = '<div class="side none">官網未列</div>'
            rows += (f'<div class="row"><div class="nm">{E(a["name"])}'
                     f'<s>{E(a["code"])}・{"廉航" if a["cls"] == "lcc" else "一般航空"}</s></div>'
                     f'<div class="v">'
                     + (f'<b>{a["total_cm"]}</b> cm' if a['total_cm'] else '未列')
                     + '</div><div class="v">'
                     + (f'<b>{a["max_kg"]}</b> kg' if a['max_kg'] else '未列')
                     + f'</div>{sd}</div>')
        return ('<div class="kick">雪具託運對照</div>'
                f'<h1>{title}</h1>'
                f'<div class="sub">{sub}</div>'
                '<div class="legend">總尺寸為長＋寬＋高。單邊標綠色的表示容得下一般板袋。'
                '超過門檻不代表不能帶，多數是要事先申請。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, n, fnote))

    out.append(('bag-03.png', page(air_card(
        3, '廉價航空 <em>4 家</em>', lcc,
        '廉航的雪具多半併入你買的行李額度，但尺寸另有門檻。'))))
    out.append(('bag-04.png', page(air_card(
        4, '一般航空 <em>5 家</em>', fsc,
        '一般航空多半計入免費額度，超過總尺寸才開始加收。'))))

    # ── 5 三個會多付錢的地方 ──
    rows = ''.join(
        f'<div class="blk"><b><i>{i:02}</i>{E(t["title"])}</b>'
        f'<s>{E(t["short"])}<br><span style="color:#8a847c">'
        f'依據：{E(t["who"])}官網條款</span></s></div>'
        for i, t in enumerate(d['traps'], 1))
    inner = ('<div class="kick">最常被多收錢的三件事</div>'
             '<h1>三個會讓你<em>多付錢</em>的地方</h1>'
             f'<div class="list">{rows}</div>' + foot(5, n, fnote))
    out.append(('bag-05.png', page(inner)))

    # ── 6 要不要事先申請 ──
    rows = ''
    for a in sorted(air, key=lambda a: (a['call_short'].startswith('不用'), a['name'])):
        need = not a['call_short'].startswith('不用')
        rows += (f'<div class="row"><div class="nm">{E(a["name"])}'
                 f'<s>{"廉航" if a["cls"] == "lcc" else "一般航空"}</s></div>'
                 f'<div class="side {"" if need else "ok"}" style="flex-basis:430px">'
                 f'{E(a["call_short"])}</div></div>')
    noneed = [a['name'] for a in air if a['call_short'].startswith('不用')]
    inner = ('<div class="kick">沒先問而被拒載，機票錢不會退</div>'
             '<h1>哪幾家<em>要先打電話</em></h1>'
             f'<div class="sub">不必事先聯繫的只有 {E("、".join(noneed))}，'
             '它們把超尺寸做成可以線上加購的選項。</div>'
             f'<div class="list">{rows}</div>' + foot(6, n, fnote))
    out.append(('bag-06.png', page(inner)))

    # ── 7 費用怎麼算 ──
    rows = ''
    for a in sorted(air, key=lambda a: ('元' not in a['fee_short'], a['name'])):
        extra = '另外收錢' in a['fee_short'] or '元' in a['fee_short']
        rows += (f'<div class="row"><div class="nm">{E(a["name"])}'
                 + (f'<s>{E(a["fee_note"])}</s>' if a.get('fee_note') else '')
                 + '</div>'
                 f'<div class="side {"" if extra else "ok"}" style="flex-basis:430px">'
                 f'{E(a["fee_short"])}</div></div>')
    inner = ('<div class="kick">尺寸要不要另外付錢</div>'
             '<h1>費用<em>怎麼算</em></h1>'
             '<div class="sub">多數航空把雪具併入你原本的行李額度，'
             '只有樂桃與捷星日本是尺寸本身另外收一筆。</div>'
             '<div class="legend">那筆錢不含重量，還是要另外買足夠的重量額度。</div>'
             f'<div class="list">{rows}</div>' + foot(7, n, fnote))
    out.append(('bag-07.png', page(inner)))

    # ── 8 還沒查的 ──
    pend = d.get('pending') or []
    inner = ('<div class="kick">這頁的範圍</div>'
             f'<h1>還有 <em>{len(pend)} 家</em>沒查</h1>'
             f'<div class="sub">上面那 {len(air)} 家是逐條對過官網原文的。'
             '以下這幾家還沒查，與其抄第三方整理，不如先空著。</div>'
             '<div class="list">'
             f'<div class="blk"><b>尚未查證</b><s>{E("、".join(pend))}</s></div>'
             '<div class="blk"><b>查證方式</b>'
             '<s>每一家都以該航空官網的行李條款原文為準，'
             '不採用旅遊網站或部落格的整理。條款隨時可能調整，'
             '出發前請以航空公司官網為準。</s></div>'
             '<div class="blk"><b>最後一道關卡是現場</b>'
             '<s>雪具能否託運最終以航空公司現場判定為準。'
             '需要事先申請的沒先講，現場被拒載的話機票錢不會退。</s></div>'
             '</div>' + foot(8, n, fnote))
    out.append(('bag-08.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.blk,.brow,.note,.stat,.hd")];'
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
