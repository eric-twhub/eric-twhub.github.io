# -*- coding: utf-8 -*-
"""東京 46 家店的分享圖卡（1080×1350，4:5）。

和 make_og_cards.py 一樣用 Chrome headless 算繪 HTML，但兩者的用途不同：
og 圖卡是每頁一張、給社群預覽用的；這一組是把整份清單做成可以直接發文的輪播。

**不掛在每日 workflow 上。** 資料只有在 tokyo-picks.json 變動時才需要重產，
而字型在 macOS 與 CI 的 Linux 上度量不同，每天在 CI 重產只會讓同樣的內容
產生不同的二進位檔，repo 天天長肥。要重產就在本機手動跑。

版面高度是算出來的不是目測的：每張卡都會檢查最後一列有沒有撞到頁尾，
撞到就直接報錯，不會默默輸出一張被切掉的圖。2026-09-28 第一版就是
目測覺得沒事、實際上第 9、10 列整個被切掉。

用法：python3 make_picks_cards.py
輸出：tokyo/worth-flying-for/cards/tokyo-46-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile
import html as htm

W, H = 1080, 1350
OUT = os.path.join('tokyo', 'worth-flying-for', 'cards')
SRC = 'tokyo-picks.json'
E = htm.escape


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


def likes(s):
    """原貼文那則留言的讚數。沒擷取到就是 0，用來排序時墊底，但不印成 0。"""
    return (s.get('src') or {}).get('likes') or 0


def area(s):
    """從地址抽一個看得懂的地名。町名比行政區好認（淺草 > 台東區）。"""
    a = s.get('addr') or ''
    m = re.search(r'東京都(.{1,4}?區)', a)
    if m:
        w = m.group(1)
        m2 = re.search(re.escape(w) + r'([^\d\s，,（(]{1,5}?)\s*\d', a)
        if m2 and len(m2.group(1)) >= 2:
            return m2.group(1)
        return w
    m = re.search(r'(千葉縣[^\d]{1,6}市)', a)
    if m:
        return m.group(1).replace('千葉縣', '')
    if '多家分店' in a or '東京多家' in a:
        return '多家分店'
    m = re.search(r'^([^：]{2,6})店：', a)
    if m:
        return m.group(1)
    return '東京'


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;
 font-family:"Noto Sans CJK TC","Noto Sans TC","PingFang TC","Hiragino Sans",
 "Hiragino Sans GB","Heiti TC",sans-serif;
 background:#f7f7f5;color:#1a1a1a;-webkit-font-smoothing:antialiased}
.card{width:1080px;height:1350px;padding:60px 68px 0;display:flex;flex-direction:column;
 background:#f7f7f5}
.kick{font-size:26px;color:#c2410c;font-weight:700;letter-spacing:.06em;margin-bottom:14px}
h1{font-size:60px;line-height:1.24;font-weight:800;letter-spacing:-.01em}
h1 em{font-style:normal;color:#c2410c}
.sub{font-size:28px;line-height:1.7;color:#63605c;margin-top:18px}
.list{margin-top:34px;flex:1 1 auto;min-height:0}
.row{display:flex;gap:20px;align-items:baseline;padding:16px 0;border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.num{flex:0 0 48px;font-size:25px;font-weight:700;color:#c2410c;font-variant-numeric:tabular-nums}
.nm{flex:1 1 auto;font-size:34px;font-weight:700;line-height:1.3;letter-spacing:-.01em}
.mt{flex:0 0 auto;font-size:23px;color:#63605c;white-space:nowrap;padding-left:14px;
 text-align:right;line-height:1.3}
.lk{flex:0 0 132px;font-size:25px;font-weight:700;color:#c2410c;text-align:right;
 white-space:nowrap;font-variant-numeric:tabular-nums;line-height:1.3}
.lk small{font-size:19px;font-weight:500;color:#63605c;margin-left:3px}
.lk.non{color:#b4afa8;font-weight:500}
.legend{font-size:22px;color:#63605c;margin-top:10px;line-height:1.6}
.dead .nm{text-decoration:line-through;text-decoration-thickness:2px;color:#c4563a}
.dead .mt{color:#c4563a}
.foot{flex:0 0 auto;padding:26px 0 44px;border-top:3px solid #1a1a1a;
 display:flex;justify-content:space-between;align-items:flex-end;margin-top:20px}
.foot b{font-size:29px;font-weight:800;display:block}
.foot span{font-size:23px;color:#63605c;display:block;margin-top:7px}
.pg{font-size:25px;color:#63605c;font-weight:700}
.cover{justify-content:center}
.cover .list{flex:0 0 auto;margin-top:0}
.stat{display:flex;gap:15px;margin-top:40px}
.stat div{flex:1;background:#fff;border:1px solid #e5e3de;border-radius:16px;padding:24px 22px}
.stat b{display:block;font-size:50px;font-weight:800;color:#c2410c;line-height:1.1;
 font-variant-numeric:tabular-nums}
.stat span{display:block;font-size:23px;color:#63605c;margin-top:9px;line-height:1.5}
.note{margin-top:38px;background:#fff;border:1px solid #e5e3de;border-left:7px solid #c2410c;
 border-radius:14px;padding:28px 30px;font-size:26px;line-height:1.75}
.fix{padding:9px 0;border-bottom:1px solid #e5e3de}
.fix:last-child{border-bottom:0}
.fix b{display:block;font-size:27px;line-height:1.4;font-weight:700}
.fix i{font-style:normal;color:#c4563a;text-decoration:line-through;text-decoration-thickness:2px}
.fix u{text-decoration:none;color:#2f8f4f}
.fix s{display:block;text-decoration:none;font-size:21px;color:#63605c;margin-top:5px;
 line-height:1.45;font-weight:400}
.fix em{font-style:normal;font-weight:800;margin-right:9px}
.bad em{color:#c4563a}
.ok em{color:#2f8f4f}
.ok i{color:#1a1a1a;text-decoration:none}
"""


def page(inner, cls=''):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS}</style></head><body><div class="card {cls}">{inner}</div>'
            '</body></html>')


def foot(i, n):
    return ('<div class="foot"><div><b>eric-twhub.github.io</b>'
            '<span>每家回查官方地址、營業時間與公休</span></div>'
            f'<div class="pg">{i} / {n}</div></div>')


def build(d):
    """回傳 [(檔名, html)]。"""
    S, by = d['stores'], {}
    for s in S:
        by.setdefault(s['grp'], []).append(s)
    meat = by['肉']
    SET = ('壽喜燒', '燒肉', '和牛燒肉', '鐵板燒', '壽喜燒與鐵板燒')
    m1 = [x for x in meat if x['cat'] in SET]
    m2 = [x for x in meat if x['cat'] not in SET]
    groups = [('肉 ①', '壽喜燒、燒肉、鐵板燒', m1),
              ('肉 ②', '炸豬排、漢堡排、牛舌、牛排', m2),
              ('麵與披薩', '拉麵、煮干、拿坡里', by['麵'] + by['披薩']),
              ('海鮮與甜點', '壽司、鰻魚、海鮮丼、蛋糕', by['海鮮'] + by['甜點與咖啡']),
              ('購物與文具', '紙品、畫材、角色商品', by['購物與文具']),
              ('景點與其他', '錢湯、劇場、樂園、酒吧', by['景點與其他'])]
    got = sum(len(g[2]) for g in groups)
    if got != len(S):
        sys.exit(f'分組漏了店：{got} != {len(S)}。tokyo-picks.json 的 grp 可能新增了分類')

    n = len(groups) + 2
    src = d['source']
    off = sum(1 for x in S if x.get('official'))
    bad = sum(1 for _, _, c in d['corrections'] if '成立' not in c)
    withlikes = sum(1 for x in S if likes(x))
    out = []

    cover = ('<div class="kick">Threads 查證系列</div>'
             f'<h1>東京，值得為它<br><em>再飛一次</em>的 {len(S)} 家店</h1>'
             f'<div class="sub">一則 {E(src["views"])}、{src["replies"]:,} 則回覆的討論串。<br>'
             '本站沒有照抄留言，每家都回查了官方資料。</div>'
             '<div class="stat">'
             '<div><b>602</b><span>則有內容的<br>回覆解析</span></div>'
             f'<div><b>{len(S)}</b><span>家店<br>整理出來</span></div>'
             f'<div><b>{off}</b><span>家找到<br>官方網站</span></div>'
             f'<div><b>{bad}</b><span>處留言<br>要修正</span></div></div>'
             '<div class="note">排序依原貼文的讚數，不是本站評的。'
             f'{len(S)} 家裡有 {withlikes} 家擷取得到讚數，其餘標「—」。</div>'
             + foot(1, n))
    out.append(('tokyo-46-01.png', page(cover, 'cover')))

    for i, (t, sub, items) in enumerate(groups, 2):
        # 和網頁同一個排序鍵：原貼文的讚數由多到少。沒有擷取到讚數的排在後面，
        # 維持原序。不要補 0，那等於宣稱它得了 0 個讚。
        items = sorted(items, key=lambda x: -likes(x))
        rows = ''
        for j, s in enumerate(items, 1):
            dead = s.get('status')
            meta = E(dead) if dead else E(s['cat']) + ' · ' + E(area(s))
            lk = likes(s)
            lkh = (f'<div class="lk">{lk:,}<small>讚</small></div>' if lk
                   else '<div class="lk non">—</div>')
            rows += (f'<div class="row{" dead" if dead else ""}">'
                     f'<div class="num">{j:02}</div>'
                     f'<div class="nm">{E(s["n"])}</div>'
                     f'<div class="mt">{meta}</div>{lkh}</div>')
        got = sum(1 for x in items if likes(x))
        inner = ('<div class="kick">東京 · 值得再飛一次</div>'
                 f'<h1>{E(t)}<em> {len(items)}</em></h1>'
                 f'<div class="sub">{E(sub)}</div>'
                 f'<div class="legend">依原貼文的讚數排序。'
                 f'這 {len(items)} 家裡有 {got} 家擷取得到讚數，'
                 f'其餘標「—」，不是零讚，是沒有數字。</div>'
                 f'<div class="list">{rows}</div>' + foot(i, n))
        out.append((f'tokyo-46-{i:02}.png', page(inner)))

    fixes = ''
    for a, b, c in d['corrections']:
        ok = '成立' in c
        fixes += (f'<div class="fix {"ok" if ok else "bad"}">'
                  f'<b><em>{"✓" if ok else "✗"}</em><i>{E(a)}</i> → <u>{E(b)}</u></b>'
                  f'<s>{E(c)}</s></div>')
    inner = ('<div class="kick">這是留言區給不了的</div>'
             '<h1>留言說的，<em>跟查到的</em></h1>'
             f'<div class="sub">{len(d["corrections"])} 則回查，{bad} 則要修正，'
             f'{len(d["corrections"]) - bad} 則證實留言是對的。</div>'
             f'<div class="list" style="margin-top:20px">{fixes}</div>' + foot(n, n))
    out.append((f'tokyo-46-{n:02}.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    """量最後一列的底部有沒有超過頁尾的頂端。目測看不出被切掉，所以用算的。"""
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.fix,.note,.stat")];'
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
        sys.exit(f'{name}：內容超出頁尾 {-gap}px，會被切掉。請減少每張的筆數或縮小字級')
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
    print(f'完成 {len(cards)} 張，輸出到 {OUT}/')


if __name__ == '__main__':
    main()
