# 名花之里頁（/nagoya/nabana-no-sato/）的「里內有什麼」插圖與提醒卡（2026-11-13）。
# 參考名花之里官網燈飾頁（nagashima-onsen.co.jp/nabana/illumination/）的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/nagoya-nabana-no-sato/*.svg（240×180、提醒小圖 120×120）。
# 說明文字放在 illust/spots/nagoya-nabana-no-sato.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'nagoya-nabana-no-sato')
W, H = 240, 180
ORANGE = '#f08a4b'
NIGHT = '#2b3560'
WARM = '#ffd98a'
LAKE = '#3f5b8c'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('nb-' + name, W, H, label, inner, bg=bg)


def full(col):
    return f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{col}"/>'


def bottom(path_top, col):
    return f'<path d="{path_top} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s:.1f}" fill="#f9d9c0"/>'
            f'<path d="M{x - 7*s:.1f},{y + 22*s:.1f} q0,{-14*s:.1f} {7*s:.1f},{-14*s:.1f} q{7*s:.1f},0 {7*s:.1f},{14*s:.1f} Z" fill="{col}"/>')


def bulbs(pts, col=WARM, r=2.2):
    return ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="none"/>' for x, y in pts)


def canopy(x, base, s=1.0, cols=(RED, ORANGE, GOLD), trunk=True):
    t = ''
    if trunk:
        t += f'<rect x="{x - 3*s:.1f}" y="{base - 16*s:.1f}" width="{6*s:.1f}" height="{16*s:.1f}" rx="2" fill="{DBROWN}"/>'
    for i, (dx, dy, r) in enumerate([(-11, -22, 11), (11, -22, 11), (0, -32, 12), (0, -20, 10)]):
        t += f'<circle cx="{x + dx*s:.1f}" cy="{base + dy*s:.1f}" r="{r*s:.1f}" fill="{cols[i % len(cols)]}" stroke-width="1.6"/>'
    return t


stars = lambda pts: ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in pts)

# 1. 光之隧道：一圈一圈暖色燈泡拱成長長的隧道
arches = ''
for i, (w, h, cy) in enumerate([(220, 150, 172), (170, 116, 160), (124, 86, 150), (86, 60, 142), (56, 40, 136), (34, 24, 132)]):
    x0, x1 = 120 - w / 2, 120 + w / 2
    top = cy - h
    arches += f'<path d="M{x0},{cy} L{x0},{top + h*.35:.1f} Q{x0},{top} 120,{top} Q{x1},{top} {x1},{top + h*.35:.1f} L{x1},{cy}" fill="none" stroke="#e9b64a" stroke-width="{5 - i*.6:.1f}"/>'
    n = 14 - i
    pts = []
    for k in range(n + 1):
        u = k / n
        a = math.pi * u
        pts.append((120 - (w / 2) * math.cos(a), top + h * .35 - h * .35 * math.sin(a) + (0 if 0.12 < u < .88 else 0)))
    arches += bulbs(pts, '#fff3c4', 2.4 - i * .2)
card('tunnel', '手繪名花之里的光之隧道，一圈一圈暖色的燈拱成長長的隧道',
     full(NIGHT)
     + f'<path d="M10,172 L230,172 L134,132 L106,132 Z" fill="#5a4a5c" stroke="none"/>'
     + f'<path d="M14,40 Q120,-6 226,40 L226,172 L14,172 Z" fill="{GOLD}" opacity=".32" stroke="none"/>'
     + arches
     + person(104, 138, PINK, .9) + person(126, 140, SKY, .9)
     + face(104, 132, .55, blush=False) + face(126, 134, .55, blush=False)
     + stars([(24, 20), (216, 22)]))

# 2. 水上燈飾：湖面上一整片會變色的燈，水面有倒影
card('water', '手繪名花之里的水上燈飾，湖面上排滿彩色的燈，水裡有倒影',
     full(NIGHT)
     + bottom('M3,104 L237,104', LAKE)
     + ''.join(f'<path d="M{x},104 L{x + 10},{70 - (i % 3) * 14} L{x + 20},104 Z" fill="{c}" opacity=".9"/>'
               for i, (x, c) in enumerate([(20, PINK), (44, SKY), (68, GOLD), (92, '#b6f5c8'), (116, PINK), (140, '#c792d6'), (164, GOLD), (188, SKY), (208, PINK)]))
     + ''.join(f'<path d="M{x + 2},108 L{x + 10},{136 + (i % 3) * 8} L{x + 18},108 Z" fill="{c}" opacity=".35" stroke="none"/>'
               for i, (x, c) in enumerate([(20, PINK), (44, SKY), (68, GOLD), (92, '#b6f5c8'), (116, PINK), (140, '#c792d6'), (164, GOLD), (188, SKY), (208, PINK)]))
     + f'<path d="M3,104 L237,104" stroke-width="2"/>'
     + f'<path d="M30,150 q10,-4 20,0 M100,160 q10,-4 20,0 M170,150 q10,-4 20,0" stroke="{WHITE}" stroke-width="2" fill="none" opacity=".7"/>'
     + face(130, 88, .7)
     + stars([(30, 24), (80, 16), (150, 26), (210, 18)]) + sparkle(120, 30) + sparkle(200, 50))

# 3. 雙子樹：兩棵燈樹，教堂鐘聲響起時點燈
def light_tree(x, base, h, col):
    t = f'<path d="M{x},{base - h} L{x + h*.32:.1f},{base} L{x - h*.32:.1f},{base} Z" fill="{col}"/>'
    pts = []
    for k in range(1, 6):
        yy = base - h + h * k / 6
        ww = h * .32 * k / 6
        for m in range(-k, k + 1, 2):
            pts.append((x + ww * m / max(k, 1), yy))
    return t + bulbs(pts, WHITE, 1.8) + star(x, base - h - 4, 7)
card('twintree', '手繪兩棵並排的燈樹，旁邊有小教堂和鐘',
     full(NIGHT)
     + bottom('M3,150 L237,150', '#3d3a52')
     + light_tree(70, 150, 110, '#7fd1c0') + light_tree(126, 150, 110, '#f6c3d0')
     + f'<rect x="168" y="96" width="50" height="54" fill="{WHITE}"/><path d="M162,98 L193,72 L224,98 Z" fill="{BRICK}"/>'
     + f'<rect x="187" y="52" width="12" height="22" fill="{WHITE}"/><path d="M193,40 L193,52 M188,45 L198,45" stroke-width="2"/>'
     + f'<path d="M186,118 Q193,104 200,118 L200,150 L186,150 Z" fill="{BROWN}"/>'
     + f'<path d="M184,60 q9,-14 18,0 Z" fill="{GOLD}" transform="translate(0,6)"/>'
     + f'<path d="M206,60 q6,-4 8,-10 M210,68 q8,-2 12,-8" stroke="{GOLD}" stroke-width="2" fill="none"/>'
     + face(98, 128, .7)
     + stars([(30, 24), (160, 22), (226, 36)]))

# 4. 秋海棠花園：大溫室裡開滿花，有吊盆
card('begonia', '手繪秋海棠花園的大溫室，裡面開滿花，上面掛著吊盆',
     full(SKY)
     + f'<path d="M18,160 L18,90 Q18,26 120,26 Q222,26 222,90 L222,160 Z" fill="#eef7fb"/>'
     + ''.join(f'<path d="M{x},160 L{x},{90 - 60*math.sin(math.acos((x - 120) / 102)):.1f}" stroke-width="1.4" opacity=".6"/>' for x in (50, 85, 120, 155, 190))
     + f'<path d="M18,90 Q120,70 222,90" fill="none" stroke-width="1.4" opacity=".6"/>'
     + ''.join(f'<path d="M{x},{y0} L{x},{y0 + 18}" stroke-width="1.2"/><path d="M{x - 12},{y0 + 18} Q{x},{y0 + 30} {x + 12},{y0 + 18} Z" fill="{BROWN}"/>'
               + ''.join(f'<circle cx="{x + dx}" cy="{y0 + 30 + dy}" r="5" fill="{c}" stroke-width="1.2"/>' for dx, dy, c in [(-8, 0, PINK), (0, 6, RED), (8, 0, PINK), (-3, 12, '#ffd1dc'), (5, 12, RED)])
               for x, y0 in [(70, 46), (120, 36), (170, 46)])
     + f'<path d="M18,160 L222,160" stroke-width="2"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}" stroke-width="1.4"/>'
               for x, y, c in [(36, 146, RED), (52, 140, PINK), (68, 148, GOLD), (90, 144, '#ffd1dc'), (150, 146, PINK), (168, 140, RED), (186, 148, GOLD), (204, 142, PINK)])
     + face(120, 132, .9)
     + bottom('M3,160 L237,160', '#9bc98e')
     + sparkle(210, 20) + sparkle(30, 22))

# 5. 紅葉點燈：池邊的楓樹晚上打燈
card('koyo', '手繪名花之里的紅葉點燈，池邊的楓樹晚上打了燈',
     full(NIGHT)
     + bottom('M3,120 Q120,110 237,120', '#3d3a52')
     + f'<ellipse cx="120" cy="150" rx="90" ry="20" fill="{LAKE}"/>'
     + canopy(46, 126, 1.3) + canopy(120, 118, 1.5, (ORANGE, RED, GOLD)) + canopy(196, 126, 1.3, (RED, GOLD, ORANGE))
     + ''.join(f'<ellipse cx="{x}" cy="150" rx="16" ry="5" fill="{c}" opacity=".5" stroke="none"/>' for x, c in [(56, RED), (120, ORANGE), (186, GOLD)])
     + face(120, 78, .9)
     + f'<path d="M30,120 L30,100 M210,120 L210,100" stroke-width="2"/>'
     + f'<path d="M24,100 L36,100 L30,92 Z M204,100 L216,100 L210,92 Z" fill="{GOLD}" stroke-width="1.4"/>'
     + stars([(30, 26), (100, 18), (180, 24), (220, 46)]))


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('nb-' + name, 120, 120, label, inner, bg='#fff3c4')


# 燈海期間桑名站前的路線巴士停駛
rem('r-kuwana', '手繪提醒：這個巴士站牌沒有車，打叉',
    f'<path d="M36,104 L36,40" stroke-width="3"/><circle cx="36" cy="34" r="18" fill="{GREEN}"/>'
    f'<rect x="26" y="28" width="20" height="10" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
    f'<rect x="66" y="50" width="44" height="30" rx="6" fill="{GRAY}"/>'
    f'<rect x="70" y="56" width="10" height="9" rx="2" fill="{WHITE}" stroke-width="1.2"/><rect x="84" y="56" width="10" height="9" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
    f'<circle cx="76" cy="82" r="4" fill="{INK}"/><circle cx="100" cy="82" r="4" fill="{INK}"/>'
    f'<path d="M60,40 L114,96 M114,40 L60,96" stroke="{RED}" stroke-width="5"/>')

# 現場窗口出票可能要排 30 分鐘以上
rem('r-queue', '手繪提醒：售票窗口前排了長長的隊伍和時鐘',
    f'<rect x="78" y="40" width="34" height="56" rx="3" fill="{WHITE}"/><path d="M74,42 L116,42 L110,30 L80,30 Z" fill="{RED}"/>'
    f'<rect x="84" y="50" width="22" height="16" rx="2" fill="{SKY}"/>'
    + ''.join(f'<circle cx="{x}" cy="78" r="6" fill="#f9d9c0"/><path d="M{x - 7},100 q0,-14 7,-14 q7,0 7,14 Z" fill="{c}"/>'
              for x, c in [(64, PINK), (46, SKY), (28, GOLD), (10, GREEN)])
    + f'<circle cx="34" cy="34" r="18" fill="{WHITE}"/><path d="M34,34 L34,22 M34,34 L34,46" stroke-width="2.6"/>')

print(save(F, OUT), 'files')
