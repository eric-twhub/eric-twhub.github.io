# -*- coding: utf-8 -*-
"""旅日信用卡登錄日曆的分享圖卡（1080×1350，4:5）。骨架見 cardkit.py。

資料同 /japan-card-register/（cards.json 的 reg_events），不另外維護一份。
日期是算出來的：月曆那張按建置當月產生，所以每個月重跑就會換成當月。

輸出：japan-card-register/cards/reg-01.png …
"""
import sys, json, calendar, datetime
import cardkit as K

E = K.E
WD = ['一', '二', '三', '四', '五', '六', '日']
OUT = 'japan-card-register/cards'

CSS = """
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:7px;margin-top:22px}
.ch{font-size:20px;color:#8a847c;text-align:center;padding:2px 0}
.cc{min-height:122px;border:1px solid #e5e3de;border-radius:9px;padding:8px 9px;
 background:#fff}
.cc.pad{border:none;background:none}
.cc u{display:block;font-size:23px;color:#8a847c;text-decoration:none;font-weight:700}
.cc s{display:block;text-decoration:none;font-size:16px;line-height:1.3;
 margin-top:5px;color:#3f3b37;word-break:keep-all}
.cc s i{font-style:normal;display:block;font-size:14px;color:#8a847c;margin-top:1px}
.cc.has{border:3px solid #c2410c}
.cc.has u{color:#c2410c}
.cc.past{opacity:.4}
.lg{font-size:21px;color:#63605c;margin-top:16px}
.lg i{font-style:normal;display:inline-block;width:17px;height:17px;border:3px solid #c2410c;
 border-radius:4px;margin-right:7px;vertical-align:-2px}
"""


def events(d):
    out = []
    for c in d['cards']:
        for e in c.get('reg_events', []):
            out.append((c, e))
    return out


def when(e):
    t = e.get('time', '')
    if e['cycle'] == 'monthly':
        s = f'每月 {e["day"]} 號'
        return s + (f' {t}' if t else '')
    if e['cycle'] == 'weekly':
        return f'每週{WD[e["weekday"]]}' + (f' {t}' if t else '')
    if e['cycle'] == 'quarterly':
        return '每季一次'
    if e['cycle'] == 'once':
        return '期間內一次'
    return '官網沒寫'


def build(d):
    today = datetime.date.today()
    y, m = today.year, today.month
    ev = events(d)
    n = 4
    note = f'登錄時間查證於 {d["checked"]}'
    out = []

    # ── 1 封面 ──
    recur = [(c, e) for c, e in ev if e['cycle'] in ('monthly', 'weekly')]
    days = sorted({e['day'] for c, e in ev if e['cycle'] == 'monthly'})
    cover = ('<div class="kick">旅日信用卡</div>'
             f'<h1>加碼要先登錄<br><em>而且各家不同天</em></h1>'
             f'<div class="sub">沒登錄就是只剩基本回饋，而且多數活動'
             f'不能回溯到登錄前的消費。</div>'
             '<div class="stat">'
             f'<div><b>{len(ev)}</b><span>個加碼活動<br>要登錄</span></div>'
             f'<div><b>{len(recur)}</b><span>個每月或<br>每週要重登</span></div>'
             f'<div><b>{len(days)}</b><span>個不同的<br>開放日期</span></div>'
             f'<div><b>{len(set(c["slug"] for c, e in ev))}</b>'
             f'<span>張卡<br>逐張查證</span></div></div>'
             f'<div class="note">每月固定的日子：'
             + '、'.join(f'{x} 號' for x in days)
             + '。另有每週二開放的，以及每季才一次的。</div>'
             + K.foot(1, n, note))
    out.append(('reg-01.png', K.page(cover, 'cover')))

    # ── 2 當月月曆 ──
    # 同一天同一張卡可能有好幾個活動（中信 6 號就有兩個，還疊到每週二），
    # 卡名重複印三次只是把格子塞滿，所以一張卡一行，時間併在後面。
    mark = {}

    def put(dd, c, tag):
        mark.setdefault(dd, {}).setdefault(c['name'], []).append(tag)

    last = calendar.monthrange(y, m)[1]
    for c, e in ev:
        if e['cycle'] == 'monthly':
            put(min(e['day'], last), c, e.get('time', ''))
        elif e['cycle'] == 'weekly':
            for dd in range(1, last + 1):
                if datetime.date(y, m, dd).weekday() == e['weekday']:
                    put(dd, c, e.get('time', ''))
        elif e['cycle'] == 'quarterly':
            for x in e.get('dates', []):
                yy, mm, dd = map(int, x['open'].split('-'))
                if (yy, mm) == (y, m):
                    put(dd, c, '已額滿' if x.get('full') else e.get('time', ''))
    cells = '<div class="cc pad"></div>' * datetime.date(y, m, 1).weekday()
    for dd in range(1, last + 1):
        who = mark.get(dd, {})
        cls = 'cc' + (' has' if who else '') + (' past' if dd < today.day else '')
        body = ''
        for nm, tags in who.items():
            ts = [t for t in dict.fromkeys(tags) if t]
            body += f'<s>{E(nm)}<i>{E(" / ".join(ts))}</i></s>'
        cells += f'<div class="{cls}"><u>{dd}</u>{body}</div>'
    inner = ('<div class="kick">這個月</div>'
             f'<h1>{y} 年 {m} 月<br><em>要登錄的日子</em></h1>'
             '<div class="cal">'
             + ''.join(f'<div class="ch">{w}</div>' for w in WD)
             + cells + '</div>'
             '<div class="lg"><i></i>橘框就是那天開放登錄。淡掉的是已經過去的日子。</div>'
             + K.foot(2, n, note))
    out.append(('reg-02.png', K.page(inner, extra_css=CSS)))

    # ── 3 每月／每週要重登的 ──
    rows = ('<div class="hd"><div class="no"></div><div class="nm">卡片與加碼</div>'
            '<div class="v">開放時間</div></div>')
    for i, (c, e) in enumerate(sorted(recur, key=lambda x: (
            x[1].get('day', 99), x[1].get('time', ''))), 1):
        q = (f'{e["quota"]:,} 名' if e.get('quota') else e.get('quota_unit', ''))
        rows += (f'<div class="row"><div class="no">{i:02}</div>'
                 f'<div class="nm">{E(c["name"])}<s>{E(e["what"])}　·　{E(q)}</s></div>'
                 f'<div class="v">{E(when(e))}</div></div>')
    inner = ('<div class="kick">錯過就要等下個月</div>'
             '<h1>每月或每週<br><em>要重新登錄的</em></h1>'
             '<div class="sub">這幾個登錄一次不夠，時間到了要再登一次。</div>'
             f'<div class="list">{rows}</div>' + K.foot(3, n, note))
    out.append(('reg-03.png', K.page(inner)))

    # ── 4 登錄一次就好的，與限量提醒 ──
    once = [(c, e) for c, e in ev if e['cycle'] in ('once', 'quarterly', 'unknown')]
    rows = ''
    for c, e in once:
        tail = ''
        for x in e.get('dates', []):
            tail += f'{x["label"]}：{x["open"]} 開放'
            tail += f'，{x["full"]} 額滿。' if x.get('full') else '。'
        rows += (f'<div class="blk"><b>{E(c["name"])}'
                 f'<span class="tag">{E(when(e))}</span></b>'
                 f'<s>{E(e["what"])}。{E(e.get("valid", ""))}'
                 + (f'<br>{E(tail)}' if tail else '') + '</s></div>')
    inner = ('<div class="kick">這幾個不用每月搶</div>'
             '<h1>登錄一次就好的<br><em>與每季一次的</em></h1>'
             '<div class="sub">期間內登錄一次就有資格，但每季一次的那個名額最少。</div>'
             f'<div class="list">{rows}</div>' + K.foot(4, n, note))
    out.append(('reg-04.png', K.page(inner)))
    return out


def payload(d):
    return [[c['name'], c.get('reg_events')] for c in d['cards']
            if c.get('reg_events')] + [d['checked']]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    K.run('cards.json', OUT, build, payload)
    import os
    LB = [('reg-01.png', '加碼要先登錄', '而且各家不同天'),
          ('reg-02.png', '這個月要登錄的日子', '月曆一眼看完'),
          ('reg-03.png', '每月或每週要重登的', '錯過等下個月'),
          ('reg-04.png', '登錄一次就好的', '與每季一次的')]
    json.dump([{'file': f, 'title': t, 'sub': s} for f, t, s in LB],
              open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
