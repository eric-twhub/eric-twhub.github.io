# -*- coding: utf-8 -*-
"""東京平價住宿的分享圖卡。骨架見 cardkit.py。不掛在每日 workflow 上。

用法：python3 make_hostel_cards.py
輸出：tokyo/hostel/cards/hs-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'tokyo/hostel/cards'
N = 7


def build(d):
    fn = f'價格與評分以 Booking.com 為準，查證於 {d["checked"]}'
    ar = d['areas']
    sm = d['sample']
    out = []
    got = [a for a in ar if a.get('total')]
    none_area = [a for a in ar if not a.get('total')]
    cheap = min(got, key=lambda a: a['total'])
    best = max(got, key=lambda a: a['score'])

    cover = ('<div class="kick">東京平價住宿</div>'
             '<h1>便宜的區跟貴的區，<br><em>差的不只是錢</em></h1>'
             f'<div class="sub">{len(ar)} 個區各挑一個代表，'
             f'{sm["nights"]} 晚 {sm["adult"]} 人同一批日期比。</div>'
             '<div class="stat">'
             f'<div><b>{cheap["total"]:,}</b>'
             f'<span>最便宜<br>{E(cheap["area"])}・{sm["nights"]} 晚</span></div>'
             f'<div><b>{best["score"]}</b>'
             f'<span>評分最高<br>{E(best["area"])}</span></div>'
             f'<div><b>{len(ar)}</b><span>個區<br>逐區比較</span></div>'
             f'<div><b>{len(d["bad_cheap"]["rows"])}</b>'
             '<span>家便宜但<br>評分被壓低</span></div></div>'
             '<div class="note">新宿與池袋的便宜住宿不是樣本不足，'
             '是<b>上千則評語撐出來的低分</b>。便宜有便宜的理由。</div>'
             + foot(1, N, fn))
    out.append(('hs-01.png', page(cover, 'cover')))

    rows = ('<div class="hd"><div class="nm">區域與代表</div>'
            '<div class="v" style="flex-basis:110px">評分</div>'
            f'<div class="v">{sm["nights"]} 晚總價</div></div>')
    for a in sorted(got, key=lambda x: x['total']):
        rows += (f'<div class="row"><div class="nm">{E(a["area"])}'
                 f'<s>{E(a["name"])}　{E(a["type"])}　{a["reviews"]:,} 則</s></div>'
                 f'<div class="v" style="flex-basis:110px">{a["score"]}</div>'
                 f'<div class="v">{a["total"]:,}</div></div>')
    for a in none_area:
        rows += (f'<div class="row"><div class="nm">{E(a["area"])}'
                 f'<s>{E(str(a.get("note") or ""))}</s></div>'
                 '<div class="v z" style="flex-basis:110px">—</div>'
                 '<div class="v z">找不到</div></div>')
    inner = ('<div class="kick">每區只列一個代表</div>'
             f'<h1>八個區的<em>價格與評分</em></h1>'
             '<div class="sub">每區只列一個代表：該區「價格 × 評分 × 樣本數」'
             '綜合最好的。</div>'
             f'<div class="legend">{E(sm["note"])}</div>'
             f'<div class="list">{rows}</div>' + foot(2, N, fn))
    out.append(('hs-02.png', page(inner)))

    bc = d['bad_cheap']
    rows = ('<div class="hd"><div class="nm">住宿</div>'
            '<div class="v" style="flex-basis:110px">評分</div>'
            '<div class="v">總價</div></div>')
    for r in sorted(bc['rows'], key=lambda x: x['score']):
        rows += (f'<div class="row"><div class="nm">{E(r["name"])}'
                 f'<s>{E(r["area"])}　{r["reviews"]:,} 則</s></div>'
                 f'<div class="v bad" style="flex-basis:110px">{r["score"]}</div>'
                 f'<div class="v">{r["total"]:,}</div></div>')
    inner = ('<div class="kick">便宜有便宜的理由</div>'
             '<h1>低分<em>不是樣本不足</em></h1>'
             f'<div class="sub">{E(bc["_說明"])}</div>'
             f'<div class="list">{rows}</div>' + foot(3, N, fn))
    out.append(('hs-03.png', page(inner)))

    pg = d['platform_gap']
    rows = ('<div class="hd"><div class="nm">住宿</div>'
            '<div class="v" style="flex-basis:150px">Trip.com</div>'
            '<div class="v" style="flex-basis:150px">Booking</div></div>')
    for r in pg['rows']:
        rows += (f'<div class="row"><div class="nm">{E(r["name"])}</div>'
                 f'<div class="v z" style="flex-basis:150px">{r["trip"]}'
                 f'<small>{r["trip_n"]:,} 則</small></div>'
                 f'<div class="v" style="flex-basis:150px">{r["bk"]}'
                 f'<small>{r["bk_n"]:,} 則</small></div></div>')
    inner = ('<div class="kick">同一家住宿，兩個平台</div>'
             '<h1>分數<em>差很多</em></h1>'
             f'<div class="sub">{E(pg["_說明"])}</div>'
             f'<div class="list">{rows}</div>' + foot(4, N, fn))
    out.append(('hs-04.png', page(inner)))

    dk = d['desks']
    rows = ''.join(
        f'<div class="row"><div class="nm">{E(r["name"])}'
        + (f'<s>{E(str(r.get("note")))}</s>' if r.get('note') else '')
        + '</div>'
        f'<div class="v" style="flex-basis:210px;font-size:24px">'
        f'{E(str(r["open"]))}</div></div>' for r in dk['rows'])
    inner = ('<div class="kick">清晨落地最在意的一件事</div>'
             '<h1>櫃檯<em>幾點開</em></h1>'
             f'<div class="sub">{E(dk["_說明"])}</div>'
             f'<div class="list">{rows}</div>' + foot(5, N, fn))
    out.append(('hs-05.png', page(inner)))

    wk = d['weakness']
    rows = ''.join(f'<div class="blk"><b>{E(r["name"])}</b><s>{E(r["weak"])}</s></div>'
                   for r in wk['rows'][:5])
    inner = ('<div class="kick">Booking 頁面預設只顯示好評</div>'
             '<h1>每一家<em>都有弱點</em></h1>'
             f'<div class="sub">{E(wk["_說明"])}</div>'
             f'<div class="list">{rows}</div>' + foot(6, N, fn))
    out.append(('hs-06.png', page(inner)))

    ap, re_ = d['airport'], d['redeye']
    inner = ('<div class="kick">最後一晚</div>'
             '<h1>清晨的班機，<br><em>訂不了市區</em></h1>'
             f'<div class="sub">{E(re_["_說明"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>·</i>以這班為例</b>'
             f'<s>{E(str(re_["example_flight"]))}　{E(str(re_["example_dep"]))} 起飛，'
             f'{E(str(re_["terminal"]))}。報到櫃檯{E(str(re_["checkin_open"]))}開，'
             f'起飛前 {re_["checkin_close_min"]} 分鐘關。</s></div>'
             f'<div class="blk"><b><i>·</i>機場旅館這一間</b>'
             f'<s>{E(ap["name"])}　評分 {ap["score"]}（{ap["reviews"]:,} 則）　'
             f'每晚 {ap["night"]:,}　{E(str(ap.get("note") or ""))}</s></div>'
             '</div>' + foot(7, N, fn))
    out.append(('hs-07.png', page(inner)))
    return out


# 指紋要讓 gen.py import 得到才有用。原本寫成 K.run() 裡的 lambda，
# 藏在 if __name__ 區塊底下，gen.py 抓不到，圖卡過期的提醒就不會響。
def payload(d):
    """圖卡真正用到的欄位。改了這些才需要重跑，其他欄位變動不算。"""
    return [d['areas'], d['bad_cheap']['rows'], d['platform_gap']['rows'],
            d['desks']['rows'], d['checked']]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    K.run('hostels.json', OUT, build, payload)
