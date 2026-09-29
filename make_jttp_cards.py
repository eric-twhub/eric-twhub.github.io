# -*- coding: utf-8 -*-
"""日本信賴旅客制度（TTP／JTTP）的分享圖卡（1080×1350，4:5）。

和其他幾支同一套：Chrome headless 算繪 HTML、版面高度用量的、
寫 cards/stamp.txt 讓 gen.py 偵測資料改了沒重跑。不掛在每日 workflow 上。

用法：python3 make_jttp_cards.py
輸出：japan-jttp/cards/jttp-01.png … -08.png
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
OUT = os.path.join('japan-jttp', 'cards')
SRC = 'jttp.json'
E = htm.escape


def fingerprint(d):
    pay = [d['fee'], d['valid'], [list(c) for c in d['cats']],
           d['catD'], [list(f) for f in d['flow']],
           {k: v for k, v in d['places'].items()},
           d['gates']['airports'], d['reject'],
           [u['what'] for u in d['unverified']], d['checked']]
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
.row{display:flex;gap:12px;align-items:baseline;padding:13px 0;
 border-bottom:1px solid #e5e3de}
.row:last-child{border-bottom:0}
.no{flex:0 0 118px;font-size:25px;font-weight:800;color:#c2410c;
 font-variant-numeric:tabular-nums}
.nm{flex:1 1 auto;font-size:28px;font-weight:700;line-height:1.3}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#63605c;
 margin-top:5px;line-height:1.55}
.v{flex:0 0 120px;text-align:right;font-size:25px;color:#63605c;white-space:nowrap}
.v.hit{color:#c4563a;font-weight:700}
.blk{padding:14px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:29px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c2410c;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.7}
.tag{display:inline-block;font-size:19px;padding:2px 10px;border-radius:999px;
 background:#f3ded6;color:#a8442a;margin-left:8px;vertical-align:4px;font-weight:600}
.tag.g{background:#e5e3de;color:#63605c}
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


def build(d):
    n = 8
    fee = d['fee']
    g = d['gates']
    fnote = f'引出入國在留管理廳與國稅廳原文，查證於 {d["checked"]}'
    out = []
    n_place = sum(len(v) for v in d['places'].values())
    n_stamp = sum(1 for v in d['places'].values() for r in v if r[2] == '印')

    # ── 1 封面 ──
    cover = ('<div class="kick">日本信賴旅客制度</div>'
             '<h1>你要申請的，<br><em>可能不是 JTTP</em></h1>'
             '<div class="sub">中文內容一律叫它 JTTP，但在日本官方的分類裡，'
             'JTTP 專指第 1 號那一類，前提是先登錄美國的 Global Entry。'
             '台灣護照走的是另一號。</div>'
             '<div class="stat">'
             f'<div><b>¥{fee["amount"]:,}</b>'
             f'<span>收入印紙<br>{fee["since"]} 起</span></div>'
             f'<div><b>+¥{fee["amount"] - fee["old"]:,}</b>'
             f'<span>比以前多<br>原本 ¥{fee["old"]:,}</span></div>'
             f'<div><b>2</b><span>趟<br>當天拿不到卡</span></div>'
             f'<div><b>{len(g["airports"])}</b><span>個機場<br>才有自動化閘門</span></div></div>'
             f'<div class="note">{E(g["warn"])}</div>'
             + foot(1, n, fnote))
    out.append(('jttp-01.png', page(cover, 'cover')))

    # ── 2 十一個要件 ──
    rows = ''
    for no, name, ent, note in d['cats']:
        hit = '9' == no
        rows += (f'<div class="row"><div class="no">第 {E(no)} 號</div>'
                 f'<div class="nm">{E(name)}'
                 + ('<span class="tag">台灣人多走這號</span>' if hit else '')
                 + f'<s>{E(note)}</s></div>'
                 f'<div class="v{" hit" if hit else ""}">{E(ent)}</div></div>')
    inner = ('<div class="kick">官方編成 1 到 11 號</div>'
             '<h1>十一個要件，<br><em>條件相同的併起來</em></h1>'
             '<div class="sub">「次數」指登錄前 1 年內入境日本的次數。</div>'
             f'<div class="list">{rows}</div>' + foot(2, n, fnote))
    out.append(('jttp-02.png', page(inner)))

    # ── 3 第 9 號 ──
    c = d['catD']
    inner = ('<div class="kick">台灣旅客最常走的一號</div>'
             '<h1>第 9 號：<em>白金卡</em></h1>'
             f'<div class="sub">官方原文寫的是「國際品牌授權的白金等級以上信用卡」。'
             f'{E(c["corp"])}</div>'
             '<div class="list">'
             f'<div class="blk"><b><i>·</i>接受的國際品牌</b>'
             f'<s>{E("、".join(c["brands"]))}</s></div>'
             f'<div class="blk"><b><i>·</i>入境次數</b><s>{E(c["entries"])}</s></div>'
             f'<div class="blk"><b><i>·</i>要準備的文件</b>'
             f'<s>{E("；".join(c["docs"]))}</s></div>'
             '<div class="blk"><b><i>!</i>台灣的卡名不等於國際品牌等級</b>'
             '<s>官方只規定國際品牌的卡片等級，沒有給各國卡別對照表。'
             '中文卡名叫什麼不代表它在國際品牌那邊是什麼等級，要問發卡行。</s></div>'
             '</div>' + foot(3, n, fnote))
    out.append(('jttp-03.png', page(inner)))

    # ── 4 流程 ──
    rows = ''.join(
        f'<div class="row"><div class="no">{E(no)}</div>'
        f'<div class="nm">{E(name)}<s>{E(desc)}</s></div></div>'
        for no, name, desc in d['flow'])
    inner = ('<div class="kick">當天不會出結果</div>'
             '<h1>流程四步，<em>要到場兩次</em></h1>'
             '<div class="sub">官方明寫申請當天不會出結果，領卡要擇日再到場一次。'
             '安排行程時要留兩趟。</div>'
             '<div class="legend">一次審查通過後 6 個月內要完成二次審查，'
             '超過原則上不予登錄。</div>'
             f'<div class="list">{rows}</div>' + foot(4, n, fnote))
    out.append(('jttp-04.png', page(inner)))

    # ── 5 地點 ──
    MK = {'印': '（要自備印紙）', '平': '（只有平日）'}
    rows = ''
    for place, lst in d['places'].items():
        seg = '；'.join(
            f'{w}{MK.get(m, "")} '
            + ('審查時間內隨時' if '出境審查開放' in h else h)
            for w, h, m in lst)
        n_ins = sum(1 for _, _, m in lst if m == '印')
        rows += (f'<div class="row"><div class="no">{E(place)}</div>'
                 f'<div class="nm">{len(lst)} 個櫃台'
                 + (f'<span class="tag">{n_ins} 個要自備印紙</span>' if n_ins else '')
                 + f'<s>{E(seg)}</s></div></div>')
    inner = ('<div class="kick">二次審查與領卡的地點</div>'
             f'<h1>{n_place} 個櫃台，<br><em>時間差很多</em></h1>'
             f'<div class="sub">其中 {n_stamp} 個在出境審查場，'
             '必須自己先備妥收入印紙，而且要過了安檢才到得了。</div>'
             '<div class="legend">出境審查場的櫃台回程當天最順，'
             '但辦完之後回不去一般管制區外的區域，購物要先買完。</div>'
             f'<div class="list">{rows}</div>' + foot(5, n, fnote))
    out.append(('jttp-05.png', page(inner)))

    # ── 6 護照不蓋章 ──
    inner = ('<div class="kick">這是最大的副作用</div>'
             '<h1>拿到卡之後，<br><em>護照就不蓋章了</em></h1>'
             '<div class="sub">入境記錄改寫在特定登録者カード上，'
             '護照不再蓋上陸許可證印。出境也一樣。</div>'
             '<div class="list">'
             '<div class="blk"><b><i>·</i>要章的話要當場說</b>'
             f'<s>{E(g["stamp_out"][:96])}</s></div>'
             '<div class="blk"><b><i>·</i>自動化閘門只有四個機場</b>'
             f'<s>{E("、".join(g["airports"]))}。'
             '飛福岡、新千歲、那霸、仙台這些地方，這張卡幫不上忙。</s></div>'
             '<div class="blk"><b><i>!</i>免稅購物會被卡</b>'
             '<s>店家要確認你是非居住者，靠的就是護照上的入境章。'
             '沒有章的話，要另外出示這張卡，見下一張。</s></div>'
             '</div>' + foot(6, n, fnote))
    out.append(('jttp-06.png', page(inner)))

    # ── 7 免稅 ──
    tf = d['taxfree']
    inner = ('<div class="kick">國稅庁 ' + E(tf['q']) + '</div>'
             '<h1>沒有入境章，<br><em>免稅怎麼買</em></h1>'
             '<div class="sub">國稅庁 的解釋是：出示<b>護照＋特定登録者カード</b>兩樣，'
             '店家就能確認你是非居住者，可以免稅販售。</div>'
             '<div class="list">'
             '<div class="blk"><b><i>·</i>卡上有在留資格與上陸年月日</b>'
             '<s>那正是店家要確認的兩件事，所以卡片可以取代護照上的章。</s></div>'
             f'<div class="blk"><b><i>!</i>{E(tf["store_gap"]["t"])}</b>'
             f'<s>{E(tf["store_gap"]["zh"])}</s></div>'
             f'<div class="blk"><b><i>!</i>那份 Q&amp;A 是 2018 年版</b>'
             f'<s>{E(tf["caveat"])}</s></div>'
             '</div>' + foot(7, n, fnote))
    out.append(('jttp-07.png', page(inner)))

    # ── 8 被拒與還沒查的 ──
    rj = ''.join(f'<div class="row"><div class="no">✗</div>'
                 f'<div class="nm">{E(x)}</div></div>' for x in d['reject'])
    uv = ''.join(f'<div class="row"><div class="no">?</div>'
                 f'<div class="nm">{E(u["what"])}<s>{E(u["why"])}</s></div></div>'
                 for u in d['unverified'][:3])
    inner = ('<div class="kick">會被拒絕，與官方沒寫明的</div>'
             '<h1>官方沒有公告<em>審查要多久</em></h1>'
             '<div class="sub">社群回報一次審查約兩個月，那是個別經驗不是規則，'
             '這裡不寫成數字。</div>'
             f'<div class="list">{rj}{uv}</div>' + foot(8, n, fnote))
    out.append(('jttp-08.png', page(inner)))
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
