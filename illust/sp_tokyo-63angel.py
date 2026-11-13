# 63 ANGEL 頁的「店裡看得到什麼」插圖與提醒卡（2026-11-13）。
# 參考官網首頁與 System 頁（rokusanangel.jp）的文字介紹畫成可愛版：只畫一般的舞台與
# 可愛的 Q 版表演女孩，不畫成任何真實成員的樣子、不畫店家或團體 logo。
# 輸出 illust/sp/tokyo-63angel/*.svg。說明文字放在 illust/spots/tokyo-63angel.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-63angel')
W, H = 240, 180
F = {}
STAGE = '#3b2f5c'
LILAC = '#c9b6ec'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ra-' + name, W, H, label, inner, bg=bg)


def girl(x, y, hair=DBROWN, dress=PINK, s=1.0, arms='up', bun=False):
    # Q 版表演女孩：大頭、蓬蓬裙、手舉起來；y 是頭的中心
    t = ''
    if arms == 'up':
        t += (f'<path d="M{x-8*s},{y+18*s} L{x-20*s},{y+4*s} M{x+8*s},{y+18*s} L{x+20*s},{y+4*s}" stroke-width="{2.6*s}"/>'
              f'<circle cx="{x-20*s}" cy="{y+4*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>'
              f'<circle cx="{x+20*s}" cy="{y+4*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>')
    elif arms == 'wave':
        t += (f'<path d="M{x-8*s},{y+18*s} L{x-18*s},{y+30*s} M{x+8*s},{y+18*s} L{x+22*s},{y+6*s}" stroke-width="{2.6*s}"/>'
              f'<circle cx="{x+22*s}" cy="{y+6*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>')
    t += (f'<path d="M{x-4*s},{y+40*s} L{x-5*s},{y+52*s} M{x+4*s},{y+40*s} L{x+5*s},{y+52*s}" stroke-width="{2.4*s}"/>'
          f'<ellipse cx="{x-6*s}" cy="{y+53*s}" rx="{4*s}" ry="{2*s}" fill="{dress}" stroke-width="1.2"/>'
          f'<ellipse cx="{x+6*s}" cy="{y+53*s}" rx="{4*s}" ry="{2*s}" fill="{dress}" stroke-width="1.2"/>'
          f'<path d="M{x-8*s},{y+14*s} L{x+8*s},{y+14*s} L{x+9*s},{y+26*s} L{x+20*s},{y+42*s} Q{x},{y+46*s} {x-20*s},{y+42*s} L{x-9*s},{y+26*s} Z" fill="{dress}"/>'
          f'<path d="M{x-18*s},{y+40*s} q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0" fill="none" stroke="{WHITE}" stroke-width="1.4"/>')
    # 頭髮（後）＋臉＋瀏海
    t += f'<path d="M{x-14*s},{y+12*s} Q{x-16*s},{y-14*s} {x},{y-15*s} Q{x+16*s},{y-14*s} {x+14*s},{y+12*s} Z" fill="{hair}"/>'
    t += f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="#f9e0cc"/>'
    t += f'<path d="M{x-12*s},{y-2*s} Q{x-10*s},{y-14*s} {x},{y-13*s} Q{x+10*s},{y-14*s} {x+12*s},{y-2*s} Q{x+6*s},{y-8*s} {x},{y-6*s} Q{x-6*s},{y-8*s} {x-12*s},{y-2*s} Z" fill="{hair}"/>'
    if bun:
        t += f'<circle cx="{x-10*s}" cy="{y-13*s}" r="{5*s}" fill="{hair}"/><circle cx="{x+10*s}" cy="{y-13*s}" r="{5*s}" fill="{hair}"/>'
    t += face(x, y + 2 * s, .55 * s)
    t += star(x + 9 * s, y - 11 * s, 3.4 * s)
    return t


def spot(x1, x2, top=8, bottom=150, col='#5d4f8c'):
    return f'<path d="M{(x1+x2)/2-6},{top} L{(x1+x2)/2+6},{top} L{x2},{bottom} L{x1},{bottom} Z" fill="{col}" stroke="none"/>'


def stars_bg(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in pts)


# 1. 舞台：大型螢幕＋會動的舞台
card('stage', '手繪舞台上三個可愛女孩在跳舞，後面是大螢幕',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{STAGE}"/>'
     + spot(40, 100) + spot(90, 150) + spot(140, 200)
     + f'<rect x="40" y="12" width="160" height="38" rx="6" fill="#4a3d78"/>'
     + ''.join(f'<path d="M{x},{y} l5,-10 l5,10 l-5,10 Z" fill="{c}" stroke-width="1.2"/>' for x, y, c in [(66, 31, PINK), (114, 31, GOLD), (162, 31, '#8ff0ff')])
     + f'<path d="M3,132 L237,132 {BOT}" fill="#6a5a9a"/>'
     + f'<ellipse cx="120" cy="136" rx="70" ry="9" fill="{LILAC}"/>'
     + girl(72, 80, DBROWN, PINK, .95) + girl(120, 74, INK, GOLD, 1.0, 'up', True) + girl(168, 80, '#c27a4a', '#8fd0e8', .95)
     + ''.join(f'<path d="M{x},{y} l6,0" stroke="{c}" stroke-width="2.4"/>' for x, y, c in [(20, 150, GOLD), (210, 152, PINK)])
     + stars_bg([(20, 20, WHITE), (220, 24, GOLD), (14, 90, WHITE), (226, 100, '#8ff0ff')]), bg=STAGE)

# 2. 花魁演目：和服與油紙傘
card('oiran', '手繪穿華麗和服、撐著紅色油紙傘的可愛女孩',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#5a2f4a"/>'
     + spot(80, 160, 8, 150, '#7a4462')
     + f'<path d="M3,140 L237,140 {BOT}" fill="#7a4060"/>'
     # 傘
     + f'<g transform="translate(22,0)"><path d="M150,22 L150,104" stroke-width="2.4"/>'
     + f'<path d="M110,48 Q150,8 190,48 Q170,40 150,48 Q130,40 110,48 Z" fill="{RED}"/>'
     + ''.join(f'<path d="M150,18 L{x},46" stroke-width="1.2"/>' for x in (122, 136, 164, 178)) + '</g>'
     # 和服女孩
     + f'<path d="M100,88 L140,88 L150,140 L90,140 Z" fill="#e88aa0"/>'
     + f'<path d="M90,96 L74,120 L92,122 Z M150,96 L170,92 L150,112 Z" fill="#e88aa0"/>'
     + f'<path d="M96,106 L144,106 L146,118 L94,118 Z" fill="{GOLD}"/>'
     + f'<path d="M118,88 L120,140" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{WHITE}" stroke="none"/>' for x, y in [(104, 128), (134, 128), (110, 96), (130, 96)])
     + f'<circle cx="171" cy="92" r="3.4" fill="#f9e0cc" stroke-width="1.2"/>'
     + f'<path d="M100,72 Q98,40 120,40 Q142,40 140,72 Z" fill="{INK}"/>'
     + f'<circle cx="120" cy="64" r="15" fill="#f9e0cc"/>'
     + f'<path d="M104,60 Q106,46 120,46 Q134,46 136,60 Q128,54 120,56 Q112,54 104,60 Z" fill="{INK}"/>'
     + f'<ellipse cx="120" cy="40" rx="16" ry="8" fill="{INK}"/>'
     + f'<path d="M100,40 L84,34 M100,44 L86,46 M140,40 L156,34" stroke="{GOLD}" stroke-width="2.4"/>'
     + f'<circle cx="104" cy="36" r="4" fill="{PINK}" stroke-width="1.2"/><circle cx="136" cy="36" r="4" fill="{PINK}" stroke-width="1.2"/>'
     + face(120, 66, .7)
     + ''.join(f'<path d="M{x},{y} q6,-6 12,0 q-6,6 -12,0 Z" fill="{PINK}" stroke-width="1.2"/>' for x, y in [(30, 40), (200, 70), (50, 100), (190, 120)])
     + stars_bg([(26, 20, WHITE), (214, 24, GOLD)]), bg='#5a2f4a')

# 3. 最前排與螢光棒
card('front', '手繪最前排的觀眾舉著螢光棒，前面是舞台',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{STAGE}"/>'
     + spot(60, 180, 8, 100)
     + f'<path d="M3,96 L237,96 L237,108 L3,108 Z" fill="{LILAC}"/>'
     + girl(90, 34, DBROWN, '#f2a46b', .8, 'wave') + girl(150, 34, '#c27a4a', PINK, .8, 'up')
     + f'<path d="M3,108 L237,108 {BOT}" fill="#2a2244"/>'
     # 觀眾的後腦勺與螢光棒
     + ''.join(f'<circle cx="{x}" cy="150" r="13" fill="{c}"/>' for x, c in [(48, DBROWN), (96, INK), (144, '#8a5c3a'), (192, INK)])
     + ''.join(f'<path d="M{x},{y1} L{x+d},{y2}" stroke="{c}" stroke-width="5"/>'
               f'<path d="M{x},{y1} L{x+d},{y2}" stroke="{WHITE}" stroke-width="1.6"/>'
               for x, y1, d, y2, c in [(60, 140, 8, 112, PINK), (110, 140, -6, 112, '#8ff0ff'), (156, 140, 6, 112, GOLD), (204, 140, -8, 112, '#b6f5c8')])
     + stars_bg([(20, 20, WHITE), (220, 22, GOLD), (16, 70, '#8ff0ff')]), bg=STAGE)

# 4. 生寫真送到座位
card('photo', '手繪表演女孩把三張照片送到觀眾的座位',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#ece3f7"/>'
     + f'<path d="M3,140 L237,140 {BOT}" fill="#d9cdea"/>'
     + girl(80, 62, DBROWN, PINK, 1.15, 'wave')
     + ''.join(f'<g transform="rotate({r} {x} {y})"><rect x="{x}" y="{y}" width="26" height="34" rx="2" fill="{WHITE}"/>'
               f'<rect x="{x+3}" y="{y+3}" width="20" height="22" fill="{c}" stroke-width="1.2"/>'
               f'<circle cx="{x+13}" cy="{y+12}" r="4" fill="#f9e0cc" stroke-width="1"/></g>'
               for x, y, r, c in [(120, 44, -12, '#f6d3d8'), (142, 40, 0, '#d6e2f2'), (164, 44, 12, '#f8e6b0')])
     + f'<rect x="150" y="104" width="64" height="36" rx="10" fill="{RED}"/>'
     + f'<rect x="156" y="96" width="52" height="16" rx="6" fill="{RED}"/>'
     + f'<path d="M168,136 L168,148 M200,136 L200,148" stroke-width="2.4"/>'
     + f'<path d="M126,102 l6,4 M134,96 l8,0" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},{y} q-6,-8 0,-12 q6,4 0,12 Z M{x},{y} q6,-8 12,-4 q-2,8 -12,4" fill="{PINK}" stroke-width="1.2"/>' for x, y in [(200, 34), (30, 120)])
     + sparkle(36, 34) + star(210, 70, 6), bg='#ece3f7')

# 5. 生日驚喜：上台拍紀念照
card('birthday', '手繪舞台上的生日蛋糕、相機和彩帶',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{STAGE}"/>'
     + spot(70, 170, 8, 140)
     + f'<path d="M3,132 L237,132 {BOT}" fill="#6a5a9a"/>'
     + f'<rect x="88" y="96" width="64" height="36" rx="6" fill="{WHITE}"/>'
     + f'<path d="M88,108 q8,6 16,0 q8,6 16,0 q8,6 16,0 q8,6 16,0" fill="none" stroke="{PINK}" stroke-width="3"/>'
     + f'<rect x="96" y="76" width="48" height="22" rx="5" fill="{PINK}"/>'
     + ''.join(f'<path d="M{x},76 L{x},64" stroke-width="2"/><path d="M{x},62 q-3,-4 0,-8 q3,4 0,8 Z" fill="{GOLD}" stroke-width="1.2"/>' for x in (108, 120, 132))
     + ''.join(f'<circle cx="{x}" cy="88" r="3" fill="{RED}" stroke-width="1"/>' for x in (104, 120, 136))
     + f'<g transform="rotate(-12 44 64)"><rect x="24" y="52" width="44" height="30" rx="6" fill="{GRAY}"/>'
     f'<circle cx="46" cy="67" r="9" fill="{NAVY}"/><circle cx="46" cy="67" r="4" fill="{SKY}" stroke-width="1"/>'
     f'<rect x="54" y="46" width="10" height="7" rx="2" fill="{GRAY}"/></g>'
     + f'<path d="M30,40 l-6,-8 M44,36 l0,-10 M58,40 l6,-8" stroke="{GOLD}" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},{y} q6,8 0,16 q-6,8 0,16" fill="none" stroke="{c}" stroke-width="2.4"/>' for x, y, c in [(180, 30, PINK), (200, 50, GOLD), (220, 26, '#8ff0ff'), (170, 70, '#b6f5c8')])
     + ''.join(f'<rect x="{x}" y="{y}" width="5" height="5" fill="{c}" stroke="none" transform="rotate(30 {x} {y})"/>' for x, y, c in
               [(160, 40, GOLD), (190, 90, PINK), (214, 66, WHITE), (70, 110, GOLD), (40, 120, PINK)])
     + stars_bg([(20, 20, WHITE), (110, 20, GOLD)]), bg=STAGE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ra-' + name, 120, 120, label, inner, bg='#fff3c4')


# VIP 只能打電話，電話預約 16:30 起
rem('r-phone', '手繪提醒：電話和指著四點半的時鐘',
    f'<path d="M20,40 q-6,24 14,50 q22,22 46,14 l-6,-16 l-16,4 q-14,-8 -22,-24 l6,-14 Z" fill="{PINK}"/>'
    f'<circle cx="84" cy="38" r="22" fill="{WHITE}"/>'
    f'<path d="M84,38 L84,58 M84,38 L94,46" stroke-width="2.6"/>'
    f'<path d="M100,78 q8,4 10,12 M96,86 q6,2 8,8" fill="none" stroke-width="1.8"/>')

# 在大樓地下 2 樓
rem('r-floor', '手繪提醒：大樓剖面，往下兩層的位置打星星',
    f'<rect x="28" y="12" width="64" height="56" fill="#e9dcc8"/>'
    + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{SKY}" stroke-width="1.2"/>' for x in (36, 54, 72) for y in (20, 38))
    + f'<path d="M8,68 L112,68" stroke-width="2.6"/>'
    f'<rect x="28" y="68" width="64" height="40" fill="#d6cbb8"/>'
    f'<path d="M28,88 L92,88" stroke-width="1.6"/>'
    f'<rect x="34" y="92" width="52" height="14" rx="3" fill="{GOLD}"/>'
    + star(60, 99, 6, RED)
    + f'<path d="M104,30 L104,96 M98,88 L104,96 L110,88" stroke="{RED}" stroke-width="3" fill="none"/>')

print(save(F, OUT), 'files')
