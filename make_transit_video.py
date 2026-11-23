"""交通卡儲值短影音（直式 1080×1920、無配音字卡）。

數字不在這裡算：直接讀線上 /japan-transit-card/ 那張「每儲 ¥10,000 約付」表，
所以影片和網站永遠是同一份試算（匯率、上限、登錄條件都跟著每日建置走）。
用法：python3 make_transit_video.py [輸出資料夾]
需要 Chrome 與 ffmpeg。
"""
import html as htm
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

URL = 'https://jptripcard.com/japan-transit-card/'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'cards/threads/短影音-交通卡儲值'
W, H = 1080, 1920
FADE = 0.25


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


def _txt(s):
    return htm.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s))).strip()


def fetch():
    req = urllib.request.Request(URL)
    s = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
    i = s.find('怎麼儲值最划算</h2>')
    if i < 0:
        sys.exit('線上頁面找不到「怎麼儲值最划算」那張表')
    lede = _txt(s[s.find('<p class="lede">', i):s.find('</p>', i)])
    tb = s[s.find('<tbody>', i):s.find('</tbody>', i)]
    cards, cash, other = [], None, None
    for r in re.findall(r'<tr>(.*?)</tr>', tb, re.S):
        td = re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)
        amt = int(re.search(r'NT\$([\d,]+)', td[1]).group(1).replace(',', ''))
        if '<a ' in td[0]:
            cards.append({
                'name': _txt(re.search(r'<a [^>]*>(.*?)</a>', td[0]).group(1)),
                'reg': _txt(re.search(r'<small[^>]*>(.*?)</small>', td[0]).group(1)),
                'pay': amt,
                'save': int(re.search(r'省 NT\$([\d,]+)', td[2]).group(1).replace(',', ''))
                        if '省' in td[2] else 0,
                'room': _txt(td[3]),
            })
        elif '現鈔' in td[0]:
            cash = amt
        else:
            other = amt
    j = s.find('<p class="disc">匯率用', i)
    disc = _txt(s[j:s.find('</p>', j)])
    m = re.search(r'匯率用 (\d{4})-(\d\d)-(\d\d) [\d:]+ 的日圓中價 ([\d.]+)', disc)
    fee = re.search(r'加上 ([\d.]+)% 國外交易手續費', lede)
    if not (cards and cash and other and m and fee):
        sys.exit('線上表格的格式和預期不同，請先看頁面再改解析')
    return {'cards': cards, 'cash': cash, 'other': other,
            'rate_date': f'{int(m.group(2))}/{int(m.group(3))}', 'rate': m.group(4),
            'fee': fee.group(1)}


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;
 font-family:"PingFang TC","Noto Sans CJK TC","Noto Sans TC","Heiti TC",sans-serif;
 background:#f7f4ee;color:#1d1b18;-webkit-font-smoothing:antialiased}
.f{position:absolute;left:0;top:0;width:1080px;height:1920px;
 padding:200px 84px 400px 84px;display:flex;flex-direction:column;justify-content:center}
.kick{font-size:40px;font-weight:800;color:#c2410c;letter-spacing:.08em;margin-bottom:26px}
h1{font-size:92px;line-height:1.22;font-weight:900;letter-spacing:-.01em}
h1 em{font-style:normal;color:#c2410c}
h2{font-size:70px;line-height:1.25;font-weight:900;margin-bottom:46px}
h2 em{font-style:normal;color:#c2410c}
.sub{font-size:40px;line-height:1.6;color:#5f5a53;margin-top:34px}
.big{font-size:230px;font-weight:900;color:#c2410c;line-height:1;margin:40px 0 0;
 font-variant-numeric:tabular-nums;letter-spacing:-.03em}
.big small{font-size:96px;margin-right:6px}
.pt{font-size:48px;line-height:1.5;font-weight:700;padding:30px 0 30px 66px;position:relative;
 border-bottom:3px dashed #ddd6cb}
.pt:last-child{border-bottom:0}
.pt i{position:absolute;left:0;top:30px;font-style:normal;color:#c2410c;font-weight:900}
.pt s{display:block;text-decoration:none;font-size:36px;font-weight:500;color:#6b655d;margin-top:8px}
.row{display:flex;align-items:center;gap:20px;padding:20px 0;border-bottom:2px solid #e3ddd2}
.row .nm{flex:0 0 400px;font-size:42px;font-weight:800;line-height:1.25}
.row .bar{flex:1 1 auto;height:56px;position:relative}
.row .bar b{position:absolute;left:0;top:0;bottom:0;background:#f0b48c;border-radius:8px}
.row .bar span{position:absolute;top:0;line-height:56px;font-size:36px;font-weight:800;
 color:#9a3412;white-space:nowrap;padding-left:12px}
.row .v{flex:0 0 190px;text-align:right;font-size:44px;font-weight:900;
 font-variant-numeric:tabular-nums}
.row.base .nm,.row.base .v{color:#6b655d}
.row.base{border-bottom:0;border-top:4px solid #1d1b18;margin-top:8px}
.hd{display:flex;font-size:30px;color:#8a837a;font-weight:700;padding-bottom:10px;
 border-bottom:4px solid #1d1b18}
.hd span:first-child{flex:0 0 420px}.hd span:nth-child(2){flex:1}
.cap{padding:28px 0;border-bottom:3px dashed #ddd6cb}
.cap b{display:block;font-size:50px;font-weight:900}
.cap s{display:block;text-decoration:none;font-size:40px;font-weight:600;color:#9a3412;
 margin-top:8px;line-height:1.45}
.reg{padding:24px 0;border-bottom:3px dashed #ddd6cb}
.reg b{display:block;font-size:46px;font-weight:900}
.reg s{display:block;text-decoration:none;font-size:38px;color:#4b463f;margin-top:6px;line-height:1.45}
.note{margin-top:40px;font-size:38px;line-height:1.6;color:#5f5a53;font-weight:600}
.brand{font-size:44px;font-weight:900}
.url{font-size:60px;font-weight:900;color:#c2410c;margin-top:16px;letter-spacing:.01em}
.tiny{font-size:30px;line-height:1.7;color:#8a837a;margin-top:60px}
"""


def page(inner):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style>'
            f'</head><body><div class="f">{inner}</div></body></html>')


def frames(d):
    e = htm.escape
    cs = d['cards']
    top = cs[0]
    out = []
    # 1 開場：第一格就給結論數字
    out.append((2.0, page(
        '<div class="kick">日本交通卡儲值</div>'
        '<h1>Suica 儲 ¥10,000<br>刷對卡少付</h1>'
        f'<div class="big"><small>NT$</small>{top["save"]:,}</div>'
        f'<div class="sub">和換日圓現鈔投現金比<br>{e(d["rate_date"])} 匯率試算</div>')))
    # 2 前提
    out.append((2.6, page(
        '<h2>先講<em>前提</em></h2>'
        '<div class="pt"><i>1</i>實體 Suica、PASMO、ICOCA<s>車站和超商儲值只收現金</s></div>'
        '<div class="pt"><i>2</i>要拿刷卡回饋<s>只能用 iPhone 的 Apple 錢包版綁卡儲值</s></div>'
        '<div class="pt"><i>3</i>Android 海外機型目前不行<s>只能投現金</s></div>')))
    # 3 排名：分兩格，先給基準再揭曉
    mx = max(c['save'] for c in cs) or 1

    def rows(show):
        r = ('<div class="hd"><span>怎麼儲</span><span>比換現鈔少付</span>'
             '<span>實付</span></div>')
        for k, c in enumerate(cs):
            vis = k < show
            w = round(c['save'] / mx * 100)
            r += (f'<div class="row" style="opacity:{1 if vis else 0}">'
                  f'<div class="nm">{e(c["name"])}</div>'
                  f'<div class="bar"><b style="width:{w * .72:.0f}%"></b>'
                  f'<span style="left:{w * .72:.0f}%">{c["save"]:,}</span></div>'
                  f'<div class="v">{c["pay"]:,}</div></div>')
        r += (f'<div class="row base"><div class="nm">換現鈔投現金</div>'
              f'<div class="bar"></div><div class="v">{d["cash"]:,}</div></div>'
              f'<div class="row base" style="border-top:0"><div class="nm">其他卡<br>'
              f'<span style="font-size:32px">再扣一般回饋</span></div>'
              f'<div class="bar"></div><div class="v">{d["other"]:,}</div></div>')
        return r
    head = '<h2>每儲 ¥10,000<br>實際付多少台幣</h2>'
    note = (f'<div class="note"@@>單位 NT$，含 {e(d["fee"])}% 國外交易手續費、扣掉回饋</div>')
    # 兩格的版面高度要一樣，揭曉時標題才不會跳
    out.append((0.8, page(head + rows(0) + note.replace('@@', ' style="opacity:0"'))))
    out.append((3.6, page(head + rows(len(cs)) + note.replace('@@', ''))))
    # 4 上限：有上限的才列
    capped = [c for c in cs if '約儲' in c['room']][:3]
    if capped:
        def room(t):
            t = re.sub(r'，帳單 NT\$[\d,]+ 為止', ' 為止', t)
            return t.replace('；', '<br>')
        out.append((3.2, page(
            '<h2>但加碼<em>有上限</em></h2>'
            + ''.join(f'<div class="cap"><b>{e(c["name"])}</b><s>{room(e(c["room"]))}</s></div>'
                      for c in capped)
            + '<div class="note">用完就掉回一般回饋<br>大額儲值，用完再換下一張</div>')))
    # 5 前置條件
    out.append((3.2, page(
        '<h2>每張都要<em>先設定</em></h2>'
        + ''.join(f'<div class="reg"><b>{e(c["name"])}</b><s>{e(c["reg"])}</s></div>'
                  for c in cs[:5]))))
    # 6 兩件事
    out.append((2.8, page(
        '<h2>還有兩件事</h2>'
        f'<div class="pt"><i>1</i>沒加碼的卡，跟換現鈔差不多'
        f'<s>刷卡 NT${d["other"]:,} 再扣回饋，現鈔 NT${d["cash"]:,}</s></div>'
        '<div class="pt"><i>2</i>Apple 錢包裡的餘額退不出來<s>分幾次少量儲，比一次儲滿安全</s></div>')))
    # 7 收尾
    out.append((2.2, page(
        '<div class="brand">日本旅遊小卡</div>'
        '<div class="url">jptripcard.com</div>'
        '<div class="sub">完整試算、上限與條款<br>搜尋「日本交通卡」</div>'
        f'<div class="tiny">{e(d["rate_date"])} 日圓中價 {e(d["rate"])} 試算，'
        f'國外交易手續費以 {e(d["fee"])}% 計<br>各行活動隨時調整，以發卡行官網公告為準</div>'
        )))
    return out


def main():
    d = fetch()
    chrome = _chrome()
    if not shutil.which('ffmpeg'):
        sys.exit('找不到 ffmpeg')
    os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    fr = frames(d)
    pngs = []
    with tempfile.TemporaryDirectory() as tmp:
        for k, (dur, src) in enumerate(fr, 1):
            f = os.path.join(tmp, f'{k:02d}.html')
            open(f, 'w', encoding='utf-8').write(src)
            png = os.path.abspath(os.path.join(OUT, 'frames', f'{k:02d}.png'))
            subprocess.run([chrome, '--headless', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', f'--window-size={W},{H}',
                            f'--screenshot={png}', f'file://{f}'],
                           capture_output=True, timeout=90)
            if not os.path.exists(png):
                sys.exit(f'{png} 沒有產生出來')
            pngs.append((dur, png))
    # 靜態字卡＋交叉淡入
    args = ['ffmpeg', '-y', '-loglevel', 'error']
    for dur, p in pngs:
        args += ['-loop', '1', '-t', f'{dur + FADE:.2f}', '-framerate', '30', '-i', p]
    flt, prev, t = [], '[0:v]', 0.0
    for k in range(1, len(pngs)):
        t += pngs[k - 1][0]
        lab = f'[x{k}]'
        flt.append(f'{prev}[{k}:v]xfade=transition=fade:duration={FADE}:offset={t:.2f}{lab}')
        prev = lab
    flt.append(f'{prev}format=yuv420p[v]')
    mp4 = os.path.join(OUT, 'transit-topup.mp4')
    args += ['-filter_complex', ';'.join(flt), '-map', '[v]', '-r', '30',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-movflags', '+faststart', mp4]
    subprocess.run(args, check=True)
    total = sum(x for x, _ in pngs) + FADE
    print(f'{mp4}  約 {total:.1f} 秒、{len(pngs)} 格；第一名 {d["cards"][0]["name"]} 少付 NT${d["cards"][0]["save"]}')


if __name__ == '__main__':
    main()
