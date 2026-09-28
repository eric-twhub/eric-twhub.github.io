# -*- coding: utf-8 -*-
"""分享圖卡的共用骨架（1080×1350，4:5）。

前面幾支產生器各自帶了一份幾乎一樣的 CSS、Chrome 尋找、版面高度檢查與輸出流程。
第十一支之後再複製一次，只會讓同一個 bug 有十幾份。共用的部分集中在這裡。

各頁的產生器只要寫一個 build(d) 回傳 [(檔名, html)]，其餘交給 run()。

版面高度是量出來的不是目測的：每張都會檢查最後一個內容區塊有沒有撞到頁尾，
撞到就報錯不輸出。目測看不出被切掉，之前踩過好幾次。
"""
import json, os, re, sys, shutil, subprocess, tempfile, hashlib
import html as htm

W, H = 1080, 1350
E = htm.escape

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
.no{flex:0 0 58px;font-size:24px;font-weight:800;color:#c2410c;
 font-variant-numeric:tabular-nums}
.nm{flex:1 1 auto;font-size:29px;font-weight:700;line-height:1.3}
.nm s{display:block;text-decoration:none;font-size:20px;font-weight:500;color:#8a847c;
 margin-top:4px;line-height:1.55}
.v{flex:0 0 150px;text-align:right;font-size:27px;font-weight:700;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.v.z{color:#b4afa8;font-weight:500;font-size:23px}
.v.ok{color:#2f8f4f}
.v.bad{color:#c4563a}
.v small{display:block;font-size:19px;font-weight:500;color:#8a847c;margin-top:3px}
.mark{flex:0 0 62px;text-align:center;font-size:30px}
.blk{padding:14px 0;border-bottom:1px solid #e5e3de}
.blk:last-child{border-bottom:0}
.blk b{display:block;font-size:29px;font-weight:700;margin-bottom:7px}
.blk b i{font-style:normal;color:#c2410c;margin-right:10px}
.blk s{display:block;text-decoration:none;font-size:23px;color:#3f3b37;line-height:1.7}
.tag{display:inline-block;font-size:19px;padding:2px 10px;border-radius:999px;
 background:#e5e3de;color:#63605c;margin-left:8px;vertical-align:4px;font-weight:600}
.tag.bad{background:#f3ded6;color:#a8442a}
.tag.ok{background:#dcebe0;color:#2f6b45}
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

# 版面檢查改成量 .list 容器本身的溢出，不再列舉區塊選擇器。
# 先前靠選擇器清單，自訂區塊（.sep、.mx）忘了加就量不到，
# 會回報一個很大的「餘裕」而實際上內容已經被切掉。


def page(inner, cls='', extra_css=''):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS}{extra_css}</style></head><body>'
            f'<div class="card {cls}">{inner}</div></body></html>')


def foot(i, n, note):
    return ('<div class="foot"><div><b>eric-twhub.github.io</b>'
            f'<span>{E(note)}</span></div>'
            f'<div class="pg">{i} / {n}</div></div>')


def digest(payload):
    return hashlib.sha1(json.dumps(payload, ensure_ascii=False,
                                   sort_keys=True).encode('utf-8')).hexdigest()[:12]


def chrome():
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


def _check(ch, tmp, name, src):
    probe = os.path.join(tmp, 'probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace(
        '</body>',
        '<script>document.title=JSON.stringify((()=>{'
        # .list 是 flex 且 min-height:0，內容超出時盒子不會變高，
        # 但 scrollHeight 會大於 clientHeight，用這個抓最可靠。
        'const L=document.querySelector(".list");'
        'const over=L?L.scrollHeight-L.clientHeight:0;'
        'const f=document.querySelector(".foot").getBoundingClientRect().top;'
        'let kids=L?[...L.children]:[];'
        'if(!kids.length){kids=[...document.querySelector(".card").children]'
        '.filter(e=>!e.classList.contains("foot"));}'
        'const b=kids.length?Math.max(...kids.map(e=>e.getBoundingClientRect().bottom)):0;'
        'return{gap:over>0?-over:Math.round(f-b)}})())</script></body>'))
    r = subprocess.run([ch, '--headless', '--disable-gpu', '--dump-dom',
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


def run(src_json, out_dir, build, stamp_payload):
    """讀資料、產圖、寫指紋。build(d) 回傳 [(檔名, html)]。"""
    d = json.load(open(src_json, encoding='utf-8'))
    ch = chrome()
    os.makedirs(out_dir, exist_ok=True)
    cards = build(d)
    with tempfile.TemporaryDirectory() as tmp:
        for name, html_src in cards:
            _check(ch, tmp, name, html_src)
            f = os.path.join(tmp, name + '.html')
            open(f, 'w', encoding='utf-8').write(html_src)
            png = os.path.join(out_dir, name)
            subprocess.run([ch, '--headless', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', f'--window-size={W},{H}',
                            f'--screenshot={os.path.abspath(png)}',
                            f'file://{os.path.abspath(f)}'],
                           capture_output=True, timeout=90)
            if not os.path.exists(png):
                sys.exit(f'{name} 沒有產生出來')
    open(os.path.join(out_dir, 'stamp.txt'), 'w').write(digest(stamp_payload(d)))
    print(f'完成 {len(cards)} 張，輸出到 {out_dir}/')
