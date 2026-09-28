# -*- coding: utf-8 -*-
"""訂房比價方法論的分享圖卡。骨架見 cardkit.py。不掛在每日 workflow 上。

用法：python3 make_pricecheck_cards.py
輸出：hotel-price-check/cards/pc-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'hotel-price-check/cards'
N = 7


def build(d):
    fn = f'同日同房型的對照實測，查證於 {d["checked"]}'
    dev, plat, ch, ck = d['device'], d['platforms'], d['channels'], d['checklist']
    sm = d['sample']
    out = []

    cover = ('<div class="kick">訂房比價</div>'
             '<h1>換個裝置，<br><em>價格就不一樣</em></h1>'
             f'<div class="sub">{E(dev["finding"])}</div>'
             '<div class="stat">'
             f'<div><b>{len(plat["rows"])}</b><span>個通路<br>同日同房型</span></div>'
             f'<div><b>{len(dev["rows"])}</b><span>組裝置<br>對照實測</span></div>'
             f'<div><b>{sm["nights"]}</b><span>晚<br>{E(str(sm["city"]))}</span></div>'
             f'<div><b>{len(ck)}</b><span>個檢查點<br>訂之前跑一次</span></div></div>'
             f'<div class="note">{E(sm["note"])}</div>'
             + foot(1, N, fn))
    out.append(('pc-01.png', page(cover, 'cover')))

    # 裝置價差：Booking 同房型的桌機 vs 手機
    rows = ('<div class="hd"><div class="nm">旅館</div>'
            '<div class="v" style="flex-basis:130px">桌機</div>'
            '<div class="v" style="flex-basis:130px">手機</div>'
            '<div class="v" style="flex-basis:110px">差</div></div>')
    for r in dev['rows']:
        dk, mb = r.get('desktop_nr'), r.get('mobile_nr')
        kind = '不可退款'
        if dk is None or mb is None:
            dk, mb, kind = r.get('desktop_fc'), r.get('mobile_fc'), '免費取消'
        gap = (1 - mb / dk) * 100 if dk and mb else None
        rows += (f'<div class="row"><div class="nm">{E(str(r["name"]))}'
                 f'<s>{E(str(r.get("area") or ""))}'
                 + ('　有 Genius 標籤' if r.get('genius') else '　無 Genius')
                 + f'　{kind}</s></div>'
                 + (f'<div class="v" style="flex-basis:130px">{dk:,}</div>'
                    f'<div class="v" style="flex-basis:130px">{mb:,}</div>'
                    if dk and mb else
                    '<div class="v z" style="flex-basis:130px">—</div>'
                    '<div class="v z" style="flex-basis:130px">—</div>')
                 + (f'<div class="v ok" style="flex-basis:110px">-{gap:.1f}%</div>'
                    if gap and gap > 0.5
                    else '<div class="v z" style="flex-basis:110px">一樣</div>')
                 + '</div>')
    inner = ('<div class="kick">Booking 同一間房，同一批日期</div>'
             '<h1>手機版<em>便宜 9.09%</em></h1>'
             f'<div class="sub">{E(dev["_說明"])}</div>'
             '<div class="legend">優先列不可退款方案的每晚房價，'
             '沒有的改列免費取消方案（列上有標）。'
             '同一間房兩種方案不一定有同樣的差，所以兩邊都要量。</div>'
             f'<div class="list">{rows}</div>' + foot(2, N, fn))
    out.append(('pc-02.png', page(inner)))

    # 哪些通路有裝置價差
    ST = {'有差': ('ok', '有差'), '無差': ('z', '沒有差'), '未測得': ('z', '未測得')}
    rows = ''
    for r in plat['rows']:
        cls, lab = ST.get(r['state'], ('z', r['state']))
        rows += (f'<div class="row"><div class="nm">{E(r["name"])}'
                 f'<s>{E(r["detail"])}</s></div>'
                 f'<div class="v {cls}">{E(lab)}</div></div>')
    inner = ('<div class="kick">不是每個通路都這樣</div>'
             '<h1>四個通路<em>測下來</em></h1>'
             f'<div class="sub">{E(plat["_說明"])}</div>'
             '<div class="legend">「未測得」是這個瀏覽器抓不到價格，'
             '不是代表沒有價差。要自己開 App 再比一次。</div>'
             f'<div class="list">{rows}</div>' + foot(3, N, fn))
    out.append(('pc-03.png', page(inner)))

    # 同一間房在各通路的總價
    rows = ('<div class="hd"><div class="nm">通路與退改</div>'
            '<div class="v">總價</div></div>')
    for r in sorted(ch['rows'], key=lambda x: x.get('total') or 0):
        rows += (f'<div class="row"><div class="nm">{E(str(r["ch"]))}'
                 f'<s>{E(str(r.get("cancel") or ""))}'
                 + (f'　{E(str(r.get("note")))}' if r.get('note') else '')
                 + '</s></div>'
                 f'<div class="v">{r["total"]:,}</div></div>')
    inner = ('<div class="kick">同一間房，同一批日期</div>'
             '<h1>比<em>結帳頁的總價</em></h1>'
             f'<div class="sub">{E(str(ch["hotel"]))}。'
             '房價看起來便宜的，加完服務費與稅不一定還便宜。</div>'
             f'<div class="legend">{E(str(ch.get("official_rule") or ""))}</div>'
             f'<div class="list">{rows}</div>' + foot(4, N, fn))
    out.append(('pc-04.png', page(inner)))

    rf = d['referral']
    inner = ('<div class="kick">為什麼本站不直接說哪家最便宜</div>'
             '<h1>比價這件事<br><em>有利益衝突</em></h1>'
             f'<div class="sub">{E(rf["_說明"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>·</i>目前的狀態</b><s>{E(str(rf["state"]))}</s></div>'
             f'<div class="blk"><b><i>·</i>為什麼</b><s>{E(str(rf["why"]))}</s></div>'
             + (f'<div class="blk"><b><i>·</i>隱藏成本</b>'
                f'<s>{E(str(rf["hidden_costs"]))}</s></div>'
                if rf.get('hidden_costs') else '')
             + '</div>' + foot(5, N, fn))
    out.append(('pc-05.png', page(inner)))

    # checklist 每條都是 {q, a}，說明都不短，拆成兩張
    for j, part in enumerate((ck[:4], ck[4:]), 0):
        rows = ''.join(
            f'<div class="blk"><b><i>{i:02}</i>{E(str(c["q"]))}</b>'
            f'<s>{E(str(c["a"]))}</s></div>'
            for i, c in enumerate(part, 1 + j * 4))
        inner = ('<div class="kick">訂之前跑一次</div>'
                 f'<h1>{len(ck)} 個<em>檢查點 {"①" if j == 0 else "②"}</em></h1>'
                 + f'<div class="list">{rows}</div>' + foot(6 + j, N, fn))
        out.append((f'pc-0{6 + j}.png', page(inner)))
    return out


if __name__ == '__main__':
    K.run('price-check.json', OUT, build,
          lambda d: [d['platforms']['rows'], d['device']['rows'],
                     d['channels']['rows'], d['checklist'], d['checked']])
