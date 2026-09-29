# -*- coding: utf-8 -*-
"""台灣假期請假攻略的分享圖卡（2026／2027 兩年各一組）。骨架見 cardkit.py。

資料來自 gen.py 輸出的 taiwan-holiday-<年>/cards-data.json，不自己重算：
連假對照、請假試算、祭典三態都是頁面上算好的，在這裡重寫一次一定會漂移。

張數跟著資料走，不固定八張。2026 只剩三段連假，硬湊八張會有半數是廢話。

用法：python3 make_twholiday_cards.py [2026|2027]
輸出：taiwan-holiday-<年>/cards/tw-01.png …
"""
import sys
import datetime as _dt
import cardkit as K

E, page, foot = K.E, K.page, K.foot
LABELS = []
YEARS = ('2026', '2027')
PER_RUN = 4       # 連假對照一張放幾段
PER_LEAVE = 6     # 請假表一張放幾列
TOP_RANK = 5      # 最划算排法列幾筆（量出來的上限）
PER_FEST = 8      # 祭典一張放幾項（量出來的上限，再多會撞到頁尾）

CSS = """
.lvh{display:flex;gap:10px;padding:0 0 9px;font-size:20px;color:#8a847c;
 border-bottom:2px solid #1a1a1a}
.lvh span{flex:0 0 86px;text-align:right}
.lvh span:first-child{flex:1 1 auto;text-align:left}
.lv{display:flex;gap:10px;align-items:baseline;padding:13px 0;
 border-bottom:1px solid #e5e3de}
.lv:last-child{border-bottom:0}
.lv .nm{flex:1 1 auto;font-size:27px;font-weight:700;line-height:1.3}
.lv .nm s{display:block;text-decoration:none;font-size:19px;font-weight:500;
 color:#8a847c;margin-top:4px}
.lv i{flex:0 0 86px;text-align:right;font-style:normal;font-size:26px;
 font-weight:700;font-variant-numeric:tabular-nums}
.lv i.g{color:#2f8f4f}
.lv i.b{color:#8a847c;font-weight:500}
.rn{padding:15px 0;border-bottom:1px solid #e5e3de}
.rn:last-child{border-bottom:0}
.rn b{display:block;font-size:30px;font-weight:700;line-height:1.3}
.rn u{display:block;text-decoration:none;font-size:20px;color:#8a847c;margin-top:4px}
.rn s{display:block;text-decoration:none;font-size:22px;color:#3f3b37;
 margin-top:8px;line-height:1.6}
.rn s em{font-style:normal;color:#c2410c;font-weight:700}
.rn s.q{color:#b4afa8}
/* 月曆：一張一個月，格子留大一點才塞得下三國的假日名稱 */
.cwd{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px;
 font-size:22px;color:#8a847c;padding:0 0 8px;text-align:center}
.cgrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px}
.cell{border:2px solid #e5e3de;border-radius:10px;padding:8px 7px;background:#fff;
 min-height:78px;overflow:hidden}
.cell.cl-pad{border:0;background:none;min-height:0}
.cell b{display:block;font-size:26px;font-weight:800;color:#8a847c;line-height:1.1}
.cell s{display:block;text-decoration:none;font-size:18px;line-height:1.3;
 margin-top:4px;word-break:break-all}
.cell.cl-we{background:#eceae5;border-color:#e0ddd6}
.cell.cl-hol{background:#fbe3dd;border-color:#eeb6a6}
.cell.cl-hol b{color:#b3391c}
.cell.cl-lv{background:#ffedd8;border-color:#c2410c;border-width:3px;padding:7px 6px}
.cell.cl-lv b{color:#c2410c}
.cell.cl-mk{background:#e6f0f7;border-color:#b9d8ea}
.cell u{display:inline-block;text-decoration:none;font-size:18px;font-weight:700;
 color:#fff;background:#c2410c;border-radius:5px;padding:1px 7px;margin-top:5px}
.clg{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:19px;color:#63605c;
 margin-top:12px}
.clg span{display:flex;align-items:center;gap:7px}
.clg i{display:inline-block;width:20px;height:20px;border-radius:5px;
 border:2px solid #e5e3de;font-style:normal}
/* 月曆下半：當月票價、祭典、推薦地區 */
.mbot{display:flex;gap:12px;margin-top:14px}
.mfare{flex:0 0 244px;background:#fff;border:2px solid #e5e3de;border-radius:14px;
 padding:13px 16px}
.mfare b{display:block;font-size:40px;font-weight:800;color:#c2410c;line-height:1.1;
 font-variant-numeric:tabular-nums}
.mfare b.z{font-size:26px;color:#8a847c}
.mfare span{display:block;font-size:19px;color:#63605c;margin-top:7px;line-height:1.5}
.marea{flex:1 1 auto;background:#fff;border:2px solid #e5e3de;border-radius:14px;
 padding:9px 16px}
.marea div{padding:6px 0;border-bottom:1px solid #eceae5}
.marea div:last-child{border-bottom:0}
.marea b{font-size:23px;font-weight:800;color:#c2410c;margin-right:9px}
.marea s{text-decoration:none;font-size:19px;color:#3f3b37;line-height:1.45}
.mfest{font-size:19px;color:#63605c;margin-top:10px;line-height:1.5}
.mfest em{font-style:normal;color:#1a1a1a;font-weight:700}
"""

_WK = '一二三四五六日'
_Y = ['']          # 這一組圖卡是哪一年，build() 進來時設定
CAL_LABELS = []
# 月曆格子放不下全名，只有這兩個要縮
_CARD_SHORT = {'臺灣光復暨金門古寧頭大捷紀念日': '光復節',
               '孔子誕辰紀念日/教師節': '教師節'}


def _d(x):
    """不同年的日期要帶年份。

    2027 年的元旦，最佳排法是請 2026 年 12 月底那四天。
    卡片上不寫年份的話，讀者會以為是 2027-12-28。
    """
    y, m, dd = int(x[:4]), int(x[5:7]), int(x[8:10])
    p = f'{y} 年 ' if x[:4] != _Y[0] else ''
    return f'{p}{m}/{dd}（{_WK[_dt.date(y, m, dd).weekday()]}）'


def _rng(a, b):
    return _d(a) if a == b else f'{_d(a)} – {_d(b)}'


def _days(xs):
    """一串請假日。年份只在換年的那一筆標出來，每筆都標會很吵。"""
    out, cur = [], _Y[0]
    for x in xs:
        out.append(_d(x) if x[:4] != cur else _d(x).split(' 年 ')[-1])
        cur = x[:4]
    return '、'.join(out)


def _short(a, b):
    """圖卡上的窄日期欄不放星期，放不下"""
    x = f'{int(a[5:7])}/{int(a[8:10])}'
    return x if a == b else f'{x}–{int(b[5:7])}/{int(b[8:10])}'


def _eff(g, L):
    """一天換到幾天。5/3 印成 1.66667 太難看，也不要四捨五入成 1.7；
    取兩位小數再把多餘的零去掉，1.75 就是 1.75。"""
    return f'{g / L:.2f}'.rstrip('0').rstrip('.')


def _chunk(xs, n):
    """切成每組不超過 n 筆，而且各組盡量一樣多。

    直接每 n 筆切一刀的話，17 筆會切成 8／8／1，最後一張幾乎是空的。
    """
    if not xs:
        return [[]]
    g = -(-len(xs) // n)
    q, r = divmod(len(xs), g)
    out, i = [], 0
    for k in range(g):
        take = q + (1 if k < r else 0)
        out.append(xs[i:i + take])
        i += take
    return out


def _mark(p, L):
    """這一格比少請一天多換到幾天。兩天以上才值得標綠，跟網頁同一套規則。"""
    cur = p['opts'].get(str(L))
    if not cur:
        return None
    prev = (p['opts'].get(str(L - 1), {}).get('tot', p['base'])
            if L > 1 else p['base'])
    return cur['tot'], cur['tot'] - prev >= 2


def build(d):
    ys = d['year']
    _Y[0] = ys
    fn = f'官方行事曆查證於 {d["checked"]}，祭典查證於 {d["fest_checked"]}'
    runs, leave = d['runs'], d['leave']
    up = [f for f in d['fest'] if not f['past']]
    est = [f for f in up if f['conf'] == 'est']
    out = []
    pend = []          # 先收 inner，最後才知道總張數 N，頁碼要對
    LABELS.clear()     # 圖庫的標題由這裡輸出，gen.py 讀 index.json，不各寫一份
    CAL_LABELS.clear()

    def add(inner, cls='', label='', sub=''):
        pend.append((inner, cls))
        LABELS.append({'title': label, 'sub': sub})

    # ── 封面 ──
    best = None
    for p in leave:
        o = p['opts'].get('1')
        if o and (not best or o['tot'] - p['base'] > best[1]):
            best = (p, o['tot'] - p['base'], o)
    if best:
        bp, bgain, bo = best
        head = (f'<h1>請 1 天，<br><em>連休 {bo["tot"]} 天</em></h1>'
                f'<div class="sub">{E(bp["name"])}。不請假是 {bp["base"]} 天，'
                f'請 {_days(bo["lv"])} 這一天，'
                f'連休變成 {_rng(bo["from"], bo["to"])}。</div>')
    else:
        head = ('<h1>今年剩下的假期，<br><em>請假延長不了</em></h1>'
                '<div class="sub">下面幾張列出每一段目前的天數。</div>')
    n_jp = sum(1 for r in runs if r['jp'])
    n_fe = sum(1 for r in runs if r['fest'])
    add(f'<div class="kick">{ys} 年台灣連假</div>' + head
        + '<div class="stat">'
        f'<div><b>{len(runs)}</b><span>段連假<br>'
        f'{"今年還沒到的" if d["partial"] else "整年"}</span></div>'
        f'<div><b>{n_jp}</b><span>段撞到<br>日本也放假</span></div>'
        f'<div><b>{n_fe}</b><span>段碰上<br>日本大型祭典</span></div>'
        f'<div><b>{len(up)}</b><span>個祭典<br>接下來會辦</span></div></div>'
        '<div class="note">機票貴是因為台灣放假，住宿貴是因為日本放假或當地有祭典。'
        '兩個高峰不一定重疊，重疊的那幾段才是真的要避開。</div>', 'cover',
        f'{ys} 年的連假與請假', '封面與關鍵數字')

    # ── 連假 × 日本／中國 ──
    for k, grp in enumerate(_chunk(runs, PER_RUN)):
        if not grp:
            break
        rows = ''
        for r in grp:
            bits = []
            if r['jp']:
                bits.append('🇯🇵 <em>日本同時連假</em>　' + '；'.join(
                    f'{"、".join(x["names"]) or "連假"} {_rng(x["start"], x["end"])}'
                    f'，重疊 {x["overlap"]} 天' for x in r['jp']))
            else:
                bits.append('🇯🇵 日本沒有連假')
            if r['cn'] is None:
                bits.append('🇨🇳 中國尚未公布')
            elif r['cn']:
                bits.append('🇨🇳 <em>中國同時連假</em>　' + '；'.join(
                    f'{"、".join(x["names"]) or "連假"} {_rng(x["start"], x["end"])}'
                    for x in r['cn']))
            else:
                bits.append('🇨🇳 中國沒有連假')
            if r['fest']:
                bits.append('🎆 <em>' + '、'.join(
                    f'{f["name"]}（{f["city"]}）' + ('・推估' if f['est'] else '')
                    for f in r['fest']) + '</em>')
            rows += (f'<div class="rn"><b>{E("、".join(r["names"]))}　'
                     f'{r["days"]} 天</b>'
                     f'<u>{_rng(r["start"], r["end"])}</u>'
                     + ''.join('<s class="q">' + x + '</s>' if 'em>' not in x
                               else '<s>' + x + '</s>' for x in bits)
                     + '</div>')
        n = len(_chunk(runs, PER_RUN))
        add(f'<div class="kick">台灣放假時，那邊在做什麼</div>'
            f'<h1>{ys} 年的連假，<br><em>日本與中國同期</em></h1>'
            + (f'<div class="legend">第 {k + 1} 組，共 {n} 組</div>' if n > 1 else '')
            + f'<div class="list">{rows}</div>', '',
            '台灣放假時，日本與中國同期',
            f'第 {k + 1} 組，共 {n} 組' if n > 1 else '逐段對照')

    # ── 請假表 ──
    for k, grp in enumerate(_chunk(leave, PER_LEAVE)):
        if not grp:
            break
        rows = ('<div class="lvh"><span>假期</span><span>不請</span>'
                '<span>請1天</span><span>請2天</span><span>請3天</span>'
                '<span>請4天</span></div>')
        for p in grp:
            cells = f'<i class="b">{p["base"]}</i>'
            for L in (1, 2, 3, 4):
                m = _mark(p, L)
                if not m:
                    cells += '<i class="b">—</i>'
                else:
                    cells += ('<i class="g">' if m[1] else '<i>') + f'{m[0]}</i>'
            rows += (f'<div class="lv"><div class="nm">{E(p["name"])}'
                     f'<s>{_rng(p["from"], p["to"])}</s></div>{cells}</div>')
        n = len(_chunk(leave, PER_LEAVE))
        add('<div class="kick">用官方行事曆逐日算的</div>'
            '<h1>請幾天假，<br><em>可以連休幾天</em></h1>'
            '<div class="legend">綠色代表多請的那一天換到兩天以上的連休。'
            '沒標色的，多請一天就只多休一天。</div>'
            + (f'<div class="legend">第 {k + 1} 組，共 {n} 組</div>' if n > 1 else '')
            + f'<div class="list">{rows}</div>', '',
            '請幾天假，可以連休幾天',
            f'第 {k + 1} 組，共 {n} 組' if n > 1 else '請 1 到 4 天的最佳排法')

    # ── 最划算的幾段：實際要請哪幾天 ──
    # 由近到遠排，先列最快要決定的那幾個。排假是有時效的事：
    # 九月的假期再划算，一月也還輪不到你煩惱。
    # 每個假期取自己最划算的那一列（看效率，不是看總共多賺幾天，
    # 因為「請 2 天多賺 4 天」沒有「請 1 天多賺 3 天」划算），
    # 否則同一個假期會用不同天數佔掉好幾格。
    rank = []
    for p in leave:
        cand = []
        for L in (1, 2, 3, 4):
            o = p['opts'].get(str(L))
            if o and o['tot'] > p['base']:
                cand.append(((o['tot'] - p['base']) / L, -L,
                             o['tot'] - p['base'], L, p, o))
        if cand:
            _e, _nl, gain, L, _p, o = max(cand)
            rank.append((p['start'], gain, L, p, o))
    rank.sort(key=lambda x: x[0])
    take = rank[:TOP_RANK]
    if take:
        rows = ''.join(
            f'<div class="blk"><b><i>{i + 1}</i>請 {L} 天休 {o["tot"]} 天'
            f'　<span class="tag ok">一天換 {_eff(g, L)} 天</span></b>'
            f'<s>{E(p["name"])}（本來 {p["base"]} 天）。'
            f'請 {_days(o["lv"])}，'
            f'連休 {_rng(o["from"], o["to"])}。</s></div>'
            for i, (_d0, g, L, p, o) in enumerate(take))
        _last = take[-1][4]['to']
        add('<div class="kick">由近到遠，先看要先決定的</div>'
            f'<h1>接下來 {len(take)} 個假期，<br><em>各自最划算的排法</em></h1>'
            f'<div class="sub">這幾段一路排到 {_rng(_last, _last)}。'
            '每個假期只列最划算的那一種：一天換到最多天的那個排法。'
            '再後面的在本站頁面上有完整的表。</div>'
            f'<div class="list">{rows}</div>', '',
            f'接下來 {len(take)} 個假期的排法', '由近到遠，附要請哪幾天')

    # ── 祭典 ──
    for k, grp in enumerate(_chunk(up, PER_FEST)):
        if not grp:
            break
        _CF = {'est': ('推估', 'bad'), 'announced': ('已公布', 'ok'),
               'fixed': ('每年固定', '')}
        rows = ''.join(
            f'<div class="row"><div class="nm">{E(f["name"])}'
            f'<s>{E(f["city"])}・{E(f["jp"])}</s></div>'
            f'<div class="v">{_short(f["start"], f["end"])}'
            f'<small>{_CF[f["conf"]][0]}</small></div></div>'
            for f in grp)
        n = len(_chunk(up, PER_FEST))
        add('<div class="kick">住宿與交通會一起被吃掉</div>'
            '<h1>日本接下來的<br><em>祭典與花火</em></h1>'
            + '<div class="legend">日期右下角寫明是官方定死的、該年度已公布的，'
              '還是本站照往年推估的。</div>'
            + (f'<div class="legend">第 {k + 1} 組，共 {n} 組</div>'
               if n > 1 else '')
            + f'<div class="list">{rows}</div>', '',
            '日本接下來的祭典與花火',
            f'第 {k + 1} 組，共 {n} 組' if n > 1 else '會吃掉住宿與交通的日子')

    # ── 日期怎麼來的 ──
    if est or d['fest_missing']:
        rows = ''.join(
            f'<div class="blk"><b><i>?</i>{E(f["name"])}'
            f'　{_rng(f["start"], f["end"])}</b><s>{E(f["why"])}</s></div>'
            for f in est)
        if d['fest_missing']:
            rows += ('<div class="blk"><b><i>—</i>這幾個今年沒有依據可以推</b>'
                     f'<s>{E("、".join(d["fest_missing"]))}。'
                     '沒有資料就不列，不用往年日期直接套。</s></div>')
        n_fx = sum(1 for f in d['fest'] if f['conf'] == 'fixed')
        n_an = sum(1 for f in d['fest'] if f['conf'] == 'announced')
        add('<div class="kick">哪些日期可以直接排</div>'
            '<h1>標「推估」的，<br><em>不要照著訂機票</em></h1>'
            '<div class="sub">官方寫明每年同一天的可以直接排。'
            '主辦單位還沒公布那一年日期的，本站標成推估，依據寫在下面。</div>'
            f'<div class="list">{rows}</div>'
            '<div class="stat">'
            f'<div><b>{n_fx}</b><span>個每年固定<br>可以直接排</span></div>'
            f'<div><b>{n_an}</b><span>個已公布<br>該年度確定</span></div>'
            f'<div><b>{len(est)}</b><span>個推估<br>等官方公布</span></div>'
            f'<div><b>{len(d["fest_missing"])}</b><span>個沒有依據<br>不列出來</span></div>'
            '</div>', '', '標「推估」的不要照著訂', '哪些日期可以直接排')

    N = len(pend)
    for i, (inner, cls) in enumerate(pend, 1):
        out.append((f'tw-{i:02d}.png',
                    page(inner + foot(i, N, fn), cls, CSS)))

    # ── 月曆：一張一個月 ──
    # 一張塞十二個月的話格子只剩三十幾 px，寫不下假日名稱。
    # 一個月一張，格子放大到 118px 高，三國的名稱才擺得進去。
    cal = d.get('cal') or {}
    ms = cal.get('months') or []
    for k, m in enumerate(ms, 1):
        out.append((f'cal-{m["ym"]}.png',
                    page(_month(m, cal, d) + foot(k, len(ms), fn), '', CSS)))
        CAL_LABELS.append({
            'file': f'cal-{m["ym"]}.png',
            'title': f'{int(m["ym"][:4])} 年 {int(m["ym"][5:7])} 月',
            'sub': _month_sub(m, cal)})
    return out


def _runs_of(ds):
    """連續的日期併成一段，10/12、10/13、10/14、10/15 太長了"""
    out = []
    for x in ds:
        t = _dt.date.fromisoformat(x)
        if out and (t - _dt.date.fromisoformat(out[-1][-1])).days == 1:
            out[-1].append(x)
        else:
            out.append([x])
    def md(x):
        return f'{int(x[5:7])}/{int(x[8:10])}'
    return '、'.join(md(g[0]) if len(g) == 1
                    else f'{md(g[0])}–{int(g[-1][8:10])}'
                    for g in out)


def _bygroup(m, cal):
    """這個月的建議請假，依假期分組。

    十月同時有國慶日與光復節兩段，全部併成一句會變成「國慶日：請八天」，
    那是把兩個假期的排法接在一起，不是任何一個假期真的要請八天。
    """
    g, order = {}, []
    for c in m['days']:
        if not c['leave']:
            continue
        if c['leave'] not in g:
            g[c['leave']] = []
            order.append(c['leave'])
        g[c['leave']].append(c['d'])
    out = []
    for nm in order:
        ds = g[nm]
        tot = (cal.get('leave') or {}).get(ds[0], {}).get('tot')
        out.append((_CARD_SHORT.get(nm, nm), ds, tot))
    return out


def _jp_of(m):
    """這個月日本的假日，連休幾天一起算出來。

    台灣沒有假期的月份，格子上剩下的就是日本那幾天，而那正是住宿會
    跳價的日子。只寫「台灣這個月沒有國定假日」等於把這張的重點丟掉。
    """
    ds = m['days']
    idx = {c['d']: i for i, c in enumerate(ds)}
    out = []
    for c in ds:
        if not c['jp']:
            continue
        i = idx[c['d']]
        a = b = i
        while a - 1 >= 0 and ds[a - 1]['jp_off']:
            a -= 1
        while b + 1 < len(ds) and ds[b + 1]['jp_off']:
            b += 1
        out.append((c['jp'], f'{int(c["d"][5:7])}/{int(c["d"][8:10])}', b - a + 1))
    return out


def _month_sub(m, cal):
    """圖庫底下那一行：這個月要注意什麼"""
    gs = _bygroup(m, cal)
    if gs:
        return '　'.join(f'{nm} 請 {len(ds)} 天休 {tot} 天' for nm, ds, tot in gs)
    hol = [c['tw'] for c in m['days'] if c['tw']]
    if hol:
        return '、'.join(dict.fromkeys(hol))[:24]
    jp = _jp_of(m)
    return ('台灣無假日，日本 '
            + '、'.join(f'{d} {n}' for n, d, _k in jp[:2])) if jp \
        else '三國這個月都沒有國定假日'


def _month(m, cal, d):
    ym = m['ym']
    y, mo = int(ym[:4]), int(ym[5:7])
    gs = _bygroup(m, cal)
    hol = [c for c in m['days'] if c['tw']]
    if gs:
        sub = ('；'.join(
            f'{nm} 請 {_runs_of(ds)} 這 {len(ds)} 天，連休 {tot} 天'
            for nm, ds, tot in gs) + '。橘框就是要請的那幾格。')
    elif hol:
        sub = ('台灣這個月放：'
               + '、'.join(dict.fromkeys(c['tw'] for c in hol)) + '。')
    else:
        jp = _jp_of(m)
        sub = '台灣這個月沒有國定假日。'
        if jp:
            sub += ('日本有 '
                    + '、'.join(f'{d} {n}' + (f'（{k} 連休）' if k >= 3 else '')
                                for n, d, k in jp)
                    + '，那幾天當地的住宿會緊。')
    if not cal.get('cn_open'):
        sub += f'中國 {_Y[0]} 年的節假日還沒公布，格子裡不會有中國的標記。'

    lead = _dt.date(y, mo, int(m['days'][0]['d'][8:10])).weekday()
    cells = '<div class="cell cl-pad"></div>' * lead
    for c in m['days']:
        cls = ''
        if c['leave']:
            cls = 'cl-lv'
        elif c['run'] or (c['off'] and c['tw']):
            cls = 'cl-hol'
        elif c['off']:
            cls = 'cl-we'
        elif c['makeup']:
            cls = 'cl-mk'
        txt = ''
        if c['tw']:
            txt += f'<s>🇹🇼 {E(_CARD_SHORT.get(c["tw"], c["tw"]))}</s>'
        elif c['makeup']:
            txt += '<s>🇹🇼 補班</s>'
        if c['jp']:
            txt += f'<s>🇯🇵 {E(c["jp"])}</s>'
        if c['cn']:
            txt += f'<s>🇨🇳 {E(c["cn"])}</s>'
        if c['leave']:
            txt += '<u>請假</u>'
        cells += f'<div class="cell {cls}"><b>{int(c["d"][8:10])}</b>{txt}</div>'
    tail = (7 - (lead + len(m['days'])) % 7) % 7
    cells += '<div class="cell cl-pad"></div>' * tail

    fa = m.get('fare') or {}
    _fd = ((cal.get('fare_src') or {}).get('generated') or '')[:10]
    fare = ''
    if fa.get('enough'):
        fare = (f'<b>NT${fa["median"]:,}</b>'
                f'<span>台北出發的中位來回票價<br>'
                f'最低 NT${fa["low"]:,}'
                + (f'・{_fd} 查的' if _fd else '') + '</span>')
    # 圖卡只放第一句。完整說明留在頁面上，全部塞進來會撞到頁尾，
    # 而第一句本來就是「為什麼是這個月」的那一句。
    areas = ''.join(
        f'<div><b>{E(a["name"])}</b>'
        f'<s>{E(a["why"].split("。")[0])}</s></div>'
        for a in (m.get('areas') or [])[:3])
    fest = ''
    if m.get('fest'):
        fest = ('<div class="mfest">當地大型活動：'
                + '、'.join(
                    f'<em>{E(f["name"])}</em> {_short(f["start"], f["end"])}'
                    + ('（推估）' if f['est'] else '')
                    for f in m['fest'])
                + '，那幾天當地住宿會緊。</div>')
    return (f'<div class="kick">{y} 年台灣連假月曆</div>'
            f'<h1>{mo} 月</h1>'
            f'<div class="sub">{E(sub)}</div>'
            '<div class="clg">'
            '<span><i style="background:#fbe3dd;border-color:#eeb6a6"></i>台灣連假</span>'
            '<span><i style="background:#ffedd8;border-color:#c2410c"></i>建議請假</span>'
            '<span><i style="background:#eceae5;border-color:#e0ddd6"></i>週末</span>'
            '<span>🇹🇼 台灣　🇯🇵 日本　🇨🇳 中國</span></div>'
            '<div class="list" style="margin-top:16px">'
            + '<div class="cwd">'
            + ''.join(f'<div>{w}</div>' for w in '一二三四五六日')
            + '</div><div class="cgrid">' + cells + '</div></div>'
            + (('<div class="mbot">'
                + (f'<div class="mfare">{fare}</div>' if fare else '')
                + (f'<div class="marea">{areas}</div>' if areas else '')
                + '</div>') if (fare or areas) else '')
            + fest)


def payload(d):
    """圖卡真正用到的欄位。

    generated 是每次建置都會變的時間戳，不能算進去。
    月票價也不算：那是每天重抓的快照，放進指紋的話每天都會喊過期，
    喊久了就沒有人會理它，真正該重跑的時候也看不出來。
    圖上的票價因此會跟當日數字有落差，所以卡片上標了抓取日期。
    """
    cal = d.get('cal')
    if cal:
        cal = dict(cal, months=[{k: v for k, v in m.items() if k != 'fare'}
                                for m in cal.get('months') or []],
                   fare_src=None)
    return [d['year'], d['checked'], d['fest_checked'], d['partial'],
            d['runs'], d['leave'], d['fest'], d['fest_missing'], cal]


def fingerprint(d):
    return K.digest(payload(d))


if __name__ == '__main__':
    import json
    for y in (sys.argv[1:] or YEARS):
        print(f'── {y} ──')
        out = f'taiwan-holiday-{y}/cards'
        K.run(f'taiwan-holiday-{y}/cards-data.json', out, build, payload)
        # 張數與每張的標題都跟著資料走，gen.py 要照著排圖庫，
        # 在那邊再寫一份標題清單一定會跟這裡對不上。
        with open(f'{out}/index.json', 'w', encoding='utf-8') as f:
            json.dump([dict(x, file=f'tw-{i:02d}.png')
                       for i, x in enumerate(LABELS, 1)],
                      f, ensure_ascii=False, indent=1)
        with open(f'{out}/cal-index.json', 'w', encoding='utf-8') as f:
            json.dump(list(CAL_LABELS), f, ensure_ascii=False, indent=1)
