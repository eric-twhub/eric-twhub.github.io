# -*- coding: utf-8 -*-
"""旅平險的分享圖卡。骨架見 cardkit.py。不掛在每日 workflow 上。

用法：python3 make_insurance_cards.py
輸出：japan-travel-insurance/cards/ins-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'japan-travel-insurance/cards'
N = 6

# 矩陣要在一張卡裡塞六欄，另外給一組窄欄位
CSS = """
.mx{display:flex;gap:6px;align-items:stretch;padding:11px 0;
 border-bottom:1px solid #e5e3de;font-size:22px}
.mx:last-child{border-bottom:0}
.mx .c{flex:1 1 auto;font-weight:700;font-size:24px;line-height:1.3}
.mx u{flex:0 0 108px;text-decoration:none;text-align:center;font-size:26px;
 font-weight:800;color:#2f8f4f}
.mx u.n{color:#c9c4bc;font-weight:500}
.mxh{display:flex;gap:6px;padding:0 0 8px;border-bottom:2px solid #1a1a1a;
 font-size:19px;color:#8a847c}
.mxh .c{flex:1 1 auto}
.mxh u{flex:0 0 108px;text-decoration:none;text-align:center;line-height:1.3}
"""


def build(d):
    fn = f'條文引金管會示範條款與保險局手冊，查證於 {d["checked"]}'
    mx, inc, nhi = d['matrix'], d['inconvenience'], d['nhi']
    out = []

    cover = ('<div class="kick">旅平險</div>'
             '<h1>這三個字底下<br><em>是三種東西</em></h1>'
             f'<div class="sub">{E(d["thesis"])}</div>'
             '<div class="stat">'
             '<div><b>3</b><span>層保障<br>賠的情況不同</span></div>'
             f'<div><b>{len(mx["rows"])}</b><span>種情況<br>逐格對照</span></div>'
             '<div><b>4</b><span>小時<br>不便險的延誤門檻</span></div>'
             '<div><b>70%</b><span>非健保身分<br>只賠這麼多</span></div></div>'
             '<div class="note">最常見的誤解：以為刷機票送的那份保全程。'
             '它只保你<b>在飛機上</b>，以及往返機場的那幾個小時。</div>'
             + foot(1, N, fn))
    out.append(('ins-01.png', page(cover, 'cover', CSS)))

    rows = ''.join(
        f'<div class="blk"><b><i>{l["n"]}</i>{E(l["name"])}</b>'
        f'<s><b style="display:inline">保障期間</b>　{E(l["when"])}<br>'
        f'{E(l["body"])}</s></div>' for l in d['layers'])
    inner = ('<div class="kick">三層分別保什麼</div>'
             '<h1>只有<em>主約</em>是全程</h1>'
             f'<div class="list">{rows}</div>' + foot(2, N, fn))
    out.append(('ins-02.png', page(inner, '', CSS)))

    hdr = ('<div class="mxh"><div class="c">情況</div>'
           + ''.join(f'<u>{E(c)}</u>' for c in mx['cols'][1:]) + '</div>')
    rows = ''
    for r in mx['rows']:
        rows += ('<div class="mx"><div class="c">' + E(r['case']) + '</div>'
                 + ''.join(f'<u class="{"" if v == "○" else "n"}">{E(v)}</u>'
                           for v in r['v']) + '</div>')
    inner = ('<div class="kick">同一件事，誰賠誰不賠</div>'
             f'<h1>{len(mx["rows"])} 種情況<em>對照</em></h1>'
             f'<div class="sub">{E(mx["note"])}</div>'
             f'<div class="legend">{E("　".join(mx["legend"][:3]))}</div>'
             f'<div class="list">{hdr}{rows}</div>' + foot(3, N, fn))
    out.append(('ins-03.png', page(inner, '', CSS)))

    rows = ('<div class="hd"><div class="nm">項目</div>'
            '<div class="v" style="flex-basis:430px">理賠門檻</div></div>')
    for r in inc['rows']:
        rows += (f'<div class="row"><div class="nm">{E(r["item"])}</div>'
                 f'<div class="v" style="flex-basis:430px;font-size:23px;'
                 f'font-weight:500;color:#3f3b37">{E(r["threshold"])}</div></div>')
    inner = (f'<div class="kick">{E(inc["title"])}</div>'
             '<h1>不便險<em>看的是門檻</em></h1>'
             f'<div class="sub">{E(inc["body"])}</div>'
             f'<div class="legend">{E(inc["key"])}</div>'
             f'<div class="list">{rows}</div>' + foot(4, N, fn))
    out.append(('ins-04.png', page(inner, '', CSS)))

    rows = ''
    for r in nhi['rows']:
        rows += (f'<div class="row"><div class="nm">{E(str(r["item"]))}</div>'
                 f'<div class="v">{E(str(r["amt"]))}</div></div>')
    inner = (f'<div class="kick">{E(nhi["title"])}</div>'
             '<h1>健保<em>也會退一點</em></h1>'
             f'<div class="sub">{E(nhi["body"])}</div>'
             f'<div class="legend">核退上限依季度公告，這是 {E(str(nhi["period"]))}。'
             f'{E(nhi["key"])}</div>'
             f'<div class="list">{rows}</div>' + foot(5, N, fn))
    out.append(('ins-05.png', page(inner, '', CSS)))

    rows = ''.join(
        f'<div class="blk"><b><i>?</i>'
        + E(u['what'] if isinstance(u, dict) else str(u)) + '</b>'
        + (f'<s>{E(u["why"])}</s>' if isinstance(u, dict) and u.get('why') else '')
        + '</div>' for u in d['unverified'])
    inner = ('<div class="kick">這頁的範圍</div>'
             '<h1>這頁<em>不是保險建議</em></h1>'
             f'<div class="sub">{E(d["disclaimer"])}</div>'
             f'<div class="list">{rows}</div>' + foot(6, N, fn))
    out.append(('ins-06.png', page(inner, '', CSS)))
    return out


# 指紋要讓 gen.py import 得到才有用。原本寫成 K.run() 裡的 lambda，
# 藏在 if __name__ 區塊底下，gen.py 抓不到，圖卡過期的提醒就不會響。
def payload(d):
    """圖卡真正用到的欄位。改了這些才需要重跑，其他欄位變動不算。"""
    return [d['layers'], d['matrix'], d['inconvenience']['rows'],
            d['nhi']['rows'], d['checked'], d['thesis']]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    K.run('travel-insurance.json', OUT, build, payload)
