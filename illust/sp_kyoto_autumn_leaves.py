# 京都賞楓頁（/kyoto/autumn-leaves/）的「這些地方長這樣」插圖與提醒卡（2026-11-13）。
# 參考東福寺、圓光寺、嵯峨野觀光鐵道等官網的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/kyoto-autumn-leaves/*.svg（240×180、提醒小圖 120×120）。
# 說明文字放在 illust/spots/kyoto-autumn-leaves.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'kyoto-autumn-leaves')
W, H = 240, 180
ORANGE = '#f08a4b'
ROOF = '#7d6b66'
RIVER = '#8fc8e6'
NIGHT = '#2b3560'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ka-' + name, W, H, label, inner, bg=bg)


def full(col):
    return f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{col}"/>'


def bottom(path_top, col):
    # 從 path_top 畫到圓角框的底
    return f'<path d="{path_top} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


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
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x},{y} L{x},{y + r*.95:.1f}" stroke-width="1.3"/>'
            f'<polygon points="{p}" fill="{col}" stroke-width="1.3"/></g>')


def canopy(x, base, s=1.0, cols=(RED, ORANGE, GOLD), trunk=True):
    t = ''
    if trunk:
        t += f'<rect x="{x - 3*s:.1f}" y="{base - 16*s:.1f}" width="{6*s:.1f}" height="{16*s:.1f}" rx="2" fill="{DBROWN}"/>'
    for i, (dx, dy, r) in enumerate([(-11, -22, 11), (11, -22, 11), (0, -32, 12), (0, -20, 10)]):
        t += f'<circle cx="{x + dx*s:.1f}" cy="{base + dy*s:.1f}" r="{r*s:.1f}" fill="{cols[i % len(cols)]}" stroke-width="1.6"/>'
    return t


def head(x, y, col=PINK, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s:.1f}" fill="#f9d9c0"/>'
            f'<path d="M{x - 7*s:.1f},{y + 18*s:.1f} q0,{-11*s:.1f} {7*s:.1f},{-11*s:.1f} q{7*s:.1f},0 {7*s:.1f},{11*s:.1f} Z" fill="{col}"/>')


# 1. 東福寺 通天橋：有屋頂的木造橋廊，架在滿是楓葉的溪谷上
card('tsutenkyo', '手繪東福寺通天橋，有屋頂的木橋架在楓葉溪谷上',
     full(SKY)
     + f'<path d="M3,70 Q40,60 70,96 L3,120 Z" fill="#a9cf9a"/>'
     + f'<path d="M237,66 Q200,58 170,96 L237,120 Z" fill="#a9cf9a"/>'
     + ''.join(f'<path d="M{x},92 L{x},150" stroke-width="2.4"/>' for x in (54, 96, 138, 180))
     + f'<path d="M12,62 L32,44 L208,44 L228,62 Z" fill="{ROOF}"/>'
     + ''.join(f'<rect x="{x}" y="62" width="5" height="22" fill="{DBROWN}" stroke-width="1.4"/>' for x in range(20, 222, 22))
     + f'<rect x="14" y="80" width="212" height="6" rx="2" fill="{BROWN}"/>'
     + f'<rect x="12" y="86" width="216" height="6" rx="2" fill="{DBROWN}"/>'
     + canopy(30, 168, 1.1) + canopy(78, 172, 1.2, (ORANGE, RED, GOLD)) + canopy(126, 170, 1.15, (GOLD, ORANGE, RED))
     + canopy(172, 172, 1.2, (RED, GOLD, ORANGE)) + canopy(214, 168, 1.05, (ORANGE, RED, RED))
     + face(126, 140, .8)
     + maple(200, 26, 8, GOLD, 15) + maple(36, 26, 7, RED, -20) + sparkle(120, 24))

# 2. 圓光寺：從屋裡看出去的楓葉庭園，旁邊是預約月曆
card('enkouji', '手繪從寺院屋裡看出去的楓葉庭園，旁邊有預約月曆',
     full(CREAM)
     + f'<rect x="22" y="20" width="196" height="104" fill="{SKY}"/>'
     + f'<path d="M22,104 Q90,92 218,100 L218,124 L22,124 Z" fill="#9bc98e"/>'
     + canopy(60, 108, 1.15, (RED, ORANGE, RED)) + canopy(120, 104, 1.3, (ORANGE, GOLD, RED)) + canopy(180, 108, 1.1, (RED, RED, GOLD))
     + face(120, 76, .8)
     + f'<rect x="14" y="14" width="10" height="120" fill="{DBROWN}"/><rect x="216" y="14" width="10" height="120" fill="{DBROWN}"/>'
     + f'<rect x="14" y="12" width="212" height="10" fill="{DBROWN}"/>'
     + f'<path d="M3,134 L237,134 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e6e2a8"/>'
     + ''.join(f'<path d="M{x},134 L{x - 14},177" stroke-width="1.4" opacity=".6"/>' for x in (70, 130, 190))
     + f'<rect x="168" y="120" width="52" height="44" rx="5" fill="{WHITE}"/>'
     + f'<rect x="168" y="120" width="52" height="12" rx="5" fill="{RED}"/>'
     + ''.join(f'<circle cx="{176 + 9*i}" cy="{142 + 10*j}" r="2" fill="{GRAY}" stroke="none"/>' for i in range(5) for j in range(2))
     + f'<path d="M193,146 l5,5 l10,-12" stroke="{GREEN}" stroke-width="3" fill="none"/>'
     + maple(40, 150, 7, RED, 25) + maple(140, 156, 6, ORANGE, -30))

# 3. 嵐山小火車：沒有玻璃窗的 5 號車「Rich 號」
car = lambda x, open_: (
    f'<rect x="{x}" y="88" width="76" height="40" rx="6" fill="{"#f3e3c3" if open_ else BRICK}"/>'
    f'<path d="M{x - 4},90 Q{x + 38},76 {x + 80},90 Z" fill="{DBROWN}"/>'
    + (''.join(f'<rect x="{x + 6 + 23*i}" y="96" width="18" height="14" rx="2" fill="{SKY}"/>' for i in range(3)) if not open_ else
       f'<path d="M{x + 4},96 L{x + 72},96" stroke-width="1.6"/>'
       + head(x + 16, 104, PINK, .7) + head(x + 38, 104, SKY, .7) + head(x + 60, 104, GREEN, .7)
       + f'<path d="M{x + 66},96 l6,-8 M{x + 8},98 l-6,-6" stroke-width="1.6"/>')
    + f'<circle cx="{x + 16}" cy="130" r="5" fill="{INK}"/><circle cx="{x + 60}" cy="130" r="5" fill="{INK}"/>')
card('torokko', '手繪嵐山小火車，後面那節是沒有玻璃窗的開放車廂',
     full(SKY)
     + f'<path d="M3,96 Q50,40 110,74 Q160,36 237,80 L237,120 L3,120 Z" fill="#a9cf9a"/>'
     + canopy(36, 96, .9) + canopy(130, 86, .9, (ORANGE, GOLD, RED)) + canopy(206, 92, .9, (RED, RED, GOLD))
     + bottom('M3,136 L237,136', RIVER)
     + f'<path d="M3,135 L237,135" stroke-width="3"/>'
     + car(28, False) + f'<path d="M104,112 L118,112" stroke-width="2.4"/>' + car(118, True)
     + f'<circle cx="182" cy="122" r="8" fill="{GOLD}"/><text x="182" y="126.5" font-size="12" font-weight="bold" '
       f'text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">5</text>'
     + maple(60, 30, 7, RED, 10) + maple(176, 26, 6, GOLD, -20) + sparkle(112, 22)
     + f'<path d="M20,156 q10,-4 20,0 M90,162 q10,-4 20,0 M170,156 q10,-4 20,0" stroke="{WHITE}" stroke-width="2" fill="none"/>')

# 4. 保津川遊船：平底木船，船夫撐著長竿
card('hozugawa', '手繪保津川遊船，平底木船上有乘客和撐竿的船夫',
     full(SKY)
     + f'<path d="M3,70 Q60,28 120,64 Q180,30 237,62 L237,110 L3,110 Z" fill="#a9cf9a"/>'
     + canopy(30, 92, .9, (RED, ORANGE, RED)) + canopy(88, 86, .9, (GOLD, RED, ORANGE)) + canopy(160, 84, .9) + canopy(214, 90, .9, (ORANGE, RED, GOLD))
     + bottom('M3,104 q20,-6 40,0 t40,0 t40,0 t40,0 t40,0 t34,0', RIVER)
     + f'<ellipse cx="200" cy="112" rx="16" ry="7" fill="{GRAY}"/>'
     + head(76, 116, PINK, .8) + head(100, 116, SKY, .8) + head(124, 116, GOLD, .8) + head(148, 116, GREEN, .8)
     + f'<path d="M30,128 L196,128 L180,146 L46,146 Z" fill="{BROWN}"/>'
     + f'<path d="M36,134 L190,134" stroke-width="1.4" opacity=".6"/>'
     # 船夫
     + f'<circle cx="52" cy="96" r="7" fill="#f9d9c0"/><path d="M42,92 Q52,82 62,92 Z" fill="{GOLD}"/>'
     + f'<path d="M44,128 L46,106 Q52,100 58,106 L60,128 Z" fill="{NAVY}"/>'
     + f'<path d="M28,74 L70,166" stroke="{DBROWN}" stroke-width="3"/>'
     + f'<path d="M58,110 L44,104" stroke-width="2"/>'
     + f'<path d="M80,160 q10,-4 20,0 M150,164 q10,-4 20,0 M200,154 q8,-3 16,0" stroke="{WHITE}" stroke-width="2" fill="none"/>'
     + maple(120, 26, 7, RED, 0) + sparkle(186, 28))

# 5. 叡山電車 楓葉隧道：晚上點燈的楓樹拱成一條隧道，電車從中間開過
leaves = ''
for i in range(13):
    a = math.pi * i / 12
    x = 120 - 104 * math.cos(a)
    y = 150 - 118 * math.sin(a)
    leaves += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="{[RED, ORANGE, GOLD][i % 3]}" stroke-width="1.6"/>'
card('eizan', '手繪叡山電車開進點燈的楓葉隧道',
     full(NIGHT)
     + f'<ellipse cx="120" cy="120" rx="96" ry="70" fill="{GOLD}" opacity=".18" stroke="none"/>'
     + leaves
     + bottom('M3,150 L237,150', '#3d3a52')
     + f'<path d="M20,152 L220,152" stroke="{GRAY}" stroke-width="2"/>'
     + f'<rect x="64" y="96" width="112" height="50" rx="10" fill="{BRICK}"/>'
     + f'<rect x="64" y="96" width="112" height="10" rx="5" fill="{WHITE}"/>'
     + ''.join(f'<rect x="{72 + 26*i}" y="112" width="20" height="16" rx="3" fill="#ffe9a8"/>' for i in range(4))
     + f'<circle cx="84" cy="148" r="5" fill="{INK}"/><circle cx="156" cy="148" r="5" fill="{INK}"/>'
     + face(120, 136, .7)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(110, 40), (130, 56), (100, 70), (140, 30)]),
     bg=NIGHT)

# 6. 清水寺 夜間：木頭架高的舞台，四周的楓葉打了燈
grid = ''.join(f'<path d="M{x},100 L{x},150" stroke-width="2"/>' for x in range(70, 186, 14))
grid += ''.join(f'<path d="M66,{y} L182,{y}" stroke-width="1.6"/>' for y in (114, 130))
card('kiyomizu', '手繪清水寺的木造舞台，晚上四周的楓葉打了燈',
     full(NIGHT)
     + f'<circle cx="200" cy="34" r="12" fill="#fff3c4"/>'
     + bottom('M3,150 Q80,140 120,150 T237,146', '#3d3a52')
     + grid
     + f'<rect x="60" y="92" width="128" height="10" fill="{BROWN}"/>'
     + f'<rect x="78" y="64" width="92" height="28" fill="{BRICK}"/>'
     + ''.join(f'<path d="M{x},64 L{x},92" stroke-width="1.4"/>' for x in (100, 124, 148))
     + f'<path d="M58,66 Q124,44 190,66 L174,50 L74,50 Z" fill="{ROOF}"/>'
     + canopy(30, 150, 1.1, (RED, ORANGE, GOLD)) + canopy(214, 150, 1.1, (ORANGE, RED, GOLD))
     + canopy(40, 104, .8, (GOLD, RED, ORANGE), False) + canopy(206, 104, .8, (RED, GOLD, ORANGE), False)
     + face(124, 80, .7)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(40, 30), (90, 22), (150, 30), (226, 60)]),
     bg=NIGHT)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ka-' + name, 120, 120, label, inner, bg='#fff3c4')


# 東福寺：通天橋上可能不讓拍照、出去不能再進來
rem('r-nophoto', '手繪提醒：橋上請不要停下來拍照',
    f'<rect x="28" y="44" width="64" height="42" rx="8" fill="{GRAY}"/>'
    f'<rect x="46" y="36" width="22" height="10" rx="3" fill="{GRAY}"/>'
    f'<circle cx="60" cy="65" r="13" fill="{WHITE}"/><circle cx="60" cy="65" r="6" fill="{NAVY}"/>'
    f'<circle cx="60" cy="62" r="40" fill="none" stroke="{RED}" stroke-width="5"/>'
    f'<path d="M32,34 L88,90" stroke="{RED}" stroke-width="5"/>')

# 永観堂白天晚上分開收票、高台寺一張到底
rem('r-ticket', '手繪提醒：白天票和晚上票是兩張',
    f'<rect x="12" y="22" width="56" height="34" rx="5" fill="{WHITE}" transform="rotate(-8 40 39)"/>'
    f'<circle cx="38" cy="40" r="8" fill="{GOLD}"/>'
    + ''.join(f'<path d="M{38 + 12*math.cos(a):.1f},{40 + 12*math.sin(a):.1f} L{38 + 15*math.cos(a):.1f},{40 + 15*math.sin(a):.1f}" stroke="{GOLD}" stroke-width="2"/>'
              for a in [i * math.pi / 4 for i in range(8)])
    + f'<rect x="52" y="64" width="56" height="34" rx="5" fill="{NAVY}" transform="rotate(6 80 81)"/>'
    f'<path d="M84,72 a10,10 0 1,0 8,16 a8,8 0 1,1 -8,-16 Z" fill="#fff3c4"/>'
    + star(66, 76, 4, WHITE))

print(save(F, OUT), 'files')
