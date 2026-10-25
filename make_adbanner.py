# -*- coding: utf-8 -*-
"""廣告版位的圖片（兩種尺寸）。

橫幅 banner-<kind>.jpg：1440×400，給整頁寬的廣告區塊用。
卡片 card-<kind>.jpg：540×360，給 /japan-card-labels/ 標籤格線裡那種
直式格子用。橫幅的 3.6:1 塞進 0.667 的格子會變成一條細線，所以另做一組。

為什麼自己做而不是用聯盟後台的素材：後台的 banner 尺寸固定、配色是對方的，
擺進來像外掛的東西。這組用站上的色票與字級做，橘色主色與站上的 --acc 同一個。

圖上不放價格與折扣。那些數字本站沒有查證，寫上去就變成本站在宣稱。
要放促銷數字的話，改用聯盟後台的官方素材，責任在對方。

存成 JPEG 而不是 PNG：底圖是漸層，PNG 一張 230KB，同樣畫質的 JPEG 只要 60KB。
廣告圖放在內容頁上，大小直接影響載入，差這麼多沒有理由用 PNG。

輸出：ads/banner-<kind>.jpg
"""
import os, sys, json, subprocess, tempfile, shutil
import html as htm

W, H = 1440, 400
CW, CH = 540, 360          # 直式格子上半部的圖
OUT = 'ads'
E = htm.escape

# 與 gen.py 的 _AD_KIND 對齊，但文案改成橫幅用的短句。
# 第四欄是平台名，一定要印在圖上：partners.json 的標示原則是
# 「每個連結都標明會前往哪個平台，讓使用者點擊前就知道目的地」。
# 只寫「看看有什麼」的話，讀者不知道會被帶去哪，不會點。
BANNERS = {
    'esim':      ('📱', '日本上網卡與 eSIM', '落地就能用，不用現場找櫃台', 'Klook'),
    'activity2': ('🎫', '日本行程與門票', '在地一日遊、景點票與體驗', 'KKday'),
    'transfer':  ('🚕', '日本機場接送', '深夜抵達也有車，先訂好不用排', 'Trip.com'),
    'car':       ('🚗', '在日本租車', '比較各家車型與保險方案', 'Trip.com'),
    'transport': ('🚄', 'JR Pass 與日本交通票', '跨城市移動前先比一次', 'Trip.com'),
    'hotel':     ('🏨', '日本住宿', '看完機票就是訂房', 'Trip.com'),
}


def _resolve():
    """標題、副標與平台名以 ads.json 的商品組為準，上面那張表只當備援。

    2026-10-25 發現圖上印「到 Trip.com 看」但連結其實送去 KKday：
    transfer／car／transport 三組在 ads.json 換過平台，而這支程式自己抄了
    一份寫死的平台名，換的時候沒跟著改，重新產生也修不好。同一個名字寫在
    兩個檔案裡遲早會各走各的，所以改成只有一個來源。
    """
    groups = (json.load(open('ads.json', encoding='utf-8'))['groups']
              if os.path.exists('ads.json') else {})
    parts = (json.load(open('partners.json', encoding='utf-8'))['partners']
             if os.path.exists('partners.json') else {})
    out = {}
    for kind, (icon, title, sub, brand) in BANNERS.items():
        g = groups.get(kind) or {}
        out[kind] = (g.get('icon') or icon,
                     g.get('title') or title,
                     g.get('sub') or sub,
                     g.get('brand') or parts.get(kind, {}).get('brand') or brand)
    return out


SPEC = _resolve()

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1440px;height:400px;overflow:hidden;
 font-family:"Noto Sans CJK TC","Noto Sans TC","PingFang TC","Hiragino Sans",sans-serif;
 -webkit-font-smoothing:antialiased}
.b{width:1440px;height:400px;display:flex;align-items:center;gap:54px;
 padding:0 72px;background:linear-gradient(110deg,#c2410c 0%,#9a3412 58%,#7c2d12 100%);
 color:#fff;position:relative;overflow:hidden}
.b::after{content:"";position:absolute;right:-120px;top:-150px;width:560px;height:560px;
 border-radius:50%;background:rgba(255,255,255,.07)}
.b::before{content:"";position:absolute;right:120px;bottom:-210px;width:380px;height:380px;
 border-radius:50%;background:rgba(255,255,255,.05)}
.ic{flex:0 0 auto;font-size:132px;line-height:1;filter:drop-shadow(0 6px 14px rgba(0,0,0,.22))}
.tx{flex:1 1 auto;min-width:0;position:relative;z-index:1}
.t{font-size:62px;font-weight:800;letter-spacing:-.01em;line-height:1.2}
.s{font-size:31px;margin-top:16px;opacity:.9;line-height:1.5}
.go{flex:0 0 auto;position:relative;z-index:1;background:#fff;color:#9a3412;
 padding:18px 36px;border-radius:18px;white-space:nowrap;text-align:center}
.go b{display:block;font-size:31px;font-weight:800;line-height:1.2}
.go s{display:block;text-decoration:none;font-size:19px;font-weight:600;
 color:#a8674a;margin-top:5px}
"""


# 直式格子裡的圖。寬度只有橫幅的三分之一，所以圖示與標題改成上下疊，
# 而且不放「到 X 看」的按鈕：那一行在 HTML 裡是真的連結，印在圖上會變成
# 兩個看起來都能點、實際只有一個能點的東西。
CARD_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:540px;height:360px;overflow:hidden;
 font-family:"Noto Sans CJK TC","Noto Sans TC","PingFang TC","Hiragino Sans",sans-serif;
 -webkit-font-smoothing:antialiased}
.c{width:540px;height:360px;display:flex;flex-direction:column;justify-content:center;
 padding:0 42px;background:linear-gradient(140deg,#c2410c 0%,#9a3412 60%,#7c2d12 100%);
 color:#fff;position:relative;overflow:hidden}
.c::after{content:"";position:absolute;right:-80px;top:-110px;width:330px;height:330px;
 border-radius:50%;background:rgba(255,255,255,.07)}
.c::before{content:"";position:absolute;left:-90px;bottom:-140px;width:260px;height:260px;
 border-radius:50%;background:rgba(255,255,255,.05)}
.ic{font-size:76px;line-height:1;position:relative;z-index:1;
 filter:drop-shadow(0 5px 12px rgba(0,0,0,.22))}
.t{font-size:40px;font-weight:800;letter-spacing:-.01em;line-height:1.25;
 margin-top:20px;position:relative;z-index:1}
.s{font-size:22px;margin-top:12px;opacity:.9;line-height:1.5;position:relative;z-index:1}
"""


def card_page(kind):
    icon, title, sub, brand = SPEC[kind]
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CARD_CSS}</style></head><body><div class="c">'
            f'<div class="ic">{icon}</div>'
            f'<div class="t">{E(title)}</div>'
            f'<div class="s">{E(sub)}</div>'
            '</div></body></html>')


def page(kind):
    icon, title, sub, brand = SPEC[kind]
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<style>{CSS}</style></head><body><div class="b">'
            f'<div class="ic">{icon}</div>'
            f'<div class="tx"><div class="t">{E(title)}</div>'
            f'<div class="s">{E(sub)}</div></div>'
            f'<div class="go"><b>到 {E(brand)} 看</b><s>查價格與供應狀況</s></div>'
            '</div></body></html>')


def chrome():
    c = os.environ.get('CHROME')
    if c and os.path.exists(c):
        return c
    mac = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(mac):
        return mac
    for n in ('google-chrome', 'chromium', 'chromium-browser'):
        import shutil
        p = shutil.which(n)
        if p:
            return p
    sys.exit('找不到 Chrome，設環境變數 CHROME 指到執行檔')


def shoot(ch, tmp, name, src, w, h, prefix):
    """name 同時當暫存檔名與輸出檔名，所以 prefix 不同的兩輪不會互相覆蓋。"""
    f = os.path.join(tmp, prefix + '-' + name + '.html')
    open(f, 'w', encoding='utf-8').write(src)
    png = os.path.join(tmp, f'{prefix}-{name}.png')
    subprocess.run([ch, '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--force-device-scale-factor=1', f'--window-size={w},{h}',
                    f'--screenshot={os.path.abspath(png)}',
                    f'file://{os.path.abspath(f)}'],
                   capture_output=True, timeout=90)
    if not os.path.exists(png):
        sys.exit(f'{name} 沒有產生出來')
    jpg = os.path.join(OUT, f'{prefix}-{name}.jpg')
    if shutil.which('sips'):
        subprocess.run(['sips', '-s', 'format', 'jpeg',
                        '-s', 'formatOptions', '88', png,
                        '--out', jpg], capture_output=True, timeout=60)
    if not os.path.exists(jpg):      # 沒有 sips 就退回 PNG，別整個失敗
        jpg = os.path.join(OUT, f'{prefix}-{name}.png')
        shutil.copy(png, jpg)
    print(f'   {os.path.basename(jpg)}  {os.path.getsize(jpg)//1024} KB')


def main():
    ch = chrome()
    os.makedirs(OUT, exist_ok=True)
    for kind, (_, title, _, brand) in SPEC.items():
        print(f'   {kind:<10} {title}  →  {brand}')
    with tempfile.TemporaryDirectory() as tmp:
        for kind in BANNERS:
            shoot(ch, tmp, kind, page(kind), W, H, 'banner')
        for kind in BANNERS:
            shoot(ch, tmp, kind, card_page(kind), CW, CH, 'card')
    print(f'完成 {len(BANNERS) * 2} 張，輸出到 {OUT}/')


if __name__ == '__main__':
    main()
