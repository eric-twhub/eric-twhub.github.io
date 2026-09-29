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
"""

_WK = '一二三四五六日'
_Y = ['']          # 這一組圖卡是哪一年，build() 進來時設定


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
    return out


def payload(d):
    """圖卡真正用到的欄位。generated 是每次建置都會變的時間戳，不能算進去。"""
    return [d['year'], d['checked'], d['fest_checked'], d['partial'],
            d['runs'], d['leave'], d['fest'], d['fest_missing']]


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
