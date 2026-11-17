# 青山剛昌ふるさと館頁的「柯南小鎮看得到什麼」插圖與提醒卡（2026-11-18）。
# 車站、沿路有銅像的街道、舊館、喫茶店、新館工地、寄放行李各畫一張可愛版的一般景色，不描照片構圖。
# 角色有版權：不畫柯南或任何角色本人、剪影、眼鏡＋領結這類能認出角色的組合，
# 也不畫館方、車站、店家的標誌與招牌，圖裡不放任何文字或數字。銅像只畫空的台座和空白的牌子。
# 輸出 illust/sp/yonago-conan-museum/*.svg（240×180 圖卡、120×120 提醒小圖）。說明文字放在 illust/spots/yonago-conan-museum.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'yonago-conan-museum')
W, H = 240, 180
F = {}
SKYW = '#e3f1f8'
FIELD = '#cfe7c4'
ROAD = '#eadcc4'
ASPH = '#c9cfd8'
LENS = '#cfe9f7'
WALL = '#f6e4c8'
STONE = '#cfc6b8'
BLUE = '#6fa8dc'
SKIN = '#f9d9c0'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'
BG = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('cn-' + name, W, H, label, inner, bg=bg)


def cloud(x, y, s=1.0):
    return (f'<path d="M{x},{y} q{-1*s},{-8*s} {7*s},{-8*s} q{3*s},{-7*s} {11*s},{-4*s} '
            f'q{7*s},{-4*s} {11*s},{3*s} q{7*s},0 {5*s},{9*s} Z" fill="{WHITE}" stroke-width="1.6"/>')


def walker(x, y, col=RED, s=1.0, back=False):
    # 側面走路的人；back=True 是往右走（眼睛在右邊）
    eye = 2.4 if not back else -2.4
    return (f'<path d="M{x-3*s},{y+18*s} L{x-7*s},{y+28*s} M{x+3*s},{y+18*s} L{x+7*s},{y+27*s}" stroke-width="{2.6*s}"/>'
            f'<path d="M{x-7*s},{y+19*s} Q{x-7*s},{y+6*s} {x},{y+6*s} Q{x+7*s},{y+6*s} {x+7*s},{y+19*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{SKIN}"/>'
            f'<circle cx="{x+eye*s}" cy="{y-.5*s}" r="{1.3*s}" fill="{INK}" stroke="none"/>')


def trees(pts, col=DGREEN):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke-width="1.6"/>' for x, y, r in pts)


def maglamp(x, base, h=56, s=1.0):
    # 頂上做成放大鏡形狀的路燈：細柱子、斜斜的握把、圓圈裡的鏡片會亮
    top = base - h
    r = 9 * s
    return (f'<path d="M{x},{base} L{x},{top+r*.6:.1f}" stroke="{NAVY}" stroke-width="{3*s:.1f}"/>'
            f'<rect x="{x-4*s:.1f}" y="{base-3*s:.1f}" width="{8*s:.1f}" height="{4*s:.1f}" rx="1.4" fill="{NAVY}" stroke-width="1.2"/>'
            f'<path d="M{x},{top+r*.6:.1f} L{x+r*.7:.1f},{top-r*.1:.1f}" stroke="{DBROWN}" stroke-width="{4.4*s:.1f}"/>'
            f'<circle cx="{x+r*1.4:.1f}" cy="{top-r*.8:.1f}" r="{r:.1f}" fill="#fff1b8" stroke-width="{3*s:.1f}"/>'
            f'<path d="M{x+r*.9:.1f},{top-r*1.2:.1f} q{r*.2:.1f},{-r*.4:.1f} {r*.6:.1f},{-r*.5:.1f}" fill="none" stroke="{WHITE}" stroke-width="1.6"/>')


def pedestal(x, y, w=26, h=24, col=STONE):
    # 空的銅像台座＋空白的小牌子（不畫銅像本身）
    return (f'<rect x="{x-w/2-3:.1f}" y="{y+h-6}" width="{w+6}" height="6" rx="1.6" fill="{col}"/>'
            f'<rect x="{x-w/2:.1f}" y="{y}" width="{w}" height="{h-6}" rx="2" fill="{col}"/>'
            f'<rect x="{x-w/2-2:.1f}" y="{y-4}" width="{w+4}" height="5" rx="1.6" fill="{col}"/>'
            f'<rect x="{x-w*.3:.1f}" y="{y+4}" width="{w*.6:.1f}" height="{h*.32:.1f}" rx="1.4" fill="#e7c27a" stroke-width="1.3"/>')


def suitcase(x, y, w=34, h=42, col=PINK):
    return (f'<path d="M{x+w*.32:.1f},{y} L{x+w*.32:.1f},{y-8} L{x+w*.68:.1f},{y-8} L{x+w*.68:.1f},{y}" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}"/>'
            f'<path d="M{x+w*.3:.1f},{y+5} L{x+w*.3:.1f},{y+h-5} M{x+w*.7:.1f},{y+5} L{x+w*.7:.1f},{y+h-5}" stroke-width="1.4"/>'
            f'<circle cx="{x+w*.2:.1f}" cy="{y+h+3}" r="3" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+w*.8:.1f}" cy="{y+h+3}" r="3" fill="{INK}" stroke="none"/>')


def qr(x, y, sz=24):
    u = sz / 7
    t = f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{WHITE}" stroke-width="1.2"/>'
    for cx, cy in [(0, 0), (4, 0), (0, 4)]:
        t += (f'<rect x="{x+cx*u+u*.3:.1f}" y="{y+cy*u+u*.3:.1f}" width="{u*2.4:.1f}" height="{u*2.4:.1f}" '
              f'fill="none" stroke-width="1.3"/>'
              f'<rect x="{x+cx*u+u*1.1:.1f}" y="{y+cy*u+u*1.1:.1f}" width="{u*.9:.1f}" height="{u*.9:.1f}" fill="{INK}" stroke="none"/>')
    for cx, cy in [(4, 4), (5.5, 4.2), (4.6, 5.6), (6, 6), (3.2, 5.8), (5.8, 3.0), (3.4, 3.4)]:
        t += f'<rect x="{x+cx*u:.1f}" y="{y+cy*u:.1f}" width="{u*.8:.1f}" height="{u*.8:.1f}" fill="{INK}" stroke="none"/>'
    return t


def clock(x, y, r, hm, mm, col=WHITE):
    # hm、mm 是時針與分針的角度（0 = 12 點方向，順時針）
    hx, hy = x + r * .5 * math.sin(math.radians(hm)), y - r * .5 * math.cos(math.radians(hm))
    mx, my = x + r * .78 * math.sin(math.radians(mm)), y - r * .78 * math.cos(math.radians(mm))
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'
            + ''.join(f'<circle cx="{x + r*.82*math.sin(math.radians(a)):.1f}" cy="{y - r*.82*math.cos(math.radians(a)):.1f}" '
                      f'r="{1.4 if a % 90 == 0 else .9}" fill="{INK}" stroke="none"/>'
                      for a in range(0, 360, 30))
            + f'<path d="M{x},{y} L{hx:.1f},{hy:.1f}" stroke-width="2.8"/>'
            f'<path d="M{x},{y} L{mx:.1f},{my:.1f}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="1.8" fill="{INK}" stroke="none"/>')


# 1. 車站：鄉下的木造小車站，前面一條路往右通出去，有人走路、也有計程車
c1 = BG
c1 += cloud(28, 34, 1.1) + cloud(160, 26, .9)
c1 += f'<path d="M3,92 Q50,62 100,76 Q150,56 200,70 Q222,64 237,72 L237,112 L3,112 Z" fill="{GREEN}"/>'
c1 += trees([(60, 76, 7), (180, 66, 7), (214, 72, 6)])
c1 += f'<path d="M3,108 L237,108 {BOT}" fill="{FIELD}"/>'
# 車站後面的鐵軌和一節小火車
c1 += f'<path d="M3,104 L237,104 M3,109 L237,109" stroke="{DBROWN}" stroke-width="1.8"/>'
c1 += ''.join(f'<path d="M{x},102 L{x},111" stroke="{DBROWN}" stroke-width="1.4" opacity=".5"/>' for x in range(10, 237, 11))
c1 += f'<rect x="132" y="78" width="80" height="26" rx="8" fill="{CREAM}"/>'
c1 += f'<path d="M132,94 L212,94 L212,96 Q212,104 204,104 L140,104 Q132,104 132,96 Z" fill="{GREEN}"/>'
c1 += ''.join(f'<rect x="{x}" y="82" width="11" height="9" rx="2" fill="{SKY}" stroke-width="1.3"/>' for x in (139, 155, 171, 187))
c1 += f'<circle cx="207" cy="98" r="2.2" fill="{GOLD}" stroke-width="1"/>'
c1 += f'<circle cx="146" cy="106" r="3.6" fill="{INK}"/><circle cx="198" cy="106" r="3.6" fill="{INK}"/>'
c1 += face(172, 98, .45, blush=False)
# 木造車站：瓦屋頂、門口的屋簷、兩扇窗、空白的站名板
c1 += f'<rect x="20" y="74" width="92" height="44" rx="2" fill="{CREAM}"/>'
c1 += f'<path d="M10,76 L30,54 L102,54 L122,76 Z" fill="{BRICK}"/>'
c1 += f'<path d="M20,65 L112,65 M42,54 L36,76 M66,54 L66,76 M90,54 L96,76" stroke-width="1.2" opacity=".45"/>'
c1 += f'<rect x="46" y="68" width="40" height="7" rx="1.6" fill="{WHITE}" stroke-width="1.4"/>'
c1 += f'<rect x="56" y="88" width="20" height="30" rx="2" fill="{DBROWN}"/>'
c1 += f'<path d="M66,88 L66,118" stroke-width="1.4"/>'
c1 += ''.join(f'<rect x="{x}" y="84" width="14" height="12" rx="2" fill="{SKY}" stroke-width="1.4"/>' for x in (28, 90))
c1 += f'<path d="M48,82 L84,82 L88,88 L44,88 Z" fill="{DBROWN}" stroke-width="1.8"/>'
# 從車站門口往右彎出去的路，有人走、也有一台計程車
c1 += f'<path d="M56,118 L78,118 Q100,134 150,136 Q200,138 237,134 L237,154 Q180,160 140,156 Q84,150 56,118 Z" fill="{ASPH}" stroke-width="1.8"/>'
c1 += f'<path d="M80,126 Q110,144 150,146 Q196,148 230,144" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-dasharray="6 6"/>'
c1 += walker(36, 128, RED, .8, back=True) + walker(50, 132, BLUE, .74, back=True)
c1 += (f'<path d="M150,150 L150,142 Q150,136 156,136 L162,128 L184,128 L190,136 Q198,136 198,142 L198,150 Z" fill="{GOLD}"/>'
       f'<path d="M165,131 L182,131 L186,136 L161,136 Z" fill="{SKY}" stroke-width="1.3"/>'
       f'<rect x="168" y="122" width="10" height="6" rx="1.6" fill="{WHITE}" stroke-width="1.4"/>'
       f'<circle cx="160" cy="151" r="5" fill="{INK}"/><circle cx="188" cy="151" r="5" fill="{INK}"/>')
c1 += face(174, 142, .45)
c1 += sparkle(100, 30) + star(214, 36, 5) + sparkle(130, 50, 3.4)
card('station', '手繪鄉下的木造小車站，後面停著一節小火車，前面的路往右彎出去，有人走路，也有一台計程車', c1)

# 2. 街道：頂上是放大鏡造型的路燈，人行道邊排著幾座空的台座
c2 = BG
c2 += cloud(150, 30, 1.0)
# 遠處的房子和山
c2 += f'<path d="M3,84 Q60,60 120,72 Q180,58 237,74 L237,100 L3,100 Z" fill="{GREEN}"/>'
for x, w, h, roof in [(16, 34, 24, BRICK), (60, 28, 20, NAVY), (148, 30, 22, BRICK), (192, 36, 26, '#7a8bb8')]:
    c2 += (f'<rect x="{x}" y="{100-h}" width="{w}" height="{h}" rx="2" fill="{WHITE}"/>'
           f'<path d="M{x-4},{102-h} L{x+w/2},{88-h} L{x+w+4},{102-h} Z" fill="{roof}"/>'
           f'<rect x="{x+w/2-4}" y="{100-h+8}" width="8" height="8" rx="1.6" fill="{SKY}" stroke-width="1.2"/>')
# 往遠處收窄的馬路與兩側人行道
c2 += f'<path d="M3,100 L237,100 {BOT}" fill="{FIELD}"/>'
c2 += f'<path d="M104,100 L136,100 L210,177 L30,177 Z" fill="{ASPH}"/>'
c2 += f'<path d="M120,104 L120,112 M120,122 L120,136 M120,148 L120,168" stroke="{WHITE}" stroke-width="2.4"/>'
c2 += f'<path d="M96,100 L104,100 L30,177 L6,166 Z" fill="{ROAD}" stroke-width="1.8"/>'
c2 += f'<path d="M136,100 L144,100 L234,166 L210,177 Z" fill="{ROAD}" stroke-width="1.8"/>'
# 放大鏡路燈（近大遠小）
c2 += maglamp(150, 108, 34, .55) + maglamp(176, 128, 52, .8) + maglamp(202, 160, 76, 1.1)
c2 += maglamp(92, 108, 34, .55) + maglamp(64, 128, 52, .8)
# 空的台座和空白牌子
c2 += pedestal(24, 116, 24, 22) + pedestal(80, 106, 16, 15)
c2 += pedestal(160, 112, 18, 16)
# 走在人行道上的人
c2 += walker(50, 142, GREEN, .82) + walker(196, 128, PINK, .7, back=True)
c2 += sparkle(30, 30) + star(80, 22, 5) + sparkle(220, 36, 3.4)
card('street', '手繪往遠處延伸的街道，路燈的燈頭做成放大鏡的形狀，人行道邊排著幾座台座，有人沿著人行道走', c2)

# 3. 舊館：兩層樓的博物館建築，門口有屋簷，前面是草地和小路
c3 = BG
c3 += cloud(30, 34, 1.0) + cloud(190, 26, .8)
c3 += f'<path d="M3,120 L237,120 {BOT}" fill="{FIELD}"/>'
c3 += trees([(26, 106, 12), (40, 112, 9), (214, 104, 13), (200, 114, 9)])
# 建築本體
c3 += f'<rect x="52" y="48" width="136" height="76" rx="3" fill="{WALL}"/>'
c3 += f'<rect x="46" y="40" width="148" height="10" rx="3" fill="{BROWN}"/>'
c3 += f'<path d="M52,86 L188,86" stroke-width="1.6" opacity=".5"/>'
c3 += ''.join(f'<rect x="{x}" y="58" width="18" height="18" rx="2" fill="{SKY}" stroke-width="1.6"/>' for x in (64, 92, 130, 158))
c3 += ''.join(f'<rect x="{x}" y="94" width="18" height="16" rx="2" fill="{SKY}" stroke-width="1.6"/>' for x in (64, 158))
# 門口：屋簷、玻璃門、空白的小看板
c3 += f'<rect x="100" y="96" width="40" height="28" rx="2" fill="{SKY}"/>'
c3 += f'<path d="M120,96 L120,124" stroke-width="1.6"/>'
c3 += f'<path d="M92,96 L148,96 L144,88 L96,88 Z" fill="{RED}"/>'
c3 += f'<rect x="150" y="112" width="18" height="16" rx="2" fill="{WHITE}" stroke-width="1.6"/>'
c3 += f'<path d="M154,128 L152,136 M164,128 L166,136" stroke-width="1.8"/>'
# 門口的小路和走進去的人
c3 += f'<path d="M104,124 L136,124 L156,177 L84,177 Z" fill="{ROAD}" stroke-width="1.8"/>'
c3 += walker(112, 136, RED, .78) + walker(132, 146, GOLD, .82)
c3 += f'<path d="M66,30 L66,40" stroke-width="1.6"/><path d="M66,30 L80,34 L66,38" fill="{GOLD}" stroke-width="1.4"/>'
c3 += sparkle(120, 22) + star(150, 18, 4.6) + sparkle(96, 28, 3)
card('museum', '手繪兩層樓的博物館，門口有紅色屋簷和玻璃門，前面的小路上有人走進去', c3)

# 4. 喫茶店：靠窗的小桌上一杯咖啡和一盤火腿三明治
c4 = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{WALL}"/>'
# 窗外是街景
c4 += f'<rect x="36" y="18" width="168" height="76" rx="8" fill="{SKYW}"/>'
c4 += f'<path d="M38,70 L202,70 L202,92 L38,92 Z" fill="{FIELD}" stroke="none"/>'
c4 += (f'<rect x="50" y="52" width="30" height="20" rx="2" fill="{WHITE}" stroke-width="1.8"/>'
       f'<path d="M46,54 L65,42 L84,54 Z" fill="{BRICK}" stroke-width="1.8"/>'
       f'<rect x="150" y="50" width="34" height="22" rx="2" fill="{WHITE}" stroke-width="1.8"/>'
       f'<path d="M146,52 L167,38 L188,52 Z" fill="{NAVY}" stroke-width="1.8"/>')
c4 += cloud(98, 40, .9)
c4 += f'<path d="M120,18 L120,94 M36,56 L204,56" stroke-width="3"/>'
c4 += f'<rect x="36" y="18" width="168" height="76" rx="8" fill="none" stroke-width="3"/>'
# 條紋遮雨棚
c4 += ''.join(f'<path d="M{x},10 L{x+21},10 L{x+21},22 Q{x+10.5},30 {x},22 Z" fill="{RED if i % 2 == 0 else WHITE}" stroke-width="1.8"/>'
              for i, x in enumerate(range(30, 210, 21)))
# 桌子
c4 += f'<path d="M30,112 L210,112 L218,132 L22,132 Z" fill="{BROWN}"/>'
c4 += f'<path d="M22,132 L218,132 L218,138 L22,138 Z" fill="{DBROWN}" stroke-width="1.8"/>'
c4 += f'<path d="M60,138 L56,172 M180,138 L184,172" stroke="{DBROWN}" stroke-width="5"/>'
# 咖啡杯＋盤子（冒熱氣）
c4 += f'<ellipse cx="72" cy="120" rx="26" ry="6" fill="{WHITE}" stroke-width="1.8"/>'
c4 += f'<path d="M86,100 q12,0 12,9 q0,9 -12,9" fill="none" stroke-width="2.6"/>'
c4 += f'<path d="M56,92 L88,92 L85,116 Q84,122 78,122 L66,122 Q60,122 59,116 Z" fill="{WHITE}"/>'
c4 += f'<ellipse cx="72" cy="92" rx="16" ry="4" fill="{DBROWN}" stroke-width="1.8"/>'
c4 += face(72, 106, .55)
c4 += f'<path d="M66,84 q-4,-5 0,-10 q4,-5 0,-10 M78,84 q-4,-5 0,-10 q4,-5 0,-10" fill="none" stroke-width="1.6" opacity=".6"/>'
# 火腿三明治＋盤子：兩塊三角形，切面看得到火腿和生菜
c4 += f'<ellipse cx="162" cy="122" rx="44" ry="8" fill="{WHITE}" stroke-width="1.8"/>'
c4 += f'<path d="M156,120 L184,84 L204,120 Z" fill="#f3d9a4"/>'
c4 += f'<path d="M124,120 L152,80 L180,120 Z" fill="#f3d9a4"/>'
c4 += f'<path d="M132,116 L152,88 L172,116 Z" fill="{CREAM}" stroke-width="1.4"/>'
c4 += f'<path d="M136,112 L168,112 L164,104 L140,104 Z" fill="{PINK}" stroke-width="1.4"/>'
c4 += f'<path d="M138,103 q3,-3 6,0 q3,-3 6,0 q3,-3 6,0 q3,-3 6,0 q3,-3 6,0" fill="none" stroke="{GREEN}" stroke-width="2.4"/>'
c4 += face(152, 96, .38, blush=False)
c4 += sparkle(110, 104, 3.4) + sparkle(212, 104, 3)
card('cafe', '手繪靠窗的小桌上擺著一杯冒熱氣的咖啡和一盤火腿三明治，窗外是小鎮的房子', c4)

# 5. 新館工地：圍籬裡的鋼骨和小吊車，旁邊是一排小商店
c5 = BG
c5 += cloud(26, 32, .9)
c5 += f'<path d="M3,124 L237,124 {BOT}" fill="{FIELD}"/>'
# 右邊一排有遮雨棚的小商店（不畫招牌）
for x, aw in [(166, GOLD), (198, GREEN)]:
    c5 += (f'<rect x="{x}" y="86" width="30" height="40" rx="2" fill="{WHITE}"/>'
           f'<path d="M{x-2},86 L{x+15},74 L{x+32},86 Z" fill="{BRICK}"/>'
           + ''.join(f'<path d="M{x+i*7.5:.1f},94 L{x+i*7.5+7.5:.1f},94 L{x+i*7.5+7.5:.1f},100 Q{x+i*7.5+3.75:.1f},104 {x+i*7.5:.1f},100 Z" '
                     f'fill="{aw if i % 2 == 0 else WHITE}" stroke-width="1.3"/>' for i in range(4))
           + f'<rect x="{x+8}" y="106" width="14" height="20" rx="1.6" fill="{SKY}" stroke-width="1.4"/>')
# 鋼骨
c5 += ''.join(f'<path d="M{x},124 L{x},70" stroke="#8fa0bb" stroke-width="5"/>' for x in (60, 92, 124))
c5 += ''.join(f'<path d="M56,{y} L128,{y}" stroke="#8fa0bb" stroke-width="4"/>' for y in (72, 98))
c5 += ''.join(f'<path d="M{x},{y} L{x+32},{y+26}" stroke="#8fa0bb" stroke-width="1.8"/>' for x in (60, 92) for y in (72,))
# 小吊車：履帶車身、駕駛室、斜伸的吊臂、垂下來的鉤子
c5 += f'<path d="M136,124 L136,116 Q136,112 140,112 L162,112 Q166,112 166,116 L166,124 Z" fill="{GOLD}"/>'
c5 += f'<rect x="132" y="122" width="38" height="8" rx="4" fill="{INK}"/>'
c5 += f'<rect x="146" y="98" width="16" height="14" rx="2" fill="{GOLD}"/>'
c5 += f'<rect x="150" y="101" width="8" height="7" rx="1.4" fill="{SKY}" stroke-width="1.2"/>'
c5 += f'<path d="M148,106 L96,30" stroke="{GOLD}" stroke-width="5"/><path d="M148,106 L96,30" stroke-width="1.2" stroke-dasharray="3 4"/>'
c5 += f'<path d="M96,30 L96,58" stroke-width="1.4"/><path d="M96,58 q4,0 4,4 q0,4 -4,4" fill="none" stroke-width="2"/>'
c5 += f'<rect x="88" y="66" width="16" height="6" rx="1.4" fill="{BROWN}" stroke-width="1.4"/>'
# 工地圍籬（白底、綠邊）和三角錐
c5 += ''.join(f'<rect x="{x}" y="112" width="24" height="26" rx="1.6" fill="{WHITE}" stroke-width="1.8"/>'
              f'<path d="M{x},116 L{x+24},116" stroke="{GREEN}" stroke-width="2.4"/>' for x in range(14, 134, 24))
c5 += ''.join(f'<path d="M{x-6},152 L{x},134 L{x+6},152 Z" fill="#f08a4b" stroke-width="1.8"/>'
              f'<path d="M{x-3},144 L{x+3},144" stroke="{WHITE}" stroke-width="2"/>'
              f'<rect x="{x-8}" y="151" width="16" height="4" rx="1.2" fill="#f08a4b" stroke-width="1.4"/>' for x in (30, 104))
# 前面經過的人
c5 += walker(176, 140, BLUE, .82)
c5 += sparkle(130, 26) + star(200, 30, 5) + sparkle(46, 60, 3.4)
card('newsite', '手繪圍籬裡蓋到一半的鋼骨和一台小吊車，旁邊是一排有遮雨棚的小商店，有人從前面經過', c5)

# 6. 寄放行李：櫃台後面一整面寄物櫃，櫃台上放著行李箱和背包
c6 = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{WALL}"/>'
# 寄物櫃：有的門關著（已經放滿），有的開著（還有空位）
_lk = [(30 + i * 30, 20 + j * 28) for j in range(3) for i in range(6)]
for k, (x, y) in enumerate(_lk):
    used = k in (0, 1, 2, 4, 6, 7, 9, 10, 11, 13)
    c6 += f'<rect x="{x}" y="{y}" width="28" height="26" rx="2" fill="{"#a9c4de" if used else "#6f8fae"}" stroke-width="1.8"/>'
    if used:
        c6 += f'<circle cx="{x+22}" cy="{y+13}" r="2" fill="{GOLD}" stroke-width="1"/>'
    else:
        c6 += f'<path d="M{x+3},{y+3} L{x+3},{y+23}" stroke="{WHITE}" stroke-width="1.4" opacity=".5"/>'
# 櫃台
c6 += f'<rect x="14" y="108" width="212" height="12" rx="3" fill="{BROWN}"/>'
c6 += f'<rect x="20" y="120" width="200" height="40" rx="2" fill="{DBROWN}"/>'
c6 += ''.join(f'<path d="M{x},126 L{x},154" stroke-width="1.2" opacity=".4"/>' for x in range(50, 220, 30))
c6 += f'<path d="M3,160 L237,160 {BOT}" fill="{STONE}"/>'
# 櫃台上的行李箱、背包和號碼牌（牌子上不寫字）
c6 += suitcase(40, 62, 36, 44, PINK)
c6 += f'<path d="M58,62 L64,52" stroke-width="1.4"/><rect x="60" y="44" width="12" height="9" rx="1.6" fill="{GOLD}" stroke-width="1.4" transform="rotate(-20 66 48)"/>'
c6 += (f'<path d="M98,108 L98,82 Q98,68 114,68 Q130,68 130,82 L130,108 Z" fill="{GREEN}"/>'
       f'<path d="M104,92 L124,92 L124,106 L104,106 Z" fill="{DGREEN}" stroke-width="1.6"/>'
       f'<path d="M106,70 q8,-10 16,0" fill="none" stroke-width="2.4"/>')
c6 += face(114, 80, .5)
c6 += f'<rect x="150" y="96" width="22" height="12" rx="2" fill="{WHITE}" stroke-width="1.6"/>'
c6 += f'<rect x="178" y="98" width="10" height="10" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
c6 += f'<path d="M180,98 L183,92 L186,98" fill="none" stroke-width="1.4"/>'
c6 += sparkle(214, 98, 3.4)
card('luggage', '手繪櫃台後面一整面寄物櫃，有的已經關上、有的還開著，櫃台上放著行李箱和背包', c6)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('cn-' + name, 120, 120, label, inner, bg='#fff3c4')


# 現在入館要先買前一天截止的網路票，賣完就沒有現場票
rem('r-ticket', '手繪提醒：要先用手機買好有 QR 碼的網路票，網路票賣完了，現場的售票窗口也買不到',
    f'<rect x="18" y="14" width="38" height="62" rx="7" fill="{NAVY}"/>'
    + f'<rect x="22" y="22" width="30" height="46" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
    + qr(25, 28, 24)
    + f'<path d="M27,58 L47,58 M27,63 L41,63" stroke="{GRAY}" stroke-width="2"/>'
    + f'<circle cx="52" cy="70" r="9" fill="{GREEN}" stroke-width="1.8"/>'
    + f'<path d="M47,70 L51,74 L57,66" fill="none" stroke="{WHITE}" stroke-width="2.4"/>'
    # 右下：關起來的售票窗口，打一個叉
    + f'<rect x="66" y="56" width="44" height="50" rx="3" fill="{BROWN}"/>'
    + f'<path d="M62,58 L70,46 L106,46 L114,58 Z" fill="{RED}"/>'
    + f'<rect x="71" y="64" width="34" height="25" rx="2" fill="{GRAY}" stroke-width="1.6"/>'
    + ''.join(f'<path d="M72,{y} L104,{y}" stroke-width="1.2" opacity=".6"/>' for y in (70, 76, 82))
    + f'<rect x="69" y="91" width="38" height="5" rx="1.4" fill="{DBROWN}" stroke-width="1.4"/>'
    + f'<path d="M78,66 L98,87 M98,66 L78,87" stroke="{RED}" stroke-width="3.4"/>'
    + sparkle(74, 22, 4) + sparkle(100, 32, 3))

# 2027/1/2 最後入館改成 16:00、16:30 閉館
rem('r-early', '手繪提醒：時鐘指著四點，博物館的門準備要關了',
    clock(42, 44, 28, 120, 0)
    # 右下：小博物館，兩扇門往中間關
    + f'<rect x="66" y="66" width="44" height="42" rx="2" fill="{WALL}"/>'
    + f'<rect x="63" y="58" width="50" height="9" rx="2.4" fill="{BROWN}"/>'
    + f'<rect x="76" y="80" width="26" height="28" rx="1.6" fill="{NAVY}"/>'
    + f'<rect x="76" y="80" width="10" height="28" rx="1.4" fill="{SKY}" stroke-width="1.6"/>'
    + f'<rect x="92" y="80" width="10" height="28" rx="1.4" fill="{SKY}" stroke-width="1.6"/>'
    + f'<path d="M86,94 l4,0 M92,94 l-4,0" stroke-width="1.6"/>'
    + f'<path d="M68,94 L74,94 M71,91 L74,94 L71,97 M108,94 L104,94 M106.5,91 L104,94 L106.5,97" fill="none" stroke="{RED}" stroke-width="1.8"/>'
    + f'<path d="M16,110 L104,110" stroke-width="2" opacity=".5"/>'
    + star(96, 20, 6) + sparkle(84, 36, 3.4))

# 日ノ丸巴士「由良駅入口」站在由良郵便局前、不在車站前；日交巴士「由良駅」站才在車站前
rem('r-bus', '手繪提醒：兩個公車站牌不在同一個地方，一個在紅色郵筒旁邊，一個在車站門口',
    # 左上：小車站和門口的站牌
    f'<rect x="16" y="32" width="42" height="24" rx="2" fill="{CREAM}"/>'
    + f'<path d="M10,34 L22,20 L52,20 L64,34 Z" fill="{BRICK}"/>'
    + f'<rect x="32" y="40" width="10" height="16" rx="1.4" fill="{DBROWN}" stroke-width="1.4"/>'
    + f'<path d="M72,56 L72,28" stroke="{INK}" stroke-width="2.4"/>'
    + f'<circle cx="72" cy="24" r="8" fill="{GREEN}" stroke-width="1.8"/><circle cx="72" cy="24" r="3.4" fill="{WHITE}" stroke-width="1.2"/>'
    + f'<rect x="66" y="54" width="12" height="4" rx="1.2" fill="{GRAY}" stroke-width="1.2"/>'
    # 中間：一條虛線的路，表示兩站隔一段距離
    + f'<path d="M78,62 Q90,72 70,76 Q56,78 50,76" fill="none" stroke="{DBROWN}" stroke-width="1.8" stroke-dasharray="4 4"/>'
    # 右下：另一個站牌在紅色郵筒和小房子旁
    + f'<rect x="78" y="82" width="32" height="26" rx="2" fill="{WHITE}"/>'
    + f'<path d="M74,84 L94,70 L113,84 Z" fill="{NAVY}"/>'
    + f'<rect x="88" y="93" width="12" height="15" rx="1.4" fill="{SKY}" stroke-width="1.4"/>'
    + f'<rect x="56" y="88" width="12" height="20" rx="3" fill="{RED}"/>'
    + f'<path d="M56,92 Q62,84 68,92" fill="{RED}" stroke-width="1.6"/>'
    + f'<path d="M59,96 L65,96" stroke-width="1.6"/>'
    + f'<path d="M40,108 L40,80" stroke="{INK}" stroke-width="2.4"/>'
    + f'<circle cx="40" cy="78" r="8" fill="{GOLD}" stroke-width="1.8"/><circle cx="40" cy="78" r="3.4" fill="{WHITE}" stroke-width="1.2"/>'
    + f'<rect x="34" y="106" width="12" height="4" rx="1.2" fill="{GRAY}" stroke-width="1.2"/>'
    + f'<path d="M16,111 L104,111" stroke-width="2" opacity=".5"/>'
    + sparkle(100, 18, 4) + sparkle(16, 72, 3))

print(save(F, OUT), 'files')
