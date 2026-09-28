# -*- coding: utf-8 -*-
"""去日本會動到錢包的新制度，分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML、版面高度用量的、
寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

用法：python3 make_rules_cards.py
輸出：japan-travel-rules/cards/rule-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-travel-rules', 'cards')
SRC = 'japan-rules.json'
E = htm.escape
# 住宿稅試算用的房價（純住宿費、未稅）
DEMO = [6000, 10000, 18000, 30000]


def fingerprint(d):
    pay = [d['departure_tax']['old'], d['departure_tax']['new'],
           d['departure_tax']['from'],
           [[c['name'], c['mode'], c.get('exempt_below'), c.get('tiers'), c.get('rate')]
            for c in d['lodging_tax']['cities']],
           [[r['n'], r['t'], r['penalty']] for r in d['power_bank']['rules']],
           d['quarantine']['outbound']['penalty'],
           [[m['claim'], m['verdict']] for m in d['quarantine']['myths']],
           [list(x) for x in d['quarantine']['tw_items']],
           d['checked']]
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
.nm{flex:1 1 auto;font-size:29px;font-weight:700;line-height:1.28}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px}
.v{flex:0 0 128px;text-align:right;font-size:27px;font-weight:700;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.v.z{color:#b4afa8;font-weight:500}
.mark{flex:0 0 62px;text-align:center;font-size:30px}
.blk{padding:14px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:30px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c2410c;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.7}
.tag{display:inline-block;font-size:19px;padding:2px 10px;border-radius:999px;
 background:#e5e3de;color:#63605c;margin-left:10px;vertical-align:4px;font-weight:600}
.tag.bad{background:#f3ded6;color:#a8442a}
.foot{flex:0 0 auto;padding:24px 0 42px;border-top:3px solid #1a1a1a;
 display:flex;justify-content:space-between;align-items:flex-end;margin-top:18px}
.foot b{font-size:28px;font-weight:800;display:block}
.foot span{font-size:22px;color:#63605c;display:block;margin-top:6px}
.pg{font-size:24px;color:#63605c;font-weight:700}
.cover{justify-content:center}
.cover .list{flex:0 0 auto;margin-top:0}
.stat{display:flex;gap:14px;margin-top:36px}
.stat div{flex:1;background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:22px 20px}
.stat b{display:block;font-size:42px;font-weight:800;color:#c2410c;line-height:1.1;
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


def short_name(name):
    """表頭用的短名。原名帶括號註記（例如「東京都（2027/4/1 起）」），
    直接截斷會變成「東京都（2」，看不出是什麼。"""
    m = re.match(r'(.{2,3})[都府縣市]?（(\d{4})/(\d{1,2})', name)
    if m:
        return f'{m.group(1)} {m.group(2)[2:]}/{int(m.group(3))}'
    return name


def lodging(c, price):
    """某地某房價的每人每晚住宿稅。純住宿費、未稅。"""
    if price < (c.get('exempt_below') or 0):
        return 0
    if c['mode'] == 'rate':
        return round(price * c['rate'] / 100)
    for lo, hi, amt in c['tiers']:
        if price >= lo and (hi is None or price < hi):
            return amt
    return 0


def build(d):
    n = 8
    dt = d['departure_tax']
    cities = d['lodging_tax']['cities']
    pb = d['power_bank']
    q = d['quarantine']
    fnote = f'每一條都讀官方原文，查證於 {d["checked"]}'
    out = []
    up = int(dt['new']) - int(dt['old'])

    # ── 1 封面 ──
    pen_n = sum(1 for r in pb['rules'] if r['penalty'])
    cover = ('<div class="kick">去日本前</div>'
             '<h1>四條新制，<br><em>都會動到你的錢包</em></h1>'
             '<div class="sub">出境稅、住宿稅、行動電源、肉製品檢疫。'
             '每一條都讀官方原文，不採用社群整理。</div>'
             '<div class="stat">'
             f'<div><b>¥{int(dt["new"]):,}</b>'
             f'<span>出境稅<br>{dt["from"]} 起</span></div>'
             f'<div><b>+¥{up:,}</b><span>比以前多<br>約 NT$400 一人</span></div>'
             f'<div><b>{len(cities)}</b><span>套住宿稅<br>算法各不同</span></div>'
             f'<div><b>{pen_n}</b><span>條行動電源規定<br>違反有罰則</span></div></div>'
             '<div class="note">出境稅看的是<b>發券日</b>，不是出發日。'
             f'{dt["from"][:4]}/6/30 之前開票的，就算出發日在 7 月之後，'
             f'仍然只收 ¥{int(dt["old"]):,}。</div>'
             + foot(1, n, fnote))
    out.append(('rule-01.png', page(cover, 'cover')))

    # ── 2 出境稅 ──
    rows = ''.join(
        f'<div class="blk"><b><i>{i:02}</i>{E(p["t"])}</b><s>{E(p["d"])}</s></div>'
        for i, p in enumerate(dt['points'], 1))
    inner = ('<div class="kick">社群上兩種說法都有人講</div>'
             f'<h1>出境稅 <em>¥{int(dt["old"]):,} → ¥{int(dt["new"]):,}</em></h1>'
             f'<div class="sub">{E(dt["name"])}，{dt["from"]} 起實施。'
             '官方文件講得很清楚，但有一條過渡措施很多人沒注意到。</div>'
             f'<div class="list">{rows}</div>' + foot(2, n, fnote))
    out.append(('rule-02.png', page(inner)))

    # ── 3 住宿稅算法 ──
    rows = ''
    for c in cities:
        if c['mode'] == 'rate':
            how = f'房價的 {c["rate"]:g}%'
        else:
            seg = []
            for lo, hi, amt in c['tiers']:
                seg.append(f'¥{lo:,} 起 ¥{amt}' if hi is None
                           else f'¥{lo:,}–{hi:,} 收 ¥{amt}')
            how = '　'.join(seg)
        ex = c.get('exempt_below') or 0
        rows += (f'<div class="blk"><b>{E(c["name"])}'
                 f'<span class="tag">{E(c["status"])}</span></b>'
                 f'<s>{E(how)}'
                 + (f'<br>未滿 ¥{ex:,} 免稅' if ex else '<br>沒有免稅門檻')
                 + '</s></div>')
    inner = ('<div class="kick">四個地區，五套算法</div>'
             '<h1>住宿稅<em>怎麼算</em></h1>'
             f'<div class="sub">{E(d["lodging_tax"]["_課稅基礎共通"])}</div>'
             f'<div class="list">{rows}</div>' + foot(3, n, fnote))
    out.append(('rule-03.png', page(inner)))

    # ── 4 住宿稅實算 ──
    rows = ('<div class="hd"><div class="nm">純住宿費</div>'
            + ''.join(f'<div class="v">{E(short_name(c["name"]))}</div>'
                       for c in cities)
            + '</div>')
    for p in DEMO:
        rows += (f'<div class="row"><div class="nm">¥{p:,}</div>'
                 + ''.join(
                     (f'<div class="v">¥{lodging(c, p):,}</div>' if lodging(c, p)
                      else '<div class="v z">免稅</div>') for c in cities)
                 + '</div>')
    inner = ('<div class="kick">同樣的房價，各地差很多</div>'
             '<h1>住宿稅<em>實算</em></h1>'
             '<div class="sub">每人每晚。以純住宿費計算，不含餐費與消費稅。</div>'
             '<div class="legend">京都沒有免稅門檻，再便宜也要課；'
             '東京現行制度未滿 ¥10,000 不課，2027/4 起改成房價的 3%。'
             '稅通常現場收，訂房網站已代收就不必重複付。</div>'
             f'<div class="list">{rows}</div>' + foot(4, n, fnote))
    out.append(('rule-04.png', page(inner)))

    # ── 5 行動電源 ──
    rows = ''
    for r in pb['rules']:
        rows += (f'<div class="row"><div class="mark">'
                 + ('⚠️' if r['penalty'] else '·') + '</div>'
                 f'<div class="nm">{E(r["t"])}'
                 + (f'<s>{E(r["d"])}</s>' if r.get('d') else '')
                 + '</div></div>')
    inner = ('<div class="kick">' + E(pb['from']) + ' 起</div>'
             f'<h1>行動電源的 <em>{len(pb["rules"])} 條</em>新規</h1>'
             f'<div class="sub">標 ⚠️ 的 {sum(1 for r in pb["rules"] if r["penalty"])} 條'
             '違反有罰則，其餘是建議。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n, fnote))
    out.append(('rule-05.png', page(inner)))

    # ── 6 肉製品：流傳的數字是錯的 ──
    rows = ''.join(
        f'<div class="blk"><b>「{E(m["claim"])}」'
        f'<span class="tag bad">{E(m["verdict"])}</span></b>'
        f'<s>{E(m["fact"])}</s></div>' for m in q['myths'])
    inner = ('<div class="kick">兩個方向都會被罰</div>'
             '<h1>肉製品：流傳的<br><em>數字是錯的</em></h1>'
             f'<div class="sub">帶去日本：{E(q["outbound"]["penalty"])}。'
             f'帶回台灣：{E(q["inbound"]["penalty"])}。</div>'
             f'<div class="list">{rows}</div>' + foot(6, n, fnote))
    out.append(('rule-06.png', page(inner)))

    # ── 7 哪些帶得了 ──
    rows = ''.join(
        f'<div class="row"><div class="mark">{E(x[1])}</div>'
        f'<div class="nm">{E(x[0])}<s>{E(x[2])}</s></div></div>'
        for x in q['tw_items'])
    inner = ('<div class="kick">出發時放進行李就已經違規</div>'
             '<h1>這些<em>帶不帶得了</em></h1>'
             '<div class="sub">台灣人最常帶的幾樣。出境入境兩個方向都適用，'
             '不是只有回程要注意。</div>'
             f'<div class="list">{rows}</div>' + foot(7, n, fnote))
    out.append(('rule-07.png', page(inner)))

    # ── 8 這頁沒涵蓋的 ──
    rows = ''.join(
        f'<div class="blk"><b>{E(u["what"])}</b><s>{E(u["why"])}</s></div>'
        for u in d['unverified'])
    inner = ('<div class="kick">這頁的範圍</div>'
             f'<h1>還沒查的 <em>{len(d["unverified"])} 件</em></h1>'
             '<div class="sub">有住宿稅的自治體不只這四個。'
             '這幾件沒查到官方公告，就不寫。</div>'
             f'<div class="list">{rows}</div>' + foot(8, n, fnote))
    out.append(('rule-08.png', page(inner)))
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
