# 大阪周遊卡頁的「一張卡能去哪裡」插圖與提醒卡（2026-11-13）。
# 畫周遊卡能免費進的代表景點與能搭的交通工具，參考官方網站（osaka-amazing-pass.com）與
# osakapass.json 的設施清單；不描照片構圖，不畫任何商標、看板或角色。
# 輸出 illust/sp/osaka-amazing-pass/*.svg。說明文字放在 illust/spots/osaka-amazing-pass.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'osaka-amazing-pass')
W, H = 240, 180
F = {}
SKYB = '#dff0fd'
WATER = '#9fd0ec'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('oap-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def roof(cx, y, w, h=14, col='#6fa59a'):
    # 日式城郭的翹角屋頂
    return (f'<path d="M{cx-w/2-8},{y} Q{cx-w/2},{y-2} {cx-w/2+6},{y-h} L{cx+w/2-6},{y-h} Q{cx+w/2},{y-2} {cx+w/2+8},{y} Z" fill="{col}"/>')


# 1. 大阪城天守閣
card('castle', '手繪大阪城天守閣，下面是石牆',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,150 L237,150 {BOT}" fill="#a9d8b1"/>'
     + f'<path d="M50,150 L64,112 L176,112 L190,150 Z" fill="#cfc7b8"/>'
     + ''.join(f'<path d="M{60+i*2},{150-i*10} L{180-i*2},{150-i*10}" stroke-width="1" opacity=".5"/>' for i in range(1, 4))
     + f'<rect x="78" y="88" width="84" height="24" fill="{WHITE}"/>' + roof(120, 90, 92)
     + f'<rect x="86" y="66" width="68" height="22" fill="{WHITE}"/>' + roof(120, 68, 76)
     + f'<rect x="94" y="46" width="52" height="20" fill="{WHITE}"/>' + roof(120, 48, 60)
     + f'<rect x="102" y="28" width="36" height="18" fill="{WHITE}"/>' + roof(120, 30, 44, 12)
     + ''.join(f'<rect x="{x}" y="{y}" width="8" height="8" rx="1" fill="{GOLD}" stroke-width="1.2"/>' for x, y in
               [(90, 96), (116, 96), (142, 96), (98, 74), (132, 74), (108, 52), (124, 52)])
     + f'<path d="M104,18 q-4,-6 2,-8 M136,18 q4,-6 -2,-8" stroke="{GOLD}" stroke-width="3" fill="none"/>'
     + face(120, 38, .65)
     + ''.join(f'<path d="M{x},{y} q-6,-14 0,-22 q6,8 0,22" fill="{GREEN}" stroke-width="1.4"/>' for x, y in [(30, 150), (40, 150), (204, 150), (214, 150)])
     + sparkle(40, 36) + star(204, 34, 7), bg=SKYB)

# 2. 梅田藍天大廈空中庭園展望台
card('sky', '手繪兩棟大樓在頂端連在一起的高樓，頂上有人在看風景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#ffe7cf"/>'
     f'<circle cx="196" cy="120" r="20" fill="#f6b26b" stroke="none" opacity=".8"/>'
     + f'<path d="M3,150 L237,150 {BOT}" fill="#cfd8e6"/>'
     + f'<rect x="70" y="50" width="34" height="100" fill="{GRAY}"/><rect x="136" y="50" width="34" height="100" fill="{GRAY}"/>'
     + ''.join(f'<path d="M{x},{y} L{x+26},{y}" stroke-width="1" opacity=".55"/>' for x in (74, 140) for y in range(62, 150, 10))
     + f'<rect x="64" y="32" width="112" height="20" rx="4" fill="{SKY}"/>'
     + f'<path d="M64,32 L176,32" stroke-width="2.4"/>'
     + f'<path d="M104,110 L136,110 L136,96 L104,96 Z" fill="{SKY}"/>'
     + f'<circle cx="92" cy="26" r="5" fill="#f9d9c0"/><circle cx="108" cy="26" r="5" fill="#f9d9c0"/><circle cx="148" cy="26" r="5" fill="#f9d9c0"/>'
     + f'<path d="M64,32 L64,22 L176,22 L176,32" fill="none" stroke-width="1.6"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{150-y}" fill="#e9dcc8"/>' for x, y, w in [(16, 110, 30), (196, 118, 28), (40, 126, 22)])
     + sparkle(36, 40) + star(210, 40, 7), bg='#ffe7cf')

# 3. 通天閣與溜滑梯
card('tower', '手繪通天閣，塔身旁邊有一條往下繞的溜滑梯',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,150 L237,150 {BOT}" fill="#e9dcc8"/>'
     + f'<path d="M84,150 L106,70 L134,70 L156,150 L140,150 L120,100 L100,150 Z" fill="{GRAY}"/>'
     + f'<path d="M96,108 L144,108" stroke-width="2"/>'
     + f'<rect x="100" y="54" width="40" height="18" rx="3" fill="{WHITE}"/>'
     + f'<rect x="106" y="30" width="28" height="24" rx="3" fill="{GRAY}"/>'
     + f'<rect x="102" y="24" width="36" height="8" rx="3" fill="{WHITE}"/>'
     + f'<path d="M120,24 L120,10" stroke-width="2"/>'
     + f'<circle cx="120" cy="42" r="7" fill="{WHITE}" stroke-width="1.4"/>'
     + f'<path d="M100,62 L140,62" stroke="{GOLD}" stroke-width="3"/>'
     # 溜滑梯：從塔下層繞出來
     + f'<path d="M144,96 Q190,96 186,116 Q182,134 150,132 Q126,130 132,146 L150,148" fill="none" stroke="{RED}" stroke-width="7"/>'
     + f'<path d="M144,96 Q190,96 186,116 Q182,134 150,132 Q126,130 132,146 L150,148" fill="none" stroke-width="1.2"/>'
     + person(184, 106, GOLD, .7)
     + f'<path d="M196,98 q6,-2 8,-8 M196,108 q8,0 10,-6" fill="none" stroke-width="1.4"/>'
     + sparkle(40, 40) + star(60, 80, 6) + star(200, 34, 7), bg=SKYB)

# 4. 道頓堀水上觀光船
card('river', '手繪河道上的觀光船，兩岸是大樓和燈',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#ffe7cf"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{100-y}" fill="{c}"/>' for x, y, w, c in
               [(10, 40, 34, '#e9c9a0'), (46, 56, 30, '#f6d3d8'), (78, 30, 30, '#cfe3c4'), (132, 46, 34, '#d6e2f2'), (168, 36, 30, '#f3c9a0'), (200, 52, 34, '#e9dcc8')])
     + ''.join(f'<rect x="{x}" y="{y}" width="8" height="8" rx="1" fill="{GOLD}" stroke-width="1.2"/>' for x, y in
               [(18, 52), (30, 68), (54, 66), (86, 42), (92, 60), (140, 58), (152, 74), (176, 48), (184, 66), (210, 64)])
     + f'<path d="M3,100 L237,100 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WATER}"/>'
     + f'<path d="M3,100 L237,100" stroke-width="2"/>'
     + f'<path d="M108,100 Q120,80 132,100" fill="none" stroke="{BRICK}" stroke-width="5"/>'
     + f'<path d="M60,126 L180,126 Q174,146 156,148 L84,148 Q66,146 60,126 Z" fill="{WHITE}"/>'
     + f'<path d="M62,134 L178,134" stroke="{RED}" stroke-width="3"/>'
     + person(92, 108, PINK, .65) + person(112, 110, GOLD, .65) + person(132, 108, GREEN, .65) + person(152, 110, SKY, .65)
     + face(120, 140, .6)
     + ''.join(f'<path d="M{x},{y} L{x+16},{y}" stroke="{c}" stroke-width="2.4" opacity=".8"/>' for x, y, c in
               [(20, 116, GOLD), (196, 118, PINK), (30, 160, PINK), (190, 160, GOLD)]), bg='#ffe7cf')

# 5. 天保山大摩天輪
card('wheel', '手繪港邊的大摩天輪',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,140 Q60,132 120,140 T237,134 {BOT}" fill="{WATER}"/>'
     + f'<circle cx="120" cy="78" r="58" fill="none" stroke-width="3"/>'
     + f'<circle cx="120" cy="78" r="48" fill="none" stroke-width="1.2"/>'
     + ''.join(f'<path d="M120,78 L{120+58*math.cos(k*math.pi/8):.1f},{78+58*math.sin(k*math.pi/8):.1f}" stroke-width="1.1"/>' for k in range(16))
     + ''.join(f'<rect x="{120+58*math.cos(k*math.pi/6)-6:.1f}" y="{78+58*math.sin(k*math.pi/6)-5:.1f}" width="12" height="11" rx="3" fill="{c}" stroke-width="1.4"/>'
               for k, c in zip(range(12), [PINK, GOLD, SKY, GREEN] * 3))
     + f'<circle cx="120" cy="78" r="12" fill="{GOLD}"/>' + face(120, 77, .55)
     + f'<path d="M120,78 L96,146 M120,78 L144,146" stroke-width="3"/>'
     + f'<rect x="84" y="140" width="72" height="8" rx="2" fill="{DBROWN}"/>'
     + sparkle(32, 36) + star(212, 32, 7)
     + ''.join(f'<path d="M{x},{y} q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>' for x, y in [(24, 156), (196, 158)]), bg=SKYB)

# 6. 地鐵：Osaka Metro 全線
card('metro', '手繪地鐵列車從月台開出來',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e8e2f3"/>'
     f'<path d="M3,40 Q120,6 237,40 L237,52 Q120,20 3,52 Z" fill="{GRAY}"/>'
     + ''.join(f'<circle cx="{x}" cy="40" r="5" fill="{GOLD}" stroke-width="1.2"/>' for x in (50, 120, 190))
     + f'<path d="M3,140 L237,140 {BOT}" fill="#cfc7b8"/>'
     + f'<path d="M3,150 L237,150" stroke-width="2"/><path d="M3,160 L237,160" stroke-width="2"/>'
     + f'<path d="M30,140 L30,72 Q30,62 44,62 L196,62 Q214,62 220,80 L226,140 Z" fill="{WHITE}"/>'
     + f'<path d="M30,116 L226,116" stroke="{RED}" stroke-width="6"/>'
     + ''.join(f'<rect x="{x}" y="74" width="24" height="26" rx="4" fill="{SKY}" stroke-width="1.6"/>' for x in (42, 74, 106, 138))
     + f'<path d="M172,74 L198,74 Q212,74 214,90 L214,100 L172,100 Z" fill="{SKY}"/>'
     + face(193, 90, .8)
     + ''.join(f'<circle cx="{x}" cy="142" r="6" fill="{INK}"/>' for x in (60, 92, 160, 196))
     + f'<circle cx="220" cy="124" r="3.4" fill="{GOLD}" stroke-width="1.2"/>', bg='#e8e2f3')


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('oap-' + name, 120, 120, label, inner, bg='#fff3c4')


# 凌晨 3 點換日
rem('r-3am', '手繪提醒：月亮和指著 3 點的時鐘',
    f'<circle cx="60" cy="64" r="34" fill="{WHITE}"/>'
    + ''.join(f'<circle cx="{60+28*math.cos(k*math.pi/6):.1f}" cy="{64+28*math.sin(k*math.pi/6):.1f}" r="1.6" fill="{INK}" stroke="none"/>' for k in range(12))
    + f'<path d="M60,64 L60,42 M60,64 L80,64" stroke-width="3"/>'
    f'<circle cx="60" cy="64" r="3" fill="{RED}" stroke="none"/>'
    f'<path d="M100,18 a12,12 0 1 0 8,20 a9,9 0 1 1 -8,-20 Z" fill="{GOLD}" stroke-width="1.6"/>'
    + star(18, 22, 5) + star(104, 100, 4))

# 空中庭園 15:00 前入場才免費
rem('r-sunset', '手繪提醒：高樓和下午 3 點的時鐘',
    f'<rect x="12" y="40" width="20" height="64" fill="{GRAY}"/><rect x="44" y="40" width="20" height="64" fill="{GRAY}"/>'
    f'<rect x="8" y="30" width="60" height="12" rx="3" fill="{SKY}"/>'
    f'<circle cx="88" cy="48" r="22" fill="{WHITE}"/>'
    f'<path d="M88,48 L88,32 M88,48 L102,48" stroke-width="2.6"/>'
    f'<path d="M72,88 a16,16 0 0 1 32,0 Z" fill="#f6b26b"/>'
    f'<path d="M66,104 L110,104 M6,104 L66,104" stroke-width="2"/>')

# 道頓堀船要先換班次
rem('r-boat', '手繪提醒：觀光船和一張班次券',
    f'<path d="M8,84 q10,-6 20,0 t20,0 t20,0 t20,0 t20,0 t20,0" fill="none" stroke="#7fc4e8" stroke-width="3"/>'
    f'<path d="M12,66 L76,66 Q72,80 62,82 L26,82 Q16,80 12,66 Z" fill="{WHITE}"/>'
    f'<path d="M14,72 L74,72" stroke="{RED}" stroke-width="2.4"/>'
    f'<g transform="rotate(8 88 36)"><rect x="66" y="18" width="44" height="34" rx="4" fill="{PINK}"/>'
    f'<path d="M98,18 L98,52" stroke-dasharray="3 3" stroke-width="1.6"/>'
    f'<path d="M72,30 L92,30 M72,40 L88,40" stroke-width="2"/></g>'
    f'<path d="M14,104 L106,104" stroke-width="2"/>')

print(save(F, OUT), 'files')
