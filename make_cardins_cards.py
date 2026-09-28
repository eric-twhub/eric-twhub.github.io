# -*- coding: utf-8 -*-
"""信用卡附贈保險的分享圖卡。骨架見 cardkit.py。不掛在每日 workflow 上。

用法：python3 make_cardins_cards.py
輸出：japan-card-insurance/cards/ci-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'japan-card-insurance/cards'
N = 8
COLS = [('班機延誤', '延誤'), ('行李遺失', '行李'), ('行程取消或縮短', '取消')]


def wan(v):
    """理賠金額用「萬」表示，表格才塞得下。

    有幾格是文字（例如附註而非金額），照原樣顯示，不要硬當數字算。
    """
    if not v:
        return None
    if not isinstance(v, (int, float)):
        return str(v)[:8]
    return f'{v / 10000:g} 萬'


def build(d):
    fn = f'逐卡查發卡行條款，查證於 {d["checked"]}'
    cmp_ = d['comparison']
    cond = d['_十家共通的生效條件']
    out = []

    has_inc = [c for c in cmp_ if any(c.get(k) for k, _ in COLS)]
    no_inc = [c for c in cmp_ if not any(c.get(k) for k, _ in COLS)]

    cover = ('<div class="kick">刷卡送的保險</div>'
             '<h1>重點不是保額，<br><em>是它賠不賠</em></h1>'
             f'<div class="sub">{len(cmp_)} 張卡逐張查發卡行條款。'
             '保額大小很好比，真正會卡住你的是生效條件。</div>'
             '<div class="stat">'
             f'<div><b>{len(cmp_)}</b><span>張卡<br>逐張查證</span></div>'
             f'<div><b>{len(cond)}</b><span>條共通的<br>生效條件</span></div>'
             f'<div><b>{len(no_inc)}</b><span>張沒有<br>旅行不便險</span></div>'
             '<div><b>70%</b><span>非健保身分<br>只賠這麼多</span></div></div>'
             '<div class="note">最容易踩的一條：'
             '<b>必須用這張卡付清全部票款</b>。哩程換票只刷機場稅、'
             '用點數折抵、優惠票未達票面三成，十家一致不理賠。</div>'
             + foot(1, N, fn))
    out.append(('ci-01.png', page(cover, 'cover')))

    def table(idx, items, title, sub):
        rows = ('<div class="hd"><div class="nm">卡片</div>'
                + ''.join(f'<div class="v" style="flex-basis:118px">{E(s)}</div>'
                          for _, s in COLS) + '</div>')
        for c in items:
            rows += (f'<div class="row"><div class="nm">{E(c["name"])}'
                     f'<s>{E(c["bank"])}</s></div>'
                     + ''.join(
                         (f'<div class="v" style="flex-basis:118px">{wan(c.get(k))}</div>'
                          if c.get(k) else
                          '<div class="v z" style="flex-basis:118px">無</div>')
                         for k, _ in COLS) + '</div>')
        return ('<div class="kick">旅行不便險的三項</div>'
                f'<h1>{title}</h1>'
                f'<div class="sub">{sub}</div>'
                '<div class="legend">金額是保額上限，不是一定賠這麼多。'
                '各項都有自己的門檻與單據要求。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, N, fn))

    half = (len(has_inc) + 1) // 2
    out.append(('ci-02.png', page(table(
        2, has_inc[:half], '有不便險的卡 <em>①</em>',
        '班機延誤、行李遺失、行程取消，這三項最常用到。'))))
    out.append(('ci-03.png', page(table(
        3, has_inc[half:], '有不便險的卡 <em>②</em>', '同一組欄位。'))))

    rows = ''.join(f'<div class="row"><div class="nm">{E(c["name"])}'
                   f'<s>{E(c["bank"])}'
                   + (f'　{E(c["note"])}' if c.get('note') else '')
                   + '</s></div>'
                   f'<div class="v z">沒有不便險</div></div>' for c in no_inc)
    inner = ('<div class="kick">有些卡只有身故失能與傷害醫療</div>'
             f'<h1>這 <em>{len(no_inc)} 張</em><br>沒有旅行不便險</h1>'
             '<div class="sub">班機延誤、行李遺失這些最常遇到的狀況，'
             '這幾張刷了也沒有。</div>'
             f'<div class="list">{rows}</div>' + foot(4, N, fn))
    out.append(('ci-04.png', page(inner)))

    # 七條的說明都不短，一張塞不下（實測超出 200px），拆成兩張。
    items = list(cond.items())
    for j, part in enumerate((items[:4], items[4:]), 0):
        rows = ''.join(
            f'<div class="blk"><b><i>{i:02}</i>{E(k)}</b><s>{E(v)}</s></div>'
            for i, (k, v) in enumerate(part, 1 + j * 4))
        inner = ('<div class="kick">十家一致的規則</div>'
                 f'<h1>保險生效的<em> {len(items)} 個條件 '
                 f'{"①" if j == 0 else "②"}</em></h1>'
                 + ('<div class="sub">這些不是單一銀行自訂，是十家都這樣寫。'
                    '任何一條沒滿足，保額再高都用不到。</div>' if j == 0 else '')
                 + f'<div class="list">{rows}</div>' + foot(5 + j, N, fn))
        out.append((f'ci-0{5 + j}.png', page(inner)))

    共 = d['_共通條款']
    rows = ''
    for k, v in 共.items():
        body = v.get('結論', '') if isinstance(v, dict) else str(v)
        extra = ''
        if isinstance(v, dict):
            if v.get('佐證'):
                extra = '　'.join(v['佐證'][:2])
            if v.get('但書'):
                extra = (extra + '　' if extra else '') + v['但書']
        rows += (f'<div class="blk"><b><i>·</i>{E(k)}</b>'
                 f'<s>{E(body)}' + (f'<br>{E(extra)}' if extra else '') + '</s></div>')
    inner = ('<div class="kick">兩條常被當成單一銀行規定的</div>'
             '<h1>其實是<em>共通條款</em></h1>'
             f'<div class="list">{rows}</div>' + foot(7, N, fn))
    out.append(('ci-07.png', page(inner)))

    rows = ''.join(
        f'<div class="blk"><b><i>?</i>'
        + E(u['what'] if isinstance(u, dict) else str(u)) + '</b>'
        + (f'<s>{E(u["why"])}</s>' if isinstance(u, dict) and u.get('why') else '')
        + '</div>' for u in d['unverified'][:4])
    inner = ('<div class="kick">這頁的範圍</div>'
             f'<h1>還沒查到的 <em>{len(d["unverified"])} 件</em></h1>'
             '<div class="sub">條款用語各家不同，查不到明文的就不寫成結論。</div>'
             f'<div class="list">{rows}</div>' + foot(8, N, fn))
    out.append(('ci-08.png', page(inner)))
    return out


if __name__ == '__main__':
    K.run('card-insurance.json', OUT, build,
          lambda d: [d['comparison'], list(d['_十家共通的生效條件'].items()),
                     d['checked']])
