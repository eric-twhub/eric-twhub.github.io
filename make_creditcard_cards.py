# -*- coding: utf-8 -*-
"""旅日信用卡的分享圖卡（1080×1350，4:5）。

和 make_picks_cards.py 同一套做法：Chrome headless 算繪 HTML，版面高度用量的不是目測的。
**不掛在每日 workflow 上**，卡片條件變動時在本機重跑。

這裡的回饋計算刻意和 gen.py 的 _back／_hit／_maxrate 同一套公式（gen.py 約 1010 行起）。
兩邊各有一份是重複，但 gen.py 一 import 就會跑完整個網站，沒辦法只借那幾個函式。
改動任一邊時兩邊都要改，數字有沒有對上可以拿線上的比較表核對
（「加碼刷到多少到頂」那一欄）。

用法：python3 make_creditcard_cards.py
輸出：japan-credit-card/cards/jp-card-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-credit-card', 'cards')
E = htm.escape

# 用來試算的消費金額。¥50,000 剛好落在多數加碼上限開始咬人的位置，
# 帳面和實際的差距在這裡最看得出來。
DEMO_JPY = 50000
LADDER = (10000, 30000, 50000, 100000, 200000)
# 判斷這一層是不是只有新戶拿得到
NEW = re.compile(r'新戶|核卡')


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
.list{margin-top:26px;flex:1 1 auto;min-height:0}
.hd{display:flex;gap:12px;align-items:flex-end;padding:0 0 9px;
 font-size:20px;color:#8a847c;border-bottom:2px solid #1a1a1a}
.row{display:flex;gap:12px;align-items:baseline;padding:15px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.num{flex:0 0 44px;font-size:23px;font-weight:700;color:#c2410c;
 font-variant-numeric:tabular-nums}
.nm{flex:1 1 auto;font-size:31px;font-weight:700;line-height:1.28;letter-spacing:-.01em}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;letter-spacing:0}
.c1{flex:0 0 108px;text-align:right;font-size:26px;color:#63605c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.c2{flex:0 0 132px;text-align:right;font-size:28px;font-weight:700;color:#c2410c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.c3{flex:0 0 152px;text-align:right;font-size:23px;color:#63605c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.c2 small,.c1 small{font-size:18px;font-weight:500;color:#8a847c;margin-left:2px}
.c2 s{display:block;text-decoration:none;font-size:19px;font-weight:600;margin-top:4px}
.warn{color:#c4563a}
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
.grp{padding:16px 0;border-bottom:1px solid #e5e3de}
.grp:last-child{border-bottom:0}
.grp b{display:block;font-size:30px;font-weight:700;margin-bottom:7px}
.grp b i{font-style:normal;color:#c2410c;margin-left:8px;font-size:25px}
.grp s{display:block;text-decoration:none;font-size:23px;color:#63605c;line-height:1.65}
.step{padding:15px 0;border-bottom:1px solid #e5e3de;display:flex;gap:16px}
.step:last-child{border-bottom:0}
.step i{font-style:normal;flex:0 0 44px;font-size:24px;font-weight:800;color:#c2410c}
.step div{flex:1 1 auto}
.step b{display:block;font-size:29px;margin-bottom:5px}
.step span{display:block;font-size:23px;color:#63605c;line-height:1.65}
"""


def page(inner, cls=''):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS}</style></head><body><div class="card {cls}">{inner}</div>'
            '</body></html>')


def foot(i, n, note='條件逐張查證，各附發卡行官方來源'):
    return ('<div class="foot"><div><b>eric-twhub.github.io</b>'
            f'<span>{E(note)}</span></div>'
            f'<div class="pg">{i} / {n}</div></div>')


# ── 回饋計算（與 gen.py 同一套公式）────────────────────────────
def make_math(CD, mid, fee):
    def bill(jpy):
        return jpy * mid * (1 + fee / 100)

    def tiers(c, scope, newbie=True):
        out = []
        for t in c['tiers']:
            if t['scope'] not in (scope, 'any'):
                continue
            if not newbie and NEW.search(t['label'] + t.get('cond', '')):
                continue
            out.append(t)
        return out

    def back(c, jpy, scope='shop', newbie=True):
        b = bill(jpy)
        v = c['base'] / 100 * b
        capped = False
        for t in tiers(c, scope, newbie):
            x = t['rate'] / 100 * b
            if t['cap'] and x > t['cap']:
                x = t['cap']
                capped = True
            v += x
        return v, capped

    def maxrate(c, scope='shop', newbie=True):
        return round(c['base'] + sum(t['rate'] for t in tiers(c, scope, newbie)), 2)

    def hit(c, scope='shop'):
        ts = [t for t in tiers(c, scope) if t['cap']]
        return round(min(t['cap'] / (t['rate'] / 100) for t in ts)) if ts else 0

    return bill, tiers, back, maxrate, hit


def build(CD, mid, fee, rate_note):
    bill, tiers, back, maxrate, hit = make_math(CD, mid, fee)
    cards = CD['cards']
    n = 8
    demo_bill = bill(DEMO_JPY)
    out = []

    def rate_txt(v):
        return f'{v:g}%'

    # 依「刷 DEMO_JPY 實際拿到多少」排序，這才是讀者真正會拿到的順序
    ranked = sorted(cards, key=lambda c: -back(c, DEMO_JPY)[0])
    newbie_gap = [c for c in cards if maxrate(c) != maxrate(c, newbie=False)]

    # ── 1 封面 ──
    top_paper = max(cards, key=lambda c: c['total'])
    top_real = ranked[0]
    cover = ('<div class="kick">旅日信用卡</div>'
             f'<h1>帳面最高 {top_paper["total"]:g}%，<br><em>實際刷下去不是</em></h1>'
             f'<div class="sub">{len(cards)} 張卡逐張查發卡行官方條件。'
             f'帳面數字幾乎都是多層加碼疊出來的，<br>而每一層都有自己的上限與門檻。</div>'
             '<div class="stat">'
             f'<div><b>{len(cards)}</b><span>張卡<br>逐張查證</span></div>'
             f'<div><b>{top_paper["total"]:g}%</b><span>帳面最高<br>（{E(top_paper["name"])}）</span></div>'
             f'<div><b>{maxrate(top_paper, newbie=False):g}%</b>'
             f'<span>同一張卡<br>老客戶只有</span></div>'
             f'<div><b>{len(newbie_gap)}</b><span>張的帳面<br>含新戶限定</span></div></div>'
             f'<div class="note">實際刷 ¥{DEMO_JPY:,}（帳單約 NT${demo_bill:,.0f}）'
             f'回饋最高的是<b>{E(top_real["name"])}</b>，'
             f'拿得到 NT${back(top_real, DEMO_JPY)[0]:,.0f}。'
             f'那不是帳面第一名的那張。</div>' + foot(1, n))
    out.append(('jp-card-01.png', page(cover, 'cover')))

    # ── 2、3 帳面 vs 實際 ──
    def rank_card(idx, part, items, start):
        rows = ('<div class="hd"><div class="num"></div><div class="nm">卡片</div>'
                '<div class="c1">帳面</div>'
                f'<div class="c2">刷 ¥{DEMO_JPY // 1000}K 實拿</div>'
                '<div class="c3">加碼到頂</div></div>')
        for j, c in enumerate(items, start):
            v, capped = back(c, DEMO_JPY)
            h = hit(c)
            rows += (f'<div class="row"><div class="num">{j:02}</div>'
                     f'<div class="nm">{E(c["name"])}<s>{E(c["plan"])}</s></div>'
                     f'<div class="c1">{rate_txt(c["total"])}</div>'
                     f'<div class="c2">{v:,.0f}<small>元</small></div>'
                     f'<div class="c3{" warn" if capped else ""}">'
                     + (f'NT${h:,}' if h else '無上限') + '</div></div>')
        return ('<div class="kick">旅日信用卡</div>'
                f'<h1>實拿排行 <em>{part}</em></h1>'
                f'<div class="sub">依「刷 ¥{DEMO_JPY:,} 實際拿到多少」排序，不是依帳面。</div>'
                '<div class="legend">「加碼到頂」是加碼額度用完的台幣帳單金額，'
                '超過之後只剩基本回饋。標紅色的表示這筆已經觸頂。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, n))

    out.append(('jp-card-02.png', page(rank_card(2, '①', ranked[:8], 1))))
    out.append(('jp-card-03.png', page(rank_card(3, '②', ranked[8:], 9))))

    # ── 4 新戶加碼 ──
    rows = ''
    for c in sorted(newbie_gap, key=lambda c: -(maxrate(c) - maxrate(c, newbie=False))):
        old = maxrate(c, newbie=False)
        nb = [t for t in c['tiers'] if NEW.search(t['label'] + t.get('cond', ''))]
        cond = nb[0].get('cond', '') if nb else ''
        rows += ('<div class="grp">'
                 f'<b>{E(c["name"])}<i>{rate_txt(c["total"])} → {rate_txt(old)}</i></b>'
                 f'<s>{E(cond[:80])}</s></div>')
    inner = ('<div class="kick">帳面數字裡的陷阱</div>'
             '<h1>有 <em>{}</em> 張的帳面<br>算進了新戶加碼'.format(len(newbie_gap)) + '</h1>'
             '<div class="sub">新戶加碼是核卡後一段期間內的一次性優惠。'
             '已經有這張卡的人，帳面數字要先扣掉這一層。</div>'
             f'<div class="list">{rows}</div>' + foot(4, n))
    out.append(('jp-card-04.png', page(inner)))

    # ── 5 刷多少決定用哪張 ──
    rows = ('<div class="hd"><div class="num"></div><div class="nm">日幣消費</div>'
            '<div class="c2">回饋最高的卡</div><div class="c3">有效回饋率</div></div>')
    for y in LADDER:
        best = max(cards, key=lambda c: back(c, y)[0])
        v = back(best, y)[0]
        b = bill(y)
        # 這幾張的第一名幾乎都帶條件，不標出來會看起來像人人有獎
        tag = []
        if maxrate(best) != maxrate(best, newbie=False):
            tag.append('含新戶加碼')
        if best.get('reg_level') == 'race':
            tag.append('要搶登錄')
        rows += ('<div class="row"><div class="num"></div>'
                 f'<div class="nm">¥{y:,}<s>帳單約 NT${b:,.0f}</s></div>'
                 f'<div class="c2" style="flex-basis:330px">{E(best["name"])}'
                 + (f'<s class="warn">{E("、".join(tag))}</s>' if tag else '')
                 + '</div>'
                 f'<div class="c3">{v / b * 100:.1f}%<small> NT${v:,.0f}</small></div></div>')
    inner = ('<div class="kick">同一張卡，刷越多越不划算</div>'
             '<h1>刷多少，<em>決定該用哪張</em></h1>'
             '<div class="sub">加碼有上限，所以「最划算的卡」會隨金額換人，'
             '有效回饋率也一路往下掉。</div>'
             '<div class="legend">有效回饋率＝實拿回饋 ÷ 台幣帳單。'
             '同樣是全部加碼成立，金額越大越接近基本回饋。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n))
    out.append(('jp-card-05.png', page(inner)))

    # ── 6 登錄門檻 ──
    LV = [('race', '要搶限量登錄', '每月固定時間開放，額滿為止。沒搶到就只有基本回饋。'),
          ('reg', '要登錄，但不限量', '活動期間內登錄一次即可，不用跟人搶。'),
          ('setup', '要在 App 切換或設定', '多數是消費當日就要在正確的狀態，事後補切沒有用。'),
          ('none', '不用登錄', '直接刷就算。')]
    rows = ''
    for k, lab, why in LV:
        ns = [c['name'] for c in cards if c.get('reg_level') == k]
        if not ns:
            continue
        rows += ('<div class="grp">'
                 f'<b>{E(lab)}<i>{len(ns)} 張</i></b>'
                 f'<s>{E("、".join(ns))}<br>{E(why)}</s></div>')
    inner = ('<div class="kick">拿不到回饋，多半是卡在這</div>'
             '<h1>哪幾張<em>要先登錄</em></h1>'
             '<div class="sub">回饋條件寫得再好，沒登錄就是只有基本回饋。</div>'
             f'<div class="list">{rows}</div>' + foot(6, n))
    out.append(('jp-card-06.png', page(inner)))

    # ── 7 交通卡儲值 ──
    tr = [(c, maxrate(c, 'transit')) for c in cards if tiers(c, 'transit')]
    tr.sort(key=lambda x: -x[1])
    rows = ('<div class="hd"><div class="num"></div><div class="nm">卡片</div>'
            '<div class="c2">儲值回饋</div></div>')
    for j, (c, r) in enumerate(tr, 1):
        lbl = '／'.join(t['label'] for t in tiers(c, 'transit'))
        ro = maxrate(c, 'transit', newbie=False)
        # 新戶那層 scope 是 any，會被算進儲值回饋。不標出來，老客戶會以為自己也有。
        note = f'{E(lbl[:30])}' + (f'　老客戶 {rate_txt(ro)}' if ro != r else '')
        rows += (f'<div class="row"><div class="num">{j:02}</div>'
                 f'<div class="nm">{E(c["name"])}<s>{note}</s></div>'
                 f'<div class="c2">{rate_txt(r)}</div></div>')
    inner = ('<div class="kick">Suica、PASMO、ICOCA</div>'
             f'<h1>儲值也有加碼的<br><em>只有 {len(tr)} 張</em></h1>'
             '<div class="sub">多數卡的海外加碼只認實體消費，交通卡儲值不算。'
             '這幾張有另外列出儲值加碼。</div>'
             '<div class="legend">儲值加碼多半另有單筆金額門檻與登錄限量，'
             '刷之前先看該卡的活動頁。</div>'
             f'<div class="list">{rows}</div>' + foot(7, n))
    out.append(('jp-card-07.png', page(inner)))

    # ── 8 五個關鍵動作 ──
    STEPS = [
        ('先確認這個月登錄了沒',
         '需要搶登錄的卡每月固定時間開放，額滿為止，沒登錄到就只有基本回饋。'),
        ('該切換的當天就要切',
         '在 App 切換權益方案的卡，看的是消費當日的狀態，事後補切沒有用。'),
        ('結帳一律選日圓',
         '選台幣是 DCC，匯率通常差 3 到 5%，而且多數銀行的海外加碼要求以外幣結帳。'),
        ('要面對面刷',
         '多數海外加碼限定當地實體商店的面對面交易，海外訂房平台、網購、訂閱常被排除。'),
        ('把加碼額度留給貴的東西',
         '加碼上限換算下來通常是一萬多元台幣，先刷小額會把額度用在回饋最少的地方。'),
    ]
    rows = ''.join(f'<div class="step"><i>{i:02}</i><div><b>{E(t)}</b>'
                   f'<span>{E(s)}</span></div></div>'
                   for i, (t, s) in enumerate(STEPS, 1))
    inner = ('<div class="kick">照著做卻拿不到，通常是這五件</div>'
             '<h1>怎麼<em>真的拿到</em>這些回饋</h1>'
             f'<div class="list">{rows}</div>'
             + foot(8, n, rate_note))
    out.append(('jp-card-08.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    """量最後一列的底部有沒有超過頁尾頂端。被切掉的圖用看的不一定看得出來。"""
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.grp,.step,.note,.stat,.hd")];'
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
    CD = json.load(open('cards.json', encoding='utf-8'))
    ap = json.load(open('apple.json', encoding='utf-8')) if os.path.exists('apple.json') else {}
    mid = (ap.get('rate', {}).get('jpy_twd_mid')
           or ap.get('rate', {}).get('jpy_twd') or 0.205)
    fee = CD['fx_fee']['typical']
    rate_note = f'匯率 {mid} ＋ 國外交易手續費 {fee:g}%　條件查證於 {CD["checked"]}'
    chrome = _chrome()
    os.makedirs(OUT, exist_ok=True)
    cards = build(CD, mid, fee, rate_note)
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
    print(f'完成 {len(cards)} 張，輸出到 {OUT}/')


if __name__ == '__main__':
    main()
