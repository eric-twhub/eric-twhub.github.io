# -*- coding: utf-8 -*-
"""東京便宜旅館（共用衛浴的私人房）的分享圖卡。骨架見 cardkit.py。

這一頁的價值在「便宜是拿什麼換的」：每一家的弱點與官網比價，
社群上那種「東京便宜住宿懶人包」不會寫。圖卡照這個重點排。

評論則數缺的就寫「沒有公開則數」，不要留白也不要當成零，
留白會讓讀者以為那家沒人評過。

用法：python3 make_budgethotel_cards.py
輸出：tokyo/budget-hotel/cards/bh-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'tokyo/budget-hotel/cards'
PER_WEAK = 5      # 弱點一張放幾家（量出來的上限）

CSS = """
.row .v small{font-size:18px}
.q{font-size:21px;color:#8a847c;margin-top:9px;line-height:1.6}
"""


def _m(n):
    return f'NT${n:,}'


def _chunk(xs, n):
    """切成每組不超過 n 筆，各組盡量一樣多。最後一張只剩一筆會很空。"""
    if not xs:
        return [[]]
    g = -(-len(xs) // n)
    q, r = divmod(len(xs), g)
    out, i = [], 0
    for k in range(g):
        t = q + (1 if k < r else 0)
        out.append(xs[i:i + t])
        i += t
    return out


def _sc(r):
    """評分那一行。則數沒查到就寫出來，不要留白讓人以為沒人評過。"""
    n = r.get('reviews')
    s = f'{r["score"]}'
    tail = (f'{r["src"]} {n:,} 則' if n else f'{r["src"]}・沒有公開則數')
    return s, tail


def build(d):
    fn = (f'樣本 {d["sample"]["checkin"]} – {d["sample"]["checkout"]}，'
          f'{d["sample"]["nights"]} 晚單人含稅，查證於 {d["checked"]}')
    cl, ot, bm = d['cluster'], d['others'], d['benchmark']
    allr = cl['rows'] + ot['rows']
    lo = min(allr, key=lambda r: r['total'])
    # 代表家只從「Booking 評分 ＋ 樣本夠厚」的挑，跟頁面同一套規則。
    # 直接取最高分會挑到 Trip.com 的 9.4／107 則，那正是這一頁自己
    # 在警告的「樣本薄，分數要打折看」，拿它當招牌會自相矛盾；
    # 而且對照組的商務飯店是 Booking 分數，跨平台的分數比不過去。
    solid = [r for r in cl['rows']
             if r.get('src') == 'Booking' and (r.get('reviews') or 0) >= 500]
    best = max(solid or cl['rows'],
               key=lambda r: (r['score'], r.get('reviews') or 0))
    nights = d['sample']['nights']
    pend = []
    LABELS.clear()

    def add(inner, cls='', label='', sub=''):
        pend.append((inner, cls))
        LABELS.append({'title': label, 'sub': sub})

    # ── 封面 ──
    add('<div class="kick">東京住宿</div>'
        '<h1>有自己一間房，<br><em>但衛浴共用</em></h1>'
        '<div class="sub">不想睡床位，也不想付商務飯店的錢。'
        f'這中間有一層很少人寫的選擇：{nights} 晚單人含稅 '
        f'{_m(best["total"])} 上下，是同級商務飯店的四分之一。</div>'
        '<div class="stat">'
        f'<div><b>{len(allr)}</b><span>家實查<br>逐家看評論</span></div>'
        f'<div><b>{_m(lo["total"])}</b><span>最便宜<br>{nights} 晚總價</span></div>'
        f'<div><b>{_m(best["total"])}</b><span>Booking 最高分<br>'
        f'{best["score"]} 分・{best["reviews"]:,} 則</span></div>'
        f'<div><b>{_m(bm["total"])}</b><span>商務飯店<br>同期同條件</span></div>'
        '</div>'
        f'<div class="note">{E(d["sample"]["note"])}。</div>',
        'cover', '東京便宜旅館', '封面與關鍵數字')

    # ── 跟商務飯店比 ──
    gap = bm['total'] - best['total']
    dsc = abs(best['score'] - bm['score'])
    add('<div class="kick">省下多少</div>'
        f'<h1>差 {dsc:.1f} 分，<br><em>{_m(gap)}</em></h1>'
        '<div class="sub">兩邊都是 Booking 的分數，同一段日期、同樣是單人。'
        '你多付的那筆，買的主要是房間裡那間廁所。</div>'
        '<div class="list">'
        f'<div class="row"><div class="nm">{E(best["name"])}'
        f'<s>共用衛浴・{E(best["near"])}<br>'
        f'{_sc(best)[0]} 分・{_sc(best)[1]}</s></div>'
        f'<div class="v ok">{_m(best["total"])}<small>{nights} 晚</small></div></div>'
        f'<div class="row"><div class="nm">{E(bm["name"])}'
        f'<s>私人衛浴・商務飯店<br>'
        f'{bm["score"]} 分・Booking {bm["reviews"]:,} 則</s></div>'
        f'<div class="v bad">{_m(bm["total"])}<small>{nights} 晚</small></div></div>'
        # 再便宜的還有，但分數會掉。只放兩列會讓人以為 3,450 就是底，
        # 底是 2,097，代價寫在同一列。
        f'<div class="row"><div class="nm">{E(lo["name"])}'
        f'<s>{E(lo.get("area") or lo.get("near") or "")}・{E(lo["room"])}<br>'
        f'{_sc(lo)[0]} 分・{_sc(lo)[1]}'
        + (f'<br>{E(lo["warn"])}' if lo.get('warn') else '')
        + '</s></div>'
        f'<div class="v z">{_m(lo["total"])}<small>{nights} 晚</small></div></div>'
        '</div>'
        f'<div class="note">{E(bm["_說明"])}</div>',
        '', '跟商務飯店比一次', f'差 {dsc:.1f} 分，價差 {_m(gap)}')

    # ── 南千住那一群 ──
    rows = ''.join(
        f'<div class="row"><div class="nm">{E(r["name"])}'
        f'<s>{E(r["room"])}・{E(r["near"])}<br>{_sc(r)[1]}</s></div>'
        f'<div class="v">{_m(r["total"])}<small>{_sc(r)[0]} 分</small></div></div>'
        for r in sorted(cl['rows'], key=lambda x: x['total']))
    add(f'<div class="kick">{E(cl["name"])}</div>'
        '<h1>便宜的私人房，<br><em>幾乎全在這一區</em></h1>'
        '<div class="legend">舊稱山谷，戰後的簡易旅館區。房間小、衛浴共用、'
        '位置分偏低，換來的是商務飯店三分之一的價格。'
        '日比谷線直達上野 3 站、銀座不用轉車。</div>'
        f'<div class="list">{rows}</div>',
        '', f'{cl["name"]}那一群', f'{len(cl["rows"])} 家，依價格排')

    # ── 每一家的弱點 ──
    weak = [(r['name'], r.get('weak') or r.get('warn'))
            for r in allr if r.get('weak') or r.get('warn')]
    grps = _chunk(weak, PER_WEAK)
    for k, grp in enumerate(grps):
        rows = ''.join(f'<div class="blk"><b><i>!</i>{E(n)}</b><s>{E(w)}</s></div>'
                       for n, w in grp)
        add('<div class="kick">便宜是拿什麼換的</div>'
            '<h1>每一家的<em>弱點</em></h1>'
            '<div class="sub">這個價位帶沒有完美的選擇，'
            '差別在弱點落在你在不在意的地方。</div>'
            + (f'<div class="legend">第 {k + 1} 組，共 {len(grps)} 組</div>'
               if len(grps) > 1 else '')
            + f'<div class="list">{rows}</div>',
            '', '每一家的弱點',
            f'第 {k + 1} 組，共 {len(grps)} 組' if len(grps) > 1
            else f'{len(weak)} 家，逐家寫明')

    # ── 官網比價 ──
    of = d['official']
    rows = ''.join(
        f'<div class="blk"><b>{E(o["name"])}'
        f'<span class="tag {"ok" if "便宜" in o["verdict"] else "bad"}">'
        f'{E(o["verdict"])}</span></b>'
        f'<s>{E(o["detail"])}'
        + (f'<br><b style="display:inline">代價</b>　{E(o["catch"])}'
           if o.get('catch') else '')
        + '</s></div>' for o in of['rows'])
    add('<div class="kick">查了三家</div>'
        '<h1>官網會<em>比較便宜嗎</em></h1>'
        f'<div class="sub">{E(of["_說明"].split("？")[-1])}</div>'
        f'<div class="list">{rows}</div>'
        f'<div class="note">{E(of["rule"])}</div>',
        '', '官網會比較便宜嗎', '查了三家，沒有通則')

    # ── 南千住以外 ──
    rows = ''.join(
        f'<div class="row"><div class="nm">{E(r["name"])}'
        f'<s>{E(r["area"])}・{E(r["room"])}<br>{_sc(r)[1]}</s></div>'
        f'<div class="v">{_m(r["total"])}<small>{_sc(r)[0]} 分</small></div></div>'
        for r in sorted(ot['rows'], key=lambda x: x['total']))
    add(f'<div class="kick">{E(cl["name"])}以外</div>'
        '<h1>價格跳<em>一個級距</em></h1>'
        f'<div class="legend">{E(ot["_說明"].split("。", 1)[-1])}</div>'
        f'<div class="list">{rows}</div>',
        '', f'{cl["name"]}以外的選擇', f'{len(ot["rows"])} 家，依價格排')

    # ── 訂之前確認三件事 ──
    rows = ''.join(f'<div class="blk"><b><i>?</i>{E(c["q"])}</b>'
                   f'<s>{E(c["a"])}</s></div>' for c in d['checklist'])
    add('<div class="kick">這個價位帶的地雷</div>'
        '<h1>訂之前<em>確認三件事</em></h1>'
        '<div class="sub">這三項在訂房頁上不一定看得到，'
        '但住起來比房價差幾百塊有感得多。</div>'
        f'<div class="list">{rows}</div>',
        '', '訂之前確認三件事', '櫃檯時間、吸菸房、電梯')

    N = len(pend)
    return [(f'bh-{i:02d}.png', page(inner + foot(i, N, fn), cls, CSS))
            for i, (inner, cls) in enumerate(pend, 1)]


LABELS = []


def payload(d):
    """圖卡真正用到的欄位。房價每天變，但這一頁本來就是查價當天的快照，
    所以價格有變就該重跑，total 要算進指紋。"""
    return [d['checked'], d['sample'], d['benchmark'],
            d['cluster']['rows'], d['others']['rows'],
            d['official']['rows'], d['official']['rule'], d['checklist']]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    import json
    K.run('budget-hotels.json', OUT, build, payload)
    with open(f'{OUT}/index.json', 'w', encoding='utf-8') as f:
        json.dump([dict(x, file=f'bh-{i:02d}.png')
                   for i, x in enumerate(LABELS, 1)], f,
                  ensure_ascii=False, indent=1)
