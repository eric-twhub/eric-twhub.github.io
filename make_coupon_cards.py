# -*- coding: utf-8 -*-
"""日本購物折扣券的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML，版面高度用量的、
並寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

只放頁面上也有的東西。coupons.json 裡的 _已解決、_待複查、_form_說明
是工作用的欄位，頁面沒有算繪，圖卡就不放，免得圖上講的和站上對不起來。

用法：python3 make_coupon_cards.py
輸出：japan-coupon/cards/cp-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib, datetime
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-coupon', 'cards')
SRC = 'coupons.json'
E = htm.escape
TAX = 10          # 日本消費稅，coupons.json 的 order 欄位寫明券以免稅後金額計算
DEMO = 10000      # 試算用的含稅金額
FORM = {'tap': ('點開條碼', '官方禁止截圖，要現場點開啟用'),
        'live': ('結帳前出示', '出示手機畫面或券面給店員掃'),
        'app': ('官方 App', '要先裝 App 並登入'),
        'image': ('靜態圖', '可以先存起來，離線也能用'),
        'counter': ('櫃台換紙本', '到店內服務台憑護照換')}


def fingerprint(d):
    """圖卡真正用到的欄位的指紋。"""
    pay = [[s.get(k) for k in ('name', 'jp', 'cat', 'rate', 'max', 'tax_min',
                               'form', 'expires', 'tiers')] + [s.get('steps')]
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


def yen(v):
    return f'¥{round(v):,}'


def build(d, today):
    n = 8
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
    cover = ('<div class="kick">日本購物折扣</div>'
             f'<h1>免稅 10% ＋ 券 {best["max"]}%<br><em>不是 {naive:g}%</em></h1>'
             '<div class="sub">券是以免稅後的金額計算，所以兩個百分比不能相加。'
             f'{len(sts)} 家的發券頁逐家查過。</div>'
             '<div class="stat">'
             f'<div><b>{len(sts)}</b><span>家店<br>逐家查證</span></div>'
             f'<div><b>{hi["max"]}%</b><span>帳面最高（{E(hi["name"].split()[0])}）<br>'
             + ('分級依據未公布' if hi.get('calc_caveat') else '　') + '</span></div>'
             f'<div><b>{eff:.1f}%</b><span>實際總折扣<br>不是 {naive:g}%</span></div>'
             f'<div><b>{sum(1 for s in sts if not s.get("expires"))}</b>'
             '<span>家發券頁<br>沒標有效期</span></div></div>'
             f'<div class="note">以含稅 {yen(DEMO)}、{E(best["name"].split()[0])} 的 '
             f'{best["max"]}% 券為例：免稅後約 {yen(untaxed)}，再折 {best["max"]}% 是 '
             f'{yen(after)}。省下 {yen(DEMO - after)}，等於 {eff:.1f}%。</div>'
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
