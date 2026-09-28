# -*- coding: utf-8 -*-
"""雪票早鳥的分享圖卡（1080×1350，4:5）。

和 make_picks_cards.py／make_creditcard_cards.py 同一套：Chrome headless 算繪 HTML，
版面高度用量的不是目測的，並寫出 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。

**不掛在每日 workflow 上。** 票價與截止日變動時在本機重跑。
気象庁 會在 2026-10-20 修正寒候期予報，那時要連同 ski-ticket.json 一起更新再重跑。

用法：python3 make_ski_cards.py
輸出：japan-ski-lift-ticket/cards/ski-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib, datetime
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-ski-lift-ticket', 'cards')
SRC = 'ski-ticket.json'
E = htm.escape
# 卡片上不放超連結，把資料裡的 <b> 之類的標記去掉再顯示
TAG = re.compile(r'<[^>]+>')


def plain(s):
    return E(TAG.sub('', s))


def fingerprint(d):
    """圖卡真正用到的欄位的指紋。用途同 make_picks_cards.fingerprint。"""
    pay = [[t.get(k) for k in ('n', 'pref', 'was', 'now', 'cut', 'form')]
           for t in d['tickets']]
    pay.append([[m['q'], TAG.sub('', m['a'])] for m in d['myths']])
    pay.append([[c['d'], c['w'], c['k'], c['note']] for c in d['calendar']])
    pay.append([list(r) for r in d['jma']['snow']] + [list(r) for r in d['jma']['temp']])
    pay.append([d['jma']['issued'], d['jma']['next_rev'], d['season'], d['checked']])
    pay.append([d['gap']['t'], d['gap']['body'], d['gap']['conc']])
    pay.append([[c['n'], c['good'], c['bad'], c['cur']] for c in d['channels']])
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
.list{margin-top:26px;flex:1 1 auto;min-height:0}
.hd{display:flex;gap:12px;align-items:flex-end;padding:0 0 9px;
 font-size:20px;color:#8a847c;border-bottom:2px solid #1a1a1a}
.row{display:flex;gap:12px;align-items:baseline;padding:14px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.num{flex:0 0 44px;font-size:23px;font-weight:700;color:#c2410c;
 font-variant-numeric:tabular-nums}
.nm{flex:1 1 auto;font-size:30px;font-weight:700;line-height:1.28;letter-spacing:-.01em}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;letter-spacing:0}
.c1{flex:0 0 150px;text-align:right;font-size:26px;font-weight:700;color:#c2410c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.c1 small{font-size:19px;font-weight:500;color:#8a847c;display:block;margin-top:3px}
.c2{flex:0 0 140px;text-align:right;font-size:24px;color:#63605c;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.c2.soon{color:#c4563a;font-weight:700}
/* 誤解卡 */
.myth{padding:12px 0;border-bottom:1px solid #e5e3de}
.myth:last-child{border-bottom:0}
.myth b{display:block;font-size:30px;font-weight:700;margin-bottom:7px}
.myth b i{font-style:normal;color:#c4563a;margin-right:10px}
.myth s{display:block;text-decoration:none;font-size:24px;color:#3f3b37;line-height:1.75}
/* 時間表 */
.tl{display:flex;gap:14px;padding:7px 0;border-bottom:1px solid #e5e3de}
.tl:last-child{border-bottom:0}
.tl i{font-style:normal;flex:0 0 96px;font-size:26px;font-weight:700;
 font-variant-numeric:tabular-nums}
.tl i span{display:block;font-size:19px;font-weight:600;margin-top:3px}
.tl div{flex:1 1 auto}
.tl b{display:block;font-size:26px;margin-bottom:3px}
.tl p{font-size:20px;color:#63605c;line-height:1.55}
.jma i{color:#3f7ae0}
.cut i{color:#c2410c}
.use i{color:#8a847c}
/* 機率條 */
.bar{display:flex;height:34px;border-radius:5px;overflow:hidden;
 font-size:19px;line-height:34px;text-align:center;color:#fff;font-weight:700}
.bar u{text-decoration:none;flex:0 0 auto}
.b1{background:#e07a3f}.b2{background:#cfc9c0;color:#1a1a1a}.b3{background:#3f7ae0}
.prow{padding:13px 0;border-bottom:1px solid #e5e3de}
.prow:last-child{border-bottom:0}
.prow b{display:block;font-size:27px;margin-bottom:3px}
.prow b span{font-weight:500;font-size:21px;color:#8a847c;margin-left:8px}
.prow p{font-size:20px;color:#63605c;margin-top:6px}
/* 通路卡 */
.ch{padding:15px 0;border-bottom:1px solid #e5e3de}
.ch:last-child{border-bottom:0}
.ch b{display:block;font-size:30px;margin-bottom:6px}
.ch b i{font-style:normal;font-size:21px;color:#8a847c;font-weight:500;margin-left:10px}
.ch s{display:block;text-decoration:none;font-size:22px;line-height:1.65;margin-top:4px}
.ok{color:#2f8f4f}.ng{color:#c4563a}
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


def first_sentence(s, cap):
    """取第一句。整段註解放進時間表會把九列撐出版面，而截在半句又難讀。"""
    t = s.split('。')[0] + '。'
    return t if len(t) <= cap else s[:cap - 1] + '…'


def off(t):
    return round((t['was'] - t['now']) / t['was'] * 100)


def build(d, today):
    n = 8
    tk = d['tickets']
    J = d['jma']
    fnote = f'票價與截止日查證於 {d["checked"]}，售完即提前結束'
    out = []
    deepest = max(tk, key=off)
    soon = sorted({t['cut'] for t in tk})[0]
    soon_n = sum(1 for t in tk if t['cut'] == soon)
    days = (datetime.date.fromisoformat(soon) - today).days

    # ── 1 封面 ──
    east = next(r for r in J['snow'] if r[0] == '東日本日本海側')
    cover = ('<div class="kick">2026-27 雪季</div>'
             f'<h1>早鳥雪票最多<em> {off(deepest)}% off</em>，<br>但退不掉</h1>'
             f'<div class="sub">{len(tk)} 個雪場的原價、早鳥價與截止日逐項抄自商品頁。'
             '<br>它綁的不是日期，是雪場。</div>'
             '<div class="stat">'
             f'<div><b>{len(tk)}</b><span>個雪場<br>逐項查證</span></div>'
             f'<div><b>{off(deepest)}%</b><span>成人票最深<br>（{E(deepest["n"])}）</span></div>'
             f'<div><b>{east[2]}%</b><span>本州日本海側<br>降雪偏少機率</span></div>'
             f'<div><b>{days}</b><span>天後<br>第一批截止</span></div></div>'
             '<div class="note">訂購當天 23:59 過後，'
             '「理由の如何を問わず」不受理取消。而同一頁又寫明，'
             '雪場的營業期間不在保證範圍內。</div>' + foot(1, n, fnote))
    out.append(('ski-01.png', page(cover, 'cover')))

    # ── 2、3 誤解 ──
    def myth_card(idx, part, items):
        rows = ''.join(
            f'<div class="myth"><b><i>✗</i>「{plain(m["q"])}」</b>'
            f'<s>{plain(m["a"])}</s></div>' for m in items)
        return ('<div class="kick">買之前先拆掉的誤解</div>'
                '<h1>四個<em>常見誤解</em></h1>'
                f'<div class="list">{rows}</div>' + foot(idx, n, fnote))

    out.append(('ski-02.png', page(myth_card(2, '', d['myths']))))

    # ── 3 共通券：把「去哪個雪場」的決定往後延 ──
    rows = ''.join(
        f'<div class="ch"><b>{E(c["n"])}<i>{E(c["who"])}</i></b>'
        f'<s><b style="display:inline;font-size:24px">{E(c["price"])}</b>'
        f'　截止 {E(c["cut"])}</s>'
        f'<s class="ok">{E(c["pick"])}</s>'
        f'<s class="ng">取消：{E(c["cancel"])}</s></div>' for c in d['common'])
    inner = ('<div class="kick">不想現在就決定去哪座山</div>'
             '<h1>共通券換到的是<em>選擇權</em>，<br>不是退票權</h1>'
             '<div class="sub">共通券讓你先付錢、到現場再選雪場。'
             '但它的定價是照涵蓋範圍裡的高價雪場訂的。</div>'
             f'<div class="list">{rows}</div>' + foot(3, n, fnote))
    out.append(('ski-03.png', page(inner)))

    # ── 4 時間表 ──
    KIND = {'jma': '預報', 'cut': '截止', 'use': '生效'}
    rows = ''.join(
        f'<div class="tl {c["k"]}"><i>{c["d"][5:].replace("-", "/")}'
        f'<span>{KIND[c["k"]]}</span></i>'
        f'<div><b>{E(c["w"])}</b><p>{E(first_sentence(c["note"], 40))}</p></div></div>'
        for c in d['calendar'] if c['k'] != 'use')
    inner = ('<div class="kick">這一頁真正的重點</div>'
             '<h1>截止日<em>對上</em>預報更新日</h1>'
             '<div class="sub">9/30 那批必須在気象庁 修正預報之前決定，等不到新資訊；'
             '12 月才截止的那批等得到。</div>'
             '<div class="legend">日期皆為 2026 年。藍色是預報更新日，橘色是早鳥票截止日。</div>'
             f'<div class="list">{rows}</div>' + foot(4, n, fnote))
    out.append(('ski-04.png', page(inner)))

    # ── 5 気象庁 ──
    def bar(lo, mid, hi):
        return ('<div class="bar">'
                f'<u class="b1" style="width:{lo}%">{lo}</u>'
                f'<u class="b2" style="width:{mid}%">{mid}</u>'
                f'<u class="b3" style="width:{hi}%">{hi}</u></div>')

    rows = ''.join(
        f'<div class="prow"><b>{E(r[0])}<span>{E(r[1])}</span></b>'
        f'{bar(r[2], r[3], r[4])}<p>{E(r[5])}</p></div>' for r in J['snow'])
    _t = {r[0]: r for r in J['temp']}
    rows += ('<div class="prow" style="border-bottom:0"><b>同一份預報的氣溫</b>'
             f'<p style="font-size:22px;line-height:1.7">平均氣溫偏高的機率，'
             f'東日本與西日本都是 {_t["東日本"][4]}%，北日本 {_t["北日本"][4]}%。'
             '氣溫與降雪量是兩件事，暖冬不等於整季都沒雪。</p></div>')
    inner = ('<div class="kick">官方怎麼寫的</div>'
             '<h1>本州日本海側<br><em>降雪偏少 50%</em></h1>'
             f'<div class="sub">気象庁 寒候期予報（12 月至 2 月），{J["issued"]} 發布。</div>'
             '<div class="legend">左橘＝偏少，中灰＝平年並，右藍＝偏多，單位百分比。'
             f'{J["next_rev"]} 會配合 10 月的 3 か月予報 重新檢討並修正發布。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n, '出處：気象庁 季節予報'))
    out.append(('ski-05.png', page(inner)))

    # ── 6 快截止的 ──
    urgent = sorted([t for t in tk if t['cut'] <= '2026-10-31'],
                    key=lambda t: (t['cut'], -off(t)))
    rows = ('<div class="hd"><div class="num"></div><div class="nm">雪場</div>'
            '<div class="c1">早鳥價</div><div class="c2">截止</div></div>')
    for j, t in enumerate(urgent, 1):
        rows += (f'<div class="row"><div class="num">{j:02}</div>'
                 f'<div class="nm">{E(t["n"])}<s>{E(t["pref"])}・原價 ¥{t["was"]:,}</s></div>'
                 f'<div class="c1">¥{t["now"]:,}<small>{off(t)}% off</small></div>'
                 f'<div class="c2{" soon" if t["cut"] == soon else ""}">'
                 f'{t["cut"][5:].replace("-", "/")}</div></div>')
    inner = ('<div class="kick">先看快沒的</div>'
             f'<h1>10 月底前截止的<em> {len(urgent)} 個</em></h1>'
             f'<div class="sub">紅色那批在 {soon[5:].replace("-", "/")} 結束，'
             f'只剩 {days} 天，而且等不到 {J["next_rev"]} 的預報修正。</div>'
             f'<div class="legend">其餘 {len(tk) - len(urgent)} 個雪場賣到 12 月中之後，'
             '可以等預報更新再決定。</div>'
             f'<div class="list">{rows}</div>' + foot(6, n, fnote))
    out.append(('ski-06.png', page(inner)))

    # ── 7 北海道的缺口 ──
    g = d['gap']
    north = next(r for r in J['snow'] if r[0] == '北日本日本海側')
    inner = ('<div class="kick">查下去才發現的</div>'
             f'<h1>想避開雪況風險去北海道，<br><em>正好買不到早鳥票</em></h1>'
             f'<div class="list">'
             f'<div class="note" style="margin-top:26px">{plain(g["body"])}</div>'
             f'<div class="note" style="border-left-color:#3f7ae0">'
             f'{plain(g["conc"])}</div>'
             f'<div class="prow" style="border:0;padding-top:22px">'
             f'<b>北日本日本海側<span>北海道、東北</span></b>'
             f'<div class="bar"><u class="b1" style="width:{north[2]}%">{north[2]}</u>'
             f'<u class="b2" style="width:{north[3]}%">{north[3]}</u>'
             f'<u class="b3" style="width:{north[4]}%">{north[4]}</u></div>'
             f'<p>{E(north[5])}</p></div>'
             '</div>' + foot(7, n, fnote))
    out.append(('ski-07.png', page(inner)))

    # ── 8 台灣人從哪買 ──
    rows = ''.join(
        f'<div class="ch"><b>{E(c["n"])}<i>{E(c["lang"])}・{E(c["cur"])}</i></b>'
        f'<s class="ok">好處：{E(c["good"])}</s>'
        f'<s class="ng">代價：{E(c["bad"][:96])}</s></div>' for c in d['channels'])
    inner = ('<div class="kick">台灣人買得到嗎</div>'
             '<h1>三個通路，<em>門檻差很多</em></h1>'
             '<div class="sub">紙本票實務上只寄日本，而且 10 月下旬才出貨。'
             '要買就挑電子票。</div>'
             f'<div class="list">{rows}</div>' + foot(8, n, fnote))
    out.append(('ski-08.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.myth,.tl,.prow,.ch,.note,.stat,.hd")];'
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
    cards = build(d, datetime.date.today())
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
