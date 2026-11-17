# 函館山纜車頁的「函館山上看得到什麼」插圖與提醒卡（2026-11-17）。
# 纜車、夜景、漁火公園、山頂餐廳、冬天封閉的登山道路、十字街各畫一張可愛版的景色，不描照片構圖；
# 纜車只畫沒有標誌的紅白色車廂，市電畫成沒有塗裝標誌的路面電車，不畫纜車公司、餐廳的商標或任何角色。
# 夜景的市街參考從函館山往下看「兩邊是海、中間變窄」的形狀，簡化成沙漏形。
# 輸出 illust/sp/hakodate-ropeway/*.svg（240×180 圖卡、120×120 提醒小圖）。說明文字放在 illust/spots/hakodate-ropeway.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'hakodate-ropeway')
W, H = 240, 180
F = {}
SKYW = '#e3f1f8'
SNOWSKY = '#e4eefa'
NSEA = '#2b3866'
NFAR = '#232b4f'
NLAND = '#3d4a7c'
DUSK = '#5a5f9a'
GLOW = '#f2a07a'
LITE = [GOLD, '#ffd98a', '#ffb066', WHITE]
WARMWIN = '#ffe7a8'
HILL = '#3f6b58'
ROAD = '#c9cfd8'
SLOPE = '#eadcc4'
WALL = '#f6e4c8'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'
BG = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('hr-' + name, W, H, label, inner, bg=bg)


def isthmus(cx, y0, y1, ym, w0, wm, w1, n, seed=7, lean=.25, r=1.0, fill=NLAND):
    # 沙漏形的市街：上面（遠處）寬、中間窄、下面（近處）再變寬，裡面撒一顆顆暖色小燈
    k0 = (w0 - wm) / (ym - y0) ** 2
    k1 = (w1 - wm) / (y1 - ym) ** 2

    def at(y):
        return cx + (y - ym) * lean, wm + (y - ym) ** 2 * (k0 if y < ym else k1)
    ys = [y0 + (y1 - y0) * i / 12 for i in range(13)]
    left = [(at(y)[0] - at(y)[1], y) for y in ys]
    right = [(at(y)[0] + at(y)[1], y) for y in reversed(ys)]
    t = ('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in left + right)
         + f' Z" fill="{fill}" stroke-width="1.8"/>')
    span = max(w0, w1) + abs(lean) * (y1 - y0)
    s, k, tries = seed, 0, 0
    while k < n and tries < n * 40:
        tries += 1
        s = (s * 1103515245 + 12345) % 2147483648
        x = cx - span + (s % 10000) / 10000 * span * 2
        s = (s * 1103515245 + 12345) % 2147483648
        y = y0 + 1.5 + (s % 10000) / 10000 * (y1 - y0 - 3)
        c, hw = at(y)
        if abs(x - c) > hw - 2.4:
            continue
        t += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + (k % 3) * .25 * r:.2f}" fill="{LITE[k % 4]}" stroke="none"/>'
        k += 1
    return t


def gondola(x, y, s=1.0, ang=0, people=False, win=WARMWIN, smile=True):
    # 沒有標誌的紅白色纜車車廂；(x, y) 是吊架掛在纜線上的那一點
    t = (f'<g transform="translate({x} {y}) scale({s})" stroke-width="{2.4/s:.2f}">'
         f'<g transform="rotate({ang})"><rect x="-12" y="-5" width="24" height="7" rx="3" fill="{GRAY}"/>'
         f'<circle cx="-7" cy="-3" r="2.6" fill="{WHITE}" stroke-width="1.2"/>'
         f'<circle cx="7" cy="-3" r="2.6" fill="{WHITE}" stroke-width="1.2"/></g>'
         f'<path d="M0,2 L0,13 M-6,13 L6,13"/>'
         f'<rect x="-23" y="13" width="46" height="42" rx="10" fill="{WHITE}"/>'
         f'<path d="M-23,25 L-23,23 Q-23,13 -13,13 L13,13 Q23,13 23,23 L23,25 Z" fill="{RED}"/>'
         f'<path d="M-23,47 L23,47 Q23,55 13,55 L-13,55 Q-23,55 -23,47 Z" fill="{RED}"/>'
         + ''.join(f'<rect x="{wx}" y="28" width="11" height="9" rx="2.4" fill="{win}" stroke-width="1.4"/>'
                   for wx in (-18, -5.5, 7)))
    if people:
        t += ''.join(f'<circle cx="{hx}" cy="35" r="2.4" fill="#f9d9c0" stroke-width="1"/>'
                     for hx in (-15.5, -10.5, -3, 2, 9.5, 14.5))
    if smile:
        t += face(0, 41, .62)
    return t + '</g>'


def person(x, y, col=RED, s=1.0, hair=None):
    # 背對我們的人（頭＋身體），hair 給了就畫頭髮
    return (f'<path d="M{x-8*s},{y+24*s} q0,{-15*s} {8*s},{-15*s} q{8*s},0 {8*s},{15*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="{hair or "#f9d9c0"}"/>')


def walker(x, y, col=RED, s=1.0):
    # 側面走路的人
    return (f'<path d="M{x-3*s},{y+18*s} L{x-7*s},{y+28*s} M{x+3*s},{y+18*s} L{x+7*s},{y+27*s}" stroke-width="{2.6*s}"/>'
            f'<path d="M{x-7*s},{y+19*s} Q{x-7*s},{y+6*s} {x},{y+6*s} Q{x+7*s},{y+6*s} {x+7*s},{y+19*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<circle cx="{x+2.4*s}" cy="{y-.5*s}" r="{1.3*s}" fill="{INK}" stroke="none"/>')


def stars(pts):
    return ''.join(star(x, y, r) for x, y, r in pts)


def tram(x, y, s=1.0, smile=True):
    # 沒有塗裝標誌的路面電車（側面），(x, y) 是車身左上角
    t = (f'<g transform="translate({x} {y}) scale({s})" stroke-width="{2.4/s:.2f}">'
         f'<path d="M30,0 L22,-12 L46,-12 L38,0 M22,-12 L46,-12" fill="none" stroke-width="2"/>'
         f'<rect x="0" y="0" width="84" height="34" rx="9" fill="{CREAM}"/>'
         f'<path d="M0,22 L84,22 L84,25 Q84,34 75,34 L9,34 Q0,34 0,25 Z" fill="{GREEN}"/>'
         + ''.join(f'<rect x="{wx}" y="6" width="12" height="11" rx="2.4" fill="{SKY}" stroke-width="1.4"/>'
                   for wx in (8, 24, 40, 56))
         + f'<rect x="71" y="6" width="8" height="22" rx="2" fill="{SKY}" stroke-width="1.4"/>'
         f'<circle cx="18" cy="37" r="5" fill="{INK}"/><circle cx="66" cy="37" r="5" fill="{INK}"/>')
    if smile:
        t += face(46, 27, .5, blush=False)
    return t + '</g>'


# 1. 纜車：一條沒有支柱的纜線從山腳拉到山頂，車廂坐滿人
c1 = BG
c1 += (f'<path d="M24,46 q-2,-12 10,-12 q4,-10 16,-6 q10,-6 16,4 q10,0 8,14 Z" fill="{WHITE}" stroke-width="1.8"/>'
       f'<path d="M100,30 q-1,-8 7,-8 q3,-7 11,-4 q7,-4 11,3 q7,0 5,9 Z" fill="{WHITE}" stroke-width="1.6"/>')
c1 += f'<path d="M3,150 Q60,140 100,104 Q150,54 196,38 Q222,30 237,42 {BOT}" fill="{GREEN}"/>'
c1 += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DGREEN}" stroke-width="1.6"/>'
              for x, y, r in [(150, 76, 8), (170, 66, 7), (214, 56, 8), (196, 86, 9), (226, 80, 7),
                              (136, 104, 8), (176, 110, 9), (214, 112, 8), (110, 132, 8), (160, 140, 9), (208, 146, 8)])
c1 += f'<path d="M3,158 Q120,148 237,160 {BOT}" fill="#cfe7c4"/>'
# 山頂站和山腳站（沒有招牌）
c1 += f'<rect x="184" y="20" width="40" height="22" rx="3" fill="{CREAM}"/>'
c1 += f'<path d="M180,22 L228,22" stroke-width="3.4"/>'
c1 += ''.join(f'<rect x="{x}" y="27" width="8" height="8" rx="1.6" fill="{SKY}" stroke-width="1.3"/>' for x in (198, 210))
c1 += f'<rect x="12" y="128" width="42" height="30" rx="3" fill="{CREAM}"/>'
c1 += f'<path d="M8,130 L58,130" stroke-width="3.4"/>'
c1 += ''.join(f'<rect x="{x}" y="136" width="8" height="8" rx="1.6" fill="{SKY}" stroke-width="1.3"/>' for x in (18, 30))
# 一條直直拉上去的纜線，中間沒有任何支柱
c1 += f'<path d="M52,136 L188,30" stroke="{INK}" stroke-width="1.8"/><path d="M52,141 L188,35" stroke="{INK}" stroke-width="1.3" opacity=".6"/>'
c1 += gondola(116, 86, .95, ang=-38, people=True, win=SKY)
c1 += f'<path d="M84,124 q-8,4 -16,2 M88,132 q-10,5 -20,3" fill="none" stroke="{WHITE}" stroke-width="2"/>'
c1 += sparkle(150, 18) + star(80, 22, 5) + sparkle(60, 70, 4)
card('gondola', '手繪一條中間沒有支柱的纜線從山腳直直拉到山頂，中間掛著一台坐滿人的紅白色纜車', c1)

# 2. 夜景：剛日落的天空、亮起燈的市街，展望台擠滿人
c2 = (f'<path d="M4.2,62 L235.8,62 L235.8,104 L4.2,104 Z" fill="{DUSK}" stroke="none"/>'
      f'<path d="M4.2,90 Q120,80 235.8,90 L235.8,104 L4.2,104 Z" fill="{GLOW}" stroke="none"/>')
c2 += stars([(30, 28, 4.6), (90, 18, 3.6), (176, 26, 4.6), (214, 46, 3.4)]) + sparkle(130, 34, 4) + sparkle(56, 52, 3)
c2 += f'<path d="M4.2,104 L235.8,104 L235.8,150 L4.2,150 Z" fill="{NSEA}" stroke="none"/>'
c2 += f'<path d="M4.2,106 Q50,94 100,100 Q160,92 235.8,102 L235.8,110 L4.2,110 Z" fill="{NFAR}" stroke-width="1.8"/>'
c2 += isthmus(120, 108, 150, 128, 72, 16, 58, 120, seed=3)
c2 += f'<path d="M18,128 q8,-3 16,0 M200,134 q8,-3 16,0" fill="none" stroke="#5b6ea6" stroke-width="1.4"/>'
# 展望台的欄杆與一整排看夜景的人（背影）
c2 += f'<path d="M3,150 L237,150 {BOT}" fill="#4a3f5e"/>'
c2 += f'<path d="M5,148 L235,148" stroke="{DBROWN}" stroke-width="4"/>'
_cols = [RED, GOLD, PINK, GREEN, '#6fa8dc', CREAM]
_hair = ['#6b4a36', INK, '#8a6a52']
for i, x in enumerate(range(26, 220, 17)):
    c2 += person(x, 158 + (i % 2) * 3, _cols[i % len(_cols)], .82, _hair[i % 3])
c2 += sparkle(120, 70, 4)
card('yakei', '手繪剛日落、天邊還有一點橘色的天空下，兩邊夾著海灣的市街亮起燈，前面的展望台擠滿看夜景的人',
     c2, bg=NAVY)

# 3. 漁火公園：從纜車站往左走，人比較少
c3 = stars([(24, 24, 4), (120, 20, 3.6), (200, 22, 4.4)]) + sparkle(160, 40, 3.4) + sparkle(70, 40, 3)
c3 += f'<path d="M108,20 a10,10 0 1,0 12,15 a7.5,7.5 0 1,1 -12,-15 Z" fill="{GOLD}" stroke-width="1.6"/>'
# 左邊遠處的海與市街燈光
c3 += f'<path d="M4.2,70 L235.8,70 L235.8,112 L4.2,112 Z" fill="{NSEA}" stroke="none"/>'
c3 += f'<path d="M4.2,72 Q40,64 80,68 Q130,62 180,70 Q210,66 235.8,70 L235.8,76 L4.2,76 Z" fill="{NFAR}" stroke-width="1.6"/>'
c3 += isthmus(80, 74, 112, 92, 46, 10, 40, 60, seed=21, lean=.2, r=.9)
# 山頂的草地與往左延伸的步道
c3 += f'<path d="M3,112 Q90,100 237,108 {BOT}" fill="{HILL}"/>'
c3 += f'<path d="M237,134 Q170,130 120,140 Q70,150 28,146 L30,158 Q80,162 128,152 Q180,142 237,150 Z" fill="#c9b99a" stroke-width="1.8"/>'
# 右邊的纜車山頂站（窗戶亮燈）與纜線
c3 += f'<path d="M237,30 L206,74" stroke="{GRAY}" stroke-width="1.6"/>'
c3 += f'<rect x="186" y="74" width="50" height="44" rx="3" fill="{CREAM}"/>'
c3 += f'<path d="M182,76 L237,76" stroke-width="3.4"/>'
c3 += ''.join(f'<rect x="{x}" y="84" width="10" height="10" rx="2" fill="{GOLD}" stroke-width="1.3"/>' for x in (194, 210))
c3 += f'<rect x="222" y="98" width="10" height="20" rx="2" fill="{DBROWN}" stroke-width="1.4"/>'
# 往左指的路牌（不寫字）
c3 += f'<path d="M160,140 L160,104" stroke="{DBROWN}" stroke-width="4"/>'
c3 += f'<path d="M136,104 L144,96 L176,96 L176,112 L144,112 Z" fill="{BROWN}"/>'
c3 += f'<path d="M150,104 L170,104" stroke="{CREAM}" stroke-width="2"/>'
# 左邊長椅上兩個人安靜看夜景
c3 += f'<path d="M36,144 L36,156 M88,144 L88,156" stroke="{DBROWN}" stroke-width="3"/>'
c3 += person(52, 124, '#6fa8dc', .9, '#6b4a36') + person(72, 125, PINK, .85, INK)
c3 += f'<rect x="28" y="138" width="68" height="7" rx="2" fill="{BROWN}"/>'
c3 += f'<path d="M62,112 q2,-6 6,-2 q4,-4 6,2" fill="none" stroke="{PINK}" stroke-width="1.6"/>'
card('isaribi', '手繪從纜車山頂站往左走的步道，路牌指向左邊，長椅上只有兩個人安靜看著遠處的夜景',
     c3, bg=NAVY)

# 4. 山頂餐廳：靠窗的餐桌擺好套餐，窗外是夜景
c4 = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{WALL}"/>'
c4 += f'<rect x="30" y="18" width="180" height="88" rx="8" fill="{NAVY}"/>'
c4 += f'<path d="M32,74 Q80,66 120,70 Q170,64 208,72 L208,104 L32,104 Z" fill="{NSEA}" stroke="none"/>'
c4 += isthmus(120, 72, 104, 86, 60, 12, 46, 70, seed=5, lean=.15, r=.9)
c4 += stars([(56, 32, 3.6), (180, 30, 4)]) + sparkle(120, 34, 3)
c4 += f'<path d="M120,18 L120,106 M30,62 L210,62" stroke-width="3"/>'
c4 += f'<rect x="30" y="18" width="180" height="88" rx="8" fill="none" stroke-width="3"/>'
# 兩側的窗簾
c4 += f'<path d="M22,14 Q40,14 42,20 Q30,60 40,110 Q28,114 20,110 Z" fill="{RED}"/>'
c4 += f'<path d="M218,14 Q200,14 198,20 Q210,60 200,110 Q212,114 220,110 Z" fill="{RED}"/>'
# 椅背、餐桌與一道道套餐
c4 += f'<path d="M20,150 L20,112 Q20,104 30,104 L36,104 L36,150" fill="{DBROWN}"/>'
c4 += f'<path d="M220,150 L220,112 Q220,104 210,104 L204,104 L204,150" fill="{DBROWN}"/>'
c4 += f'<path d="M64,140 L60,170 M176,140 L180,170" stroke="{DBROWN}" stroke-width="4"/>'
c4 += f'<path d="M40,124 L200,124 L206,142 L34,142 Z" fill="{WHITE}"/>'
c4 += f'<path d="M34,142 L206,142 L206,148 L34,148 Z" fill="{WHITE}" stroke-width="1.8"/>'
c4 += f'<ellipse cx="88" cy="128" rx="20" ry="6" fill="{CREAM}" stroke-width="1.8"/>'
c4 += f'<path d="M72,126 Q88,140 104,126 Z" fill="{GOLD}" stroke-width="1.8"/>'
c4 += face(88, 129, .38, blush=False)
c4 += f'<ellipse cx="142" cy="132" rx="24" ry="7" fill="{WHITE}" stroke-width="1.8"/>'
c4 += f'<path d="M130,130 Q142,120 154,130 Z" fill="{BRICK}" stroke-width="1.6"/>'
c4 += f'<circle cx="136" cy="132" r="3" fill="{GREEN}" stroke-width="1.2"/><circle cx="150" cy="132" r="3" fill="{GREEN}" stroke-width="1.2"/>'
c4 += f'<path d="M60,120 L60,134 M174,120 L174,134 M170,120 L170,126 Q170,130 174,130 Q178,130 178,126 L178,120" fill="none" stroke-width="1.6"/>'
c4 += f'<path d="M188,110 L196,110 L194,124 L190,124 Z M192,124 L192,132 M187,133 L197,133" fill="{SKY}" stroke-width="1.6"/>'
c4 += f'<rect x="114" y="112" width="8" height="14" rx="2" fill="{CREAM}" stroke-width="1.6"/>'
c4 += f'<path d="M118,112 q-3,-5 0,-9 q3,4 0,9 Z" fill="{GOLD}" stroke-width="1.2"/>'
c4 += f'<path d="M3,160 L237,160 {BOT}" fill="{BROWN}"/>'
card('genova', '手繪靠窗的餐桌擺好湯、主菜和刀叉的套餐，窗外是夜景的燈光', c4)

# 5. 冬天的山路：登山道路封閉，只有纜車上得去
c5 = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SNOWSKY}"/>'
c5 += snow([(20, 24), (52, 40), (96, 20), (140, 46), (180, 18), (222, 40), (70, 70), (200, 70), (30, 90)], 2.6, WHITE)
c5 += f'<path d="M3,132 Q60,96 110,70 Q160,44 200,40 Q224,40 237,50 {BOT}" fill="{WHITE}"/>'
c5 += f'<path d="M120,80 q20,-8 40,-6 M150,64 q16,-6 30,-4" fill="none" stroke="{GRAY}" stroke-width="1.6"/>'
c5 += ''.join((f'<path d="M{x},{b-h} L{x+w/2},{b} L{x-w/2},{b} Z" fill="{DGREEN}"/>'
               f'<path d="M{x-w*.18:.1f},{b-h*.64:.1f} L{x},{b-h} L{x+w*.18:.1f},{b-h*.64:.1f} Q{x},{b-h*.56:.1f} {x-w*.18:.1f},{b-h*.64:.1f} Z" fill="{WHITE}" stroke-width="1.4"/>')
              for x, b, h, w in [(186, 70, 26, 18), (210, 74, 24, 16), (40, 132, 28, 20), (210, 104, 26, 18)])
# 彎彎的山路與封閉的柵欄
_rd = 'M128,177 Q126,150 138,132 Q152,112 142,96 Q132,80 178,58'
c5 += f'<path d="{_rd}" fill="none" stroke="{ROAD}" stroke-width="20"/>'
c5 += f'<path d="{_rd}" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-dasharray="6 7"/>'
c5 += f'<path d="M106,138 L106,112 M172,134 L172,108" stroke="{INK}" stroke-width="4"/>'
c5 += f'<rect x="98" y="112" width="82" height="11" rx="3" fill="{WHITE}"/>'
c5 += ''.join(f'<path d="M{x},112 L{x+8},123 L{x+16},123 L{x+8},112 Z" fill="{RED}" stroke="none"/>' for x in (102, 120, 138, 156))
c5 += f'<rect x="98" y="112" width="82" height="11" rx="3" fill="none"/>'
c5 += f'<path d="M100,112 q6,-5 12,0 q8,-5 14,0 q8,-5 14,0 q8,-5 14,0 q8,-5 14,0 q6,-4 10,0" fill="{WHITE}" stroke-width="1.4"/>'
# 停在柵欄前的小車
c5 += f'<path d="M100,164 L100,154 Q100,146 108,146 L114,136 L138,136 L144,146 Q152,146 152,154 L152,164 Z" fill="#6fa8dc"/>'
c5 += f'<path d="M118,140 L136,140 L140,146 L114,146 Z" fill="{SKY}" stroke-width="1.4"/>'
c5 += f'<path d="M114,136 q12,-6 24,0" fill="{WHITE}" stroke-width="1.4"/>'
c5 += f'<circle cx="112" cy="166" r="6" fill="{INK}"/><circle cx="140" cy="166" r="6" fill="{INK}"/>'
c5 += face(126, 154, .5)
# 上面的纜車照樣往山頂開
c5 += f'<path d="M3,112 L237,28" stroke="{INK}" stroke-width="1.6"/>'
c5 += gondola(60, 91.4, .62, ang=-20, win=SKY)
c5 += sparkle(30, 60, 3.4)
card('road', '手繪下雪的彎彎山路被紅白柵欄擋住，小車停在柵欄前，上面的纜車照樣往山頂開', c5, bg=SNOWSKY)

# 6. 十字街：市電到站，沿坡道走上纜車站
c6 = BG
c6 += f'<path d="M150,30 q-1,-8 7,-8 q3,-7 11,-4 q7,-4 11,3 q7,0 5,9 Z" fill="{WHITE}" stroke-width="1.6"/>'
c6 += f'<path d="M96,96 Q150,30 200,26 Q226,26 237,36 L237,104 L96,104 Z" fill="{GREEN}"/>'
c6 += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DGREEN}" stroke-width="1.6"/>'
              for x, y, r in [(150, 60, 7), (176, 46, 8), (206, 44, 7), (226, 60, 7), (190, 70, 8)])
# 坡道上方的纜車山麓站與往山頂的纜線
c6 += f'<path d="M214,82 L236,40" stroke="{INK}" stroke-width="1.6"/>'
c6 += f'<rect x="196" y="80" width="40" height="28" rx="3" fill="{CREAM}"/>'
c6 += f'<path d="M192,82 L237,82" stroke-width="3.4"/>'
c6 += ''.join(f'<rect x="{x}" y="88" width="8" height="8" rx="1.6" fill="{SKY}" stroke-width="1.3"/>' for x in (204, 218))
# 地面與往右上爬的坡道（南部坂），兩旁有小房子
c6 += f'<path d="M3,104 L237,104 {BOT}" fill="#cfe7c4"/>'
c6 += f'<path d="M96,150 L196,108 L224,108 L130,150 Z" fill="{SLOPE}"/>'
c6 += f'<path d="M112,146 L206,110" stroke="{WHITE}" stroke-width="1.6" stroke-dasharray="5 6"/>'
c6 += (f'<rect x="112" y="112" width="24" height="18" rx="2" fill="{WHITE}"/>'
       f'<rect x="120" y="120" width="7" height="10" rx="1.4" fill="{DBROWN}" stroke-width="1.2"/>'
       f'<path d="M108,114 L124,100 L140,114 Z" fill="#6fa8dc"/>'
       f'<rect x="146" y="100" width="20" height="13" rx="2" fill="{CREAM}"/>'
       f'<path d="M143,102 L156,91 L169,102 Z" fill="{BRICK}"/>')
c6 += walker(164, 106, RED, .78)
# 下面的路面電車：電線、軌道、電車
c6 += f'<path d="M3,114 L237,114" stroke="{INK}" stroke-width="1.4"/>'
c6 += f'<path d="M3,170 L120,170" stroke="{GRAY}" stroke-width="3"/>'
c6 += tram(8, 128, 1.0)
c6 += f'<path d="M104,130 L104,166" stroke="{INK}" stroke-width="2.4"/><circle cx="104" cy="126" r="6" fill="{GOLD}" stroke-width="1.6"/>'
c6 += sparkle(60, 30) + star(110, 20, 5) + sparkle(30, 70, 3.4)
card('jujigai', '手繪路面電車停在站上，旁邊一條坡道往右上通到山腳的纜車站，有人沿著坡道走上去', c6)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('hr-' + name, 120, 120, label, inner, bg='#fff3c4')


def head(x, y, col, r=6):
    return (f'<path d="M{x-r},{y+16} q0,-10 {r},-10 q{r},0 {r},10 Z" fill="{col}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f9d9c0" stroke-width="1.6"/>')


def clock(x, y, r, hm, mm, col=WHITE):
    # hm、mm 是時針與分針的角度（0 = 12 點方向，順時針）
    import math as _m
    hx, hy = x + r * .5 * _m.sin(_m.radians(hm)), y - r * .5 * _m.cos(_m.radians(hm))
    mx, my = x + r * .78 * _m.sin(_m.radians(mm)), y - r * .78 * _m.cos(_m.radians(mm))
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'
            + ''.join(f'<circle cx="{x + r*.82*_m.sin(_m.radians(a)):.1f}" cy="{y - r*.82*_m.cos(_m.radians(a)):.1f}" r="1" fill="{INK}" stroke="none"/>'
                      for a in range(0, 360, 90))
            + f'<path d="M{x},{y} L{hx:.1f},{hy:.1f}" stroke-width="2.4"/>'
            f'<path d="M{x},{y} L{mx:.1f},{my:.1f}" stroke-width="1.8"/>')


# 官網的網路預售票不打折，也不能優先搭、沒有專用排隊線
rem('r-advance', '手繪提醒：手機上的網路票和紙本票一樣價錢，也要跟大家排同一條隊',
    f'<rect x="10" y="8" width="30" height="50" rx="6" fill="{NAVY}"/>'
    + f'<rect x="14" y="16" width="22" height="32" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
    + f'<path d="M17,26 L33,26 L33,30 q-2,2 0,4 L33,38 L17,38 L17,34 q2,-2 0,-4 Z" fill="{GOLD}" stroke-width="1.2"/>'
    + f'<path d="M50,30 L62,30 M50,37 L62,37" stroke-width="3"/>'
    + f'<g transform="rotate(8 92 32)"><path d="M72,20 L112,20 L112,28 q-4,4 0,8 L112,44 L72,44 L72,36 q4,-4 0,-8 Z" fill="{GOLD}"/>'
      f'<path d="M100,23 L100,41" stroke-width="1.3" stroke-dasharray="2 3"/></g>'
    # 下面：大家排同一條隊，旁邊的快速通道打叉
    + head(18, 80, RED) + head(36, 80, GREEN) + head(54, 80, '#6fa8dc') + head(72, 80, PINK)
    + f'<rect x="76" y="88" width="7" height="11" rx="1.6" fill="{NAVY}" stroke-width="1.2"/>'
    + f'<path d="M6,106 L114,106" stroke-width="2" opacity=".5"/>'
    + f'<path d="M86,70 L108,70 M102,64 L108,70 L102,76" fill="none" stroke="{GREEN}" stroke-width="2.6"/>'
    + f'<circle cx="98" cy="70" r="11" fill="none" stroke="{RED}" stroke-width="2.6"/>'
    + f'<path d="M90,78 L106,62" stroke="{RED}" stroke-width="2.6"/>')

# 人多時上山排 30 分鐘以上、下山排 1 小時以上，官方建議夜景出來 1 小時後再上山
rem('r-queue', '手繪提醒：人多時上山、下山都要排長長的隊，下山排得比上山更久',
    f'<path d="M86,10 a9,9 0 1,0 10,14 a7,7 0 1,1 -10,-14 Z" fill="{GOLD}" stroke-width="1.6"/>'
    + sparkle(108, 14, 3)
    # 上山：短一點的隊伍＋往上的箭頭＋時鐘轉半圈
    + f'<path d="M10,30 L10,14 M5,19 L10,14 L15,19" fill="none" stroke="{GREEN}" stroke-width="2.6"/>'
    + head(26, 22, RED, 5) + head(40, 22, GOLD, 5) + head(54, 22, PINK, 5)
    + clock(72, 30, 9, 0, 180)
    + f'<path d="M6,46 L114,46" stroke-width="1.6" opacity=".4"/>'
    # 下山：更長的隊伍＋往下的箭頭＋時鐘轉一整圈
    + f'<path d="M10,62 L10,78 M5,73 L10,78 L15,73" fill="none" stroke="{RED}" stroke-width="2.6"/>'
    + head(24, 66, '#6fa8dc', 5) + head(37, 66, GREEN, 5) + head(50, 66, PINK, 5) + head(63, 66, GOLD, 5)
    + head(76, 66, RED, 5) + head(89, 66, '#6fa8dc', 5)
    + clock(104, 74, 10, 30, 0)
    + f'<path d="M96,62 a12,12 0 1,1 -2,4" fill="none" stroke="{RED}" stroke-width="1.6"/>'
    + f'<path d="M10,104 q8,-4 16,0 t16,0 t16,0 t16,0 t16,0 t16,0" fill="none" stroke="#7a86b8" stroke-width="2"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>'
              for x, y in [(20, 96), (34, 98), (52, 95), (66, 98), (82, 96), (98, 98)]))

# 冬天接駁巴士下山最後一班 19:35，比纜車末班早很多，晚一點下山要走到十字街搭市電
rem('r-bus', '手繪提醒：冬天的接駁巴士很早就開走了，晚一點下山要走到電車站搭電車',
    clock(26, 26, 18, 7 * 30 + 35 * .5, 35 * 6)
    + f'<path d="M50,26 L60,26 M56,22 L60,26 L56,30" fill="none" stroke-width="2"/>'
    + f'<rect x="64" y="12" width="48" height="28" rx="7" fill="{GOLD}"/>'
    + ''.join(f'<rect x="{x}" y="17" width="9" height="9" rx="2" fill="{SKY}" stroke-width="1.3"/>' for x in (69, 81, 93))
    + f'<rect x="104" y="17" width="5" height="14" rx="1.5" fill="{SKY}" stroke-width="1.3"/>'
    + face(86, 33, .42, blush=False)
    + f'<circle cx="74" cy="41" r="4.4" fill="{INK}"/><circle cx="102" cy="41" r="4.4" fill="{INK}"/>'
    + f'<path d="M58,36 l-6,0 M60,42 l-8,0" stroke-width="1.6" opacity=".6"/>'
    # 下面：沿坡道走下去，坐路面電車
    + f'<path d="M14,60 L58,92" stroke="{SLOPE}" stroke-width="10"/>'
    + walker(28, 58, '#6fa8dc', .62)
    + f'<path d="M40,72 L52,80" stroke-width="1.6" stroke-dasharray="3 4"/>'
    + tram(58, 82, .62)
    + f'<path d="M54,76 L114,76" stroke="{INK}" stroke-width="1.2"/>'
    + f'<path d="M50,110 L116,110" stroke="{GRAY}" stroke-width="2.4"/>')

print(save(F, OUT), 'files')
