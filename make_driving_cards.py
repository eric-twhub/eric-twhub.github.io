# -*- coding: utf-8 -*-
"""台灣駕照在日本開車的分享圖卡。骨架見 cardkit.py。不掛在每日 workflow 上。

用法：python3 make_driving_cards.py
輸出：japan-driving-licence/cards/dl-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'japan-driving-licence/cards'
N = 6


def build(d):
    fn = f'引日本台灣交流協會與公路局原文，查證於 {d["checked"]}'
    c, p, ap, fg = d['core'], d['period'], d['apply'], d['forgot']
    out = []

    cover = ('<div class="kick">台灣駕照在日本開車</div>'
             '<h1>國際駕照<em>不能用</em></h1>'
             f'<div class="sub">{E(d["thesis"])}</div>'
             '<div class="stat">'
             '<div><b>3</b><span>樣文件<br>缺一不可</span></div>'
             '<div><b>9</b><span>人以下<br>你的譯本只到這</span></div>'
             '<div><b>1</b><span>年<br>入境後能開多久</span></div>'
             '<div><b>100</b><span>元・1 小時<br>臨櫃辦譯本</span></div></div>'
             f'<div class="note">{E(c["quote_zh"])}</div>'
             + foot(1, N, fn))
    out.append(('dl-01.png', page(cover, 'cover')))

    rows = ''.join(f'<div class="row"><div class="no">{b["n"]:02}</div>'
                   f'<div class="nm">{E(b["what"])}<s>{E(b["note"])}</s></div></div>'
                   for b in d['bring'])
    inner = ('<div class="kick">缺一樣就租不到車</div>'
             '<h1>要帶的<em>三樣</em></h1>'
             '<div class="sub">法規上的最低要求。個別租車公司可能另有規定。</div>'
             f'<div class="list">{rows}</div>' + foot(2, N, fn))
    out.append(('dl-02.png', page(inner)))

    rows = ''.join(f'<div class="blk"><b><i>!</i>{E(t["title"])}</b>'
                   f'<s>{E(t["body"])}</s></div>' for t in d['traps'])
    inner = ('<div class="kick">商家跟部落格幾乎都沒講</div>'
             '<h1>兩個會讓你<br><em>當場租不到車</em>的細節</h1>'
             f'<div class="list">{rows}</div>' + foot(3, N, fn))
    out.append(('dl-03.png', page(inner)))

    inner = (f'<div class="kick">{E(p["title"])}</div>'
             '<h1>入境後 <em>1 年內</em></h1>'
             f'<div class="sub">{E(p["rule"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>·</i>離境再入境會重新起算</b>'
             f'<s>{E(p["reentry"])}</s></div>'
             f'<div class="blk"><b><i>!</i>超過就是無照駕駛</b>'
             f'<s>{E(p["quote_zh"])}　官方原文：{E(p["quote"])}</s></div>'
             '</div>' + foot(4, N, fn))
    out.append(('dl-04.png', page(inner)))

    rows = ('<div class="hd"><div class="nm">辦法</div>'
            '<div class="v">規費</div><div class="v">時間</div></div>')
    for r in ap['rows']:
        rows += (f'<div class="row"><div class="nm">{E(r["way"])}'
                 f'<s>{E(r["doc"])}</s></div>'
                 f'<div class="v">{E(r["fee"])}</div>'
                 f'<div class="v">{E(r["time"])}</div></div>')
    inner = (f'<div class="kick">{E(ap["title"])}</div>'
             '<h1>三種辦法，<em>臨櫃最快</em></h1>'
             '<div class="sub">只有指定機關發的譯本才算數，自己翻譯或旅行社代翻無效。</div>'
             f'<div class="legend">{E(ap["expired"])}</div>'
             f'<div class="list">{rows}</div>' + foot(5, N, fn))
    out.append(('dl-05.png', page(inner)))

    rows = ''.join(f'<div class="blk"><b><i>·</i>{E(x["t"])}</b><s>{E(x["d"])}</s></div>'
                   for x in d['notes'])
    inner = ('<div class="kick">辦好之後</div>'
             '<h1>不用每次去<em>都重辦</em></h1>'
             f'<div class="sub">{E(fg["body"][:74])}</div>'
             f'<div class="list">{rows}</div>' + foot(6, N, fn))
    out.append(('dl-06.png', page(inner)))
    return out


# 指紋要讓 gen.py import 得到才有用。原本寫成 K.run() 裡的 lambda，
# 藏在 if __name__ 區塊底下，gen.py 抓不到，圖卡過期的提醒就不會響。
def payload(d):
    """圖卡真正用到的欄位。改了這些才需要重跑，其他欄位變動不算。"""
    return [d['bring'], [t['title'] for t in d['traps']], d['apply']['rows'],
            d['notes'], d['checked'], d['thesis']]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    K.run('jp-driving.json', OUT, build, payload)
