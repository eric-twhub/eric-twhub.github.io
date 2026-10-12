# -*- coding: utf-8 -*-
"""把封存特價頁裡「台灣虎航 台中→沖繩」那些票價卡換成查證說明。

2026-10-12 查證：台灣虎航的官方時刻表（涵蓋 2026/06/02 到 2027/10/30，共 45
條航線）台灣端的出發地只有 TPE、KHH、TNN，沒有台中；虎航飛沖繩的班次是
TPE 的 IT230／IT232 與 TNN 的 IT796，起飛時間都對不上資料庫那幾筆的 07:10。
到 Trip.com 查同一天，搜尋結果裡也沒有虎航。這個班次不存在。

gen.py 已經在 load() 擋掉這種筆數（見 airline-routes.json），但封存的特價頁
不會再重新產生，所以要用這支腳本就地修補。

做兩件事：
  1. 每一張虎航台中的票價卡換成說明區塊（行內樣式，不動頁面的 CSS）
  2. 主打就是這筆的頁面，另外改掉 h1、title、og:title、描述與「為什麼值得買」

用法：python3 fix_phantom_tigerair.py [--dry]
"""
import re, glob, sys, io

CHECKED = '2026-10-12'
SRC = 'https://www.tigerairtw.com/zh-tw/flight-information/flight-schedule'

CARD = re.compile(r'<article class="card[^"]*"[^>]*>.*?</article>', re.S)
PRICE = re.compile(r'<div class="pr">NT\$([\d,]+)<span')
DATES = re.compile(r'<div class="dt">([\d-]+(?: – [\d-]+)?)')

# grid-column 讓說明塊橫跨整列：.grid 是多欄格線，單獨一個子元素會被壓成一直條
BOX = ('grid-column:1/-1;background:#fff;border:1px solid var(--line);'
       'border-left:3px solid var(--hot);border-radius:10px;padding:14px 16px;'
       'margin:0 0 12px')
DIM = 'color:var(--dim);font-size:.86rem;margin:8px 0 0;line-height:1.65'


def notice(items):
    """一頁一張查證說明，取代該頁所有虎航台中的票價卡

    同一頁最多有四張，每張都貼一份同樣的說明會讓整頁變成複製貼上，
    所以併成一塊，被拿掉的那幾筆用刪除線列在最上面。
    """
    head = ''.join(
        f'<div style="font-size:.82rem;color:var(--dim);text-decoration:line-through">'
        f'台中 → 沖繩　NT${p} 來回含稅' + (f'　{d}' if d else '') + '</div>'
        for p, d in items)
    return (
        f'<div style="{BOX}">'
        f'{head}'
        f'<p style="margin:8px 0 0;font-weight:700">'
        f'{"這幾班飛機都不存在，這些價格訂不到。" if len(items) > 1 else "這班飛機不存在，這個價格訂不到。"}</p>'
        f'<p style="{DIM}">台灣虎航的官方時刻表上沒有任何台中出發的航線。'
        f'虎航飛沖繩只有兩個出發地：桃園（IT230 06:35／06:50、IT232 18:20／18:30）'
        f'與台南（IT796 15:05／15:20）。這一筆標的 07:10 起飛對不上任何一班。</p>'
        f'<p style="{DIM}">價格來自票價資料庫，上面標的販售通路是 Trip.com，'
        f'但到 Trip.com 查同一天的台中到沖繩，搜尋結果裡沒有虎航。</p>'
        f'<p style="{DIM}">查證於 {CHECKED}，依據'
        f'<a href="{SRC}" target="_blank" rel="nofollow noopener">台灣虎航官方時刻表</a>。'
        f'同一天真的飛台中到沖繩的是轉機航班，直飛要從桃園或台南出發。</p>'
        f'</div>')


def is_tiger(card):
    return '台灣虎航' in card and '台中' in card


def patch_cards(h):
    hits, items = [], []
    for m in CARD.finditer(h):
        if not is_tiger(m.group(0)):
            continue
        p = PRICE.search(m.group(0))
        d = DATES.search(m.group(0))
        hits.append((m.start(), m.end()))
        items.append((p.group(1) if p else '—', d.group(1) if d else ''))
    if not hits:
        return h, 0
    # 後面的先刪，位移才不會跑掉；說明塊補在第一張的位置
    for a, b in reversed(hits[1:]):
        h = h[:a] + h[b:]
    a, b = hits[0]
    h = h[:a] + notice(items) + h[b:]
    # 主卡那格原本限寬 340px，放一張卡剛好，放整段說明會擠成一直條
    h = h.replace('<div class="grid" style="max-width:340px">', '<div class="grid">')
    return h, len(hits)


def patch_head(h):
    """主打就是虎航那筆的頁面：標題、描述、導言、為什麼值得買"""
    m = re.search(r'<h1>台中飛沖繩 NT\$([\d,]+) 來回含稅｜台灣虎航 [\d/]+ 出發</h1>', h)
    if not m:
        return h, False
    price = m.group(1)
    new_t = f'台中飛沖繩 NT${price} 這一筆查不到：虎航沒有台中出發的航線'
    new_d = (f'這筆台中飛沖繩 NT${price} 查證不到。台灣虎航的官方時刻表上沒有任何'
             f'台中出發的航線，Trip.com 同一天也查不到這班。查證於 {CHECKED}，'
             f'這一頁保留下來說明原因。')

    old_t = re.search(r'<title>(.*?)</title>', h).group(1)
    h = h.replace(f'<title>{old_t}</title>', f'<title>{new_t}</title>')
    h = h.replace(f'content="{old_t}"', f'content="{new_t}"')
    h = h.replace(f'"headline": "{old_t}"', f'"headline": "{new_t}"')
    h = re.sub(r'<h1>.*?</h1>', f'<h1>{new_t}</h1>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*"',
               f'<meta name="description" content="{new_d}"', h, count=1)
    h = re.sub(r'(<meta property="og:description" content=)"[^"]*"',
               rf'\1"{new_d}"', h, count=1)
    h = re.sub(r'("description": )"[^"]*"', rf'\1"{new_d}"', h, count=1)
    h = re.sub(r'<p class="lede">台中飛沖繩，.*?</p>',
               '<p class="lede">這一頁原本是一則特價，後來查出那班飛機不存在。'
               '原始內容保留在下面，加上查不到的原因。</p>', h, count=1, flags=re.S)

    # 「這個價格為什麼值得買」整段換掉：那幾條理由算的是一個不存在的價格
    m2 = re.search(r'<h2 id="(h-[0-9a-f]+)">這個價格為什麼值得買</h2>(.*?)(?=<h2 )',
                   h, re.S)
    if m2:
        h = h.replace(m2.group(0),
                      f'<h2 id="{m2.group(1)}">為什麼這一頁留著</h2>'
                      '<p class="lede">網址已經被引用，整頁拿掉會變成死連結。'
                      '原本「這個價格為什麼值得買」那幾條，算的是一個不存在的班次，'
                      '所以移掉，換成查不到的原因。同航線其他家的選擇仍然有效。</p>')
        h = h.replace('>這個價格為什麼值得買</a>', '>為什麼這一頁留著</a>')
    return h, True


def drop_empty_alts(h):
    """「同航線其他選擇」裡的卡全被拿掉時，整段移除

    留一個只有標題的空區塊，讀者會以為是頁面壞了。
    """
    m = re.search(r'<h2 id="(h-[0-9a-f]+)">同航線其他選擇</h2>(.*?)(?=<h2 )', h, re.S)
    if not m or '<article class="card' in m.group(2):
        return h, False
    h = h.replace(m.group(0), '')
    h = re.sub(r'<a href="#' + m.group(1) + r'">同航線其他選擇</a>', '', h)
    return h, True


def main():
    dry = '--dry' in sys.argv
    files = sorted(glob.glob('deals/*/index.html'))
    n_card = n_head = n_file = 0
    for f in files:
        h = io.open(f, encoding='utf-8').read()
        if '台灣虎航' not in h or '台中' not in h:
            continue
        h2, n = patch_cards(h)
        h2, head = patch_head(h2)
        h2, drop = drop_empty_alts(h2)
        if n or head:
            n_file += 1
            n_card += n
            n_head += 1 if head else 0
            print(f'  {f}　卡 {n} 張' + ('　＋標題與導言' if head else '')
                  + ('　＋移除空的其他選擇' if drop else ''))
            if not dry:
                io.open(f, 'w', encoding='utf-8').write(h2)
    print(f'{"（試跑）" if dry else ""}共 {n_file} 頁，'
          f'換掉 {n_card} 張票價卡，其中 {n_head} 頁連標題一起改')


if __name__ == '__main__':
    main()
