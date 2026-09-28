# -*- coding: utf-8 -*-
"""iPhone 持有成本（二手回收行情）的分享圖卡。骨架見 cardkit.py。
不掛在每日 workflow 上。

用法：python3 make_resale_cards.py
輸出：iphone-cost/cards/rs-01.png …
"""
import datetime
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'iphone-cost/cards'
N = 6


def months(launch, today):
    a = datetime.date.fromisoformat(launch)
    return max((today - a).days / 30.44, 1)


def build(d):
    today = datetime.date.today()
    fn = f'回收價查詢於 {d["updated"]}，{d["src_name"]}'
    out = []

    # 逐一容量算「每月持有成本」＝（上市價 − 回收價）÷ 上市至今月數
    items = []
    for r in d['rows']:
        caps = [c for c in r['caps'] if c[1] and c[2]]
        if not caps:
            continue
        cap, listp, buyp = caps[0]
        m = months(r['launch'], today)
        items.append({
            'name': r['name'], 'cap': cap, 'tier': r['tier'],
            'list': listp, 'buy': buyp, 'm': m,
            'keep': buyp / listp * 100, 'per': (listp - buyp) / m})
    n_all = sum(len([c for c in r['caps'] if c[1] and c[2]]) for r in d['rows'])
    items.sort(key=lambda x: -x['keep'])
    best, worst = items[0], items[-1]

    cover = ('<div class="kick">iPhone 持有成本</div>'
             '<h1>台日價差幾千，<br><em>回收價差更多</em></h1>'
             f'<div class="sub">用台灣實際的二手回收行情，把機身價攤成每月成本。'
             f'{n_all} 個機種容量組合，這裡每個機種列基本容量。</div>'
             '<div class="stat">'
             f'<div><b>{best["keep"]:.0f}%</b>'
             f'<span>保值最好<br>{E(best["name"])}</span></div>'
             f'<div><b>{worst["keep"]:.0f}%</b>'
             f'<span>保值最差<br>{E(worst["name"])}</span></div>'
             f'<div><b>{n_all}</b><span>個組合<br>逐項查報價</span></div>'
             f'<div><b>{len(d["hike"]["items"])}</b>'
             '<span>個機種<br>剛漲過價</span></div></div>'
             f'<div class="note">{E(d["src_note"])}</div>'
             + foot(1, N, fn))
    out.append(('rs-01.png', page(cover, 'cover')))

    def table(idx, part, title, sub):
        rows = ('<div class="hd"><div class="nm">機種</div>'
                '<div class="v" style="flex-basis:126px">上市價</div>'
                '<div class="v" style="flex-basis:126px">回收價</div>'
                '<div class="v" style="flex-basis:104px">保值</div></div>')
        for x in part:
            rows += (f'<div class="row"><div class="nm">{E(x["name"])}'
                     f'<s>{E(x["cap"])}　上市 {x["m"]:.0f} 個月</s></div>'
                     f'<div class="v" style="flex-basis:126px">{x["list"]:,}</div>'
                     f'<div class="v" style="flex-basis:126px">{x["buy"]:,}</div>'
                     f'<div class="v {"ok" if x["keep"] >= 70 else "bad"}" '
                     f'style="flex-basis:104px">{x["keep"]:.0f}%</div></div>')
        return ('<div class="kick">保值率＝回收價 ÷ 上市價</div>'
                f'<h1>{title}</h1>'
                f'<div class="sub">{sub}</div>'
                '<div class="legend">每個機種列基本容量，其餘容量見網站上的完整表。回收價是收購商的公開報價，'
                '現場驗機後可能更低；自己在拍賣平台賣通常更高，但要花時間。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, N, fn))

    half = (len(items) + 1) // 2
    out.append(('rs-02.png', page(table(
        2, items[:half], '保值率 <em>前段</em>', '依保值率由高到低。'))))
    out.append(('rs-03.png', page(table(
        3, items[half:], '保值率 <em>後段</em>', '同一組算法。'))))

    per = sorted(items, key=lambda x: x['per'])
    rows = ('<div class="hd"><div class="nm">機種</div>'
            '<div class="v">每月持有成本</div></div>')
    for x in per[:7]:
        rows += (f'<div class="row"><div class="nm">{E(x["name"])}'
                 f'<s>{E(x["cap"])}　上市價 {x["list"]:,} − 回收 {x["buy"]:,}，'
                 f'攤 {x["m"]:.0f} 個月</s></div>'
                 f'<div class="v">{x["per"]:,.0f}</div></div>')
    inner = ('<div class="kick">換個算法看同一件事</div>'
             '<h1>每月<em>實際花多少</em></h1>'
             '<div class="sub">（上市價 − 現在的回收價）÷ 上市至今的月數。'
             '這是你真正付掉的錢，不是標價。</div>'
             '<div class="legend">由低到高，只列最省的七個。'
             '愈晚買、愈快換，攤下來的每月成本愈高。</div>'
             f'<div class="list">{rows}</div>' + foot(4, N, fn))
    out.append(('rs-04.png', page(inner)))

    hk = d['hike']
    rows = ('<div class="hd"><div class="nm">機種</div>'
            '<div class="v" style="flex-basis:130px">原價</div>'
            '<div class="v" style="flex-basis:130px">現價</div></div>')
    for nm, old, new in hk['items']:
        rows += (f'<div class="row"><div class="nm">{E(nm)}</div>'
                 f'<div class="v z" style="flex-basis:130px">{old:,}</div>'
                 f'<div class="v bad" style="flex-basis:130px">{new:,}</div></div>')
    inner = (f'<div class="kick">{E(hk["date"])}</div>'
             '<h1>舊機<em>反而漲價</em></h1>'
             f'<div class="sub">{E(hk["note"])}</div>'
             '<div class="legend">上市價一漲，同一支的保值率分母就變了。'
             '拿漲價後的標價去比舊的回收行情會失真。</div>'
             f'<div class="list">{rows}</div>' + foot(5, N, fn))
    out.append(('rs-05.png', page(inner)))

    inner = ('<div class="kick">這頁怎麼用</div>'
             '<h1>比標價<em>不夠</em></h1>'
             '<div class="list">'
             '<div class="blk"><b><i>01</i>台日價差是一次性的，保值率是持續的</b>'
             '<s>台日價差多半幾千元，但同一支機器兩三年後的回收價差距往往更大。'
             '兩個一起看，結論常常和只比標價不一樣。</s></div>'
             '<div class="blk"><b><i>02</i>保值率高不等於便宜</b>'
             '<s>保值率是比例。高價機種即使保值率好，攤下來的每月成本仍可能比較高。'
             '要看的是上一張的絕對金額。</s></div>'
             f'<div class="blk"><b><i>03</i>回收價每天在變</b>'
             f'<s>{E(d["src_note"])}這一頁的報價查詢於 {d["updated"]}，'
             '決定買賣前請再確認一次當日報價。</s></div>'
             f'<div class="blk"><b><i>04</i>上市價的來源</b>'
             f'<s>{E(d["list_src"])}。'
             '有機種在 2026-09-10 調過價，見上一張。</s></div>'
             '</div>' + foot(6, N, fn))
    out.append(('rs-06.png', page(inner)))
    return out


if __name__ == '__main__':
    K.run('resale.json', OUT, build,
          lambda d: [d['rows'], d['hike'], d['updated']])
