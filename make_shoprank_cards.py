# -*- coding: utf-8 -*-
"""各店刷哪張卡的分享圖卡（1080×1350，4:5）。

資料來源是 cards.json 與 coupons.json，算法要和 gen.py 的店家頁
「刷多少，哪張卡拿最多」完全一樣，不然圖上和站上會對不起來。
四個過濾一個都不能少：新戶層、sold_out、store_scope、cat_scope。

版面、CSS、頁尾、溢出檢查都跟 make_creditcard_cards.py 借，
那邊改了這邊跟著變。

用法：python3 make_shoprank_cards.py
輸出：japan-coupon/rank-cards/rank-01.png … -05.png
"""
import json, os, re, sys, subprocess, tempfile, hashlib
import html as htm

from make_creditcard_cards import (W, H, E, CSS, page, foot, check, _chrome)

# 自己一個資料夾：gen.py 的圖卡過期檢查是逐資料夾讀 stamp.txt，
# 和 make_coupon_cards 共用 japan-coupon/cards 會把對方的指紋蓋掉。
OUT = os.path.join('japan-coupon', 'rank-cards')
YEN = (10000, 30000, 50000)
NEW = re.compile(r'新戶|核卡')
MARK = ('①', '②', '③')

# .grp 的三行名次要有自己的標記顏色，其餘沿用 make_creditcard_cards 的 CSS
EXTRA = """
.grp s em{font-style:normal;color:#c2410c;font-weight:800;margin-right:10px}
.grp b i{font-weight:500}
.sub b{color:#1a1a1a}
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


def groups(CD, CP, mid, fee, catmap):
    """把 22 家店按「三個金額的前三名完全相同」分組。

    分組是算出來的不是手列的：哪張卡的指定店家名單改了，組就跟著變，
    不會變成圖上寫 Bic 和唐吉訶德一組、實際上已經不是。
    """
    g = {}
    for st in CP['stores']:
        key, cols = [], []
        for y in YEN:
            b, rows = rank_at(CD, st, y, mid, fee, catmap)
            top = rows[:3]
            key.append(tuple(r['c']['slug'] for r in top))
            cols.append((y, b, top))
        g.setdefault(tuple(key), {'stores': [], 'cols': cols})['stores'].append(st)
    # 店家少的組排前面：那幾家才是「這家店特別不一樣」的重點
    return sorted(g.values(), key=lambda x: len(x['stores']))


def build(CD, CP, mid, fee, catmap, rate_note):
    gs = groups(CD, CP, mid, fee, catmap)
    n = len(gs) + 2
    out, picked = [], {}

    # ── 1 封面 ──
    flips = 0
    for g in gs:
        if len({c[2][0]['c']['slug'] for c in g['cols']}) > 1:
            flips += len(g['stores'])
    cover = ('<div class="kick">旅日購物</div>'
             '<h1>同一張卡，<br><em>不是每家店都最強</em></h1>'
             f'<div class="sub">{len(CP["stores"])} 家常去的店，各自算 '
             f'¥10,000、¥30,000、¥50,000 三個金額<br>該刷哪張卡。'
             f'答案分成 {len(gs)} 組，而且會隨金額換人。</div>'
             '<div class="stat">'
             f'<div><b>{len(CP["stores"])}</b><span>家店<br>逐家算</span></div>'
             f'<div><b>{len(gs)}</b><span>種答案<br>不是一張卡通吃</span></div>'
             f'<div><b>{flips}</b><span>家店的第一名<br>會隨金額換人</span></div>'
             '</div>'
             '<div class="note">回饋有上限，所以「％最高」不等於「拿最多」。'
             '中信 uniopen 的 11% 在台幣帳單 NT$6,250 就到頂，'
             '聯邦吉鶴的 8% 要刷到 NT$20,000，於是小額 uniopen 贏、'
             '大額換吉鶴。</div>'
             + foot(1, n, rate_note))
    out.append(('rank-01.png', rank_page(cover, 'cover')))

    # ── 2..k 每一組 ──
    for i, g in enumerate(gs, 2):
        names = '、'.join(s['name'] for s in g['stores'])
        rows = ''
        for y, b, top in g['cols']:
            li = ''
            for k, r in enumerate(top):
                picked[r['c']['slug']] = r
                li += (f'<em>{MARK[k]}</em>{E(r["c"]["name"])}　'
                       f'{money(r["v"])}・{r["rate"]:g}%'
                       + ('（加碼已滿）' if r['capped'] else '') + '<br>')
            rows += (f'<div class="grp"><b>刷 ¥{y:,}<i>　帳單約 {money(b)}</i></b>'
                     f'<s>{li.rstrip("<br>")}</s></div>')
        # 標題要講這一組的news，不是「有幾家店」。第一名會不會隨金額換人，
        # 是這組最值得單獨做一張的理由，不講出來等於白分組。
        firsts = [c[2][0]['c'] for c in g['cols']]
        flip = len({x['slug'] for x in firsts}) > 1
        if flip:
            h1 = (f'<h1>這 {len(g["stores"])} 家店<br>'
                  f'<em>大額要換一張卡</em></h1>')
            lead = (f'刷 ¥{YEN[0]:,} 是{E(firsts[0]["name"])}，'
                    f'刷到 ¥{YEN[-1]:,} 換成{E(firsts[-1]["name"])}。')
        else:
            h1 = (f'<h1>這 {len(g["stores"])} 家店<br>'
                  f'<em>三個金額同一張</em></h1>')
            lead = f'{E(firsts[0]["name"])}三個金額都第一。'
        inner = ('<div class="kick">旅日購物</div>'
                 + h1
                 + f'<div class="sub"><b>{lead}</b></div>'
                 + f'<div class="legend">{E(names)}</div>'
                 + f'<div class="list">{rows}</div>' + foot(i, n, rate_note))
        out.append((f'rank-{i:02}.png', rank_page(inner)))

    # ── 最後一張：條件 ──
    li = ''
    for r in sorted(picked.values(), key=lambda x: -x['rate']):
        c = r['c']
        li += ('<div class="grp">'
               f'<b>{E(c["name"])}<i>　做滿 {r["rate"]:g}%</i></b>'
               f'<s>{E(c.get("reg_short") or "官方沒寫")}。'
               f'沒做滿只剩基本回饋 {c["base"]:g}%。</s></div>')
    cond = ('<div class="kick">旅日購物</div>'
            '<h1>這些數字<br><em>都有前提</em></h1>'
            '<div class="sub">上面的％是把該做的事都做完才有。'
            '沒做的話掉到基本回饋，差距比選錯卡還大。</div>'
            f'<div class="list">{li}</div>'
            + foot(n, n, '以發卡行官方公告為準'))
    out.append((f'rank-{n:02}.png', rank_page(cond)))
    return out


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
