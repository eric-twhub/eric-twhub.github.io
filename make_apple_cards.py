# -*- coding: utf-8 -*-
"""台日 Apple 價差的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML、版面高度用量的、
寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

**匯率每天都會動**，所以卡片上印出匯率與報價時間。指紋只涵蓋品項與定價，
不含匯率，否則每天都會跳過期警告；價格或機種變動時才需要重跑。

用法：python3 make_apple_cards.py
輸出：apple-japan-price/cards/ap-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
OUT = os.path.join('apple-japan-price', 'cards')
SRC = 'apple.json'
E = htm.escape
VAT = 0.05          # 手機關稅 0%，超過免稅額的部分主要是 5% 營業稅
# 刷卡試算的前提，與頁面上的「加上信用卡回饋」同一組假設
OV, FEE = 0.03, 0.015


def fingerprint(d):
    """只涵蓋品項與定價。匯率天天變，放進來會每天誤報。"""
    pay = [[p.get(k) for k in ('cat', 'name', 'spec', 'jpy', 'twd', 'new')]
           for p in d['products']]
    pay.append([d['tax']['jp_consumption'], d['tax']['tw_duty_free_allowance'],
                d['price_checked']])
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
.nm{flex:1 1 auto;font-size:29px;font-weight:700;line-height:1.28;letter-spacing:-.01em}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;letter-spacing:0}
.v{flex:0 0 146px;text-align:right;font-size:25px;color:#63605c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.sv{flex:0 0 148px;text-align:right;font-size:29px;font-weight:800;color:#2f8f4f;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.sv.neg{color:#c4563a}
.sv small{display:block;font-size:19px;font-weight:600;color:#8a847c;margin-top:3px}
.blk{padding:15px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:30px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c2410c;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.7}
.foot{flex:0 0 auto;padding:24px 0 42px;border-top:3px solid #1a1a1a;
 display:flex;justify-content:space-between;align-items:flex-end;margin-top:18px}
.foot b{font-size:28px;font-weight:800;display:block}
.foot span{font-size:22px;color:#63605c;display:block;margin-top:6px}
.pg{font-size:24px;color:#63605c;font-weight:700}
.cover{justify-content:center}
.cover .list{flex:0 0 auto;margin-top:0}
.stat{display:flex;gap:14px;margin-top:36px}
.stat div{flex:1;background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:22px 20px}
.stat b{display:block;font-size:44px;font-weight:800;color:#c2410c;line-height:1.1;
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


def nt(v):
    return f'NT${round(v):,}'


def build(d):
    n = 8
    MID = d['rate']['jpy_twd_mid']
    CUR = d['rate']['jpy_twd']            # 中間匯率＋換匯成本，頁面上的「目前匯率」
    SP = d['rate']['spread']
    TAXR = 1 + d['tax']['jp_consumption']
    AL = d['tax']['tw_duty_free_allowance']
    ps = d['products']
    fnote = (f'定價核對於 {d["price_checked"]}　匯率 {CUR}'
             f'（含約 {round(SP * 100, 1)}% 換匯成本）')
    out = []

    def jp_cash(p):
        """量販店免稅價，換成台幣，含換匯成本。"""
        return p['jpy'] / TAXR * MID * (1 + SP)

    def raw(p):
        return p['twd'] - jp_cash(p)

    def duty(p):
        return max(0.0, jp_cash(p) - AL) * VAT

    def flip_rate(p):
        """日本免稅價與台灣售價打平的匯率。"""
        return p['twd'] / (p['jpy'] / TAXR)

    ip = [p for p in ps if p['cat'] == 'iPhone']
    etc = [p for p in ps if p['cat'] != 'iPhone']
    over = [p for p in ps if jp_cash(p) > AL]
    best = max(ps, key=raw)
    worst = min(ps, key=raw)

    # ── 1 封面 ──
    cover = ('<div class="kick">台日 Apple 定價</div>'
             '<h1>日本買比較便宜，<br><em>但別忘了報關</em></h1>'
             f'<div class="sub">{len(ps)} 個品項照 Apple 日本／台灣官網定價逐項換算。'
             '日本要到有 Tax-Free 標示的量販店才拿得到免稅價。</div>'
             '<div class="stat">'
             f'<div><b>{nt(raw(best))}</b>'
             f'<span>省最多<br>{E(best["name"])} {E(best["spec"])}</span></div>'
             f'<div><b>{raw(best) / best["twd"] * 100:.0f}%</b>'
             '<span>換算成<br>比例</span></div>'
             f'<div><b>{len(over)}/{len(ps)}</b><span>個品項超過<br>入境免稅額</span></div>'
             f'<div><b>{nt(duty(best))}</b><span>那一支要補的<br>5% 營業稅</span></div></div>'
             f'<div class="note">台灣入境行李免稅額 {nt(AL)}，超出部分要申報。'
             f'手機關稅 0%，主要是 5% 營業稅。'
             f'{E(best["name"])} {E(best["spec"])} 帳面省 {nt(raw(best))}，'
             f'補完稅實際是 {nt(raw(best) - duty(best))}。</div>'
             + foot(1, n, fnote))
    out.append(('ap-01.png', page(cover, 'cover')))

    # ── 2、3 iPhone 價差 ──
    def price_card(idx, title, items, sub):
        rows = ('<div class="hd"><div class="nm">機型</div>'
                '<div class="v">日本免稅價</div><div class="v">台灣售價</div>'
                '<div class="sv">價差</div></div>')
        for p in items:
            r = raw(p)
            rows += (f'<div class="row"><div class="nm">{E(p["name"])}'
                     f'<s>{E(p["spec"])}</s></div>'
                     f'<div class="v">{nt(jp_cash(p))}</div>'
                     f'<div class="v">{nt(p["twd"])}</div>'
                     f'<div class="sv{" neg" if r < 0 else ""}">{r:+,.0f}'
                     f'<small>{r / p["twd"] * 100:+.1f}%</small></div></div>')
        return ('<div class="kick">台日定價對照</div>'
                f'<h1>{title}</h1>'
                f'<div class="sub">{sub}</div>'
                '<div class="legend">日本欄是量販店免稅價（日圓定價 ÷ 1.1）換成台幣，'
                f'已含約 {round(SP * 100, 1)}% 換匯成本。綠色是日本比較便宜。</div>'
                f'<div class="list">{rows}</div>' + foot(idx, n, fnote))

    out.append(('ap-02.png', page(price_card(
        2, 'iPhone <em>①</em>', ip[:8], '依官網定價排列，容量由小到大。'))))
    out.append(('ap-03.png', page(price_card(
        3, 'iPhone <em>②</em>', ip[8:], '同一組換算方式。'))))
    out.append(('ap-04.png', page(price_card(
        4, 'Watch 與 <em>AirPods</em>', etc,
        f'配件的價差小很多，{E(worst["name"])} 甚至是日本比較貴。'))))

    # ── 5 申報 ──
    top = sorted(over, key=lambda p: -raw(p))[:7]
    rows = ('<div class="hd"><div class="nm">機型</div>'
            '<div class="v">帳面省</div><div class="v">5% 營業稅</div>'
            '<div class="sv">實際省</div></div>')
    for p in top:
        rows += (f'<div class="row"><div class="nm">{E(p["name"])}'
                 f'<s>{E(p["spec"])}</s></div>'
                 f'<div class="v">{raw(p):+,.0f}</div>'
                 f'<div class="v">−{duty(p):,.0f}</div>'
                 f'<div class="sv">{raw(p) - duty(p):+,.0f}</div></div>')
    inner = ('<div class="kick">帳面價差不是你實際省的</div>'
             f'<h1>{len(over)} 個品項<br><em>超過入境免稅額</em></h1>'
             f'<div class="sub">台灣入境行李免稅額 {nt(AL)}，超出的要申報。</div>'
             f'<div class="legend">手機關稅 0%，主要是 5% 營業稅，'
             f'而且只課超出的那一段，不是全額。以下列價差最大的 7 個，'
             f'實際以海關核定為準。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n, fnote))
    out.append(('ap-05.png', page(inner)))

    # ── 6 臨界匯率 ──
    fl = sorted([p for p in ip], key=lambda p: flip_rate(p))[:7]
    rows = ('<div class="hd"><div class="nm">機型</div>'
            '<div class="v">現在省</div><div class="v">臨界匯率</div>'
            '<div class="sv">日圓還需升值</div></div>')
    for p in fl:
        fr = flip_rate(p)
        rows += (f'<div class="row"><div class="nm">{E(p["name"])}'
                 f'<s>{E(p["spec"])}</s></div>'
                 f'<div class="v">{raw(p):+,.0f}</div>'
                 f'<div class="v">{fr:.4f}</div>'
                 f'<div class="sv">{(fr / CUR - 1) * 100:.1f}%</div></div>')
    inner = ('<div class="kick">這個答案有保存期限</div>'
             '<h1>日圓要升值多少，<br><em>結論才會翻盤</em></h1>'
             f'<div class="sub">目前匯率 {CUR}。日圓升值時，日本售價換成台幣就變貴，'
             '價差隨之縮小。</div>'
             '<div class="legend">臨界匯率＝日本免稅價與台灣售價打平的那個匯率，'
             '越接近現在的匯率越禁不起日圓走強。以下列最禁不起的 7 個。</div>'
             f'<div class="list">{rows}</div>' + foot(6, n, fnote))
    out.append(('ap-06.png', page(inner)))

    # ── 7 刷卡回饋 ──
    need = []
    for p in ip:
        jp_card = p['jpy'] / TAXR * MID * (1 + FEE) * (1 - OV)
        need.append((1 - jp_card / p['twd'], p))
    need.sort()
    lo, hi = need[0], need[-1]
    inner = ('<div class="kick">別只看機身標價</div>'
             '<h1>台灣的回饋夠高，<br><em>結論就翻過來</em></h1>'
             f'<div class="sub">假設海外刷卡回饋 {OV * 100:.0f}%、'
             f'國外交易手續費 {FEE * 100:.1f}%。</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>→</i>國內回饋只要 {lo[0] * 100:.1f}% 到 '
             f'{hi[0] * 100:.1f}%</b>'
             f'<s>日本的免稅價差就被完全抵銷。門檻最低的是 {E(lo[1]["name"])} '
             f'{E(lo[1]["spec"])}（{lo[0] * 100:.1f}%），'
             f'最高的是 {E(hi[1]["name"])} {E(hi[1]["spec"])}（{hi[0] * 100:.1f}%）。</s></div>'
             '<div class="blk"><b><i>→</i>新機上市期間的加碼常到這個量級</b>'
             '<s>國內通路在首購期間的回饋活動確實出現過 10% 以上，'
             '所以這個門檻不是理論值。</s></div>'
             '<div class="blk"><b><i>→</i>海外刷卡要先加手續費</b>'
             '<s>多數發卡行約 1.5%（國際組織 1% ＋ 發卡行 0.5%，'
             '金管會規定發卡行加收不得逾 0.5%）。美國運通約 2%。</s></div>'
             '</div>' + foot(7, n, fnote))
    out.append(('ap-07.png', page(inner)))

    # ── 8 買之前要知道的 ──
    inner = ('<div class="kick">價差之外的成本</div>'
             '<h1>買之前<em>要知道的</em></h1>'
             '<div class="list">'
             '<div class="blk"><b><i>01</i>Apple 直營店已經不能退稅</b>'
             '<s>日本直營店自 2024 年 6 月起取消對外國旅客的免稅服務。'
             '要拿到免稅價，得去有 Tax-Free 標示的家電量販店（Bic Camera、'
             'Yodobashi 等），結帳時出示護照。量販店定價未必和官網相同。</s></div>'
             '<div class="blk"><b><i>02</i>量販店的折扣券，Apple 用不到</b>'
             '<s>那些 5% 到 7% 的旅客折扣券多半排除 Apple 商品，'
             '別把券的折扣也算進價差裡。</s></div>'
             '<div class="blk"><b><i>03</i>保固是區域性的</b>'
             '<s>日本買的機器在台灣的授權維修中心可能不受理，需要寄回日本處理。'
             '重視售後就要把這個風險計入。</s></div>'
             '<div class="blk"><b><i>04</i>兩三年後的回收價差更大</b>'
             '<s>台日價差多半是幾千元，但同一支機器的二手回收行情差距往往更大。'
             '用每月持有成本來看，結論常常不一樣。</s></div>'
             '</div>' + foot(8, n, fnote))
    out.append(('ap-08.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.blk,.note,.stat,.hd")];'
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
    cards = build(d)
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
