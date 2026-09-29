# -*- coding: utf-8 -*-
"""日本 eSIM 比較的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML、版面高度用量的、
寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

profile（原生／漫遊）五個商品都還是 null，那是要實機測才知道的。
卡片上照實標「未查證」，不要因為欄位是空的就算繪成「漫遊」。

用法：python3 make_esim_cards.py
輸出：japan-esim/cards/esim-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-esim', 'cards')
SRC = 'esim.json'
E = htm.escape
DEMO_DAYS = 5


def fingerprint(d):
    pay = [[p.get(k) for k in ('name', 'id', 'carrier', 'rating', 'reviews',
                               'hotspot', 'throttle', 'profile', 'refund_short')]
           + [len(p.get('plans') or [])] for p in d['products']]
    pay.append([[x['name'], x['rating'], x['reviews'], x['ci']]
                for x in d['_評價分析']['items']])
    pay.append([[x['what'], x['detail']] for x in d['_觀察_條款差異']['items']])
    vc = d['profile_guide'].get('verified_cases') or {}
    pay.append([[r['name'], r.get('profile'), r.get('verify')]
                for r in vc.get('rows', [])])
    pay.append([d['checked'], vc.get('checked')])
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
h1{font-size:56px;line-height:1.24;font-weight:800;letter-spacing:-.01em}
h1 em{font-style:normal;color:#c2410c}
.sub{font-size:27px;line-height:1.7;color:#63605c;margin-top:16px}
.legend{font-size:21px;color:#63605c;margin-top:9px;line-height:1.6}
.list{margin-top:24px;flex:1 1 auto;min-height:0}
.hd{display:flex;gap:12px;align-items:flex-end;padding:0 0 9px;
 font-size:20px;color:#8a847c;border-bottom:2px solid #1a1a1a}
.row{display:flex;gap:12px;align-items:baseline;padding:14px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.nm{flex:1 1 auto;font-size:27px;font-weight:700;line-height:1.3}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px}
.v{flex:0 0 150px;text-align:right;font-size:27px;font-weight:700;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.v.z{color:#b4afa8;font-weight:500;font-size:23px}
.v small{display:block;font-size:19px;font-weight:500;color:#8a847c;margin-top:3px}
/* 信賴區間 */
.ci{padding:15px 0;border-bottom:1px solid #e5e3de}
.ci:last-child{border-bottom:0}
.ci b{display:block;font-size:26px;margin-bottom:3px}
.ci b i{font-style:normal;color:#8a847c;font-weight:500;font-size:21px;margin-left:10px}
.cbar{position:relative;height:34px;margin-top:9px}
.cbar u{position:absolute;height:12px;top:11px;background:#c2410c;border-radius:6px;
 text-decoration:none}
.cbar em{position:absolute;top:0;bottom:0;border-left:2px dashed #b4afa8;font-style:normal}
.cbar span{position:absolute;top:0;line-height:34px;font-size:20px;font-weight:700;
 color:#1a1a1a;white-space:nowrap}
.axis{display:flex;justify-content:space-between;font-size:19px;color:#8a847c;
 border-top:1px solid #e5e3de;padding-top:6px;margin-top:4px}
.blk{padding:14px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:29px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c2410c;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.7}
.tag{display:inline-block;font-size:19px;padding:2px 10px;border-radius:999px;
 background:#e5e3de;color:#63605c;margin-left:10px;vertical-align:4px;font-weight:600}
.tag.bad{background:#f3ded6;color:#a8442a}
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


def short(name):
    """商品名很長，取得出來的品牌線索。"""
    for k in ('Sakura Mobile', '小資專業型', '吃到飽，不穩就退',
              '電子郵件寄送', '掃描QR Code'):
        if k in name:
            return k
    return name[:14]


def build(d):
    n = 9
    ps = d['products']
    fnote = f'五個商品逐頁查證於 {d["checked"]}'
    out = []

    def cheapest(p):
        pls = [x for x in (p.get('plans') or []) if x.get('price')]
        return min(pls, key=lambda x: x['price']) if pls else None

    def unlimited5(p):
        c = [x for x in (p.get('plans') or [])
             if x['days'] == DEMO_DAYS and x.get('price')
             and (x['gb'] is None or '限' in str(x.get('label')) or '吃到飽' in str(x.get('label')))]
        return min(c, key=lambda x: x['price']) if c else None

    lo = min((cheapest(p) for p in ps if cheapest(p)), key=lambda x: x['price'])
    lop = next(p for p in ps if cheapest(p) is lo)
    u5 = [(p, unlimited5(p)) for p in ps if unlimited5(p)]
    u5.sort(key=lambda t: t[1]['price'])
    rv = sorted(d['_評價分析']['items'], key=lambda x: -x['reviews'])
    top = rv[0]
    star = max(d['_評價分析']['items'], key=lambda x: x['rating'])

    # ── 1 封面 ──
    cover = ('<div class="kick">日本 eSIM</div>'
             f'<h1>「NT${lo["price"]} 起」，<br><em>起的是什麼</em></h1>'
             f'<div class="sub">{len(ps)} 個商品、'
             f'{sum(len(p.get("plans") or []) for p in ps)} 個方案逐頁查過。'
             '最低價那個方案不是你會買的那個。</div>'
             '<div class="stat">'
             f'<div><b>NT${lo["price"]}</b>'
             f'<span>最低價方案<br>{lo["days"]} 天 {E(str(lo["label"]))}</span></div>'
             + (f'<div><b>NT${u5[0][1]["price"]}</b>'
                f'<span>{DEMO_DAYS} 天吃到飽<br>最便宜</span></div>'
                f'<div><b>NT${u5[-1][1]["price"]}</b>'
                f'<span>同樣條件<br>最貴</span></div>' if len(u5) > 1 else '')
             + f'<div><b>{len(ps)}</b><span>個商品<br>沒有一個全贏</span></div></div>'
             f'<div class="note">那個 NT${lo["price"]} 是 {lo["days"]} 天 '
             f'{E(str(lo["label"]))}。真的要用一趟五天的行程，'
             + (f'同一個商品的吃到飽是 NT${u5[0][1]["price"]}。' if u5 else '價格是另一回事。')
             + '</div>' + foot(1, n, fnote))
    out.append(('esim-01.png', page(cover, 'cover')))

    # ── 2 同需求比價 ──
    rows = ('<div class="hd"><div class="nm">商品</div>'
            f'<div class="v">{DEMO_DAYS} 天吃到飽</div></div>')
    for p, pl in u5:
        rows += (f'<div class="row"><div class="nm">{E(short(p["name"]))}'
                 f'<s>{E(str(pl["label"]))}</s></div>'
                 f'<div class="v">NT${pl["price"]:,}</div></div>')
    for p in ps:
        if not unlimited5(p):
            rows += (f'<div class="row"><div class="nm">{E(short(p["name"]))}'
                     '<s>沒有這個天數的吃到飽方案</s></div>'
                     '<div class="v z">無</div></div>')
    gap = (u5[-1][1]['price'] / u5[0][1]['price'] - 1) * 100 if len(u5) > 1 else 0
    inner = ('<div class="kick">同樣的需求才比得出來</div>'
             f'<h1>{DEMO_DAYS} 天吃到飽，<em>差 {gap:.0f}%</em></h1>'
             '<div class="sub">各商品的方案切法完全不同，'
             '只比「最低價」等於在比不同的東西。</div>'
             '<div class="legend">這是同一個天數、同樣不限流量的方案互比。'
             '沒有這個組合的商品標「無」，不是它比較貴。</div>'
             f'<div class="list">{rows}</div>' + foot(2, n, fnote))
    out.append(('esim-02.png', page(inner)))

    # ── 3 評價與樣本數 ──
    LOMIN, LOMAX = 4.0, 4.9
    def pos(v):
        return (v - LOMIN) / (LOMAX - LOMIN) * 100
    rows = ''
    for x in rv:
        a, b = x['ci']
        rows += (f'<div class="ci"><b>{E(short(x["name"]))}'
                 f'<i>{x["rating"]} 星・{x["reviews"]:,} 則</i></b>'
                 f'<div class="cbar">'
                 f'<u style="left:{pos(a):.1f}%;width:{max(pos(b) - pos(a), 0.8):.1f}%"></u>'
                 + (f'<span style="right:{100 - pos(a) + 1.5:.1f}%;text-align:right">'
                    f'{a:.2f}–{b:.2f}</span>' if pos(b) > 72
                    else f'<span style="left:{pos(b) + 1.5:.1f}%">{a:.2f}–{b:.2f}</span>')
                 + '</div></div>')
    inner = ('<div class="kick">星等排序不等於推薦順序</div>'
             '<h1>評價要<em>連樣本數</em>一起看</h1>'
             f'<div class="sub">{star["rating"]} 星那個的樣本數只有 '
             f'{top["rating"]} 星那個的 1/{round(top["reviews"] / star["reviews"])}。'
             '橫條是 95% 信賴區間，越短代表越可信。</div>'
             '<div class="legend">區間重疊就表示分不出高下。'
             f'則數最少的那個（{rv[-1]["reviews"]} 則）區間寬到 '
             f'{rv[-1]["ci"][1] - rv[-1]["ci"][0]:.2f}，那個星等其實沒告訴你什麼。</div>'
             f'<div class="list">{rows}'
             f'<div class="axis"><span>{LOMIN:.1f}</span><span>4.45</span>'
             f'<span>{LOMAX:.1f}</span></div></div>' + foot(3, n, fnote))
    out.append(('esim-03.png', page(inner)))

    # ── 4 逐頁查完才知道的 ──
    rows = ''.join(
        f'<div class="blk"><b><i>{i:02}</i>{E(x["what"])}</b><s>{E(x["detail"])}</s></div>'
        for i, x in enumerate(d['_觀察_條款差異']['items'], 1))
    inner = ('<div class="kick">商品頁上不會並排給你看</div>'
             '<h1>逐頁查完<br><em>才知道的三件事</em></h1>'
             f'<div class="list">{rows}</div>' + foot(4, n, fnote))
    out.append(('esim-04.png', page(inner)))

    # ── 5 基本資料 ──
    rows = ('<div class="hd"><div class="nm">商品</div>'
            '<div class="v">熱點</div><div class="v">超量降速</div></div>')
    for p in ps:
        hs = p.get('hotspot')
        th = p.get('throttle')
        rows += (f'<div class="row"><div class="nm">{E(short(p["name"]))}'
                 f'<s>{E(str(p.get("carrier") or "商品頁沒寫電信商"))}</s></div>'
                 + (f'<div class="v">可</div>' if hs
                    else '<div class="v z">未寫明</div>')
                 + (f'<div class="v">{E(str(th))}</div>' if th
                    else '<div class="v z">未寫明</div>')
                 + '</div>')
    inner = ('<div class="kick">五個商品的基本資料</div>'
             '<h1>吃到飽<em>降速到多少</em>，<br>只有一家寫</h1>'
             '<div class="sub">「未寫明」是商品頁上真的找不到，'
             '不是沒有這個限制。</div>'
             '<div class="legend">128kbps 大概是什麼概念：文字訊息可以，'
             '地圖會很吃力，影片不用想。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n, fnote))
    out.append(('esim-05.png', page(inner)))

    # ── 6 原生還是漫遊 ──
    g = d['profile_guide']
    inner = ('<div class="kick">多數人只問了一半</div>'
             '<h1>「原生還是漫遊」<br><em>其實是兩個問題</em></h1>'
             f'<div class="sub">{E(g["thesis"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>1</i>{E(g["layer1"]["title"])}</b>'
             '<s>走 Home Routed 的話，資料先回到發行方所在地的網路才出去，'
             '公網 IP 會落在香港、新加坡或英國。'
             '這就是「用到一半變成香港的網路」的真正來源。</s></div>'
             f'<div class="blk"><b><i>2</i>{E(g["layer2"]["title"])}</b>'
             '<s>日本的 MVNO 向大手電信商租網路，訊號涵蓋一樣，'
             '但午休、通勤、夜間會塞。這是總務省自己寫的。</s></div>'
             '<div class="blk"><b><i>→</i>會讓 IP 跑到國外的只有漫遊</b>'
             '<s>而且是從頭到尾如此，不是中途發生的。'
             '多 IMSI 產品在訊號差時切的是另一家日本電信商，'
             '那是在日本國內換，IP 出口不會因此跑到香港。</s></div>'
             '</div>' + foot(6, n, fnote))
    out.append(('esim-06.png', page(inner)))

    # ── 7 自己驗 ──
    inner = ('<div class="kick">啟用之後三十秒</div>'
             '<h1>自己<em>驗一次</em></h1>'
             '<div class="list">'
             '<div class="blk"><b><i>01</i>看電信商名稱</b>'
             '<s>iPhone：設定 → 行動服務 → 點那張 eSIM → 看「網路供應商」。'
             '顯示 NTT DOCOMO、SoftBank 之類，代表無線電那一段接的是那家日本網路。'
             '但這只說明無線電，不代表 IP 出口在日本。</s></div>'
             '<div class="blk"><b><i>02</i>查公網 IP 落在哪一國</b>'
             '<s>瀏覽器搜尋「my ip」，看它判斷你在哪。'
             '顯示日本就是本地出口，顯示香港或新加坡就是走漫遊回程。</s></div>'
             '<div class="blk"><b><i>03</i>買之前先撥 *#06#</b>'
             '<s>看得到 EID 才代表這支手機支援 eSIM。'
             '有一個商品寫明「因相容性問題無法使用，恕無法取消或退款」，'
             '手機不支援是你自己的責任。</s></div>'
             '</div>' + foot(7, n, fnote))
    out.append(('esim-07.png', page(inner)))

    # ── 8 沒有一個全贏 ──
    noprof = sum(1 for p in ps if p.get('profile') is None)
    rows = ''.join(f'<div class="blk"><b>{E(c[:18])}</b><s>{E(c)}</s></div>'
                   for c in d['_評價分析']['_結論'][:2])
    inner = ('<div class="kick">這頁的範圍</div>'
             '<h1>沒有一個商品<br><em>在所有項目都贏</em></h1>'
             f'<div class="list">{rows}'
             f'<div class="blk"><b>這五個商品的原生／漫遊仍未查證</b>'
             f'<s>這 {noprof} 個商品的商品頁都沒寫是原生還是漫遊。'
             '那要實機插卡、查 IP 出口才知道，光看商品頁判斷不了。'
             '寫「未查證」，不寫「漫遊」。另外兩個查得到官方文件的案例見下一張。</s></div>'
             '</div>' + foot(8, n, fnote))
    out.append(('esim-08.png', page(inner)))

    # ── 9 查得到官方文件的兩個案例 ──
    vc = d['profile_guide'].get('verified_cases')
    if vc:
        VD = {'roaming': ('漫遊', 'bad'), 'native': ('原生', 'ok')}
        rows = ''
        for r in vc['rows']:
            lab, cls = VD.get(r.get('profile'), ('仍未判定', 'z'))
            ev = '；'.join(f'［{e["strength"]}］{e["what"]}' for e in r['evidence'][:3])
            rows += (f'<div class="blk"><b>{E(r["name"])}'
                     f'<span class="tag {"bad" if cls == "bad" else ""}">{E(lab)}</span></b>'
                     f'<s><b style="display:inline">發行方</b>　'
                     f'{E(str(r.get("issuer_region"))[:52])}<br>'
                     f'<b style="display:inline">依據</b>　{E(ev)}<br>'
                     f'{E(str(r.get("verify") or ""))}</s></div>')
        inner = ('<div class="kick">只收查得到官方文件的</div>'
                 '<h1>兩個案例，<em>結論不一樣</em></h1>'
                 f'<div class="sub">{E(vc["_說明"])}</div>'
                 '<div class="legend">證據分硬、中、軟三級。'
                 '硬證據是官方文件或法人登記，軟證據是使用者回報，不單獨當結論。</div>'
                 f'<div class="list">{rows}</div>' + foot(9, n, fnote))
        out.append(('esim-09.png', page(inner)))
    return out


def check(chrome, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'const it=[...document.querySelectorAll(".row,.blk,.ci,.note,.stat,.hd,.axis")];'
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
