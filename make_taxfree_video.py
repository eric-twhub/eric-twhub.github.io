"""日本免稅新制（2026/11/1 起先付全額、出境後才退）短影音（直式 1080×1920、手繪貼紙＋原創破關風配樂）。

數字不在這裡寫死，全部讀線上 /japan-tax-free-2026/：
- 開場：「要先墊多少錢？」表的 ¥100,000 那列（先墊的消費稅與台幣）
- 排名：「各店公告的手續費」表（只算店家官網或新聞稿寫出來的），挑「買 ¥10,000（稅前）退回」有數字的店；
  手續費與退回金額完全一樣的店併成一列；「有公告，沒寫費率」的店不畫長條，只在畫面寫出家數（沒寫 ≠ 不收）
- 三個地雷：自動閘門入境要當場蓋章、託運前先辦海關確認、整筆交易連坐，頁上的句子找不到就停
畫面算繪、合成與配樂沿用 make_transit_video_v2。
用法：python3 make_taxfree_video.py [輸出資料夾]
"""
import html as htm
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else 'cards/threads/短影音-免稅新制'
sys.argv = sys.argv[:1]
import make_transit_video_v2 as V  # noqa: E402
import make_roam_video as RV  # noqa: E402  （共用樣式）

URL = 'https://jptripcard.com/japan-tax-free-2026/'
W, H, FPS = V.W, V.H, V.FPS
BEAT = V.BEAT
T2 = 8 * BEAT
_txt = RV._txt


def _num(s):
    return int(s.replace(',', ''))


def fetch():
    s = urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8')
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    upd = re.search(r'最後更新 (?:<!--lm-->)?(\d{4}-\d\d-\d\d)', s)
    if not upd:
        sys.exit('頁尾找不到「最後更新」日期')
    tables = {}
    for tb in re.findall(r'<table.*?</table>', s, re.S):
        rows = [[_txt(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)] for r in re.findall(r'<tr[^>]*>(.*?)</tr>', tb, re.S)]
        if rows:
            tables.setdefault(rows[0][0], rows)   # 兩張表頭都是「店家」：第一張是官方公告
    pay = tables.get('購物金額（稅前）')
    fees = tables.get('店家')
    if not pay or not fees or fees[0][:5] != ['店家', '狀態', '手續費', '從哪個金額算', '買 ¥10,000（稅前）退回']:
        sys.exit('「要先墊多少錢」或「各店公告的手續費」表的格式和預期不同，請先看頁面')
    r100 = next((r for r in pay if r[0] == '¥100,000'), None)
    if not r100:
        sys.exit('「要先墊多少錢」表找不到 ¥100,000 那列')
    pre_jpy, pre_twd = _num(r100[1].lstrip('¥')), _num(r100[2].replace('NT$', ''))
    # 店家手續費（第一張「店家」表＝官方公告；回報的那張表頭是「回報的手續費」，不會撞名）
    groups, nofee = [], []
    for r in fees[1:]:
        name, st, fee, base, back = r[:5]
        if st == '有公告，沒寫費率':
            nofee.append(name)
            continue
        m = re.match(r'(約 |至少 )?¥([\d,]+)(?:～¥([\d,]+))?$', back)
        if not m:
            sys.exit(f'{name} 的「退回」欄「{back}」讀不懂，請先看頁面')
        lo = _num(m.group(2))
        hi = _num(m.group(3)) if m.group(3) else None
        key = (fee, base, back)
        g = next((x for x in groups if x['key'] == key), None)
        cash = '機場領現金' in (r[5] if len(r) > 5 else '')
        if g:
            g['names'].append(name)
            g['cash'] = g['cash'] and cash
        else:
            groups.append({'key': key, 'names': [name], 'fee': fee, 'base': base, 'pre': (m.group(1) or '').strip(),
                           'lo': lo, 'hi': hi, 'back': back, 'cash': cash})
    if len(groups) < 4:
        sys.exit(f'有公告費率的店只讀到 {len(groups)} 組，畫面要改')
    t = _txt(s[s.find('<h1'):])
    for ph in ('走自動閘門入境', '入境審查當下請職員蓋章', '事後補不了', '要在託運行李之前', '整筆交易連坐', '整筆都失去免稅資格'):
        if ph not in t:
            sys.exit(f'頁上找不到「{ph}」，地雷那段要重看')
    fx = re.search(r'換算匯率 ([\d.]+)', t)
    return {'today': upd.group(1), 'buy': r100[0], 'pre_jpy': pre_jpy, 'pre_twd': pre_twd, 'fx': fx.group(1) if fx else None,
            'groups': sorted([{k: v for k, v in g.items() if k != 'key'} for g in groups], key=lambda g: (-g['lo'], -(g['hi'] or 0))),
            'nofee': nofee}


CSS = RV.CSS + r"""
#num{font-size:230px}
#h1{font-size:80px}
#t2{font-size:66px}
.rw .br{background:#f6b8a8}
.rw.free .br{background:#7fc8a9}
.rw .ex{position:absolute;top:0;height:58px;border:5px dashed #c05a45;border-left:0;border-radius:0 16px 16px 0;background:rgba(246,184,168,.35);width:0}
.rw .nm{display:inline-block}
#nofee{left:75px;width:900px;font-size:32px;font-weight:800;color:#8a6a55;line-height:1.4}
"""

JS = r"""
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-cl(x),3);
const eb=x=>{x=cl(x);const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
function tf(el,x,y,s,r,o){el.style.transform=`translate(${x}px,${y}px) scale(${s}) rotate(${r||0}deg)`;if(o!==undefined)el.style.opacity=o}
function scene(id,a,b,t){const el=$(id);const i=eo((t-a)/.3),o=b<99?1-eo((t-b+.05)/.28):1;
 const v=t<a-.01||t>b+.3?0:Math.min(i,o);el.style.opacity=v;
 el.style.transform=`translateY(${(1-i)*50}px) scale(${1-(1-o)*.06})`;}
const fmt=n=>Math.round(n).toLocaleString('en-US');
function render(t){
 $('bg').style.transform=`translate(${-(t*6)%60}px,${-(t*4)%60}px)`;
 scene('s1',0,D.T2,t);scene('s2',D.T2,D.T3,t);scene('s3',D.T3,D.T4,t);scene('s4',D.T4,99,t);
 tf($('k1'),0,(1-eb(t/.5))*-60,1,0,cl(t/.3));
 tf($('st1'),0,(1-eb((t-.15)/.6))*120+Math.sin(t*2.4)*8,.6+.4*eb((t-.15)/.6),Math.sin(t*1.7)*3,cl((t-.15)/.2));
 tf($('st1b'),0,Math.sin(t*2+1)*10,eb((t-.45)/.5),8+Math.sin(t*1.3)*4,cl((t-.45)/.2));
 tf($('h1'),0,(1-eo((t-.4)/.4))*40,1,0,cl((t-.4)/.3));
 const L=D.LAND, p=cl((t-.7)/(L-.7));
 $('nv').textContent=fmt(D.top*eo(p));
 tf($('num'),0,0,t<L?.85+.15*p:1+.18*Math.exp(-(t-L)*7)*Math.cos((t-L)*18),0,cl((t-.6)/.2));
 tf($('sub1'),0,(1-eo((t-L)/.4))*30,1,0,cl((t-L)/.3));
 tf($('q1'),0,0,eb((t-L-.35)/.5),0,cl((t-L-.35)/.2));
 tf($('t2'),(1-eo((t-D.T2)/.4))*-80,0,1,0,cl((t-D.T2)/.3));
 D.R.forEach((R,i)=>{
  const r=$('r'+i), a=eo((t-R)/.35), g=eo((t-R-.1)/.5), g2=eo((t-R-.5)/.4);
  tf(r,(1-a)*-120,0,1,0,cl((t-R)/.2));
  r.querySelector('.br').style.width=(D.W[i]*g)+'px';
  const ex=r.querySelector('.ex'); let end=D.W[i]*g;
  if(ex){ex.style.left=(D.W[i]-6)+'px';ex.style.width=((D.X[i]-D.W[i]+6)*g2)+'px';end=Math.max(end,D.W[i]-6+(D.X[i]-D.W[i]+6)*g2)}
  const pr=r.querySelector('.pr');pr.style.left=(end+18)+'px';
  pr.textContent=D.A[i]+'¥'+fmt(D.P[i]*g)+(D.Q[i]&&g2>0?'～'+fmt(D.P[i]+(D.Q[i]-D.P[i])*g2):'');
 });
 const C=D.R[0]+.45;
 if(D.CX===null)D.CX=75+$('r0').querySelector('.nm').scrollWidth+24;
 tf($('crown'),D.CX,D.CY,eb((t-C)/.4),0,cl((t-C)/.15));
 tf($('nofee'),0,0,1,0,cl((t-D.R[0]-.8)/.3));
 tf($('stamp'),0,0,1+.6*(1-eb((t-D.T3)/.35)),-3,cl((t-D.T3)/.12));
 ['b1','b2','b3'].forEach((id,k)=>tf($(id),(1-eo((t-D.T3-.45-k*.3)/.4))*(k%2?900:-900),0,1,k%2?1:-1,1));
 tf($('st4'),0,(1-eb((t-D.T4)/.6))*-100+Math.sin(t*2)*8,1,0,cl((t-D.T4)/.2));
 tf($('brand'),0,0,eb((t-D.T4-.15)/.4),0,cl((t-D.T4-.15)/.2));
 tf($('url'),0,0,eb((t-D.T4-.3)/.45),-2,cl((t-D.T4-.3)/.2));
 tf($('srch'),0,(1-eo((t-D.T4-.45)/.4))*30,1,0,cl((t-D.T4-.45)/.3));
 tf($('tiny'),0,0,1,0,cl((t-D.T4-.6)/.3));
}
"""


def build_html(d):
    e = htm.escape
    gs = d['groups']
    n = len(gs)
    R = [0.0] * n
    for k in range(n):               # 先出現退得最少的，最後出現的 index 0 退得最多
        R[n - 1 - k] = T2 + BEAT * (2 + 2 * k)
    T3 = T2 + BEAT * (2 + 2 * n + 4)
    T4 = T3 + 9 * BEAT
    DUR = T4 + 7 * BEAT
    V.T_RANK, V.T_CAP, V.T_END, V.T_LAND, V.DUR = T2, T3, T4, 4 * BEAT, DUR
    top0, rh, bw = 400, 176, 600
    full = 1000
    Wd = [max(60, round(bw * g['lo'] / full)) for g in gs]
    Xd = [round(bw * (g['hi'] or g['lo']) / full) for g in gs]
    rows = ''
    for i, g in enumerate(gs):
        free = g['fee'] == '不收'
        base = '' if free else ('・沒寫從哪個金額算' if g['base'] == '沒寫' else f'・從{g["base"]}算')
        pl = (('不收手續費' + ('・機場領現金另收' if g['cash'] else '')) if free else f'手續費 {g["fee"]}{base}')
        rows += (f'<div id="r{i}" class="ab rw{" free" if free else ""}" style="top:{top0 + i * rh}px">'
                 f'<div class="nm">{e("、".join(g["names"]))}</div>'
                 f'<div class="tr"><div class="br"></div>{"<div class=ex></div>" if g["hi"] else ""}<div class="pr hn"></div></div>'
                 f'<div class="pl">{e(pl)}</div></div>')
    nf = d['nofee']
    nofee = (f'<div id="nofee" class="ab" style="top:{top0 + n * rh + 6}px">另有 {len(nf)} 家（{e("、".join(nf[:3]))}等）'
             f'<br>公告會收手續費，但沒寫費率</div>') if nf else ''
    s1 = (f'<div id="s1" class="sc"><div id="k1" class="ab"><span class="pill hn">日本免稅 11/1 起新制</span></div>'
          f'<div id="st1" class="ab stk sh">{V._svg("receipt")}</div>'
          f'<div id="st1b" class="ab stk sh">{V._svg("yen")}</div>'
          f'<div id="h1" class="ab hn">買 {d["buy"]} 要先墊</div>'
          f'<div id="num" class="ab hn"><small>NT$</small><span id="nv">0</span></div>'
          f'<div id="sub1" class="ab">結帳先付含稅全額<br>出境經海關確認後才退</div>'
          f'<div id="q1" class="ab"><span class="hn">退回來都是 10% 嗎？</span></div></div>')
    s2 = (f'<div id="s2" class="sc"><div id="t2" class="ab hn">買 ¥10,000 實際退回<small>本來該退 ¥1,000・只列官網公告費率的店</small></div>'
          f'{rows}{nofee}<div id="crown" class="ab"><span class="hn">全額退</span></div></div>')
    s3 = (f'<div id="s3" class="sc"><div id="stamp" class="ab"><span class="hn">三個地雷</span></div>'
          f'<div id="b1" class="ab bx" style="top:470px"><h3>走自動閘門入境</h3>'
          f'<p>當場請職員蓋入境章<small>沒有章就辦不了免稅，事後補不了</small></p></div>'
          f'<div id="b2" class="ab bx" style="top:770px"><h3>出境那天<em>先別託運</em></h3>'
          f'<p>先辦海關確認（機台或手機）<small>紅燈要帶東西給關員看</small></p></div>'
          f'<div id="b3" class="ab bx" style="top:1070px"><h3>整筆交易<em>連坐</em></h3>'
          f'<p>一項沒過海關確認<small>同一筆交易整筆失去免稅</small></p></div></div>')
    tiny = ['手續費是各店官網公告，可能隨時調整']
    if d['fx']:
        tiny.append(f'以 1 日圓 = {d["fx"]} 元換算')
    tiny.append('以各店與觀光廳公告為準')
    s4 = (f'<div id="s4" class="sc"><div id="st4" class="ab stk sh">{V._svg("luggage")}</div>'
          f'<div id="brand" class="ab hn">日本旅遊小卡</div>'
          f'<div id="url" class="ab"><span class="hn">jptripcard.com</span></div>'
          f'<div id="srch" class="ab">各店手續費與出境那天怎麼辦</div>'
          f'<div id="tiny" class="ab">{"<br>".join(e(x) for x in tiny)}</div></div>')
    D = {'T2': T2, 'T3': T3, 'T4': T4, 'LAND': 4 * BEAT, 'top': d['pre_twd'], 'R': R, 'W': Wd, 'X': Xd,
         'P': [g['lo'] for g in gs], 'Q': [g['hi'] for g in gs], 'A': [(g['pre'] + ' ') if g['pre'] else '' for g in gs],
         'CX': None, 'CY': top0 - 6}
    page = ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Huninn&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body><div id="bg"></div>{s1}{s2}{s3}{s4}'
            f'<script>window.D={json.dumps(D)};{JS}</script></body></html>')
    return page, R, DUR


def main():
    from playwright.sync_api import sync_playwright
    d = fetch()
    if os.environ.get('DRY'):
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src, R, DUR = build_html(d)
    keep = os.environ.get('KEEP_FRAMES')
    mp4 = os.path.join(OUT, 'taxfree-game.mp4')
    with tempfile.TemporaryDirectory() as tmp:
        hf = os.path.join(tmp, 'v.html')
        open(hf, 'w', encoding='utf-8').write(src)
        wav = os.path.join(tmp, 'm.wav')
        V.make_music_game(wav, R, 3)
        ff = subprocess.Popen(
            ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
             '-c:v', 'png', '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4],
            stdin=subprocess.PIPE)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=V.base._chrome())
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
            pg.goto('file://' + hf)
            pg.evaluate('document.fonts.ready')
            if not pg.evaluate('document.fonts.check(\'40px "Huninn"\')'):
                sys.exit('Huninn 字型沒有載入（需要網路連到 Google Fonts）')
            for f in range(int(DUR * FPS)):
                t = f / FPS
                pg.evaluate(f'render({t})')
                png = pg.screenshot(type='png')
                ff.stdin.write(png)
                if keep and any(abs(t - float(x)) < .5 / FPS for x in keep.split(',')):
                    open(os.path.join(V.keep_dir(), f'{t:05.2f}.png'), 'wb').write(png)
            b.close()
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit('ffmpeg 合成失敗')
    print(mp4, f'{DUR:.1f}s')


if __name__ == '__main__':
    main()
