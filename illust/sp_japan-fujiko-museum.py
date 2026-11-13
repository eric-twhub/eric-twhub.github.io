# 藤子不二雄博物館頁的「館內有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網的常設展示、F 劇場、みんなのひろば 頁（fujiko-museum.com）畫成一般的書桌、展示室、劇場、書架、扭蛋機與屋頂草地。
# 角色 IP：不畫任何角色、角色的招牌元素（任意門、空地的水泥管、恐龍等都不畫）、商標或 logo。
# 輸出 illust/sp/japan-fujiko-museum/*.svg。說明文字放在 illust/spots/japan-fujiko-museum.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-fujiko-museum')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('fm-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


BOOK = [RED, SKY, GOLD, GREEN, PINK, '#c9b6e8', BROWN, NAVY]


def books(x, y, w, h, seed=0):
    s = ''
    cx = x + 2
    i = seed
    while cx < x + w - 6:
        bw = 6 + (i * 3) % 5
        bh = h - 4 - (i * 5) % 7
        s += f'<rect x="{cx}" y="{y+h-bh}" width="{bw}" height="{bh}" rx="1" fill="{BOOK[i % len(BOOK)]}" stroke-width="1.1"/>'
        cx += bw + 1
        i += 1
    return s


# 1. 老師的房間：工作桌與頭上的巨大書櫃
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f6efe2"/>'
     f'<rect x="14" y="12" width="212" height="68" rx="4" fill="#c99a6a"/>')
for r in range(3):
    t += books(18, 15 + r * 21, 204, 19, r * 3) + f'<path d="M14,{35+r*21} L226,{35+r*21}" stroke-width="2"/>'
t += (bottom(150, '#e3d3b2')
      + f'<rect x="40" y="110" width="160" height="12" rx="3" fill="{DBROWN}"/>'
      + f'<path d="M52,122 L52,160 M188,122 L188,160" stroke-width="5"/>'
      + f'<rect x="150" y="122" width="34" height="30" rx="2" fill="{BROWN}"/><path d="M150,136 L184,136" stroke-width="1.6"/>'
      + f'<rect x="70" y="98" width="56" height="14" rx="1" fill="{WHITE}" transform="rotate(-4 98 105)"/>'
      + f'<path d="M78,104 L118,101" stroke-width="1.2" opacity=".6"/>'
      + f'<path d="M136,96 L156,110" stroke="{NAVY}" stroke-width="3"/>'
      + f'<rect x="160" y="92" width="10" height="18" rx="2" fill="{SKY}"/>'
      + f'<path d="M100,100 L104,84 L118,84 L122,100" fill="{GOLD}" stroke-width="1.6"/><path d="M110,84 L110,72" stroke-width="2"/>'
      + f'<rect x="90" y="132" width="40" height="8" rx="3" fill="{RED}"/><path d="M96,140 L96,160 M124,140 L124,160" stroke-width="3"/>'
      + sparkle(220, 100, 4))
card('desk', '手繪一張工作桌，桌上有稿紙、筆和檯燈，頭上是塞滿書的大書櫃', t, bg='#f6efe2')

# 2. 展示室：漫畫原稿和彩色原畫
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f4ede6"/>'
     + bottom(150, '#e0d4c4'))
for x, y, w, h, c in [(18, 26, 56, 70, '#fde7ea'), (84, 20, 72, 52, '#e3f1f8'), (166, 26, 56, 70, '#fff3c4')]:
    t += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{BROWN}"/>'
          f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" fill="{c}" stroke-width="1.4"/>'
          f'<circle cx="{x+w*.35:.0f}" cy="{y+h*.38:.0f}" r="{min(w,h)*.12:.0f}" fill="{GOLD}" stroke-width="1.2"/>'
          f'<path d="M{x+8},{y+h-10} Q{x+w*.4:.0f},{y+h*.5:.0f} {x+w-8},{y+h-12}" fill="none" stroke="{GREEN}" stroke-width="2.4"/>')
# 展示櫃裡的原稿（分格線）
t += (f'<rect x="40" y="104" width="160" height="40" rx="4" fill="#e3f1f8"/>'
      f'<rect x="50" y="108" width="40" height="30" fill="{WHITE}" stroke-width="1.2"/>'
      f'<path d="M50,120 L90,120 M70,108 L70,120 M64,120 L64,138" stroke-width="1.2"/>'
      f'<rect x="100" y="108" width="40" height="30" fill="{WHITE}" stroke-width="1.2"/>'
      f'<path d="M100,118 L140,118 M100,128 L140,128 M122,118 L122,128" stroke-width="1.2"/>'
      f'<rect x="150" y="108" width="40" height="30" fill="{WHITE}" stroke-width="1.2"/>'
      f'<path d="M150,124 L190,124 M168,108 L168,124" stroke-width="1.2"/>'
      f'<path d="M40,144 L40,164 M200,144 L200,164" stroke-width="3"/>'
      + person(214, 128, PINK, .7) + sparkle(120, 90, 4))
card('gallery', '手繪展示室：牆上掛著三幅彩色畫，玻璃展示櫃裡平放著分格的漫畫原稿', t, bg='#f4ede6')

# 3. F 劇場：200 吋大銀幕
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#3f3a5c"/>'
     f'<rect x="22" y="16" width="196" height="92" rx="6" fill="#dff0fd"/>'
     f'<path d="M22,88 Q70,62 120,80 T218,72 L218,102 Q218,108 212,108 L28,108 Q22,108 22,102 Z" fill="#b6e3c6"/>'
     + ''.join(f'<path d="M{x},{y} q6,-6 12,0 q6,-6 12,0" fill="{WHITE}" stroke-width="1.4"/>' for x, y in [(50, 40), (150, 34)])
     + f'<circle cx="190" cy="40" r="10" fill="{GOLD}"/>'
     + f'<text x="56" y="100" font-size="13" text-anchor="middle" fill="{DBROWN}" stroke="none" font-family="sans-serif" font-weight="bold">200"</text>')
for row, (y, n, x0) in enumerate([(126, 8, 26), (148, 9, 14)]):
    for k in range(n):
        x = x0 + k * 24
        t += f'<path d="M{x},{y+14} L{x},{y} q0,-8 9,-8 q9,0 9,8 L{x+18},{y+14} Z" fill="{GOLD if (k+row) % 2 else "#f2a46b"}" stroke-width="1.8"/>'
card('theater', '手繪劇場裡的大銀幕，前面兩排黃色和橘色的座位', t, bg='#3f3a5c')

# 4. 漫畫角：自由翻閱作品
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef4e2"/>'
     + bottom(146, '#d9c9a8'))
for c in range(2):
    x = 16 + c * 120
    t += f'<rect x="{x}" y="24" width="88" height="110" rx="4" fill="#c99a6a"/>'
    for r in range(4):
        t += books(x + 4, 28 + r * 26, 80, 22, r + c * 4) + f'<path d="M{x},{50+r*26} L{x+88},{50+r*26}" stroke-width="2"/>'
t += (f'<rect x="96" y="118" width="48" height="12" rx="4" fill="{RED}"/><path d="M102,130 L102,146 M138,130 L138,146" stroke-width="3"/>'
      + person(120, 92, SKY, .9)
      + f'<path d="M108,106 L120,110 L132,106 L132,118 L120,122 L108,118 Z" fill="{WHITE}" stroke-width="1.6"/>'
      + f'<path d="M120,110 L120,122" stroke-width="1.2"/>'
      + sparkle(120, 20) + star(216, 156, 6))
card('manga', '手繪兩座塞滿漫畫的書架，中間有人坐在紅色長椅上翻書', t, bg='#eef4e2')

# 5. 只有這裡轉得到的扭蛋
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fde7ea"/>'
     + bottom(150, '#f3c9cf'))
for x, c in [(30, RED), (96, SKY), (162, GOLD)]:
    t += (f'<rect x="{x}" y="40" width="50" height="110" rx="6" fill="{c}"/>'
          f'<rect x="{x+5}" y="46" width="40" height="42" rx="4" fill="#f6fbff"/>'
          + ''.join(f'<circle cx="{x+px}" cy="{py}" r="7" fill="{cc}" stroke-width="1.2"/>' for px, py, cc in [(14, 78, PINK), (28, 76, '#b6e3c6'), (20, 64, '#c9b6e8'), (34, 60, GOLD), (12, 54, SKY)])
          + f'<circle cx="{x+25}" cy="106" r="10" fill="{GRAY}"/><rect x="{x+22}" y="97" width="6" height="18" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
          f'<rect x="{x+13}" y="126" width="24" height="14" rx="3" fill="#5a4a50"/>')
t += (f'<ellipse cx="214" cy="160" rx="6" ry="8" fill="{GOLD}"/>'
      + f'<ellipse cx="198" cy="164" rx="5" ry="7" fill="{SKY}"/>'
      + sparkle(28, 24) + sparkle(212, 26) + star(120, 22, 6))
card('gacha', '手繪三台扭蛋機，透明的蓋子裡裝滿彩色扭蛋，地上滾著兩顆', t, bg='#fde7ea')

# 6. 屋頂的草地廣場
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + ''.join(f'<path d="M{x},{y} q8,-10 16,0 q8,-10 16,0 q4,8 -4,10 L{x+4},{y+10} q-8,-2 -4,-10 Z" fill="{WHITE}" stroke-width="1.6"/>' for x, y in [(30, 34), (150, 26)])
     + f'<circle cx="210" cy="40" r="12" fill="{GOLD}"/>'
     + f'<path d="M3,112 Q120,96 237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9ccc8a"/>'
     + f'<path d="M3,112 L237,112" stroke-width="0" />'
     + f'<rect x="10" y="100" width="220" height="10" rx="3" fill="{GRAY}" opacity=".0" stroke="none"/>'
     + ''.join(f'<path d="M{x},{y} l-3,-8 M{x},{y} l0,-10 M{x},{y} l3,-8" stroke="{DGREEN}" stroke-width="1.8"/>' for x, y in [(30, 140), (60, 160), (190, 150), (214, 132), (110, 168)])
     + f'<rect x="130" y="128" width="50" height="10" rx="4" fill="{BROWN}"/><path d="M136,138 L136,152 M174,138 L174,152" stroke-width="3"/>'
     + person(80, 118, PINK, .9) + person(100, 122, SKY, .8)
     + f'<rect x="94" y="96" width="14" height="10" rx="2" fill="{NAVY}"/><circle cx="101" cy="101" r="3" fill="{SKY}" stroke-width="1"/>'
     + f'<path d="M3,100 L237,100" stroke="{DBROWN}" stroke-width="0"/>'
     + ''.join(f'<path d="M{x},112 L{x},98" stroke-width="1.6"/>' for x in range(12, 236, 16))
     + f'<path d="M6,100 L234,100" stroke-width="2"/>'
     + sparkle(96, 40) + star(124, 60, 5))
card('rooftop', '手繪屋頂的草地廣場，四周有欄杆，有人在拍照，旁邊一張長椅', t, bg=SKY)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('fm-' + name, 120, 120, label, inner, bg='#fff3c4')


# F 劇場每人只能看一次
rem('r-theater', '手繪提醒：一張劇場入場券，上面寫著 1',
    f'<path d="M14,34 L96,34 L96,50 q-8,0 -8,8 q0,8 8,8 L96,82 L14,82 L14,66 q8,0 8,-8 q0,-8 -8,-8 Z" fill="{GOLD}"/>'
    f'<path d="M70,34 L70,82" stroke-width="1.6" stroke-dasharray="4 4"/>'
    f'<rect x="26" y="44" width="34" height="26" rx="3" fill="#3f3a5c"/>'
    f'<rect x="30" y="48" width="26" height="14" rx="2" fill="#dff0fd" stroke-width="1"/>'
    f'<text x="80" y="66" font-size="20" text-anchor="middle" fill="{RED}" stroke="none" font-family="sans-serif" font-weight="bold">1</text>'
    + star(100, 102, 8) + sparkle(24, 100))

print(save(F, OUT), 'files')
