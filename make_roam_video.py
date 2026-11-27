"""日本上網：原號漫遊 vs eSIM 短影音（直式 1080×1920、手繪貼紙長條排名＋原創破關風配樂）。

數字不在這裡寫死：直接讀線上 /japan-roaming-vs-esim/ 的「12 種情境比價」表，挑一個情境（預設 5 天・每天 1GB），
三家電信那三欄算「漫遊」、其他欄算「eSIM」；頁首摘要寫的兩個最便宜價格要和表上算出來的一致，不一致就停下來。
「選哪個」段落的價差區間（3 天、5 天以上）與 eSIM 的數據漫遊提醒也從頁面讀，讀不到就停。
畫面算繪與合成、配樂沿用 make_transit_video_v2（Playwright 截圖 → ffmpeg、make_music_game）。
用法：python3 make_roam_video.py [輸出資料夾]；環境變數 SCEN='5 天・每天 1GB' 換情境
"""
import html as htm
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else 'cards/threads/短影音-漫遊vsESIM'
sys.argv = sys.argv[:1]
import make_transit_video_v2 as V  # noqa: E402

URL = 'https://jptripcard.com/japan-roaming-vs-esim/'
W, H, FPS = V.W, V.H, V.FPS
SCEN = os.environ.get('SCEN', '5 天・每天 1GB')
ROAM = ('中華電信', '台灣大哥大', '遠傳')
BEAT = V.BEAT
T2 = 8 * BEAT


def _txt(s):
    return re.sub(r'\s+', ' ', htm.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def fetch():
    s = urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8')
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    upd = re.search(r'最後更新 (?:<!--lm-->)?(\d{4}-\d\d-\d\d)', s)
    if not upd:
        sys.exit('頁尾找不到「最後更新」日期')
    tb = re.findall(r'<table.*?</table>', s, re.S)
    if not tb:
        sys.exit('找不到比價表')
    rows = [[_txt(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)] for r in re.findall(r'<tr[^>]*>(.*?)</tr>', tb[0], re.S)]
    head = rows[0]
    if head[0] != '情境' or not all(x in head for x in ROAM):
        sys.exit(f'比價表的表頭和預期不同：{head}')
    row = next((r for r in rows[1:] if r[0] == SCEN), None)
    if not row:
        sys.exit(f'表上沒有「{SCEN}」這個情境')
    opts = []
    for name, cell in zip(head[1:], row[1:]):
        m = re.match(r'NT\$([\d,]+)\s*(.*)', cell)
        if not m:
            continue  # 「—」：這個通路沒有符合的單一方案
        opts.append({'name': name, 'kind': 'roam' if name in ROAM else 'esim',
                     'price': int(m.group(1).replace(',', '')), 'plan': m.group(2).strip()})
    r_min = min(x['price'] for x in opts if x['kind'] == 'roam')
    e_min = min(x['price'] for x in opts if x['kind'] == 'esim')
    t = _txt(s[s.find('<h1'):])
    # 頁首摘要：「5 天、每天 1GB：漫遊最便宜 NT$488 （中華電信），eSIM 最便宜 NT$111」
    sm = re.search(r'漫遊最便宜 NT\$([\d,]+).{0,30}?eSIM 最便宜 NT\$([\d,]+)', t)
    if SCEN == '5 天・每天 1GB' and (not sm or (int(sm.group(1).replace(',', '')), int(sm.group(2).replace(',', ''))) != (r_min, e_min)):
        sys.exit(f'頁首摘要和表上算出來的不一致（表：漫遊 {r_min}、eSIM {e_min}；摘要：{sm and sm.groups()}）')
    d3 = re.search(r'只去三天.{0,40}?漫遊比 eSIM 貴 NT\$([\d,]+) 到 NT\$([\d,]+)', t)
    d5 = re.search(r'五天以上.{0,40}?漫遊比 eSIM 貴 NT\$([\d,]+) 到 NT\$([\d,]+)', t)
    if not d3 or not d5:
        sys.exit('「選哪個」段落的價差區間讀不到，請先看頁面')
    if '台灣門號照常收簡訊' not in t:
        sys.exit('頁上找不到「台灣門號照常收簡訊」，漫遊那格的說法要重看')
    if not re.search(r'開著數據漫遊又沒指定給 eSIM.{0,30}照原價計費', t):
        sys.exit('頁上找不到 eSIM 的數據漫遊提醒，請先看頁面')
    fx = re.search(r'用 1 日圓 = ([\d.]+) 元換算', t)
    chk = re.search(r'漫遊方案查證於 (\d{4})-(\d\d)-(\d\d)', t)
    jcb = '台灣發行的 JCB 卡' in t
    for x in opts:
        x['note'] = '限台灣發行的 JCB 卡' if (x['name'] == 'MyJapan+' and jcb) else ''
    return {'today': upd.group(1), 'scen': SCEN, 'opts': sorted(opts, key=lambda x: (x['price'], x['kind'] != 'esim')),
            'r_min': r_min, 'e_min': e_min, 'gap': r_min - e_min,
            'd3': [d3.group(1), d3.group(2)], 'd5': [d5.group(1), d5.group(2)],
            'fx': fx.group(1) if fx else None,
            'checked': f'{int(chk.group(2))}/{int(chk.group(3))}' if chk else None}


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#fbf3e4}
body{font-family:"PingFang TC","Noto Sans TC",sans-serif;color:#5a3d2b;-webkit-font-smoothing:antialiased}
.hn{font-family:"Huninn","PingFang TC",sans-serif;font-weight:400}
#bg{position:absolute;inset:-120px;background:
 linear-gradient(#efe2cc 2px,transparent 2px) 0 0/60px 60px,
 linear-gradient(90deg,#efe2cc 2px,transparent 2px) 0 0/60px 60px,#fbf3e4}
.sc{position:absolute;inset:0;transform-origin:540px 860px;opacity:0}
.ab{position:absolute;will-change:transform}
.stk svg{width:100%;height:auto;display:block}
.sh{filter:drop-shadow(0 10px 0 rgba(90,61,43,.12))}
.pill{display:inline-block;background:#5a3d2b;color:#fbf3e4;border-radius:999px;padding:16px 42px;font-size:50px}
/* 開場 */
#k1{left:0;width:1080px;top:236px;text-align:center}
#st1{left:330px;top:340px;width:400px}
#st1b{left:690px;top:470px;width:220px}
#h1{left:0;width:1080px;top:760px;text-align:center;font-size:84px}
#num{left:0;width:1080px;top:860px;text-align:center;color:#e8553e;font-size:250px;line-height:1;text-shadow:0 12px 0 #ffd0c4;white-space:nowrap}
#num small{font-size:110px;margin-right:6px;color:#5a3d2b;text-shadow:none}
#sub1{left:0;width:1080px;top:1150px;text-align:center;font-size:50px;font-weight:800;color:#8a6a55;line-height:1.45}
#q1{left:0;width:1080px;top:1330px;text-align:center}
#q1 span{display:inline-block;background:#ffe48a;border:5px solid #5a3d2b;border-radius:30px;padding:14px 44px;font-size:62px;transform:rotate(-3deg)}
/* 排名 */
#t2{left:75px;top:215px;font-size:72px}
#t2 small{display:block;font-family:"PingFang TC",sans-serif;font-size:36px;font-weight:800;color:#8a6a55;margin-top:6px}
#leg2{left:75px;top:395px;font-size:32px;font-weight:800}
#leg2 i{display:inline-block;width:30px;height:30px;border-radius:8px;border:4px solid #5a3d2b;margin:0 10px 0 0;vertical-align:-5px}
#leg2 span{margin-right:34px}
.rw{left:75px;width:900px;height:160px}
.rw .nm{font-size:44px;font-weight:800;white-space:nowrap}
.rw .nm i{font-style:normal;display:inline-block;font-size:30px;color:#fff;border-radius:10px;padding:2px 12px;margin-right:14px;vertical-align:5px}
.rw .tr{position:relative;height:58px;margin-top:6px}
.rw .br{position:absolute;left:0;top:0;height:58px;border:5px solid #5a3d2b;border-radius:16px;width:0}
.rw .pr{position:absolute;top:2px;font-size:46px;white-space:nowrap}
.rw .pl{font-size:28px;font-weight:700;color:#8a6a55;margin-top:6px;white-space:nowrap}
.rw.esim .br{background:#7fc8a9}.rw.esim .nm i{background:#3f8f6e}
.rw.roam .br{background:#f6b8a8}.rw.roam .nm i{background:#c05a45}
#crown{left:0;top:0}
#crown span{display:inline-block;background:#ffe48a;border:5px solid #5a3d2b;border-radius:18px;padding:4px 20px;font-size:40px;transform:rotate(4deg)}
/* 選哪個 */
#stamp{left:0;width:1080px;top:240px;text-align:center}
#stamp span{display:inline-block;background:#e8553e;color:#fff;border:7px solid #5a3d2b;border-radius:28px;
 padding:18px 50px;font-size:88px;box-shadow:0 14px 0 #5a3d2b}
.bx{left:70px;width:900px;background:#fff;border:5px solid #5a3d2b;border-radius:34px;padding:22px 36px 26px;box-shadow:0 10px 0 #ead9c4}
.bx h3{font-family:"Huninn",sans-serif;font-weight:400;font-size:50px}
.bx h3 em{font-style:normal;color:#e8553e}
.bx p{font-size:40px;font-weight:800;margin-top:10px;line-height:1.3}
.bx p small{display:block;font-size:32px;color:#8a6a55;font-weight:700;margin-top:4px}
/* 收尾 */
#st4{left:340px;top:330px;width:400px}
#brand{left:0;width:1080px;top:740px;text-align:center;font-size:84px}
#url{left:0;width:1080px;top:860px;text-align:center}
#url span{display:inline-block;background:#e8553e;color:#fff;border:6px solid #5a3d2b;border-radius:999px;
 padding:20px 60px;font-size:92px;box-shadow:0 12px 0 #5a3d2b}
#srch{left:0;width:1080px;top:1060px;text-align:center;font-size:52px;font-weight:800}
#tiny{left:80px;width:850px;top:1160px;text-align:center;font-size:29px;line-height:1.6;color:#8a6a55;font-weight:600}
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
 // 開場
 tf($('k1'),0,(1-eb(t/.5))*-60,1,0,cl(t/.3));
 tf($('st1'),0,(1-eb((t-.15)/.6))*120+Math.sin(t*2.4)*8,.6+.4*eb((t-.15)/.6),Math.sin(t*1.7)*3,cl((t-.15)/.2));
 tf($('st1b'),0,Math.sin(t*2+1)*10,eb((t-.45)/.5),8+Math.sin(t*1.3)*4,cl((t-.45)/.2));
 tf($('h1'),0,(1-eo((t-.4)/.4))*40,1,0,cl((t-.4)/.3));
 const L=D.LAND, p=cl((t-.7)/(L-.7));
 $('nv').textContent=fmt(D.top*eo(p));
 tf($('num'),0,0,t<L?.85+.15*p:1+.18*Math.exp(-(t-L)*7)*Math.cos((t-L)*18),0,cl((t-.6)/.2));
 tf($('sub1'),0,(1-eo((t-L)/.4))*30,1,0,cl((t-L)/.3));
 tf($('q1'),0,0,eb((t-L-.35)/.5),0,cl((t-L-.35)/.2));
 // 排名：從最貴的一列開始，由下往上出現
 tf($('t2'),(1-eo((t-D.T2)/.4))*-80,0,1,0,cl((t-D.T2)/.3));
 tf($('leg2'),0,0,1,0,cl((t-D.T2-.3)/.3));
 D.R.forEach((R,i)=>{
  const r=$('r'+i), a=eo((t-R)/.35), g=eo((t-R-.1)/.5);
  tf(r,(1-a)*-120,0,1,0,cl((t-R)/.2));
  r.querySelector('.br').style.width=(D.W[i]*g)+'px';
  const pr=r.querySelector('.pr');pr.style.left=(D.W[i]*g+18)+'px';
  pr.textContent='NT$'+fmt(D.P[i]*g);
 });
 const C=D.R[0]+.45;
 tf($('crown'),D.CX,D.CY,eb((t-C)/.4),0,cl((t-C)/.15));
 // 選哪個
 tf($('stamp'),0,0,1+.6*(1-eb((t-D.T3)/.35)),-3,cl((t-D.T3)/.12));
 ['b1','b2','b3'].forEach((id,k)=>tf($(id),(1-eo((t-D.T3-.45-k*.3)/.4))*(k%2?900:-900),0,1,k%2?1:-1,1));
 // 收尾
 tf($('st4'),0,(1-eb((t-D.T4)/.6))*-100+Math.sin(t*2)*8,1,0,cl((t-D.T4)/.2));
 tf($('brand'),0,0,eb((t-D.T4-.15)/.4),0,cl((t-D.T4-.15)/.2));
 tf($('url'),0,0,eb((t-D.T4-.3)/.45),-2,cl((t-D.T4-.3)/.2));
 tf($('srch'),0,(1-eo((t-D.T4-.45)/.4))*30,1,0,cl((t-D.T4-.45)/.3));
 tf($('tiny'),0,0,1,0,cl((t-D.T4-.6)/.3));
}
"""


def build_html(d):
    e = htm.escape
    opts = d['opts']
    n = len(opts)
    # 時間軸（150 BPM）：開場 8 拍；排名先 2 拍標題，之後每列 2 拍、最後留 4 拍；選哪個 9 拍；收尾 7 拍
    R = [0.0] * n
    for k in range(n):               # k=0 最先出現（最貴），最後出現的是 index 0（最便宜）
        R[n - 1 - k] = T2 + BEAT * (2 + 2 * k)
    T3 = T2 + BEAT * (2 + 2 * n + 4)
    T4 = T3 + 9 * BEAT
    DUR = T4 + 7 * BEAT
    V.T_RANK, V.T_CAP, V.T_END, V.T_LAND, V.DUR = T2, T3, T4, 4 * BEAT, DUR
    top0, rh, bw = 460, 176, 640
    mx = max(x['price'] for x in opts)
    Wd = [max(60, round(bw * x['price'] / mx)) for x in opts]
    rows = ''
    for i, x in enumerate(opts):
        tag = '漫遊' if x['kind'] == 'roam' else 'eSIM'
        pl = x['plan'] + (f'・{x["note"]}' if x['note'] else '')
        rows += (f'<div id="r{i}" class="ab rw {x["kind"]}" style="top:{top0 + i * rh}px">'
                 f'<div class="nm"><i>{tag}</i>{e(x["name"])}</div>'
                 f'<div class="tr"><div class="br"></div><div class="pr hn"></div></div>'
                 f'<div class="pl">{e(pl)}</div></div>')
    sc = d['scen'].replace('・', '、')
    s1 = (f'<div id="s1" class="sc"><div id="k1" class="ab"><span class="pill hn">日本上網・{e(sc)}</span></div>'
          f'<div id="st1" class="ab stk sh">{V._svg("phone")}</div>'
          f'<div id="st1b" class="ab stk sh">{V._svg("plane")}</div>'
          f'<div id="h1" class="ab hn">漫遊和 eSIM 差</div>'
          f'<div id="num" class="ab hn"><small>NT$</small><span id="nv">0</span></div>'
          f'<div id="sub1" class="ab">漫遊最便宜 NT${d["r_min"]:,}<br>eSIM 最便宜 NT${d["e_min"]:,}</div>'
          f'<div id="q1" class="ab"><span class="hn">哪家最便宜？</span></div></div>')
    s2 = (f'<div id="s2" class="sc"><div id="t2" class="ab hn">{e(sc)}<small>各家最便宜的方案</small></div>'
          f'<div id="leg2" class="ab"><span><i style="background:#f6b8a8"></i>原號漫遊</span>'
          f'<span><i style="background:#7fc8a9"></i>eSIM</span></div>'
          f'{rows}<div id="crown" class="ab"><span class="hn">最便宜</span></div></div>')
    s3 = (f'<div id="s3" class="sc"><div id="stamp" class="ab"><span class="hn">選哪個？</span></div>'
          f'<div id="b1" class="ab bx" style="top:470px"><h3>只去 3 天、不想設定</h3>'
          f'<p>漫遊：貴 NT${d["d3"][0]}～{d["d3"][1]}<small>不用裝，台灣門號照常收簡訊</small></p></div>'
          f'<div id="b2" class="ab bx" style="top:770px"><h3>待 5 天以上</h3>'
          f'<p>eSIM：省 NT${d["d5"][0]}～{d["d5"][1]}<small>差多少看你是哪家電信</small></p></div>'
          f'<div id="b3" class="ab bx" style="top:1070px"><h3>裝 eSIM <em>要注意</em></h3>'
          f'<p>台灣門號的數據漫遊沒關、又沒指定給 eSIM<small>流量會從台灣門號走，照原價計費</small></p></div></div>')
    tiny = []
    if d['checked']:
        tiny.append(f'價格查證於 {d["checked"]}，漫遊方案多為限時優惠')
    if d['fx']:
        tiny.append(f'povo、MyJapan+ 以 1 日圓 = {d["fx"]} 元換算')
        tiny.append('刷卡另有國外交易手續費')
    tiny.append('以各電信與平台公告為準')
    s4 = (f'<div id="s4" class="sc"><div id="st4" class="ab stk sh">{V._svg("phone")}</div>'
          f'<div id="brand" class="ab hn">日本旅遊小卡</div>'
          f'<div id="url" class="ab"><span class="hn">jptripcard.com</span></div>'
          f'<div id="srch" class="ab">12 種情境逐格比價</div>'
          f'<div id="tiny" class="ab">{"<br>".join(e(x) for x in tiny)}</div></div>')
    D = {'T2': T2, 'T3': T3, 'T4': T4, 'LAND': 4 * BEAT, 'top': d['gap'], 'R': R, 'W': Wd,
         'P': [x['price'] for x in opts], 'CX': 75 + Wd[0] + 250, 'CY': top0 - 8}
    page = ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Huninn&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body><div id="bg"></div>{s1}{s2}{s3}{s4}'
            f'<script>window.D={json.dumps(D)};{JS}</script></body></html>')
    return page, R, DUR


def main():
    from playwright.sync_api import sync_playwright
    d = fetch()
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src, R, DUR = build_html(d)
    keep = os.environ.get('KEEP_FRAMES')
    mp4 = os.path.join(OUT, 'roam-esim-game.mp4')
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
    for x in d['opts']:
        print(x['kind'], x['name'], x['price'], x['plan'], x['note'])
    print('差', d['gap'], '｜3 天', d['d3'], '｜5 天以上', d['d5'], '｜匯率', d['fx'], '｜查證', d['checked'])


if __name__ == '__main__':
    main()
