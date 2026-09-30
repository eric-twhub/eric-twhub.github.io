# -*- coding: utf-8 -*-
"""日本購物折扣券的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML，版面高度用量的、
並寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

只放頁面上也有的東西。coupons.json 裡的 _已解決、_待複查、_form_說明
是工作用的欄位，頁面沒有算繪，圖卡就不放，免得圖上講的和站上對不起來。

用法：python3 make_coupon_cards.py
輸出：japan-coupon/cards/cp-01.png … -16.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib, datetime
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-coupon', 'cards')
SRC = 'coupons.json'
E = htm.escape
TAX = 10          # 日本消費稅，coupons.json 的 order 欄位寫明券以免稅後金額計算
DEMO = 30000      # 試算用的含稅金額。太小的話各家實付只差幾十圓，看不出差別
FORM = {'tap': ('點開條碼', '官方禁止截圖，要現場點開啟用'),
        'live': ('結帳前出示', '出示手機畫面或券面給店員掃'),
        'app': ('官方 App', '要先裝 App 並登入'),
        'image': ('靜態圖', '可以先存起來，離線也能用'),
        'counter': ('櫃台換紙本', '到店內服務台憑護照換')}


def fingerprint(d):
    """圖卡真正用到的欄位的指紋。"""
    pay = [[s.get(k) for k in ('name', 'jp', 'cat', 'rate', 'max', 'tax_min',
                               'form', 'expires', 'tiers', 'note', 'combo', 'src')]
           + [s.get('steps'), s.get('watch')]
           for s in d['stores']]
    pay.append([d['checked'], d['order'], d['tax_note']])
    return hashlib.sha1(json.dumps(pay, ensure_ascii=False,
                                   sort_keys=True).encode('utf-8')).hexdigest()[:12]


def _chrome():
    c = os.environ.get('CHROME')
    if c and os.path.exists(c):
        return c
    mac = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(mac):
        return mac
    for n in ('google-chrome', 'google-chrome-stable', 'chromium-browser', 'chromium'):
        p = shutil.which(n)
        if p:
            return p
    sys.exit('找不到 Chrome，請設定 CHROME 環境變數')


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;
 font-family:"Noto Sans CJK TC","Noto Sans TC","PingFang TC","Hiragino Sans",
 "Heiti TC",sans-serif;
 background:#f7f7f5;color:#1a1a1a;-webkit-font-smoothing:antialiased}
.qrg{display:grid;grid-template-columns:1fr 1fr;gap:20px 26px;margin-top:26px}
.qrc{background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:18px 20px;
 display:flex;gap:16px;align-items:center}
.qrc svg{width:150px;height:150px;flex:0 0 150px;display:block}
.qrc div{min-width:0}
.qrc b{display:block;font-size:25px;line-height:1.3;letter-spacing:-.01em}
.qrc s{display:block;text-decoration:none;color:#63605c;font-size:19px;
 line-height:1.45;margin-top:5px}
.qrc u{display:block;text-decoration:none;color:#c2410c;font-weight:700;
 font-size:27px;margin-top:7px}
.card{width:1080px;height:1350px;padding:58px 64px 0;display:flex;flex-direction:column;
 background:#f7f7f5}
.kick{font-size:26px;color:#c2410c;font-weight:700;letter-spacing:.06em;margin-bottom:14px}
h1{font-size:58px;line-height:1.24;font-weight:800;letter-spacing:-.01em}
h1 em{font-style:normal;color:#c2410c}
.sub{font-size:27px;line-height:1.7;color:#63605c;margin-top:16px}
.legend{font-size:21px;color:#63605c;margin-top:9px;line-height:1.6}
.list{margin-top:24px;flex:1 1 auto;min-height:0}
.hd{display:flex;gap:12px;align-items:flex-end;padding:0 0 9px;
 font-size:20px;color:#8a847c;border-bottom:2px solid #1a1a1a}
.row{display:flex;gap:12px;align-items:baseline;padding:14px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.num{flex:0 0 42px;font-size:22px;font-weight:700;color:#c2410c;
 font-variant-numeric:tabular-nums}
.nm{flex:1 1 auto;font-size:30px;font-weight:700;line-height:1.28;letter-spacing:-.01em}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;letter-spacing:0}
.rate{flex:0 0 150px;text-align:right;font-size:30px;font-weight:800;color:#c2410c;
 white-space:nowrap}
.rate small{display:block;font-size:19px;font-weight:500;color:#8a847c;margin-top:3px}
.exp{flex:0 0 156px;text-align:right;font-size:22px;color:#63605c;white-space:nowrap}
.exp.no{color:#b4afa8}
.exp.dead{color:#c4563a;font-weight:700}
/* 疊加步驟 */
.step{display:flex;gap:18px;padding:16px 0;border-bottom:1px solid #e5e3de}
.step:last-child{border-bottom:0}
.step i{font-style:normal;flex:0 0 46px;font-size:25px;font-weight:800;color:#c2410c}
.step div{flex:1 1 auto}
.step b{display:block;font-size:30px;margin-bottom:5px}
.step p{font-size:23px;color:#63605c;line-height:1.65}
.step u{text-decoration:none;flex:0 0 190px;text-align:right;font-size:28px;
 font-weight:700;font-variant-numeric:tabular-nums}
/* 一般段落卡 */
.blk{padding:13px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:30px;font-weight:700;margin-bottom:6px}
.blk b i{font-style:normal;color:#c4563a;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.68}
.tag{display:inline-block;font-size:20px;padding:2px 10px;border-radius:999px;
 background:#e5e3de;color:#63605c;margin-left:10px;vertical-align:3px;font-weight:600}
.foot{flex:0 0 auto;padding:24px 0 42px;border-top:3px solid #1a1a1a;
 display:flex;justify-content:space-between;align-items:flex-end;margin-top:18px}
.foot b{font-size:28px;font-weight:800;display:block}
.foot span{font-size:22px;color:#63605c;display:block;margin-top:6px}
.pg{font-size:24px;color:#63605c;font-weight:700}
.cover{justify-content:center}
.cover .list{flex:0 0 auto;margin-top:0}
.stat{display:flex;gap:14px;margin-top:36px}
.stat div{flex:1;background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:22px 20px}
.stat b{display:block;font-size:46px;font-weight:800;color:#c2410c;line-height:1.1;
 font-variant-numeric:tabular-nums}
.stat span{display:block;font-size:22px;color:#63605c;margin-top:8px;line-height:1.5}
.note{margin-top:34px;background:#fff;border:1px solid #e5e3de;border-left:7px solid #c2410c;
 border-radius:14px;padding:26px 28px;font-size:25px;line-height:1.75}
"""


def page(inner, cls=''):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS}</style></head><body><div class="card {cls}">{inner}</div>'
            '</body></html>')


def foot(i, n, note):
    return ('<div class="foot"><div><b>eric-twhub.github.io</b>'
            f'<span>{E(note)}</span></div>'
            f'<div class="pg">{i} / {n}</div></div>')


def rate_at(s, untaxed):
    """券的折扣看未稅金額落在哪一級，沒有級距的用單一費率。跟頁面同一套。"""
    st = s.get('steps')
    if not st:
        return s['max']
    r = 0
    for amt, pc in st:
        if untaxed >= amt:
            r = pc
    return r


def yen(v):
    return f'¥{round(v):,}'


def build(d, today):
    n = 16
    sts = d['stores']
    fnote = f'發券頁逐家查證於 {d["checked"]}'
    out = []

    def dead(s):
        return bool(s.get('expires')) and s['expires'] < today

    live = [s for s in sts if not dead(s)]
    hi = max(live, key=lambda s: s['max'])
    # 試算要用條件講清楚的那一家。最高的 COSMOS 官方頁只寫「最大 9%」，
    # 沒有門檻也沒有排除品項（資料裡的 calc_caveat 就是在講這件事），
    # 拿它當範例等於把未查證的數字當成人人拿得到。
    spec = [s for s in live if s.get('basis') or s.get('steps')]
    best = max(spec, key=lambda s: s['max']) if spec else hi
    # 免稅先扣，券再以免稅後金額計算。兩個百分比不能直接相加。
    untaxed = DEMO / (1 + TAX / 100)
    after = untaxed * (1 - best['max'] / 100)
    eff = (DEMO - after) / DEMO * 100
    naive = TAX + best['max']

    # ── 1 封面 ──
    # 讀者要的是「我這筆會付多少」，不是「這家的券是幾 %」。封面直接給金額。
    pays = sorted(((untaxed * (1 - rate_at(s, untaxed) / 100), s) for s in live),
                  key=lambda x: x[0])
    lo_pay, lo_s = pays[0]
    hi_pay, hi_s = pays[-1]
    cover = ('<div class="kick">日本購物折扣</div>'
             f'<h1>含稅 {yen(DEMO)} 的東西<br>最低<em>實付 {yen(lo_pay)}</em></h1>'
             f'<div class="sub">免稅先扣，券再以免稅後的金額計算。同一筆錢，'
             f'挑對店與挑錯店差 {yen(hi_pay - lo_pay)}。</div>'
             '<div class="stat">'
             f'<div><b>{yen(DEMO - lo_pay)}</b><span>最多省下<br>'
             f'{E(lo_s["name"].split()[0])}</span></div>'
             f'<div><b>{lo_pay / DEMO * 10:.1f} 折</b><span>相當於<br>原價的</span></div>'
             f'<div><b>{yen(hi_pay - lo_pay)}</b><span>選錯店<br>多付的</span></div>'
             f'<div><b>{len(sts)}</b><span>家店<br>逐家查證</span></div></div>'
             f'<div class="note">兩個百分比不能相加。免稅 {TAX}% 加券 {best["max"]}% '
             f'不是 {naive:g}%：免稅後約 {yen(untaxed)}，再折 {best["max"]}% 是 '
             f'{yen(after)}，實際等於 {eff:.1f}%。</div>'
             + foot(1, n, fnote))
    out.append(('cp-01.png', page(cover, 'cover')))

    # ── 2 疊加順序 ──
    rows = (f'<div class="step"><i>00</i><div><b>結帳前的原價</b>'
            f'<p>含稅標價，也就是架上看到的數字</p></div>'
            f'<u>{yen(DEMO)}</u></div>'
            f'<div class="step"><i>01</i><div><b>先扣免稅</b>'
            f'<p>消費稅 {TAX}%，同一店舖同一天未稅合計 ¥5,000 以上</p></div>'
            f'<u>{yen(untaxed)}</u></div>'
            f'<div class="step"><i>02</i><div><b>券以免稅後的金額計算</b>'
            f'<p>這就是為什麼不能把兩個百分比相加</p></div>'
            f'<u>{yen(after)}</u></div>'
            f'<div class="step"><i>03</i><div><b>最後才是刷卡回饋</b>'
            f'<p>以實付金額計算，不是原價</p></div>'
            f'<u>看卡片</u></div>')
    inner = ('<div class="kick">順序決定你實際省多少</div>'
             '<h1>免稅、券、刷卡<br><em>要照這個順序疊</em></h1>'
             f'<div class="sub">以含稅 {yen(DEMO)}、券 {best["max"]}% 為例。</div>'
             f'<div class="legend">{E(d["order"])}</div>'
             f'<div class="list">{rows}</div>' + foot(2, n, fnote))
    out.append(('cp-02.png', page(inner)))

    # ── 3、4 全部店家 ──
    ordered = sorted(sts, key=lambda s: (dead(s), -s['max'], s['cat']))

    def store_card(idx, part, items, start):
        rows = ('<div class="hd"><div class="num"></div><div class="nm">店家</div>'
                '<div class="rate">券的折扣</div><div class="exp">有效期</div></div>')
        for j, s in enumerate(items, start):
            if dead(s):
                ex = f'<div class="exp dead">已過期 {s["expires"]}</div>'
            elif s.get('expires'):
                ex = f'<div class="exp">{s["expires"]}</div>'
            else:
                ex = '<div class="exp no">發券頁未標</div>'
            rows += (f'<div class="row"><div class="num">{j:02}</div>'
                     f'<div class="nm">{E(s["name"])}<s>{E(s["cat"])}・{E(s["jp"])}</s></div>'
                     f'<div class="rate">{E(str(s["rate"]))}'
                     f'<small>{E(s["tax_min"])}起</small></div>{ex}</div>')
        return ('<div class="kick">折扣幅度一覽</div>'
                f'<h1>{len(sts)} 家常見店家 <em>{part}</em></h1>'
                '<div class="sub">依券的最高折扣排序。滿額級距與排除品項各家不同，'
                '結帳前看發券頁。</div>'
                '<div class="legend">「發券頁未標」表示那一頁沒有寫有效期限，'
                '不是永久有效，隨時可能換掉。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, n, fnote))

    half = (len(ordered) + 1) // 2
    out.append(('cp-03.png', page(store_card(3, '①', ordered[:half], 1))))
    out.append(('cp-04.png', page(store_card(4, '②', ordered[half:], half + 1))))

    # ── 5 滿額級距 ──
    tiered = [s for s in sts if s.get('steps') and len(s['steps']) >= 1]
    tiered.sort(key=lambda s: -len(s['steps']))
    rows = ''
    for s in tiered:
        seg = '　'.join(f'滿 {yen(a)} 折 {b}%' for a, b in s['steps'])
        rows += (f'<div class="blk"><b>{E(s["name"])}'
                 f'<span class="tag">最高 {s["max"]}%</span></b>'
                 f'<s>{E(seg)}</s></div>')
    inner = ('<div class="kick">湊到下一階划不划算</div>'
             f'<h1>有滿額級距的 <em>{len(tiered)} 家</em></h1>'
             '<div class="sub">級距一律以未稅金額計算，'
             '所以架上的含稅標價要先除以 1.1 再看。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n, fnote))
    out.append(('cp-05.png', page(inner)))

    # ── 6 三個常犯的錯 ──
    MISS = [('把百分比直接相加',
             f'免稅 {TAX}% 加券 {best["max"]}% 不等於 {naive:g}%。'
             f'券是以免稅後的金額計算，實際約 {eff:.1f}%。'),
            ('結帳到一半才拿出券',
             '多數店家要在結帳前出示。已經開始免稅手續才拿出來，通常不能補折。'),
            ('以為每家都能併用',
             '少數店家的券與免稅二擇一，百貨或車站內的櫃位也常有另外的規則。')]
    rows = ''.join(f'<div class="blk"><b><i>✗</i>{E(t)}</b><s>{E(s)}</s></div>'
                   for t, s in MISS)
    inner = ('<div class="kick">最容易少拿到折扣的三件事</div>'
             '<h1>三個<em>常犯的錯</em></h1>'
             f'<div class="list">{rows}</div>' + foot(6, n, fnote))
    out.append(('cp-06.png', page(inner)))

    # ── 7 券的形式 ──
    by = {}
    for s in sts:
        by.setdefault(s.get('form') or 'live', []).append(s['name'])
    rows = ''
    for k, (lab, why) in FORM.items():
        if k not in by:
            continue
        rows += (f'<div class="blk"><b>{E(lab)}'
                 f'<span class="tag">{len(by[k])} 家</span></b>'
                 f'<s>{E("、".join(by[k]))}<br>{E(why)}</s></div>')
    inner = ('<div class="kick">有些券不能先截圖</div>'
             '<h1>券長什麼樣，<br><em>決定你要怎麼準備</em></h1>'
             '<div class="sub">出發前能先存起來的只有靜態圖那一類。</div>'
             f'<div class="list">{rows}</div>' + foot(7, n, fnote))
    out.append(('cp-07.png', page(inner)))

    # ── 8 11/1 免稅新制 ──
    inner = ('<div class="kick">2026 年 11 月 1 日起</div>'
             '<h1>免稅改成<em>出境後才退</em></h1>'
             '<div class="list">'
             '<div class="blk"><b>券的折扣不變</b>'
             '<s>券仍然是當場扣，這一段沒有改。</s></div>'
             '<div class="blk"><b>消費稅要先付</b>'
             '<s>結帳當下要多掏一筆，出境經海關確認後才退還。'
             '最終負擔差不多，但現金流不一樣。</s></div>'
             '<div class="blk"><b>要記得完成出境手續</b>'
             '<s>沒有完成確認就退不到。購買日起有 90 天的確認期限。</s></div>'
             f'<div class="blk"><b>免稅門檻沒有變</b>'
             f'<s>{E(d["tax_note"][:96])}</s></div>'
             '</div>' + foot(8, n, fnote))
    out.append(('cp-08.png', page(inner)))

    # ── 9 查不到的與條件不明的 ──
    pend = d.get('_待複查') or []
    no = [x for x in pend if not x.get('listed')]
    soft = [x for x in pend if x.get('listed')]
    rows = ''.join(
        f'<div class="blk"><b>{E(x["store"])}'
        + ('<span class="tag">已列入，條件不明</span>' if x.get('listed')
           else '<span class="tag">沒有列入</span>')
        + f'</b><s>{E(x["why"])}</s></div>' for x in (no + soft))
    inner = ('<div class="kick">哪些數字站得住</div>'
             f'<h1>沒有官方發券頁的 <em>{len(no)} 家</em></h1>'
             f'<div class="sub">社群整理常出現，但這幾家沒有給旅客的官方折扣頁，'
             f'所以沒有列進上面那 {len(d["stores"])} 家。'
             + (f'另有 {len(soft)} 家列了，但條件沒公布。' if soft else '') + '</div>'
             f'<div class="list">{rows}</div>' + foot(9, n, fnote))
    out.append(('cp-09.png', page(inner)))

    # ── 10 百貨與電器量販 ──
    # 藥妝那篇已經單獨發過，這組是給百貨與免稅店那篇用的。
    shop = [s for s in sts if s.get('cat') != '藥妝']
    shop.sort(key=lambda s: (dead(s), -s['max']))
    def _min(s):
        # tax_min 各家寫法不一，欄位窄，只留金額。唐吉訶德那筆講的是用券門檻，
        # 其餘是免稅門檻，兩種意思不能混在一起不標。
        t = str(s['tax_min'])
        amt = re.search(r'¥[\d,]+', t)
        if not amt:
            return E(t)
        return amt.group(0) + ('<small>　用券</small>' if '可用券' in t else '')

    shop.sort(key=lambda s: (dead(s), untaxed * (1 - rate_at(s, untaxed) / 100)))
    rows = ('<div class="hd"><div class="nm">店家</div>'
            '<div class="rate">實付</div><div class="exp">省下</div></div>')
    for s in shop:
        r = rate_at(s, untaxed)
        pay = untaxed * (1 - r / 100)
        rows += (f'<div class="row"><div class="nm">{E(s["name"])}'
                 f'<s>{E(s["cat"])}・這筆適用 {r}%</s></div>'
                 f'<div class="rate">{yen(pay)}</div>'
                 f'<div class="exp">{yen(DEMO - pay)}</div></div>')
    inner = ('<div class="kick">藥妝以外的那幾家</div>'
             f'<h1>同一筆 {yen(DEMO)}，<em>實付多少</em></h1>'
             '<div class="sub">免稅每家都是 10%，差的全在券。</div>'
             f'<div class="legend">券的級距看未稅金額，含稅標價要先除以 1.1。'
             f'這裡以含稅 {yen(DEMO)}、未稅約 {yen(untaxed)} 試算。</div>'
             f'<div class="list">{rows}</div>' + foot(10, n, fnote))
    out.append(('cp-10.png', page(inner)))

    # ── 11 大丸那張券 ──
    dm = next((s for s in sts if s['name'].startswith('大丸')), None)
    if dm:
        def _w(kw):
            # 用關鍵字找，不用索引：coupons.json 的 watch 順序以後可能會變
            return next((x for x in dm['watch'] if kw in x), '')

        blocks = [('不是電子券，要到櫃台換',
                   f'{dm["how"]}。{dm["form_note"]}'),
                  ('只能用在化妝品賣場', _w('化妝品賣場')),
                  ('這些賣場不適用', _w('不適用')),
                  ('免稅還要再扣一筆手續費', _w('手續費')),
                  ('限外國籍', _w('入境未滿'))]
        rows = ''.join(f'<div class="blk"><b><i>!</i>{E(t)}</b><s>{E(b)}</s></div>'
                       for t, b in blocks if b)
        inner = ('<div class="kick">百貨那張最容易白跑</div>'
                 f'<h1>{E(dm["name"].split()[0])} 的 '
                 f'<em>{dm["max"]}% 券</em></h1>'
                 f'<div class="sub">{E(dm["combo"])}。'
                 '百貨那張看起來只有 5%，但真正會讓人白跑的是下面這幾條。</div>'
                 f'<div class="list">{rows}</div>' + foot(11, n, fnote))
        out.append(('cp-11.png', page(inner)))

    # ── 12 逐家的地雷 ──
    def _w(st, kw):
        return next((x for x in (st.get('watch') or []) if kw in x), '')

    # 每家挑不重複的兩條。watch 和 note 常講同一件事，直接接起來會變複讀。
    PICK = [('唐吉訶德', lambda x: [x.get('form_note'), _w(x, '限用一張')]),
            ('Bic Camera', lambda x: [x.get('note')]),
            ('LAOX', lambda x: [_w(x, '指定分店'), _w(x, '排除')]),
            ('愛電王', lambda x: [x.get('note')])]
    rows = ''
    for pre, pick in PICK:
        st = next((x for x in sts if x['name'].startswith(pre)), None)
        if not st:
            continue
        body = '。'.join(t.rstrip('。') for t in pick(st) if t) + '。'
        rows += (f'<div class="blk"><b><i>!</i>{E(st["name"])}</b>'
                 f'<s>{E(body)}</s></div>')
    # ── 13 級距門檻 ──
    cliff = []
    for st in sts:
        steps = st.get('steps') or []
        for i in range(1, len(steps)):
            amt, pc = steps[i]
            prev = steps[i - 1][1]
            below = (amt - 1) * (1 - prev / 100)
            at = amt * (1 - pc / 100)
            if at < below:
                cliff.append((below - at, st, amt, prev, pc, below, at))
    # 級距一樣的併成一列：松本清與 SUNDRUG 的表完全相同，分開列只是重複
    grp = {}
    for g, st, amt, p, c, b, a in cliff:
        grp.setdefault((amt, p, c), [g, [], b, a])[1].append(st['name'].split()[0])
    rows = ''.join(
        f'<div class="blk"><b>{E("、".join(v[1]))}'
        f'<span class="tag">未稅 {yen(k[0])}</span></b>'
        f'<s>{yen(k[0] - 1)} 實付 {yen(v[2])}，{yen(k[0])} 實付 {yen(v[3])}。'
        f'多 1 圓少付 {yen(v[0])}，折扣 {k[1]}% 跳 {k[2]}%。</s></div>'
        for k, v in sorted(grp.items(), key=lambda x: -x[1][0]))
    inner = ('<div class="kick">差一圓，差幾百圓</div>'
             '<h1>快到門檻時<br><em>再拿一件</em></h1>'
             '<div class="sub">券的級距看未稅金額。停在門檻下面一圓，'
             '整筆都少一級的折扣。</div>'
             f'<div class="list">{rows}</div>' + foot(13, n, fnote))
    out.append(('cp-13.png', page(inner)))

    inner = ('<div class="kick">每一家都有自己的排除條款</div>'
             '<h1>這四家<em>要先知道</em></h1>'
             '<div class="sub">折扣率一樣不代表拿得到，'
             '排除的商品與分店範圍各家不同。</div>'
             f'<div class="list">{rows}</div>' + foot(12, n, fnote))
    out.append(('cp-12.png', page(inner)))
    out[-2], out[-1] = out[-1], out[-2]   # 12 是排除條款、13 是門檻，頁碼本來就對

    # ── 14-16 掃碼直接到官方發券頁 ──
    # 券本身在店家的發券頁上，本站不重製券面。圖卡能做的是把人帶到那一頁，
    # 所以放 QR：存下這張圖，到日本掃一下就開了。
    try:
        import segno
    except ImportError:
        sys.exit('缺 segno（產 QR 用）：pip3 install --user segno')

    def qr_svg(url):
        import io as _io
        buf = _io.BytesIO()
        segno.make(url, error='m').save(buf, kind='svg', xmldecl=False,
                                        svgns=True, omitsize=True, border=2,
                                        dark='#1a1a1a')
        return buf.getvalue().decode('utf-8')

    GROUPS = [('藥妝', '藥妝', ['藥妝']),
              ('電器量販', '電器', ['電器']),
              ('百貨・綜合・運動', '其他', ['百貨', '綜合', '運動'])]
    for gi, (title, kick, cats) in enumerate(GROUPS):
        items = [x for x in sts if x['cat'] in cats and x.get('src')]
        items.sort(key=lambda x: -x['max'])
        cells = ''.join(
            f'<div class="qrc">{qr_svg(x["src"])}'
            f'<div><b>{E(x["name"].split()[0])}</b>'
            f'<s>{E(x["src_name"])}</s>'
            f'<u>{E(str(x["rate"]))}</u></div></div>' for x in items)
        inner = (f'<div class="kick">{E(kick)}・掃碼直接開</div>'
                 f'<h1>{E(title)} <em>{len(items)} 家</em><br>的官方發券頁</h1>'
                 '<div class="sub">券在店家自己的發券頁上，掃這裡直接開。'
                 '結帳前出示，有幾家要當場點開才會啟用。</div>'
                 f'<div class="qrg">{cells}</div>' + foot(14 + gi, n, fnote))
        out.append((f'cp-{14 + gi}.png', page(inner)))
    return out



def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.blk,.step,.note,.stat,.hd")];'
        'const b=it.length?Math.max(...it.map(e=>e.getBoundingClientRect().bottom)):0;'
        'return{gap:Math.round(f-b)}})())</script></body>'))
    r = subprocess.run([chrome, '--headless', '--disable-gpu', '--dump-dom',
                        '--virtual-time-budget=1500', f'file://{os.path.abspath(probe)}'],
                       capture_output=True, text=True, timeout=60)
    m = re.search(r'<title>(\{.*?\})</title>', r.stdout)
    if not m:
        print(f'   ! {name} 量不到版面，略過檢查')
        return
    gap = json.loads(htm.unescape(m.group(1)))['gap']
    if gap < 0:
        sys.exit(f'{name}：內容超出頁尾 {-gap}px，會被切掉。請減少筆數或縮小字級')
    print(f'   {name}  底部餘裕 {gap}px')


def main():
    d = json.load(open(SRC, encoding='utf-8'))
    chrome = _chrome()
    os.makedirs(OUT, exist_ok=True)
    cards = build(d, datetime.date.today().isoformat())
    with tempfile.TemporaryDirectory() as tmp:
        for name, src in cards:
            check(chrome, tmp, name, src)
            f = os.path.join(tmp, name + '.html')
            open(f, 'w', encoding='utf-8').write(src)
            png = os.path.join(OUT, name)
            subprocess.run([chrome, '--headless', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', f'--window-size={W},{H}',
                            f'--screenshot={os.path.abspath(png)}',
                            f'file://{os.path.abspath(f)}'],
                           capture_output=True, timeout=90)
            if not os.path.exists(png):
                sys.exit(f'{name} 沒有產生出來')
    open(os.path.join(OUT, 'stamp.txt'), 'w').write(fingerprint(d))
    print(f'完成 {len(cards)} 張，輸出到 {OUT}/')


if __name__ == '__main__':
    main()
