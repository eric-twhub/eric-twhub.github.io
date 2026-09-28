# -*- coding: utf-8 -*-
"""日本租車 NOC 的分享圖卡。骨架見 cardkit.py。不掛在每日 workflow 上。

用法：python3 make_noc_cards.py
輸出：japan-rentacar-noc/cards/noc-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'japan-rentacar-noc/cards'
N = 6


def build(d):
    fn = f'條款逐家引官方頁面原文，查證於 {d["checked"]}'
    w, m, x = d['what'], d['math'], d['exclusions']
    out = []

    cover = ('<div class="kick">日本租車</div>'
             '<h1>買了免責補償，<br><em>不等於不用賠</em></h1>'
             f'<div class="sub">{E(d["thesis"])}</div>'
             '<div class="stat">'
             + ''.join(f'<div><b>{E(a["amt"].replace(" 円", ""))}</b>'
                       f'<span>円<br>{E(a["case"][:10])}</span></div>'
                       for a in d['amounts'][:2])
             + f'<div><b>{len(d["table"])}</b><span>家業者<br>逐家查官網</span></div>'
             '<div><b>14%</b><span>加購划算的<br>機率門檻</span></div></div>'
             f'<div class="note">{E(w["key"])}</div>'
             + foot(1, N, fn))
    out.append(('noc-01.png', page(cover, 'cover')))

    inner = (f'<div class="kick">{E(w["title"])}</div>'
             '<h1>它跟修車費、<br>跟免責補償<em>都是兩回事</em></h1>'
             f'<div class="sub">{E(w["body"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b>官方原文</b><s>{E(w["quote"])}</s></div>'
             f'<div class="blk"><b>中文</b><s>{E(w["quote_zh"])}</s></div>'
             f'<div class="blk"><b><i>!</i>重點在「汚損」與「清掃」</b>'
             f'<s>{E(w["key"])}</s></div>'
             '</div>' + foot(2, N, fn))
    out.append(('noc-02.png', page(inner)))

    rows = ''.join(f'<div class="row"><div class="nm">{E(a["case"])}</div>'
                   f'<div class="v bad">{E(a["amt"])}</div></div>'
                   for a in d['amounts'])
    inner = ('<div class="kick">三種情況，三種金額</div>'
             '<h1>NOC <em>要賠多少</em></h1>'
             '<div class="sub">不用撞車就會產生。這是豐田租車官網列的金額。</div>'
             f'<div class="list">{rows}</div>' + foot(3, N, fn))
    out.append(('noc-03.png', page(inner)))

    rows = ''.join(
        f'<div class="blk"><b>{E(t["name"])}</b>'
        f'<s><b style="display:inline">NOC</b>　{E(t["noc"])}<br>'
        f'<b style="display:inline">免責補償</b>　{E(t["cdw"])}<br>'
        f'<b style="display:inline">免除方案</b>　{E(t["waiver"])}<br>'
        f'{E(t["extra"])}</s></div>' for t in d['table'])
    inner = ('<div class="kick">三家全國性業者</div>'
             '<h1>免除方案<em>怎麼賣</em></h1>'
             f'<div class="list">{rows}</div>' + foot(4, N, fn))
    out.append(('noc-04.png', page(inner)))

    inner = (f'<div class="kick">{E(m["title"])}</div>'
             '<h1>加購划算的<br><em>機率門檻是 14%</em></h1>'
             f'<div class="sub">{E(m["body"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>=</i>算式</b><s>{E(m["rule"])}</s></div>'
             f'<div class="blk"><b><i>!</i>觸發門檻比想的低</b><s>{E(m["note"])}</s></div>'
             f'<div class="blk"><b><i>!</i>{E(x["title"])}</b><s>{E(x["body"])}</s></div>'
             f'<div class="blk"><b><i>!</i>丟在路邊那條，加購也照收</b>'
             f'<s>{E(x["also"])}</s></div>'
             '</div>' + foot(5, N, fn))
    out.append(('noc-05.png', page(inner)))

    rows = ''.join(f'<div class="blk"><b><i>·</i>{E(x["t"])}</b><s>{E(x["d"])}</s></div>'
                   for x in d['notes'])
    rows += ''.join(f'<div class="blk"><b><i>?</i>{E(u["what"])}</b><s>{E(u["why"])}</s></div>'
                    for u in d['unverified'])
    inner = ('<div class="kick">還有這幾條</div>'
             '<h1>沒報警<em>可能整個不賠</em></h1>'
             f'<div class="list">{rows}</div>' + foot(6, N, fn))
    out.append(('noc-06.png', page(inner)))
    return out


if __name__ == '__main__':
    K.run('rentacar-noc.json', OUT, build,
          lambda d: [d['amounts'], d['table'], d['notes'], d['checked'], d['thesis']])
