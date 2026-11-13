# 阿倍野 HARUKAS 300 展望台頁的「上面有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網施設案內（abenoharukas-300.jp/observatory/guide.html）、FAQ、EDGE 與直升機坪頁
# （頁面資料 harukas.json）畫成可愛版，不描照片構圖；不畫合作活動的角色與商標。
# 輸出 illust/sp/osaka-abeno-harukas/*.svg，說明文字在 illust/spots/osaka-abeno-harukas.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'osaka-abeno-harukas')
W, H = 240, 180
SKYB = '#cfe8f7'
WOOD = '#d9a877'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ah-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def plant(x, y, s=1.0):
    return (f'<rect x="{x-9*s}" y="{y}" width="{18*s}" height="{14*s}" rx="3" fill="{DBROWN}"/>'
            f'<path d="M{x},{y} q{-14*s},{-6*s} {-12*s},{-22*s} q{8*s},{4*s} {12*s},{16*s} '
            f'q{2*s},{-20*s} {12*s},{-24*s} q{4*s},{14*s} {-12*s},{30*s} Z" fill="{GREEN}"/>')


# 1. 60 樓：從地板到天花板的玻璃迴廊
card('corridor', '手繪 60 樓整面落地玻璃的迴廊，人走在窗邊，窗外是一大片街景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .9) + cloud(150, 30, 1.0)
     + f'<path d="M3,112 Q60,100 120,108 T237,104 L237,140 L3,140 Z" fill="#d7ecd0"/>'
     + ''.join(f'<rect x="{x}" y="{136-h}" width="{w}" height="{h}" rx="1.5" fill="{GRAY}" stroke-width="1.2"/>'
               for x, w, h in [(10, 8, 10), (20, 6, 16), (30, 10, 8), (60, 8, 14), (90, 6, 10), (130, 10, 12), (150, 6, 18), (176, 8, 9), (200, 10, 14), (220, 6, 10)])
     + ''.join(f'<path d="M{x},3 L{x},150" stroke-width="3"/>' for x in (60, 120, 180))
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M3,150 L237,150" stroke-width="2.4"/>'
     + back(84, 128, PINK, 1.1) + back(150, 130, GREEN, 1.0) + kid(206, 126, GOLD, 1.1)
     + sparkle(100, 24, 4) + star(214, 26, 6))

# 2. 天氣好的時候看得到的地方：山、大橋與島、飛機
card('view', '手繪遠方的山、一座吊橋和小島，還有從機場起飛的飛機',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,96 L40,58 L70,86 L104,48 L140,90 L3,90 Z" fill="#a8c7a0"/>'
     + f'<path d="M150,92 L176,66 L204,88 L237,70 L237,96 Z" fill="#b9d3b1"/>'
     + f'<path d="M3,92 L237,92 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ea"/>'
     + f'<path d="M150,128 q30,-20 70,-6 L224,140 L146,140 Z" fill="#a8c7a0"/>'
     + f'<path d="M34,128 L150,128" stroke-width="3"/>'
     + f'<path d="M60,128 L60,96 M124,128 L124,96" stroke-width="3"/>'
     + f'<path d="M34,120 Q60,96 60,96 Q92,124 124,96 Q138,110 150,122" fill="none" stroke-width="1.8"/>'
     + ''.join(f'<path d="M{x},128 L{x},{y}" stroke-width="1"/>' for x, y in [(72, 106), (84, 112), (100, 112), (112, 106)])
     + f'<g transform="translate(176,40) rotate(-18)">'
     + f'<path d="M-24,0 Q-24,-6 -16,-6 L18,-6 Q26,-6 28,0 Q26,6 18,6 L-16,6 Q-24,6 -24,0 Z" fill="{WHITE}"/>'
     + f'<path d="M-4,-6 L6,-20 L12,-20 L8,-6 Z M-4,6 L6,20 L12,20 L8,6 Z M-20,-6 L-24,-14 L-18,-14 L-12,-6 Z" fill="{SKY}"/>'
     + f'<circle cx="16" cy="-1" r="1.6" fill="{INK}" stroke="none"/></g>'
     + f'<path d="M150,62 q-10,10 -26,14" fill="none" stroke-width="1.4" stroke-dasharray="3 4"/>'
     + cloud(30, 40, .8) + sparkle(112, 30, 4))

# 3. 58 樓天空庭園：挑空的戶外廣場，木地板和植物
card('garden', '手繪挑空的屋頂庭園，木頭地板、盆栽，頭上是天空',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(80, 40, 1.0) + cloud(150, 60, .7)
     + f'<path d="M3,40 Q3,3 25,3 L44,3 L44,112 L3,112 Z" fill="{GRAY}"/>'
     + f'<path d="M196,3 L215,3 Q237,3 237,25 L237,112 L196,112 Z" fill="{GRAY}"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="12" height="16" rx="2" fill="#e6f4fb" stroke-width="1.2"/>' for x in (14, 208) for y in (24, 52, 80))
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WOOD}"/>'
     + ''.join(f'<path d="M{x},112 L{x-20+(x-120)*.2:.0f},177" stroke-width="1.2" opacity=".5"/>' for x in range(30, 230, 22))
     + f'<path d="M3,112 L237,112" stroke-width="2.4"/>'
     + plant(30, 116, 1.0) + plant(210, 116, 1.0) + plant(60, 140, .8)
     + kid(112, 118, PINK, 1.1) + kid(150, 122, SKY, 1.0)
     + ''.join(f'<path d="M{x},{y} q8,-4 16,0" fill="none" stroke-width="1.6" opacity=".6"/>' for x, y in [(100, 98), (140, 100)])
     + sparkle(186, 24, 4))

# 4. 冬天的暖桌：圍著暖桌吃關東煮
card('kotatsu', '手繪圍著暖桌吃關東煮的兩個人，桌上一鍋冒著熱氣',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#2f3a63"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{c}" stroke="none"/>' for x, y, c in [(30, 30, WHITE), (80, 22, GOLD), (200, 30, WHITE), (220, 60, GOLD), (40, 70, GOLD)])
     + ''.join(f'<rect x="{x}" y="{96-h}" width="{w}" height="{h}" rx="1" fill="#4a557f" stroke-width="1.2"/>' for x, w, h in [(12, 12, 16), (26, 8, 24), (190, 14, 20), (206, 10, 28)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>' for x, y in [(16, 86), (30, 80), (196, 82), (210, 76)])
     + f'<path d="M3,96 L237,96 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WOOD}"/>'
     + kid(70, 92, RED, 1.2) + kid(170, 92, GOLD, 1.2)
     + f'<path d="M50,124 L190,124 L198,166 L42,166 Z" fill="{RED}"/>'
     + f'<path d="M58,124 L182,124" stroke="{GOLD}" stroke-width="2"/>'
     + f'<rect x="44" y="114" width="152" height="12" rx="3" fill="{BROWN}"/>'
     + f'<path d="M90,114 q0,-16 30,-16 q30,0 30,16 Z" fill="{GRAY}"/>'
     + f'<circle cx="108" cy="104" r="5" fill="{WHITE}" stroke-width="1.4"/><path d="M122,100 l8,8 l-8,4 Z" fill="{GOLD}" stroke-width="1.4"/><circle cx="138" cy="106" r="4" fill="{BROWN}" stroke-width="1.4"/>'
     + f'<path d="M108,92 q-5,-6 0,-12 q5,-6 0,-12 M132,92 q-5,-6 0,-12 q5,-6 0,-12" fill="none" stroke="{WHITE}" stroke-width="1.8" opacity=".8"/>'
     + star(120, 24, 6), bg='#2f3a63')

# 5. EDGE THE HARUKAS：大樓頂端的戶外步道
card('edge', '手繪大樓頂端邊緣的窄步道，戴安全帽繫著安全繩的人在上面走',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(20, 150, 1.3) + cloud(160, 160, 1.4) + cloud(176, 40, .8)
     + f'<rect x="30" y="96" width="180" height="60" fill="{GRAY}"/>'
     + ''.join(f'<path d="M30,{y} L210,{y}" stroke-width="1.2" opacity=".45"/>' for y in (110, 124, 138))
     + f'<rect x="20" y="86" width="200" height="10" rx="2" fill="{WHITE}"/>'
     + f'<path d="M24,40 L216,40" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{x},40 L{x},86" stroke-width="2"/>' for x in (24, 216))
     + kid(110, 56, RED, 1.15)
     + f'<path d="M100,50 q10,-14 20,0 Z" fill="{GOLD}"/>'
     + f'<path d="M112,70 L130,40" stroke="{RED}" stroke-width="2"/>'
     + f'<path d="M103,76 l-3,10 M117,76 l3,10" stroke-width="2.6"/>'
     + kid(166, 60, GREEN, .95) + f'<path d="M158,54 q8,-12 16,0 Z" fill="{GOLD}"/>' + f'<path d="M168,72 L180,40" stroke="{RED}" stroke-width="2"/>'
     + f'<path d="M160,78 l-2,8 M172,78 l2,8" stroke-width="2.4"/>'
     + sparkle(50, 24, 4) + star(80, 70, 5))

# 6. 直升機停機坪
card('heliport', '手繪大樓頂上畫著 H 的圓形直升機停機坪，有人站在旁邊看',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(26, 46, .9) + cloud(170, 36, 1.0)
     + f'<path d="M3,104 L237,104 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#b9bfc9"/>'
     + f'<ellipse cx="120" cy="134" rx="78" ry="24" fill="#8f97a6"/>'
     + f'<ellipse cx="120" cy="134" rx="64" ry="19" fill="none" stroke="{WHITE}" stroke-width="3"/>'
     + f'<path d="M106,124 L104,144 M136,124 L134,144 M105,134 L135,134" stroke="{GOLD}" stroke-width="5"/>'
     + kid(36, 96, PINK, 1.0) + kid(204, 96, GOLD, 1.0)
     + f'<path d="M22,82 l-6,-6 M50,82 l6,-6" stroke-width="1.6"/>'
     + sparkle(120, 70, 5) + star(120, 26, 6))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ah-' + name, 120, 120, label, inner, bg='#fff3c4')


# 接駁電梯在地下 1 樓或 2 樓
rem('r-shuttle', '手繪提醒：從地下樓層搭電梯直上 16 樓',
    f'<rect x="16" y="14" width="50" height="94" rx="4" fill="{GRAY}"/>'
    + f'<rect x="20" y="18" width="42" height="18" rx="2" fill="{GOLD}"/>'
    + f'<text x="41" y="32" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">16F</text>'
    + f'<path d="M16,84 L66,84" stroke-width="2"/>'
    + f'<rect x="28" y="88" width="26" height="20" rx="2" fill="{WHITE}"/>'
    + f'<path d="M92,100 L92,30 M82,42 L92,28 L102,42" stroke="{RED}" stroke-width="4" fill="none"/>'
    + f'<text x="92" y="114" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">B1</text>')

# 限定商品只在 59 樓
rem('r-shop', '手繪提醒：紀念品袋和 59 樓',
    f'<path d="M20,50 L66,50 L72,104 L14,104 Z" fill="{PINK}"/>'
    + f'<path d="M32,50 q0,-18 11,-18 q11,0 11,18" fill="none" stroke-width="2.6"/>'
    + star(43, 76, 9)
    + f'<rect x="78" y="20" width="32" height="20" rx="3" fill="{GOLD}"/>'
    + f'<text x="94" y="35" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">59F</text>'
    + sparkle(94, 64, 6) + sparkle(100, 92, 4) + star(84, 104, 5))

print(save(F, OUT), 'files')
