# 豪斯登堡頁的「園區裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網地圖頁（huistenbosch.co.jp/map/）與各設施頁的介紹畫成可愛版，不描照片構圖；
# 米飛兔等角色 IP 一律不畫。
# 輸出 illust/sp/nagasaki-huis-ten-bosch/*.svg。說明文字放在 illust/spots/nagasaki-huis-ten-bosch.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'nagasaki-huis-ten-bosch')
W, H = 240, 180
F = {}
SKYB = '#dff0fd'
WATER = '#9fd0ec'
NIGHT = '#34416e'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('htb-' + name, W, H, label, inner, bg=bg)


def windmill(x, base, s=1.0, rot=15, face_on=True):
    # 荷蘭風車：梯形塔身＋四片扇葉
    t = (f'<path d="M{x-16*s},{base} L{x-10*s},{base-56*s} L{x+10*s},{base-56*s} L{x+16*s},{base} Z" fill="#e9dcc8"/>'
         f'<path d="M{x-12*s},{base-56*s} Q{x},{base-72*s} {x+12*s},{base-56*s} Z" fill="{BRICK}"/>'
         f'<rect x="{x-5*s}" y="{base-16*s}" width="{10*s}" height="{16*s}" rx="{4*s}" fill="{DBROWN}"/>')
    hub = (x, base - 58 * s)
    for k in range(4):
        a = rot + 90 * k
        t += (f'<g transform="rotate({a} {hub[0]} {hub[1]})">'
              f'<rect x="{hub[0]-4*s}" y="{hub[1]-46*s}" width="{10*s}" height="{40*s}" fill="{WHITE}" stroke-width="1.6"/>'
              + ''.join(f'<path d="M{hub[0]-4*s},{hub[1]-(14+8*j)*s} L{hub[0]+6*s},{hub[1]-(14+8*j)*s}" stroke-width="1"/>' for j in range(4))
              + '</g>')
    t += f'<circle cx="{hub[0]}" cy="{hub[1]}" r="{4*s}" fill="{GOLD}"/>'
    if face_on:
        t += face(x, base - 34 * s, .7 * s)
    return t


def tulips(x0, x1, y, cols=(RED, PINK, GOLD, '#f2a46b')):
    t = ''
    for i, x in enumerate(range(x0, x1, 12)):
        yy = y + (i % 2) * 6
        t += (f'<path d="M{x},{yy+14} L{x},{yy+4}" stroke="{DGREEN}" stroke-width="1.6"/>'
              f'<path d="M{x-5},{yy} q0,7 5,7 q5,0 5,-7 l-2.5,3 l-2.5,-4 l-2.5,4 Z" fill="{cols[i % len(cols)]}" stroke-width="1.3"/>')
    return t


def house(x, base, w, h, col, roof=BRICK):
    # 荷蘭式階梯山牆小屋
    t = (f'<path d="M{x},{base} L{x},{base-h} L{x+w*.2},{base-h} L{x+w*.2},{base-h-8} L{x+w*.35},{base-h-8} '
         f'L{x+w*.35},{base-h-16} L{x+w*.65},{base-h-16} L{x+w*.65},{base-h-8} L{x+w*.8},{base-h-8} L{x+w*.8},{base-h} '
         f'L{x+w},{base-h} L{x+w},{base} Z" fill="{col}"/>')
    t += f'<rect x="{x+w*.32}" y="{base-h+4}" width="{w*.36}" height="{h*.3:.1f}" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    t += f'<rect x="{x+w*.32}" y="{base-h*.5:.1f}" width="{w*.36}" height="{h*.3:.1f}" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    return t


# 1. 花之路：入口附近的風車與花田
card('windmill', '手繪荷蘭風車和一片鬱金香花田',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,124 Q80,114 160,122 T237,118 {BOT}" fill="#a9d8b1"/>'
     + windmill(80, 128, 1.15, 20) + windmill(186, 122, .75, 50, False)
     + tulips(14, 236, 138)
     + sparkle(30, 36) + star(140, 30, 7), bg=SKYB)

# 2. 運河與運河船
card('canal', '手繪運河上的古典遊船，岸邊是荷蘭式房子',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + house(14, 104, 44, 52, '#f3c9a0') + house(60, 104, 40, 62, '#cfe3c4', DBROWN) + house(102, 104, 44, 48, '#f6d3d8')
     + house(148, 104, 40, 58, '#e9dcc8') + house(190, 104, 40, 50, '#d6e2f2')
     + f'<path d="M3,104 L237,104 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WATER}"/>'
     # 船
     + f'<path d="M56,128 L184,128 Q178,148 160,150 L80,150 Q62,148 56,128 Z" fill="{WHITE}"/>'
     f'<path d="M58,136 L182,136" stroke="{NAVY}" stroke-width="3"/>'
     f'<rect x="84" y="112" width="70" height="16" rx="4" fill="{NAVY}"/>'
     + ''.join(f'<rect x="{x}" y="115" width="10" height="9" rx="2" fill="{SKY}" stroke-width="1.2"/>' for x in (90, 104, 118, 132))
     + f'<path d="M170,128 L170,110 M170,110 L182,114 L170,118" stroke-width="1.8" fill="{RED}"/>'
     + face(120, 142, .7)
     + ''.join(f'<path d="M{x},{y} q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>' for x, y in [(20, 120), (196, 124), (30, 160), (200, 160)])
     + sparkle(120, 30), bg=SKYB)

# 3. 象徵塔：高 105 公尺，80 公尺有展望室
card('tower', '手繪很高的象徵塔，上面的展望室可以看到海',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,132 Q60,124 120,130 T237,126 {BOT}" fill="{WATER}"/>'
     + f'<path d="M3,150 Q80,140 160,148 T237,144 {BOT}" fill="#a9d8b1"/>'
     + f'<rect x="96" y="66" width="48" height="84" fill="#e9c9a0"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="8" height="12" rx="3" fill="{SKY}" stroke-width="1.2"/>' for x in (104, 116, 128) for y in (100, 124))
     + f'<rect x="102" y="40" width="36" height="26" fill="#e9c9a0"/>'
     f'<rect x="92" y="62" width="56" height="8" rx="2" fill="{BRICK}"/>'
     f'<rect x="106" y="46" width="28" height="12" rx="3" fill="{SKY}" stroke-width="1.4"/>'
     f'<circle cx="114" cy="52" r="3.4" fill="#f9d9c0" stroke-width="1.2"/><circle cx="126" cy="52" r="3.4" fill="#f9d9c0" stroke-width="1.2"/>'
     f'<path d="M104,40 Q120,6 136,40 Z" fill="{GREEN}"/>'
     f'<path d="M120,24 L120,13" stroke-width="2"/>'
     f'<circle cx="120" cy="80" r="8" fill="{WHITE}" stroke-width="1.6"/><path d="M120,80 L120,75 M120,80 L124,82" stroke-width="1.4"/>'
     + windmill(40, 150, .5, 10, False) + house(170, 150, 36, 40, '#f6d3d8')
     + f'<path d="M150,46 q8,-6 16,0 M160,60 q8,-6 16,0" fill="none" stroke-width="1.6"/>'
     + sparkle(44, 36) + star(200, 30, 7), bg=SKYB)

# 4. 豪斯登堡宮殿：重現荷蘭宮殿
card('palace', '手繪左右對稱的宮殿和前面的庭園',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,124 L237,124 {BOT}" fill="#a9d8b1"/>'
     + f'<rect x="40" y="66" width="160" height="58" fill="#f3e2c0"/>'
     f'<rect x="92" y="46" width="56" height="78" fill="#f3e2c0"/>'
     f'<path d="M88,48 L120,24 L152,48 Z" fill="{NAVY}"/>'
     f'<path d="M36,68 L60,54 L180,54 L204,68 Z" fill="{NAVY}"/>'
     f'<rect x="88" y="44" width="64" height="6" rx="2" fill="{GOLD}"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="12" height="16" rx="5" fill="{SKY}" stroke-width="1.4"/>' for x in (50, 70, 160, 178) for y in (76, 100))
     + f'<path d="M108,124 L108,98 Q120,84 132,98 L132,124 Z" fill="{DBROWN}"/>'
     + face(120, 70, .8)
     + ''.join(f'<path d="M{x},{y} q14,-8 28,0 q-14,8 -28,0 Z" fill="{GREEN}" stroke-width="1.4"/>' for x, y in [(22, 146), (70, 154), (142, 154), (190, 146)])
     + f'<path d="M120,126 L120,168" stroke="#e9dcc8" stroke-width="10"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{c}" stroke-width="1.2"/>' for x, y, c in [(36, 136, PINK), (56, 140, GOLD), (180, 138, PINK), (204, 136, GOLD)])
     + sparkle(30, 30) + star(206, 28, 7), bg=SKYB)

# 5. 燈海：整個園區的燈飾
card('lights', '手繪夜晚的街道和運河，到處都是閃亮的燈飾',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + house(14, 110, 44, 52, '#5e6aa0') + house(62, 110, 40, 64, '#6a5e9a') + house(140, 110, 44, 54, '#5e6aa0') + house(188, 110, 40, 48, '#6a5e9a')
     + f'<path d="M3,110 L237,110 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#2a3358"/>'
     + lights(10, 70, 120, 56, 20, 8) + lights(120, 56, 232, 72, 18, 8)
     + windmill(120, 112, .6, 30, False)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{c}" stroke="none"/>' for x, y, c in
               [(24, 30, GOLD), (60, 22, WHITE), (180, 26, GOLD), (214, 40, WHITE), (150, 18, '#8ff0ff')])
     + ''.join(f'<path d="M{x},{y} L{x+14},{y}" stroke="{c}" stroke-width="2.6" opacity=".8"/>' for x, y, c in
               [(20, 126, GOLD), (60, 136, PINK), (110, 128, GOLD), (160, 140, '#8ff0ff'), (200, 128, PINK), (40, 150, '#8ff0ff'), (140, 156, GOLD)])
     + star(120, 22, 8), bg=NIGHT)

# 6. 港區的煙火
card('fireworks', '手繪港口上空的煙火',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(
         ''.join(f'<path d="M{cx+r*.25*math.cos(k*math.pi/6):.1f},{cy+r*.25*math.sin(k*math.pi/6):.1f} L{cx+r*math.cos(k*math.pi/6):.1f},{cy+r*math.sin(k*math.pi/6):.1f}" stroke="{c}" stroke-width="2.6"/>' for k in range(12))
         + ''.join(f'<circle cx="{cx+(r+5)*math.cos(k*math.pi/6):.1f}" cy="{cy+(r+5)*math.sin(k*math.pi/6):.1f}" r="2" fill="{c}" stroke="none"/>' for k in range(12))
         for cx, cy, r, c in [(70, 54, 30, PINK), (160, 46, 34, GOLD), (204, 92, 18, '#8ff0ff'), (34, 104, 14, GOLD)])
     + f'<path d="M3,130 L237,130 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#2a3358"/>'
     + ''.join(f'<path d="M{x},{y} L{x+16},{y}" stroke="{c}" stroke-width="2.4" opacity=".75"/>' for x, y, c in
               [(60, 140, PINK), (150, 144, GOLD), (100, 156, PINK), (180, 158, GOLD)])
     + f'<path d="M20,130 L20,112 L48,112 L48,130" fill="#6a5e9a"/><path d="M196,130 L196,116 L226,116 L226,130" fill="#6a5e9a"/>'
     + f'<path d="M100,138 L140,138 Q136,148 128,148 L112,148 Q104,148 100,138 Z" fill="{WHITE}"/><path d="M120,138 L120,122 L132,132 Z" fill="{GOLD}" stroke-width="1.4"/>',
     bg=NIGHT)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('htb-' + name, 120, 120, label, inner, bg='#fff3c4')


# 港區平常免費，花火日要票
rem('r-harbor', '手繪提醒：港口的煙火和一張門票',
    ''.join(f'<path d="M50,36 L{50+22*math.cos(k*math.pi/4):.1f},{36+22*math.sin(k*math.pi/4):.1f}" stroke="{c}" stroke-width="2.4"/>'
            for k, c in zip(range(8), [RED, GOLD, PINK, GOLD, RED, GOLD, PINK, GOLD]))
    + f'<path d="M8,80 q10,-6 20,0 t20,0 t20,0 t20,0 t20,0 t20,0" fill="none" stroke="#7fc4e8" stroke-width="3"/>'
    f'<g transform="rotate(-10 86 74)"><rect x="64" y="58" width="46" height="28" rx="4" fill="{PINK}"/>'
    f'<path d="M98,58 L98,86" stroke-dasharray="3 3" stroke-width="1.6"/><circle cx="80" cy="72" r="5" fill="{WHITE}" stroke-width="1.4"/></g>'
    f'<path d="M14,104 L106,104" stroke-width="2"/>')

# 運河船是單程
rem('r-canal', '手繪提醒：船只往一個方向開',
    f'<path d="M8,74 q10,-6 20,0 t20,0 t20,0 t20,0 t20,0 t20,0" fill="none" stroke="#7fc4e8" stroke-width="3"/>'
    f'<path d="M20,60 L92,60 Q88,72 78,74 L34,74 Q24,72 20,60 Z" fill="{WHITE}"/>'
    f'<rect x="36" y="48" width="38" height="12" rx="3" fill="{NAVY}"/>'
    f'<path d="M24,94 L94,94 M84,86 L94,94 L84,102" stroke="{RED}" stroke-width="3" fill="none"/>'
    f'<path d="M92,22 a14,14 0 1 1 -18,4" fill="none" stroke="{GRAY}" stroke-width="2.6"/>'
    f'<path d="M80,18 L102,40 M102,18 L80,40" stroke="{RED}" stroke-width="3"/>')

print(save(F, OUT), 'files')
