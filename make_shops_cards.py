# -*- coding: utf-8 -*-
"""東京潮牌選物店的分享圖卡。骨架見 cardkit.py。

這一組的重點不是「十六家店」，是「那份被分享的清單有幾家對不上」。
圖卡照這個排：先講幾家要修正，再逐家列，最後才是按實際位置重排的分區。

長註解只放第一句。完整說明留在頁面上，全部塞進圖卡會撞到頁尾，
而第一句本來就是「差在哪」的那一句。

用法：python3 make_shops_cards.py
輸出：tokyo/street-fashion/cards/sf-01.png …
"""
import cardkit as K

E, page, foot = K.E, K.page, K.foot
OUT = 'tokyo/street-fashion/cards'
PER_FIX = 4        # 修正那幾張一張放幾家（量出來的上限）
LABELS = []

CSS = """
.sh{padding:15px 0;border-bottom:1px solid #e5e3de}
.sh:last-child{border-bottom:0}
.sh b{display:block;font-size:29px;font-weight:700;line-height:1.3}
.sh b em{font-style:normal;color:#c2410c;font-size:21px;margin-left:10px;
 font-weight:700}
.sh u{display:block;text-decoration:none;font-size:22px;color:#c2410c;
 font-weight:700;margin-top:6px}
.sh s{display:block;text-decoration:none;font-size:21px;color:#3f3b37;
 margin-top:5px;line-height:1.55}
.sh s.q{color:#8a847c}
.grp{display:flex;gap:14px;margin-top:6px;flex-wrap:wrap}
.grp div{flex:1 1 44%;background:#fff;border:2px solid #e5e3de;border-radius:14px;
 padding:16px 18px}
.grp b{display:block;font-size:34px;font-weight:800;color:#c2410c;line-height:1.1}
.grp b i{font-style:normal;font-size:22px;color:#63605c;margin-left:8px}
.grp s{display:block;text-decoration:none;font-size:20px;color:#3f3b37;
 margin-top:8px;line-height:1.5}
"""


def _first(t):
    return (t or '').split('。')[0]


def build(d):
    fn = f'逐家回查官方頁面，查證於 {d["checked"]}'
    items = d['lists'][0]['items']
    fix = [x for x in items if x.get('state') == 'fix']
    ok = [x for x in items if x.get('state') == 'ok']
    no = [x for x in items if x.get('state') == 'none']
    moved = [x for x in items if x.get('area_moved')]
    pend = []
    LABELS.clear()

    def add(inner, cls='', label='', sub=''):
        pend.append((inner, cls))
        LABELS.append({'title': label, 'sub': sub})

    grp = {}
    for x in items:
        grp.setdefault(x.get('area_real') or '未分區', []).append(x)

    # ── 封面 ──
    add('<div class="kick">社群清單回查</div>'
        f'<h1>那份東京潮牌清單，<br><em>{len(fix)} 家對不上</em></h1>'
        '<div class="sub">Threads 上有人問東京男生必逛，最紅的一則回覆列了 '
        f'{len(items)} 家店，被分享 164 次。逐家查官方頁面之後是這樣。</div>'
        '<div class="stat">'
        f'<div><b>{len(fix)}</b><span>家要修正<br>名稱樓層或區域</span></div>'
        f'<div><b>{len(ok)}</b><span>家對得上<br>跟留言一致</span></div>'
        f'<div><b>{len(no)}</b><span>家查不到<br>官方分店頁</span></div>'
        f'<div><b>{len(moved)}</b><span>家歸錯區<br>要走另一個車站</span></div>'
        '</div>'
        '<div class="note">最容易踩的一個：WACKO MARIA 的旗艦店叫 '
        'PARADISE TOKYO，地圖上搜品牌名找不到。</div>',
        'cover', '那份清單逐家查完是這樣', f'{len(items)} 家裡 {len(fix)} 家對不上')

    # ── 要修正的 ──
    gs = [fix[i:i + PER_FIX] for i in range(0, len(fix), PER_FIX)]
    for k, part in enumerate(gs, 1):
        rows = ''.join(
            f'<div class="sh"><b>{E(x["name"])}'
            + ('<em>歸錯區</em>' if x.get('area_moved') else '')
            + '</b>'
            + (f'<u>{E(x["address"])}</u>' if x.get('address') else '')
            + (f'<s class="q">{E(x["hours"])}</s>' if x.get('hours') else '')
            + f'<s>{E(_first(x["check_note"]))}</s></div>' for x in part)
        add('<div class="kick">店都還在，但照留言去找會出問題</div>'
            f'<h1>要修正的 <em>{len(fix)} 家</em>'
            + (f' {"①②③"[k - 1]}' if len(gs) > 1 else '') + '</h1>'
            f'<div class="list">{rows}</div>', '',
            f'要修正的 {len(fix)} 家' + (f' {"①②③"[k - 1]}' if len(gs) > 1 else ''),
            '實際地址與差在哪')

    # ── 對得上的 ──
    rows = ''.join(
        f'<div class="sh"><b>{E(x["name"])}</b>'
        + (f'<u>{E(x["address"])}</u>' if x.get('address') else '')
        + (f'<s class="q">{E(x["hours"])}</s>' if x.get('hours') else '')
        + f'<s>{E(_first(x["check_note"]))}</s></div>' for x in ok)
    add('<div class="kick">跟留言寫的一致</div>'
        f'<h1>對得上的 <em>{len(ok)} 家</em></h1>'
        f'<div class="list">{rows}</div>', '',
        f'對得上的 {len(ok)} 家', '查到官方來源')

    # ── 查不到的 ──
    rows = ''.join(
        f'<div class="blk"><b><i>?</i>{E(x["name"])}</b>'
        f'<s>{E(x["check_note"])}</s></div>' for x in no)
    add('<div class="kick">查不到不等於不存在</div>'
        f'<h1>本站查不到<br><em>官方頁的 {len(no)} 家</em></h1>'
        '<div class="sub">查得到官方來源才寫成確定，其餘不用第三方整理來補。</div>'
        f'<div class="list">{rows}</div>', '',
        f'查不到官方頁的 {len(no)} 家', '查不到不等於不存在')

    # ── 按實際位置重排 ──
    def _short(n):
        for t in (' 澀谷', ' 中目黑', ' 原宿店', ' 原宿', '旗艦店'):
            n = n.replace(t, '')
        return n
    cells = ''.join(
        f'<div><b>{E(a)}<i>{len(v)} 家</i></b><s>'
        + '、'.join(E(_short(x['name']))
                   + ('（留言歸在' + E(x['area'].split('（')[0]) + '）'
                      if x.get('area_moved') else '')
                   for x in v)
        + '</s></div>'
        for a, v in sorted(grp.items(), key=lambda kv: -len(kv[1])))
    add('<div class="kick">照留言排會多走一趟</div>'
        '<h1>按實際位置<em>重排</em></h1>'
        f'<div class="sub">{E(d["_重新分區"].split("。")[0])}。'
        '行政區是渋谷区沒錯，但要走的是原宿或明治神宮前站。</div>'
        f'<div class="grp">{cells}</div>', '',
        '按實際位置重排', '原宿 8、澀谷 4、中目黑 3、南青山 1')

    # ── 這串沒回答的 ──
    add('<div class="kick">那串問了但沒人回的</div>'
        '<h1>69 則留言，<br><em>沒有一則回美食</em></h1>'
        '<div class="sub">原 PO 問了燒肉、拉麵、海鮮，整串留言全部在回潮牌。</div>'
        '<div class="list">'
        '<div class="blk"><b><i>·</i>美食另外整理過</b>'
        '<s>另外整理過 46 家東京餐廳，每一家都回查過官方營業時間與公休，'
        '其中一家在留言寫完之後已經歇業。</s></div>'
        '<div class="blk"><b><i>!</i>什麼時候去，比逛哪幾家更影響花費</b>'
        '<s>日本的免稅 2026/11/1 改制。10/31 之前結帳直接扣 10%，當場就是免稅價；'
        '11/1 起要先付含稅全額，出境經海關確認後才由店家退還，'
        '購買日起 90 天內要完成確認。要掃貨的話，差的是現金流。</s></div>'
        '</div>', '',
        '那串沒有人回答的', '美食與 11/1 免稅新制')

    N = len(pend)
    return [(f'sf-{i:02d}.png', page(inner + foot(i, N, fn), cls, CSS))
            for i, (inner, cls) in enumerate(pend, 1)]


def payload(d):
    """圖卡真正用到的欄位。"""
    return [d['checked'], d['lists'][0]['items'], d['_重新分區']]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    import json
    K.run('tokyo-shops-raw.json', OUT, build, payload)
    with open(f'{OUT}/index.json', 'w', encoding='utf-8') as f:
        json.dump([dict(x, file=f'sf-{i:02d}.png')
                   for i, x in enumerate(LABELS, 1)], f,
                  ensure_ascii=False, indent=1)
