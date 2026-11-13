# 全國紅葉見頃頁（/japan-autumn-leaves/）的「各地楓紅長這樣」插圖與提醒卡（2026-11-13）。
# 各地景色參考嵐山、高尾山、香嵐渓、富士河口湖紅葉祭、黑部峽谷鐵道官網的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/japan-autumn-leaves/*.svg（240×180、提醒小圖 120×120）。
# 說明文字放在 illust/spots/japan-autumn-leaves.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-autumn-leaves')
W, H = 240, 180
ORANGE = '#f08a4b'
RIVER = '#8fc8e6'
NIGHT = '#2b3560'
VERMIL = '#e0533f'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ja-' + name, W, H, label, inner, bg=bg)


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


def maple(x, y, r=8, col=RED, rot=0):
    tips = [(-90, 1), (-30, .92), (25, .6), (155, .6), (210, .92)]
    seq = []
    for i, (a, rr) in enumerate(tips):
        seq.append((a, rr))
        na = tips[(i + 1) % len(tips)][0]
        if na < a:
            na += 360
        seq.append(((a + na) / 2, .28 if a == 25 else .4))
    p = ' '.join(f'{x + r*rr*math.cos(math.radians(a)):.1f},{y + r*rr*math.sin(math.radians(a)):.1f}' for a, rr in seq)
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x},{y} L{x},{y + r*.95:.1f}" stroke-width="1.4"/>'
            f'<polygon points="{p}" fill="{col}" stroke-width="1.4"/></g>')


def maple_big(x, y, r=40, col=RED, rot=0):
    # 雞爪槭：5 片細長的尖裂片，兩側各有小鋸齒，加兩片小的
    tips = [(-90, 1), (-38, .95), (12, .72), (90, .0), (168, .72), (218, .95)]
    pts = []
    for a, L in tips:
        if L == 0:
            pts.append((a, .18))
            continue
        pts += [(a - 22, .3), (a - 11, .66 * L), (a - 8, .6 * L), (a - 5, .86 * L), (a, L), (a + 5, .86 * L), (a + 8, .6 * L), (a + 11, .66 * L), (a + 22, .3)]
    p = ' '.join(f'{x + r*rr*math.cos(math.radians(a)):.1f},{y + r*rr*math.sin(math.radians(a)):.1f}' for a, rr in pts)
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x},{y} L{x},{y + r*.85:.1f}" stroke-width="2"/>'
            f'<polygon points="{p}" fill="{col}" stroke-width="2"/></g>')


def ginkgo(x, y, r=8, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x},{y} L{x},{y + r*.9:.1f}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} L{x - r},{y - r*.8:.1f} Q{x - r*.5:.1f},{y - r*1.25:.1f} {x - r*.1:.1f},{y - r*.95:.1f} L{x},{y - r*.72:.1f} '
            f'L{x + r*.1:.1f},{y - r*.95:.1f} Q{x + r*.5:.1f},{y - r*1.25:.1f} {x + r},{y - r*.8:.1f} Z" fill="{GOLD}" stroke-width="1.4"/></g>')


def dots(cols, pts, r=9):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cols[i % len(cols)]}" stroke-width="1.4"/>' for i, (x, y) in enumerate(pts))


def head(x, y, col=PINK, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s:.1f}" fill="#f9d9c0"/>'
            f'<path d="M{x - 7*s:.1f},{y + 18*s:.1f} q0,{-11*s:.1f} {7*s:.1f},{-11*s:.1f} q{7*s:.1f},0 {7*s:.1f},{11*s:.1f} Z" fill="{col}"/>')


# 1. 京都嵐山：長長的木橋橫過河，後面的山染紅
card('arashiyama', '手繪京都嵐山，長長的木橋橫過河，後面的山染成紅色',
     full(SKY)
     + f'<path d="M3,96 Q40,34 100,60 Q150,22 237,58 L237,110 L3,110 Z" fill="#a9cf9a"/>'
     + dots((RED, ORANGE, GOLD, RED), [(30, 80), (56, 64), (84, 74), (120, 54), (150, 46), (176, 62), (206, 52), (224, 76), (104, 90), (160, 86), (60, 96), (196, 92)], 11)
     + face(150, 46, .7)
     + bottom('M3,106 L237,106', RIVER)
     + ''.join(f'<path d="M{x},118 L{x},146" stroke="{DBROWN}" stroke-width="3"/>' for x in range(22, 224, 20))
     + f'<rect x="10" y="110" width="220" height="9" rx="2" fill="{BROWN}"/>'
     + f'<path d="M10,110 L230,110" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},103 L{x},110" stroke-width="1.6"/>' for x in range(14, 230, 12))
     + f'<path d="M10,103 L230,103" stroke-width="1.6"/>'
     + head(70, 92, PINK, .7) + head(170, 92, SKY, .7)
     + f'<path d="M30,160 q10,-4 20,0 M110,166 q10,-4 20,0 M180,158 q10,-4 20,0" stroke="{WHITE}" stroke-width="2" fill="none"/>'
     + maple(200, 24, 7, RED, 15) + sparkle(40, 26))

# 2. 東京高尾山：楓紅的山和登山步道
card('takao', '手繪東京高尾山，紅葉的山坡上有登山步道和爬山的人',
     full(SKY)
     + f'<path d="M3,150 Q70,40 130,30 Q190,40 237,110 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#a9cf9a"/>'
     + dots((RED, GOLD, ORANGE), [(70, 80), (96, 58), (130, 46), (160, 56), (186, 76), (210, 100), (50, 110), (110, 92), (150, 96), (40, 140), (200, 140)], 12)
     + f'<path d="M60,176 Q90,140 130,130 Q170,118 150,92 Q132,70 130,40" fill="none" stroke="#e9dcc8" stroke-width="6"/>'
     + f'<path d="M60,176 Q90,140 130,130 Q170,118 150,92 Q132,70 130,40" fill="none" stroke-width="1.2" stroke-dasharray="3 6"/>'
     + f'<circle cx="104" cy="134" r="6" fill="#f9d9c0"/><path d="M97,156 q0,-14 7,-14 q7,0 7,14 Z" fill="{RED}"/>'
     + f'<rect x="108" y="140" width="8" height="12" rx="3" fill="{GOLD}"/>'
     + f'<path d="M96,148 L90,162" stroke="{DBROWN}" stroke-width="2"/>'
     + face(130, 46, .7) + sparkle(200, 28) + sparkle(36, 40))

# 3. 愛知香嵐渓：紅色的拱橋與楓紅的溪谷
card('korankei', '手繪愛知香嵐渓，紅色拱橋跨過溪流，兩岸都是紅葉',
     full(SKY)
     + f'<path d="M3,40 Q50,30 90,70 L90,120 L3,120 Z" fill="#a9cf9a"/><path d="M237,40 Q190,30 150,70 L150,120 L237,120 Z" fill="#a9cf9a"/>'
     + canopy(26, 70, 1.0) + canopy(64, 90, 1.0, (ORANGE, RED, GOLD)) + canopy(214, 70, 1.0, (RED, GOLD, ORANGE)) + canopy(176, 90, 1.0, (GOLD, RED, ORANGE))
     + bottom('M3,120 Q120,108 237,120', RIVER)
     + f'<path d="M30,122 Q120,66 210,122 L210,130 Q120,76 30,130 Z" fill="{VERMIL}"/>'
     + f'<path d="M36,112 Q120,58 204,112" fill="none" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},{y1} L{x},{y1 + 9}" stroke-width="1.6"/>' for x, y1 in [(50, 98), (70, 87), (95, 79), (120, 76), (145, 79), (170, 87), (190, 98)])
     + face(120, 92, .7)
     + f'<ellipse cx="80" cy="150" rx="14" ry="6" fill="{GRAY}"/><ellipse cx="170" cy="156" rx="12" ry="5" fill="{GRAY}"/>'
     + maple(110, 140, 7, RED, 20) + maple(140, 162, 6, GOLD, -10) + sparkle(120, 26))

# 4. 雞爪槭和銀杏：tenki.jp 只預測雞爪槭
card('leaves', '手繪一片紅色的雞爪槭葉子和一片黃色的銀杏葉',
     full(CREAM)
     + f'<circle cx="74" cy="84" r="54" fill="#fde3dc"/>'
     + f'<circle cx="170" cy="84" r="54" fill="#fdf0c8"/>'
     + maple_big(74, 90, 42, RED, -8)
     + face(74, 76, .9)
     + ginkgo(170, 112, 44, 6)
     + face(170, 84, .9)
     + f'<path d="M60,156 l8,8 l16,-18" stroke="{GREEN}" stroke-width="4" fill="none"/>'
     + f'<text x="170" y="164" font-size="22" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">?</text>'
     + sparkle(120, 30) + sparkle(222, 30))

# 5. 河口湖紅葉迴廊：晚上點燈的楓葉隧道，遠處是富士山
card('kawaguchiko', '手繪河口湖紅葉迴廊晚上點燈，遠處是富士山',
     full(NIGHT)
     + f'<path d="M60,90 L104,40 Q120,32 136,40 L180,90 Z" fill="#7d8bb8"/>'
     + f'<path d="M104,40 Q120,32 136,40 L148,54 Q140,50 132,56 Q124,48 116,56 Q106,50 94,54 Z" fill="{WHITE}"/>'
     + bottom('M3,96 L237,96', '#3d3a52')
     + f'<path d="M96,177 L112,96 L128,96 L144,177 Z" fill="#6b5f6e"/>'
     + canopy(30, 168, 1.6, (RED, ORANGE, RED)) + canopy(76, 130, 1.1, (GOLD, RED, ORANGE)) + canopy(98, 108, .7, (RED, GOLD, RED))
     + canopy(210, 168, 1.6, (ORANGE, RED, GOLD)) + canopy(164, 130, 1.1, (RED, ORANGE, RED)) + canopy(142, 108, .7, (GOLD, RED, ORANGE))
     + face(30, 130, .8)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(30, 30), (70, 22), (190, 26), (220, 50)]),
     bg=NIGHT)

# 6. 富山黑部峽谷：小火車過紅色鐵橋，下面是深谷
card('kurobe', '手繪黑部峽谷的小火車開過紅色鐵橋，下面是很深的溪谷',
     full(SKY)
     + f'<path d="M3,30 Q30,40 60,96 L70,177 L3,177 Z" fill="#a9cf9a"/><path d="M237,30 Q210,40 180,96 L170,177 L237,177 Z" fill="#a9cf9a"/>'
     + dots((RED, ORANGE, GOLD), [(14, 54), (30, 76), (44, 104), (22, 120), (50, 140), (226, 54), (210, 76), (196, 104), (218, 122), (190, 142)], 10)
     + bottom('M60,160 Q120,150 180,160', RIVER)
     + f'<rect x="20" y="92" width="200" height="8" fill="{VERMIL}"/>'
     + ''.join(f'<path d="M{x},100 L{x + 20},124 L{x + 40},100" fill="none" stroke="{VERMIL}" stroke-width="3"/>' for x in range(60, 180, 40))
     + f'<path d="M60,124 L180,124" stroke="{VERMIL}" stroke-width="3"/>'
     + f'<rect x="40" y="64" width="34" height="26" rx="4" fill="{GOLD}"/><rect x="46" y="70" width="10" height="8" fill="{SKY}"/>'
     + ''.join(f'<rect x="{x}" y="70" width="34" height="20" rx="3" fill="{c}"/><path d="M{x - 2},70 L{x + 36},70" stroke-width="3"/>'
               + f'<circle cx="{x + 10}" cy="76" r="4" fill="#f9d9c0"/><circle cx="{x + 24}" cy="76" r="4" fill="#f9d9c0"/>'
               for x, c in [(78, BRICK), (116, GREEN), (154, BRICK)])
     + ''.join(f'<circle cx="{x}" cy="91" r="3.4" fill="{INK}"/>' for x in (48, 66, 86, 104, 124, 142, 162, 180))
     + face(57, 82, .6, blush=False)
     + sparkle(120, 30) + maple(160, 28, 7, RED, 10))


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ja-' + name, 120, 120, label, inner, bg='#fff3c4')


# 「11月13日～」是起點，不是只有那一天
rem('r-tilde', '手繪提醒：月曆上從某一天開始往後延伸的箭頭',
    f'<rect x="14" y="20" width="92" height="80" rx="6" fill="{WHITE}"/><rect x="14" y="20" width="92" height="16" rx="6" fill="{RED}"/>'
    + ''.join(f'<circle cx="{26 + 17*i}" cy="{50 + 14*j}" r="2.4" fill="{GRAY}" stroke="none"/>' for i in range(5) for j in range(4))
    + f'<circle cx="43" cy="64" r="7" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    + f'<path d="M50,64 L98,64 M90,57 L98,64 L90,71" stroke="{GREEN}" stroke-width="3.4" fill="none"/>'
    + f'<path d="M26,78 L100,78" stroke="{GOLD}" stroke-width="3.4" stroke-dasharray="6 5"/>')

# 河口湖第一停車場收費，只收無現金付款
rem('r-parking', '手繪提醒：停車場只收卡片或手機付款，現金打叉',
    f'<rect x="12" y="14" width="30" height="30" rx="5" fill="{NAVY}"/>'
    f'<text x="27" y="37" font-size="22" font-weight="bold" text-anchor="middle" fill="{WHITE}" stroke="none" font-family="sans-serif">P</text>'
    f'<rect x="52" y="20" width="56" height="36" rx="5" fill="{SKY}"/><rect x="52" y="28" width="56" height="7" fill="{INK}" stroke="none"/>'
    f'<rect x="58" y="42" width="12" height="8" rx="2" fill="{GOLD}" stroke-width="1.2"/>'
    f'<circle cx="38" cy="84" r="18" fill="{GOLD}"/><circle cx="38" cy="84" r="10" fill="none" stroke-width="1.6"/>'
    f'<path d="M22,68 L54,100 M54,68 L22,100" stroke="{RED}" stroke-width="4"/>'
    f'<rect x="72" y="66" width="28" height="44" rx="5" fill="{NAVY}"/><rect x="76" y="72" width="20" height="30" rx="2" fill="{WHITE}"/>'
    f'<path d="M80,88 l4,4 l8,-10" stroke="{GREEN}" stroke-width="2.6" fill="none"/>')

# 黑部欅平站周邊在施工，只能待在車站和遊客中心
rem('r-kurobe', '手繪提醒：車站外面在施工，只能待在車站附近',
    f'<rect x="12" y="24" width="56" height="44" rx="4" fill="{WHITE}"/><path d="M8,26 L40,8 L72,26 Z" fill="{BRICK}"/>'
    f'<rect x="32" y="44" width="16" height="24" fill="{BROWN}"/>'
    + ''.join(f'<path d="M{x},96 L{x + 8},72 L{x + 16},96 Z" fill="{ORANGE}"/><path d="M{x + 3},88 L{x + 13},88" stroke="{WHITE}" stroke-width="2.4"/>'
              for x in (10, 36, 62))
    + f'<rect x="8" y="96" width="76" height="6" rx="2" fill="{GOLD}"/>'
    + f'<circle cx="96" cy="44" r="16" fill="{WHITE}"/><path d="M96,44 L96,33 M96,44 L104,48" stroke-width="2.4"/>')

print(save(F, OUT), 'files')
