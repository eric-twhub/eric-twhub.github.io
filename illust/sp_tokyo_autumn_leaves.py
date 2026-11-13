# 東京賞楓頁（/tokyo/autumn-leaves/）的「這些地方長這樣」插圖與提醒卡（2026-11-13）。
# 參考東京都公園協會（六義園、小石川後樂園）、昭和紀念公園「秋の夜散歩」、高尾登山電鐵、新宿御苑官網的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/tokyo-autumn-leaves/*.svg（240×180、提醒小圖 120×120）。
# 說明文字放在 illust/spots/tokyo-autumn-leaves.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-autumn-leaves')
W, H = 240, 180
ORANGE = '#f08a4b'
ROOF = '#6f6a72'
POND = '#5d79a8'
NIGHT = '#2b3560'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ta-' + name, W, H, label, inner, bg=bg)


def full(col):
    return f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{col}"/>'


def bottom(path_top, col):
    return f'<path d="{path_top} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def canopy(x, base, s=1.0, cols=(RED, ORANGE, GOLD), trunk=True):
    t = ''
    if trunk:
        t += f'<rect x="{x - 3*s:.1f}" y="{base - 16*s:.1f}" width="{6*s:.1f}" height="{16*s:.1f}" rx="2" fill="{DBROWN}"/>'
    for i, (dx, dy, r) in enumerate([(-11, -22, 11), (11, -22, 11), (0, -32, 12), (0, -20, 10)]):
        t += f'<circle cx="{x + dx*s:.1f}" cy="{base + dy*s:.1f}" r="{r*s:.1f}" fill="{cols[i % len(cols)]}" stroke-width="1.6"/>'
    return t


def ginkgo_tree(x, base, s=1.0):
    return (f'<rect x="{x - 2.5*s:.1f}" y="{base - 14*s:.1f}" width="{5*s:.1f}" height="{14*s:.1f}" rx="2" fill="{DBROWN}"/>'
            f'<path d="M{x},{base - 60*s:.1f} Q{x + 22*s:.1f},{base - 30*s:.1f} {x + 18*s:.1f},{base - 16*s:.1f} '
            f'Q{x},{base - 10*s:.1f} {x - 18*s:.1f},{base - 16*s:.1f} Q{x - 22*s:.1f},{base - 30*s:.1f} {x},{base - 60*s:.1f} Z" fill="{GOLD}" stroke-width="1.6"/>')


def ginkgo(x, y, r=8, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x},{y} L{x},{y + r*.9:.1f}" stroke-width="1.3"/>'
            f'<path d="M{x},{y} L{x - r},{y - r*.8:.1f} Q{x - r*.5:.1f},{y - r*1.25:.1f} {x - r*.1:.1f},{y - r*.95:.1f} L{x},{y - r*.72:.1f} '
            f'L{x + r*.1:.1f},{y - r*.95:.1f} Q{x + r*.5:.1f},{y - r*1.25:.1f} {x + r},{y - r*.8:.1f} Z" fill="{GOLD}" stroke-width="1.3"/></g>')


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s:.1f}" fill="#f9d9c0"/>'
            f'<path d="M{x - 7*s:.1f},{y + 22*s:.1f} q0,{-14*s:.1f} {7*s:.1f},{-14*s:.1f} q{7*s:.1f},0 {7*s:.1f},{14*s:.1f} Z" fill="{col}"/>')


stars = lambda pts: ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in pts)

# 1. 六義園 夜間：池邊點燈的楓樹，土藏的白牆上有投影
card('rikugien', '手繪六義園夜間，池邊的楓樹打燈，倉庫白牆上有投影',
     full(NIGHT)
     + f'<path d="M150,46 L232,46 L224,30 L158,30 Z" fill="{ROOF}"/>'
     + f'<rect x="156" y="46" width="70" height="56" fill="{WHITE}"/>'
     + f'<circle cx="176" cy="66" r="10" fill="{PINK}" opacity=".85" stroke="none"/>'
     + f'<circle cx="200" cy="78" r="12" fill="{SKY}" opacity=".9" stroke="none"/>'
     + f'<circle cx="212" cy="60" r="7" fill="{GOLD}" opacity=".9" stroke="none"/>'
     + f'<path d="M168,88 q10,-8 20,0 q10,8 20,0" stroke="{GREEN}" stroke-width="2.4" fill="none"/>'
     + bottom('M3,112 Q120,100 237,112', '#3d3a52')
     + f'<ellipse cx="96" cy="146" rx="80" ry="22" fill="{POND}"/>'
     + canopy(40, 118, 1.2) + canopy(100, 112, 1.3, (ORANGE, RED, GOLD)) + canopy(150, 120, .9, (RED, GOLD, ORANGE))
     + ''.join(f'<ellipse cx="{x}" cy="146" rx="12" ry="5" fill="{c}" opacity=".55" stroke="none"/>' for x, c in [(48, RED), (98, ORANGE), (140, GOLD)])
     + f'<rect x="196" y="122" width="10" height="20" fill="{GRAY}"/><path d="M190,122 L212,122 L201,112 Z" fill="{ROOF}"/>'
     + f'<rect x="198" y="126" width="6" height="6" fill="{GOLD}" stroke-width="1"/>'
     + face(100, 92, .8) + stars([(30, 26), (80, 18), (128, 30)]))

# 2. 小石川後樂園 夜間：圓月橋（倒影湊成滿月）的投影，旁邊是做了雪吊的松樹
card('koishikawa', '手繪小石川後樂園的圓月橋，倒影湊成一個圓，旁邊是做了雪吊的松樹',
     full(NIGHT)
     + bottom('M3,100 L237,100', POND)
     + f'<path d="M50,100 A44,44 0 0,1 138,100 L150,100 L150,108 L38,108 L38,100 Z" fill="#b9b3ad"/>'
     + f'<path d="M62,100 A32,32 0 0,1 126,100 Z" fill="{NIGHT}"/>'
     + f'<path d="M62,108 A32,32 0 0,0 126,108" fill="none" stroke="#b9b3ad" stroke-width="3" stroke-dasharray="6 4" opacity=".8"/>'
     + f'<path d="M50,108 A44,44 0 0,0 138,108" fill="none" stroke="#b9b3ad" stroke-width="2" stroke-dasharray="3 5" opacity=".6"/>'
     + f'<circle cx="80" cy="74" r="6" fill="{PINK}" opacity=".9" stroke="none"/>'
     + f'<circle cx="104" cy="66" r="5" fill="{GOLD}" opacity=".9" stroke="none"/>'
     + f'<circle cx="124" cy="78" r="5" fill="{SKY}" opacity=".9" stroke="none"/>'
     + face(94, 86, .7)
     # 雪吊：中間一根柱子，繩子往下拉成傘狀
     + f'<path d="M196,20 L196,94" stroke-width="2.4"/>'
     + ''.join(f'<path d="M196,22 L{x},{y}" stroke="{GOLD}" stroke-width="1.4"/>' for x, y in [(160, 70), (172, 76), (184, 80), (208, 80), (220, 76), (232, 70)])
     + f'<ellipse cx="174" cy="74" rx="18" ry="9" fill="{DGREEN}"/><ellipse cx="218" cy="74" rx="16" ry="9" fill="{DGREEN}"/>'
     + f'<ellipse cx="196" cy="60" rx="14" ry="8" fill="{GREEN}"/>'
     + f'<path d="M196,94 L196,100" stroke="{DBROWN}" stroke-width="5"/>'
     + stars([(30, 26), (60, 40), (140, 22)]))

# 3. 昭和紀念公園 銀杏並木：一整排金黃的銀杏
card('ginkgo', '手繪昭和紀念公園的銀杏並木，兩排金黃色的銀杏中間有人散步',
     full('#ffe7b8')
     + f'<path d="M3,96 L237,96 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#f6d27a"/>'
     + f'<path d="M108,96 L132,96 L170,177 L70,177 Z" fill="#f1e2c4"/>'
     + ginkgo_tree(98, 100, .55) + ginkgo_tree(142, 100, .55)
     + ginkgo_tree(80, 116, .8) + ginkgo_tree(160, 116, .8)
     + ginkgo_tree(52, 144, 1.1) + ginkgo_tree(188, 144, 1.1)
     + ginkgo_tree(16, 176, 1.3) + ginkgo_tree(224, 176, 1.3)
     + person(112, 138, PINK, .8) + person(130, 142, SKY, .8)
     + face(52, 112, .7)
     + ginkgo(40, 40, 8, -20) + ginkgo(200, 34, 7, 25) + ginkgo(120, 60, 6, 10) + sparkle(160, 50) + sparkle(76, 26))

# 4. 高尾山纜車：很陡的坡
card('takao', '手繪高尾山纜車爬上很陡的山坡，旁邊是紅葉',
     full(SKY)
     + f'<path d="M3,160 L200,30 L237,30 L237,155 Q237,177 215,177 L25,177 Q3,177 3,160 Z" fill="#a9cf9a"/>'
     + f'<path d="M14,166 L214,34" stroke-width="2.4"/><path d="M24,170 L222,40" stroke-width="2.4"/>'
     + f'<g transform="rotate(-33 112 104)"><rect x="80" y="86" width="64" height="34" rx="6" fill="{GOLD}"/>'
       f'<rect x="88" y="92" width="14" height="12" rx="2" fill="{SKY}"/><rect x="106" y="92" width="14" height="12" rx="2" fill="{SKY}"/>'
       f'<rect x="124" y="92" width="14" height="12" rx="2" fill="{SKY}"/>'
       f'<circle cx="92" cy="122" r="4" fill="{INK}"/><circle cx="132" cy="122" r="4" fill="{INK}"/></g>'
     + face(116, 114, .7)
     + canopy(180, 110, .9) + canopy(214, 92, .9, (ORANGE, GOLD, RED)) + canopy(196, 150, 1.0, (RED, RED, GOLD))
     + canopy(40, 60, .8, (ORANGE, RED, GOLD))
     + f'<path d="M40,150 A30,30 0 0,0 52,134" fill="none" stroke="{RED}" stroke-width="2"/>'
     + sparkle(90, 30) + sparkle(150, 22))

# 5. 新宿御苑：大草坪、大樹，遠處是城市大樓
card('shinjuku', '手繪新宿御苑的大草坪和紅黃色的大樹，遠處是大樓',
     full(SKY)
     + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{100 - y}" fill="{GRAY}"/>' for x, y, w in [(20, 50, 22), (46, 34, 18), (160, 44, 20), (186, 26, 24), (214, 56, 18)])
     + ''.join(f'<path d="M{x + 5},{y + 8} L{x + 5},{y + 30}" stroke-width="1.2" opacity=".5"/>' for x, y, w in [(20, 50, 22), (46, 34, 18), (160, 44, 20), (186, 26, 24)])
     + bottom('M3,100 Q120,86 237,100', '#9bc98e')
     + canopy(46, 120, 1.4, (RED, ORANGE, RED)) + canopy(120, 104, 1.6, (GOLD, ORANGE, GOLD)) + canopy(196, 122, 1.4, (ORANGE, RED, GOLD))
     + face(120, 70, .8)
     + f'<path d="M84,150 L130,146 L136,166 L88,170 Z" fill="{PINK}"/>'
     + ''.join(f'<path d="M{86 + 10*i},{151 - .9*i} L{90 + 10*i},{169 - .9*i}" stroke-width="1" opacity=".5"/>' for i in range(5))
     + person(100, 136, SKY, .7) + person(120, 134, GOLD, .7)
     + sparkle(80, 24) + sparkle(140, 30))


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ta-' + name, 120, 120, label, inner, bg='#fff3c4')


# 六義園網路前售票：要給工作人員操作手機畫面，截圖、列印都不行
qr = ''.join(f'<rect x="{30 + 6*i}" y="{40 + 6*j}" width="5" height="5" fill="{INK}" stroke="none"/>'
             for i in range(5) for j in range(5) if (i * 7 + j * 3) % 4 != 0)
rem('r-screen', '手繪提醒：手機畫面才算數，紙本列印打叉',
    f'<rect x="20" y="18" width="50" height="86" rx="8" fill="{NAVY}"/><rect x="25" y="28" width="40" height="64" rx="3" fill="{WHITE}"/>'
    + qr
    + f'<path d="M30,82 l6,6 l12,-14" stroke="{GREEN}" stroke-width="3" fill="none"/>'
    + f'<rect x="78" y="40" width="30" height="38" rx="2" fill="{WHITE}" transform="rotate(8 93 59)"/>'
    + f'<path d="M80,46 L106,76 M106,46 L80,76" stroke="{RED}" stroke-width="4"/>')

# 進門和出門不是同一個門
gate = lambda x, col, arrow_in: (
    f'<path d="M{x},40 L{x + 44},40 L{x + 40},32 L{x + 4},32 Z" fill="{ROOF}"/>'
    f'<rect x="{x + 6}" y="40" width="6" height="50" fill="{DBROWN}"/><rect x="{x + 32}" y="40" width="6" height="50" fill="{DBROWN}"/>'
    + (f'<path d="M{x + 22},62 L{x + 22},96 M{x + 14},70 L{x + 22},62 L{x + 30},70" stroke="{col}" stroke-width="4" fill="none"/>' if arrow_in else
       f'<path d="M{x + 22},62 L{x + 22},96 M{x + 14},88 L{x + 22},96 L{x + 30},88" stroke="{col}" stroke-width="4" fill="none"/>'))
rem('r-gate', '手繪提醒：一個門只能進、另一個門只能出',
    gate(8, GREEN, True) + gate(66, RED, False))

# 昭和紀念公園夜間只能從兩個門進出，走到日本庭園很遠
rem('r-walk', '手繪提醒：從入口走到日本庭園有一段路',
    f'<path d="M16,100 L16,30" stroke-width="3"/><rect x="8" y="22" width="34" height="18" rx="3" fill="{GREEN}"/>'
    + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="6" fill="{BROWN}" stroke-width="1.2" transform="rotate(60 {x} {y})"/>'
              for x, y in [(34, 94), (46, 86), (58, 94), (70, 84), (82, 92)])
    + f'<path d="M86,62 L112,62 L106,52 L92,52 Z" fill="{ROOF}"/><rect x="90" y="62" width="18" height="16" fill="{WHITE}"/>'
    + f'<text x="52" y="58" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">1.6km</text>')

print(save(F, OUT), 'files')
