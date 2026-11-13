# -*- coding: utf-8 -*-
"""各店刷哪張卡的分享圖卡（1080×1350，4:5）。

資料來源是 cards.json 與 coupons.json，算法要和 gen.py 的店家頁
「刷多少，哪張卡拿最多」完全一樣，不然圖上和站上會對不起來。
四個過濾一個都不能少：新戶層、sold_out、store_scope、cat_scope。

版面、CSS、頁尾、溢出檢查都跟 make_creditcard_cards.py 借，
那邊改了這邊跟著變。

用法：python3 make_shoprank_cards.py
輸出：japan-coupon/rank-cards/rank-<店家 slug>.png，一家店一張
"""
import json, os, re, sys, subprocess, tempfile, hashlib
import html as htm

from make_creditcard_cards import (W, H, E, CSS, page, foot, _chrome)

# 自己一個資料夾：gen.py 的圖卡過期檢查是逐資料夾讀 stamp.txt，
# 和 make_coupon_cards 共用 japan-coupon/cards 會把對方的指紋蓋掉。
OUT = os.path.join('japan-coupon', 'rank-cards')
YEN = (10000, 30000, 50000)
NEW = re.compile(r'新戶|核卡')
MARK = ('①', '②', '③')

# .grp 的三行名次要有自己的標記顏色，其餘沿用 make_creditcard_cards 的 CSS
# 一家店一張，九個名次加條件都要塞進同一頁，所以把 grp 收緊，
# 條件另外用單行的 .cond，不用 .step（一張兩行太高，五張就滿了）。
EXTRA = """
.grp{padding:11px 0}
.grp b{font-size:27px;margin-bottom:5px}
.grp b i{font-weight:500;font-size:23px}
.grp s{font-size:23px;line-height:1.62}
.grp s em{font-style:normal;color:#c2410c;font-weight:800;margin-right:9px}
.sub b{color:#1a1a1a}
.ch{font-size:22px;color:#8a847c;font-weight:700;letter-spacing:.04em;
 margin-top:20px;padding-bottom:7px;border-bottom:2px solid #1a1a1a}
.cond div{padding:9px 0;border-bottom:1px solid #e5e3de;font-size:22px;
 line-height:1.55;color:#63605c}
.cond div:last-child{border-bottom:0}
.cond b{color:#1a1a1a;font-weight:700;font-size:25px}
.cond em{font-style:normal;color:#c2410c;font-weight:800}
"""


def rank_page(inner, cls=''):
    return page(inner, cls).replace('</style>', EXTRA + '</style>')


def tier_state(c, t, st, catmap):
    """這一層在這家店成不成立：yes／no／unknown。與 gen.py 的 _tier_state 同一套。"""
    if 'store_scope' in t and st['slug'] not in t['store_scope']:
        return 'no'
    tags = t.get('cat_scope')
    if not tags:
        return 'yes'
    out = []
    for x in tags:
        m = catmap.get(c['slug'], {}).get(x)
        if m is None:
            sys.exit(f'cards.json：{c["slug"]} 的 cat_scope「{x}」沒有逐店判定，'
                     f'圖卡會把它當成到處都拿得到')
        if m.get('unknown_all'):
            out.append('unknown')
        elif st['slug'] in m.get('yes', []):
            out.append('yes')
        elif st['slug'] in m.get('unknown', []):
            out.append('unknown')
        else:
            out.append('no')
    return 'yes' if 'yes' in out else ('unknown' if 'unknown' in out else 'no')


def shop_tiers(c, st, catmap):
    """既有卡友在這家店實際拿得到的加碼層。四個過濾一次套完。"""
    return [t for t in c['tiers']
            if t['scope'] in ('shop', 'any')
            and not NEW.search(t['label'] + t.get('cond', ''))
            and not t.get('sold_out')
            and tier_state(c, t, st, catmap) == 'yes']


def rank_at(CD, st, jpy, mid, fee, catmap):
    b = jpy * mid * (1 + fee / 100)
    out = []
    for c in CD['cards']:
        ts = shop_tiers(c, st, catmap)
        nb = any(t.get('no_base') for t in ts)
        v = 0 if nb else c['base'] / 100 * b
        capped = False
        for t in ts:
            x = t['rate'] / 100 * b
            if t['cap'] and x > t['cap']:
                x, capped = t['cap'], True
            v += x
        out.append({'c': c, 'v': v, 'capped': capped,
                    'rate': round((0 if nb else c['base'])
                                  + sum(t['rate'] for t in ts), 2)})
    out.sort(key=lambda x: -x['v'])
    return b, out


def money(n):
    return f'NT${round(n):,}'


def check(chrome, tmp, name, src):
    """量最後一個區塊的底部有沒有撞到頁尾。

    和 make_creditcard_cards.check 同一套，只是多量 .cond 與 .ch，
    那兩個是這支自己的區塊，不加進去就等於沒量到條件那一段。
    """
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.grp,.step,.note,.stat,'
        '.hd,.cond div,.ch")];'
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
        sys.exit(f'{name}：內容超出頁尾 {-gap}px，會被切掉')
    print(f'   {name}  底部餘裕 {gap}px')


def store_card(CD, st, mid, fee, catmap, i, n, rate_note):
    """一家店一張：三個金額各前三名，底下是那幾張卡的條件與沒做滿的數字。"""
    rows, picked = '', {}
    for y in YEN:
        b, ranked = rank_at(CD, st, y, mid, fee, catmap)
        top = ranked[:3]
        li = ''
        for k, r in enumerate(top):
            picked[r['c']['slug']] = r
            li += (f'<em>{MARK[k]}</em>{E(r["c"]["name"])}　'
                   f'{money(r["v"])}・{r["rate"]:g}%'
                   + ('（加碼已滿）' if r['capped'] else '') + '<br>')
        rows += (f'<div class="grp"><b>刷 ¥{y:,}<i>　帳單約 {money(b)}</i></b>'
                 f'<s>{li.rstrip("<br>")}</s></div>')

    # 第一名會不會隨金額換人，是這張卡唯一的「新聞」，沒有就不要硬掰
    firsts = [rank_at(CD, st, y, mid, fee, catmap)[1][0]['c'] for y in YEN]
    if len({x['slug'] for x in firsts}) > 1:
        lead = (f'刷 ¥{YEN[0]:,} 是{E(firsts[0]["name"])}，'
                f'刷到 ¥{YEN[-1]:,} 要換成{E(firsts[-1]["name"])}。')
    else:
        lead = f'{E(firsts[0]["name"])}三個金額都第一。'

    cond = ''
    for r in sorted(picked.values(), key=lambda x: -x['rate']):
        c = r['c']
        cond += (f'<div><b>{E(c["name"])}</b>　{E(c.get("reg_short") or "官方沒寫")}'
                 f'　<em>{r["rate"]:g}%</em>，沒做滿只剩 {c["base"]:g}%</div>')

    inner = ('<div class="kick">旅日購物</div>'
             # 「在Bic Camera」中文字緊貼西文很醜，開頭是半形就補一個空格
             + f'<h1>在{" " if st["name"][0].isascii() else ""}{E(st["name"])}'
               f'<br><em>刷哪張卡</em></h1>'
             f'<div class="sub"><b>{lead}</b></div>'
             f'<div class="list">{rows}'
             '<div class="ch">這幾張卡要做什麼，沒做滿剩多少</div>'
             f'<div class="cond">{cond}</div></div>'
             + foot(i, n, rate_note))
    return rank_page(inner)


def build(CD, CP, mid, fee, catmap, rate_note):
    sts = CP['stores']
    n = len(sts)
    return [(f'rank-{st["slug"]}.png',
             store_card(CD, st, mid, fee, catmap, i, n, rate_note))
            for i, st in enumerate(sts, 1)]

def fingerprint(CD):
    """gen.py 的過期檢查只會餵 cards.json，店家清單自己讀。"""
    CP = json.load(open('coupons.json', encoding='utf-8'))
    pay = [[c.get(k) for k in ('name', 'slug', 'base', 'reg_short')]
           + [[t['label'], t['rate'], t['cap'], t['scope'], t.get('sold_out'),
               t.get('store_scope'), t.get('cat_scope'), t.get('no_base')]
              for t in c['tiers']]
           for c in CD['cards']]
    pay.append([s['slug'] for s in CP['stores']])
    pay.append(CD.get('_cat_scope_map'))
    return hashlib.sha1(json.dumps(pay, ensure_ascii=False,
                                   sort_keys=True).encode('utf-8')).hexdigest()[:12]


def main():
    CD = json.load(open('cards.json', encoding='utf-8'))
    CP = json.load(open('coupons.json', encoding='utf-8'))
    ap = json.load(open('apple.json', encoding='utf-8')) if os.path.exists('apple.json') else {}
    mid = (ap.get('rate', {}).get('jpy_twd_mid')
           or ap.get('rate', {}).get('jpy_twd') or 0.205)
    fee = CD['fx_fee']['typical']
    catmap = CD.get('_cat_scope_map', {})
    rate_note = (f'日圓標價　匯率 {mid} ＋ 手續費 {fee:g}%　'
                 f'條件查證於 {CD["checked"]}')
    chrome = _chrome()
    os.makedirs(OUT, exist_ok=True)
    cards = build(CD, CP, mid, fee, catmap, rate_note)
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
    open(os.path.join(OUT, 'stamp.txt'), 'w').write(fingerprint(CD))
    print(f'完成 {len(cards)} 張，輸出到 {OUT}/')


if __name__ == '__main__':
    main()
