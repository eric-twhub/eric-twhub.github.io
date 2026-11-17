# 石垣島離島船票頁的「八重山的島長什麼樣子」插圖與提醒卡（2026-11-17）。
# 竹富島、西表島、由布島、小濱島、黑島、波照間島六座島各畫一張可愛版的島上景色，不描照片構圖；
# 船只畫沒有標誌的白色高速船，不畫兩家船公司的商標、船名或吉祥物，也不畫任何角色。
# 輸出 illust/sp/ishigaki-ferry/*.svg（240×180 圖卡、120×120 提醒小圖）。說明文字放在 illust/spots/ishigaki-ferry.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'ishigaki-ferry')
W, H = 240, 180
F = {}
SKYW = '#e3f1f8'
TQ = '#4fc6c0'
TQ2 = '#a8e6df'
DEEP = '#3b9fc4'
SAND = '#f6e3b4'
WSAND = '#fbf6ea'
STONE = '#d9cfbf'
STONE2 = '#c4b8a5'
BUFF = '#8a8f99'
COW = '#6b4a36'
CANE = '#8cc56a'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'
BG = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ig-' + name, W, H, label, inner, bg=bg)


def sea(y, col=TQ, hi=TQ2):
    return (f'<path d="M3,{y} q14,-6 28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t10,0 {BOT}" fill="{col}"/>'
            f'<path d="M30,{y+16} q8,-4 16,0 M150,{y+18} q8,-4 16,0 M96,{y+10} q6,-3 12,0" fill="none" stroke="{hi}" stroke-width="1.6"/>')


def ferry(x, y, s=1.0, rot=0, smile=True):
    # 沒有標誌的白色高速船（x 是船中間，y 是吃水線），船頭朝右
    t = (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke-width="{2.4/s:.2f}">'
         f'<path d="M-54,-20 L54,-24 Q48,-4 30,0 L-42,0 Q-52,0 -54,-10 Z" fill="{WHITE}"/>'
         f'<path d="M-52,-8 L44,-10" stroke="#3a8fd0" stroke-width="3.4"/>'
         f'<path d="M-40,-20 L-40,-38 Q-40,-46 -32,-46 L14,-46 Q26,-46 34,-32 L38,-22 Z" fill="{WHITE}"/>'
         + ''.join(f'<rect x="{wx}" y="-40" width="9" height="8" rx="2" fill="{SKY}" stroke-width="1.4"/>' for wx in (-33, -20, -7))
         + f'<path d="M16,-42 Q26,-41 30,-32 L16,-32 Z" fill="{SKY}" stroke-width="1.4"/>'
         f'<path d="M-12,-46 L-12,-56 M-18,-56 L-6,-56" stroke-width="2.2"/>'
         f'<circle cx="-12" cy="-58" r="2.4" fill="{RED}" stroke-width="1.2"/>'
         + (face(20, -19, .7) if smile else '')
         + '</g>')
    return t


def splash(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" stroke-width="1.4"/>' for x, y, r in pts)


def palm(x, base, h=40, lean=-6):
    tx, ty = x + lean, base - h
    t = (f'<path d="M{x},{base} Q{x+lean*.2:.0f},{base-h*.5:.0f} {tx},{ty}" fill="none" stroke="{BROWN}" stroke-width="5"/>'
         f'<path d="M{x},{base} Q{x+lean*.2:.0f},{base-h*.5:.0f} {tx},{ty}" fill="none" stroke-width="1.2" opacity=".5" stroke-dasharray="2 4"/>')
    for dx, dy, ex, ey in [(-12, -10, -24, 2), (-6, -18, -16, -22), (8, -18, 18, -16), (14, -8, 22, 6)]:
        t += (f'<path d="M{tx},{ty} Q{tx+dx},{ty+dy} {tx+ex},{ty+ey} Q{tx+dx},{ty+dy+8} {tx},{ty} Z" '
              f'fill="{GREEN}" stroke-width="1.6"/>')
    return t


def trees(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN if i % 2 else DGREEN}" stroke-width="1.8"/>'
                   for i, (x, y, r) in enumerate(pts))


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def redroof(x, y, w, h, smile=False):
    # 紅瓦屋頂的平房：瓦片之間有白色的灰泥線
    rt = y - h * .62
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{CREAM}"/>'
         f'<rect x="{x+w*.38:.0f}" y="{y+h*.35:.0f}" width="{w*.24:.0f}" height="{h*.65:.0f}" rx="2" fill="{DBROWN}" stroke-width="1.6"/>'
         f'<path d="M{x-8},{y+3} L{x+w*.22:.0f},{rt:.0f} L{x+w*.78:.0f},{rt:.0f} L{x+w+8},{y+3} Z" fill="{BRICK}"/>')
    for k in (1, 2):
        yy = rt + (y + 3 - rt) * k / 3
        u = k / 3
        xl = x + w * .22 - (w * .22 + 8) * u
        xr = x + w * .78 + (w * .22 + 8) * u
        t += f'<path d="M{xl+2:.0f},{yy:.0f} L{xr-2:.0f},{yy:.0f}" stroke="{WHITE}" stroke-width="2"/>'
    t += (f'<path d="M{x+w*.22:.0f},{rt:.0f} L{x-6},{y+2} M{x+w*.78:.0f},{rt:.0f} L{x+w+6},{y+2}" stroke="{WHITE}" stroke-width="2.2"/>'
          f'<path d="M{x+w*.22-2:.0f},{rt:.0f} L{x+w*.78+2:.0f},{rt:.0f}" stroke="{WHITE}" stroke-width="3"/>')
    if smile:
        t += face(x + w * .2, y + h * .5, .55)
    return t


def stonewall(x1, x2, y, h=24):
    # 一顆顆圓圓的石頭疊成的矮牆
    t = f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="{h}" rx="5" fill="{STONE}"/>'
    row = 0
    yy = y + 6
    while yy < y + h - 2:
        xx = x1 + (8 if row % 2 else 3)
        while xx + 10 < x2:
            t += f'<ellipse cx="{xx+6}" cy="{yy}" rx="6" ry="4" fill="{STONE2}" stroke-width="1.1" opacity=".75"/>'
            xx += 14
        yy += 8
        row += 1
    return t


def flower(x, y, col=RED, r=3.4):
    return (''.join(f'<circle cx="{x+r*.9*dx:.1f}" cy="{y+r*.9*dy:.1f}" r="{r}" fill="{col}" stroke-width="1.1"/>'
                    for dx, dy in [(0, -1), (.95, -.3), (.6, .8), (-.6, .8), (-.95, -.3)])
            + f'<circle cx="{x}" cy="{y}" r="{r*.5:.1f}" fill="{GOLD}" stroke-width="1"/>')


# 1. 竹富島：紅瓦屋頂、石牆、白沙路的老聚落
card('taketomi', '手繪紅瓦屋頂的平房、圓石頭疊的矮牆，中間一條白沙路',
     BG
     + trees([(14, 60, 12), (34, 52, 13), (112, 56, 12), (128, 50, 13), (226, 58, 12)])
     + redroof(24, 72, 66, 34, smile=True)
     + redroof(150, 70, 70, 34)
     + f'<path d="M3,112 L237,112 {BOT}" fill="{GREEN}" stroke="none"/>'
     + f'<path d="M104,104 L136,104 L196,177 L44,177 Z" fill="{WSAND}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{STONE2}" stroke="none"/>'
               for x, y in [(112, 120), (128, 132), (98, 146), (140, 156), (84, 166), (160, 170), (120, 160)])
     + stonewall(3, 98, 100, 30) + stonewall(142, 237, 100, 30)
     + flower(30, 100) + flower(46, 104, PINK) + flower(196, 100) + flower(214, 104, PINK)
     + person(122, 128, PINK, .8)
     + sparkle(84, 24) + star(150, 26, 5))

# 2. 西表島：島上大部分是森林，船停在港口
forest = trees([(30, 70, 16), (54, 54, 18), (82, 46, 20), (110, 52, 18), (138, 44, 20), (166, 56, 18),
                (192, 66, 16), (216, 76, 14), (44, 86, 14), (72, 78, 16), (100, 80, 15), (128, 76, 16),
                (156, 82, 15), (184, 88, 14)])
card('iriomote', '手繪整座被森林蓋滿的島，岸邊有紅樹林，港口停著一艘白色的船',
     BG
     + f'<path d="M3,100 Q20,72 46,62 Q80,36 112,42 Q150,30 178,52 Q214,62 237,92 L237,112 L3,112 Z" fill="{DGREEN}"/>'
     + forest
     + face(138, 46, .8)
     + sea(116)
     # 紅樹林：一叢叢踩在水裡的小樹
     + ''.join(f'<path d="M{x-8},118 Q{x-6},108 {x},106 Q{x+6},108 {x+8},118 M{x},106 L{x},98" fill="none" stroke="{DBROWN}" stroke-width="2"/>'
               f'<circle cx="{x}" cy="96" r="9" fill="{GREEN}" stroke-width="1.6"/>' for x in (22, 44, 66))
     # 港口的堤防
     + f'<rect x="150" y="108" width="84" height="12" rx="3" fill="{GRAY}"/>'
     + ferry(176, 140, .62)
     + splash([(140, 136, 3), (144, 141, 4)])
     + sparkle(200, 24) + star(30, 26, 6) + sparkle(56, 20, 4))

# 3. 由布島：水牛車走過淺海到對岸
buffalo = (f'<path d="M150,128 L150,142 M160,130 L160,144 M178,130 L178,144 M188,128 L188,142" stroke="{BUFF}" stroke-width="5"/>'
           f'<ellipse cx="168" cy="122" rx="26" ry="15" fill="{BUFF}"/>'
           f'<path d="M188,110 Q186,100 196,98 L210,100 Q218,104 214,116 Q210,124 198,122 Z" fill="{BUFF}"/>'
           f'<path d="M196,100 Q186,86 198,84 M208,100 Q222,90 214,82" fill="none" stroke="{CREAM}" stroke-width="3.4"/>'
           f'<path d="M196,100 Q186,86 198,84 M208,100 Q222,90 214,82" fill="none" stroke-width="1.2"/>'
           + face(203, 109, .55)
           + f'<path d="M142,118 q-6,4 -4,12" fill="none" stroke-width="2"/>')
cart = (f'<path d="M66,92 L66,118 M124,92 L124,118" stroke="{DBROWN}" stroke-width="2.6"/>'
        f'<path d="M58,94 Q95,78 132,94 Z" fill="{RED}"/>'
        f'<path d="M66,94 Q76,88 86,94 Q95,88 104,94 Q114,88 124,94" fill="none" stroke="{WHITE}" stroke-width="2"/>'
        + person(82, 102, NAVY, .7) + person(98, 100, GOLD, .75) + person(114, 103, PINK, .7)
        + f'<rect x="58" y="116" width="76" height="9" rx="2" fill="{BROWN}"/>'
        f'<path d="M134,120 L150,120" stroke="{DBROWN}" stroke-width="3"/>'
        f'<circle cx="72" cy="132" r="13" fill="{BROWN}"/><circle cx="72" cy="132" r="4" fill="{DBROWN}" stroke-width="1.4"/>'
        f'<circle cx="120" cy="132" r="13" fill="{BROWN}"/><circle cx="120" cy="132" r="4" fill="{DBROWN}" stroke-width="1.4"/>')
card('yubu', '手繪水牛拉著有遮陽頂的車，載著人走過淺淺的海，對岸是有椰子樹的小島',
     BG
     + f'<path d="M150,88 Q176,72 237,74 L237,96 L150,96 Z" fill="{SAND}"/>'
     + palm(196, 82, 36, -4) + palm(222, 80, 30, 6)
     + sea(92, TQ2, WHITE)
     + cart + buffalo
     + f'<path d="M3,138 q14,-5 28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t10,0 {BOT}" fill="{TQ2}" opacity=".85"/>'
     + ''.join(f'<path d="M{x-8},{y} q8,-4 16,0" fill="none" stroke="{WHITE}" stroke-width="1.6"/>'
               for x, y in [(72, 148), (120, 148), (155, 146), (184, 146), (40, 160), (210, 162)])
     + sparkle(40, 30) + star(70, 22, 5) + sparkle(120, 40, 4))

# 4. 小濱島：甘蔗田中間的路一路通到海邊
cane = ''
for side, xs in (('l', range(10, 96, 9)), ('r', range(146, 236, 9))):
    for i, x in enumerate(xs):
        top = 100 + (i * 7 % 13)
        cane += (f'<path d="M{x},{top} L{x},150" stroke="{CANE}" stroke-width="2.4"/>'
                 f'<path d="M{x},{top+4} q-7,-4 -9,-12 M{x},{top+12} q7,-4 9,-12" fill="none" stroke="{DGREEN}" stroke-width="1.8"/>')
card('kohama', '手繪兩旁長滿甘蔗的小路，一路往下通到海邊，海上有一艘白色的船',
     BG
     + f'<circle cx="200" cy="32" r="13" fill="{GOLD}" stroke-width="1.8"/>'
     + f'<path d="M3,72 L237,72 L237,96 L3,96 Z" fill="{TQ}" stroke="none"/>'
     + f'<path d="M3,72 L237,72" stroke-width="2"/>'
     + f'<path d="M24,72 Q40,58 62,72 Z M150,72 Q160,64 176,72 Z" fill="{DGREEN}" stroke-width="1.8"/>'
     + ferry(100, 78, .38, smile=False)
     + f'<path d="M3,96 Q60,86 120,94 Q180,86 237,96 {BOT}" fill="{GREEN}"/>'
     + cane
     + f'<path d="M112,94 L128,94 Q150,140 176,177 L64,177 Q96,140 112,94 Z" fill="#ead9b8"/>'
     + f'<path d="M120,104 L120,114 M120,126 L120,140 M120,152 L120,168" stroke="{WHITE}" stroke-width="2.4"/>'
     + face(120, 158, .7)
     + sparkle(40, 30) + star(70, 22, 5))

# 5. 黑島：平平的牧場上有牛
def cow(x, y, s=1.0, smile=True):
    t = (f'<g transform="translate({x} {y}) scale({s})" stroke-width="{2.4/s:.2f}">'
         f'<path d="M-18,8 L-18,24 M-8,10 L-8,26 M12,10 L12,26 M22,8 L22,24" stroke="{COW}" stroke-width="5"/>'
         f'<ellipse cx="2" cy="4" rx="26" ry="15" fill="{COW}"/>'
         f'<path d="M-26,0 q-8,4 -6,14" fill="none" stroke-width="2"/>'
         f'<ellipse cx="32" cy="-6" rx="13" ry="12" fill="{COW}"/>'
         f'<ellipse cx="36" cy="0" rx="8" ry="5" fill="#d9a88a" stroke-width="1.4"/>'
         f'<path d="M24,-14 l-6,-6 M40,-16 l4,-7" stroke="{CREAM}" stroke-width="3"/>'
         f'<ellipse cx="20" cy="-10" rx="5" ry="3" fill="{COW}" stroke-width="1.4"/>'
         + (f'<circle cx="27" cy="-9" r="3.2" fill="{WHITE}" stroke-width="1"/><circle cx="37" cy="-9" r="3.2" fill="{WHITE}" stroke-width="1"/>'
            f'<circle cx="27.6" cy="-8.6" r="1.7" fill="{INK}" stroke="none"/><circle cx="37.6" cy="-8.6" r="1.7" fill="{INK}" stroke="none"/>'
            f'<ellipse cx="24" cy="-3" rx="2.6" ry="1.6" fill="{PINK}" stroke="none"/>' if smile else '')
         + '</g>')
    return t


card('kuroshima', '手繪平平的綠色牧場和木柵欄，一頭牛站在草地上，遠處是海',
     BG
     + f'<path d="M3,78 L237,78 L237,90 L3,90 Z" fill="{TQ}" stroke="none"/>'
     + f'<path d="M3,78 L237,78" stroke-width="2"/>'
     + f'<path d="M3,90 Q120,84 237,90 {BOT}" fill="{GREEN}"/>'
     + trees([(30, 86, 9), (46, 82, 11), (204, 84, 10)])
     + ''.join(f'<path d="M{x},96 L{x},124" stroke="{DBROWN}" stroke-width="3"/>' for x in range(14, 237, 30))
     + f'<path d="M6,102 L234,102 M6,116 L234,116" stroke="{BROWN}" stroke-width="3"/>'
     + cow(112, 130, 1.25)
     + cow(196, 106, .55, smile=False)
     + flower(36, 150, GOLD, 3) + flower(60, 162, PINK, 3) + flower(206, 156, WHITE, 3)
     + f'<path d="M180,40 q6,-8 12,0 q6,-8 12,0" fill="none" stroke-width="1.8"/>'
     + sparkle(50, 30) + star(130, 24, 5))

# 6. 波照間島：日本最南端的有人島，船走外海、浪比較大
card('hateruma', '手繪白色的船在大浪裡上下搖，遠方小島上有一塊石碑和椰子樹',
     BG
     + f'<circle cx="34" cy="32" r="12" fill="{GOLD}" stroke-width="1.8"/>'
     + f'<path d="M150,82 Q160,62 196,60 Q226,60 237,72 L237,96 L150,96 Z" fill="{SAND}"/>'
     + f'<path d="M180,62 L180,50 Q186,42 192,50 L192,62 Z" fill="{GRAY}"/>'
     + f'<rect x="174" y="60" width="24" height="6" rx="2" fill="{STONE2}" stroke-width="1.6"/>'
     + palm(216, 66, 34, 4)
     + f'<path d="M100,30 q10,-4 20,0 M108,40 q10,-4 20,0 M60,52 q8,-3 16,0" fill="none" stroke-width="1.6" opacity=".6"/>'
     + f'<path d="M3,96 Q30,78 58,96 Q86,78 114,96 Q142,78 170,96 Q198,78 226,96 L237,96 {BOT}" fill="{DEEP}"/>'
     + ferry(104, 112, .7, rot=-9)
     + splash([(150, 98, 5), (156, 92, 4), (160, 102, 6), (50, 112, 4)])
     + f'<path d="M3,130 Q24,112 48,128 Q60,136 68,124 Q90,112 112,130 Q136,112 160,128 Q172,136 180,124 '
       f'Q206,110 237,128 {BOT}" fill="{TQ}"/>'
       + ''.join(f'<path d="M{x},{y} q6,-6 12,-2" fill="none" stroke="{WHITE}" stroke-width="2.2"/>'
                 for x, y in [(40, 124), (100, 124), (154, 124), (210, 122)])
     + sparkle(140, 30) + star(70, 22, 5))


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ig-' + name, 120, 120, label, inner, bg='#fff3c4')


def ticket(x, y, col, rot=0):
    return (f'<g transform="rotate({rot} {x+22} {y+14})">'
            f'<path d="M{x},{y} L{x+44},{y} L{x+44},{y+10} q-5,4 0,8 L{x+44},{y+28} L{x},{y+28} L{x},{y+18} q5,-4 0,-8 Z" fill="{col}"/>'
            f'<path d="M{x+30},{y+3} L{x+30},{y+25}" stroke-width="1.4" stroke-dasharray="2 3"/>'
            f'<path d="M{x+6},{y+16} L{x+24},{y+16} L{x+21},{y+21} L{x+9},{y+21} Z M{x+11},{y+16} L{x+11},{y+10} L{x+19},{y+10} L{x+20},{y+16}" '
            f'fill="{WHITE}" stroke-width="1.3"/>'
            '</g>')


# 兩家船公司的船票不能互搭，回程也要坐同一家
rem('r-company', '手繪提醒：兩種顏色的船票不能換著用',
    ticket(8, 22, GREEN, -10)
    + ticket(66, 22, '#6fa8dc', 10)
    + f'<circle cx="60" cy="40" r="11" fill="{WHITE}"/><path d="M54,34 L66,46 M66,34 L54,46" stroke="{RED}" stroke-width="3"/>'
    # 下面：同一家的船來回兩座島（去程、回程都是同一家）
    + f'<path d="M6,94 Q18,78 32,94 Z M88,94 Q102,78 114,94 Z" fill="{SAND}" stroke-width="1.6"/>'
    + f'<path d="M8,95 q8,-3 16,0 t16,0 t16,0 t16,0 t16,0 t16,0 t16,0" fill="none" stroke="{TQ}" stroke-width="3"/>'
    + f'<path d="M28,70 Q60,58 92,70" fill="none" stroke-width="2"/><path d="M92,70 l-8,-3 M92,70 l-5,6" stroke-width="2"/>'
    + f'<path d="M92,104 Q60,116 28,104" fill="none" stroke-width="2"/><path d="M28,104 l8,-1 M28,104 l4,6" stroke-width="2"/>'
    + ferry(60, 92, .3, smile=False)
    + f'<path d="M56,74 L56,67 L63,69.5 L56,72" fill="{GREEN}" stroke-width="1.4"/>')

# 冬天北風時上原港常停航，改到大原港再轉接駁巴士
rem('r-uehara', '手繪提醒：北風吹時船改停另一個港，再轉坐巴士',
    f'<path d="M10,30 q14,-8 28,0 q12,6 22,-2 M14,44 q12,-6 24,0 q10,5 18,-1" fill="none" stroke="#7fa6c8" stroke-width="2.4"/>'
    + f'<path d="M56,28 q6,-6 2,-12" fill="none" stroke="#7fa6c8" stroke-width="2.4"/>'
    + f'<path d="M66,20 Q66,10 78,12 Q84,4 96,10 Q110,8 110,20 Q116,24 110,30 L72,30 Q62,30 66,20 Z" fill="{GRAY}"/>'
    + f'<path d="M4,70 q10,-5 20,0 t20,0 t20,0 L64,80 L4,80 Z" fill="{TQ}" stroke-width="1.6"/>'
    + ferry(30, 72, .3, smile=False)
    + f'<path d="M42,82 Q48,92 58,94" fill="none" stroke-width="2" stroke-dasharray="3 4"/><path d="M58,94 l-8,0 M58,94 l-4,-7" stroke-width="2"/>'
    + f'<rect x="64" y="70" width="50" height="30" rx="7" fill="{GOLD}"/>'
    + ''.join(f'<rect x="{x}" y="75" width="9" height="9" rx="2" fill="{SKY}" stroke-width="1.3"/>' for x in (70, 82, 94))
    + f'<rect x="105" y="75" width="6" height="14" rx="1.5" fill="{SKY}" stroke-width="1.3"/>'
    + face(86, 91, .45, blush=False)
    + f'<circle cx="76" cy="101" r="5" fill="{INK}"/><circle cx="104" cy="101" r="5" fill="{INK}"/>'
    + f'<path d="M4,110 L116,110" stroke-width="2" opacity=".5"/>')

# 兩家船公司都不讓穿濕衣服上船，玩水後先換好
rem('r-wet', '手繪提醒：滴著水的濕衣服不能直接上船，先換上乾衣服',
    f'<path d="M14,28 L28,20 Q34,28 40,20 L54,28 L50,40 L44,38 L44,70 L24,70 L24,38 L18,40 Z" fill="#7fc1e8"/>'
    + ''.join(f'<path d="M{x},{y} q-4,6 0,9 q4,-3 0,-9 Z" fill="#7fc1e8" stroke-width="1.2"/>' for x, y in [(26, 78), (40, 82), (34, 94)])
    + f'<circle cx="48" cy="22" r="10" fill="{WHITE}"/><path d="M43,17 L53,27 M53,17 L43,27" stroke="{RED}" stroke-width="3"/>'
    + f'<path d="M58,56 L70,56 M66,51 L72,56 L66,61" fill="none" stroke-width="2.4"/>'
    + f'<path d="M78,44 L90,38 Q96,44 102,38 L114,44 L110,54 L106,52 L106,78 L82,78 L82,52 L78,54 Z" fill="{CREAM}"/>'
    + face(94, 62, .5)
    + sparkle(110, 28, 4) + sparkle(76, 32, 3)
    + f'<path d="M66,104 q8,-4 16,0 t16,0 t16,0" fill="none" stroke="{TQ}" stroke-width="3"/>'
    + ferry(30, 108, .26, smile=False))

print(save(F, OUT), 'files')
