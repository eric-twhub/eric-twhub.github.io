# 富士急樂園頁的「樂園裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網アトラクション頁（fujiq.jp/attraction/）的介紹畫成可愛版，不描照片構圖；
# 角色 IP（湯瑪士、進擊的巨人、San-X 等）一律不畫。
# 輸出 illust/sp/japan-fuji-q/*.svg。說明文字放在 illust/spots/japan-fuji-q.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-fuji-q')
W, H = 240, 180
F = {}
SKYB = '#dff0fd'
FUJI = '#8fa8d6'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('fq-' + name, W, H, label, inner, bg=bg)


def fuji(x, base, w=150, h=70, col=FUJI):
    # 富士山：藍灰色山體＋白色山頂積雪
    l, r = x - w / 2, x + w / 2
    return (f'<path d="M{l},{base} L{x-14},{base-h} Q{x},{base-h-4} {x+14},{base-h} L{r},{base} Z" fill="{col}"/>'
            f'<path d="M{x-14},{base-h} Q{x},{base-h-4} {x+14},{base-h} L{x+26},{base-h+22} '
            f'q-8,6 -14,-2 q-6,8 -12,0 q-6,8 -12,0 q-6,8 -14,2 Z" fill="{WHITE}"/>')


def car(x, y, col=RED, rot=0, s=1.0):
    # 一節可愛的雲霄飛車車廂，坐兩個人
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<circle cx="-8" cy="-14" r="6" fill="#f9d9c0"/><circle cx="8" cy="-14" r="6" fill="#f9d9c0"/>'
            f'<path d="M-12,-20 l-3,-7 M12,-20 l3,-7" stroke-width="1.6"/>'
            f'<rect x="-18" y="-10" width="36" height="14" rx="5" fill="{col}"/>'
            f'<circle cx="-10" cy="6" r="3.2" fill="{GRAY}" stroke-width="1.4"/><circle cx="10" cy="6" r="3.2" fill="{GRAY}" stroke-width="1.4"/>'
            f'</g>')


def clouds(pts):
    return ''.join(f'<path d="M{x},{y} q4,-10 14,-6 q6,-8 14,0 q10,-2 10,8 Z" fill="{WHITE}" stroke-width="1.6"/>' for x, y in pts)


# 1. FUJIYAMA：沒有翻圈的大型雲霄飛車，背景富士山
card('fujiyama', '手繪大型雲霄飛車，背後是富士山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + fuji(168, 150, 124, 70)
     + clouds([(20, 40)])
     + ''.join(f'<path d="M{x},{150} L{x},{y}" stroke="{DBROWN}" stroke-width="1.8"/>' for x, y in
               [(30, 120), (44, 74), (58, 40), (72, 46), (86, 90), (100, 128), (128, 112), (150, 100), (176, 112), (200, 132)])
     + f'<path d="M14,142 Q40,140 52,40 Q60,24 70,40 Q86,140 112,130 Q150,82 182,110 Q204,130 230,132" fill="none" stroke="{RED}" stroke-width="5"/>'
     + f'<path d="M14,142 Q40,140 52,40 Q60,24 70,40 Q86,140 112,130 Q150,82 182,110 Q204,130 230,132" fill="none" stroke-width="1.4"/>'
     + car(44, 82, GOLD, -72, .8)
     + f'<path d="M3,150 Q60,144 120,150 T237,148 {BOT}" fill="#a9d8b1"/>'
     + sparkle(120, 30) + star(210, 30, 7), bg=SKYB)

# 2. 高飛車：最大落下角度 121 度，比垂直還陡
card('takabisha', '手繪比垂直還陡、往內側掉下去的雲霄飛車軌道',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + fuji(60, 150, 110, 52)
     + f'<path d="M3,150 Q60,144 120,150 T237,148 {BOT}" fill="#a9d8b1"/>'
     # 往上爬到頂，再往內側（左下）掉
     + f'<path d="M232,140 L170,140 Q150,140 150,120 L150,40 Q150,20 132,24 Q118,28 124,60 L140,140" fill="none" stroke="{NAVY}" stroke-width="5"/>'
     + f'<path d="M232,140 L170,140 Q150,140 150,120 L150,40 Q150,20 132,24 Q118,28 124,60 L140,140" fill="none" stroke-width="1.4" stroke="{GRAY}"/>'
     + ''.join(f'<path d="M150,{y} L162,{y}" stroke-width="1.6"/>' for y in (60, 80, 100, 120))
     + f'<path d="M162,40 L162,150" stroke="{DBROWN}" stroke-width="2"/>'
     + car(128, 34, RED, -150, .75)
     # 角度記號
     + f'<path d="M124,96 L124,70 M124,96 A26,26 0 0 0 104,80" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="4 3"/>'
     + f'<path d="M100,40 q-6,-6 -12,0 M96,52 q-6,-6 -12,0" fill="none" stroke-width="1.6"/>'
     + sparkle(200, 36) + star(212, 74, 6), bg=SKYB)

# 3. ええじゃないか：座椅會一直轉圈的雲霄飛車
card('eejanaika', '手繪座椅一直轉圈的雲霄飛車，旁邊畫了轉圈的箭頭',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#efe4fa"/>'
     + f'<path d="M3,150 Q60,144 120,150 T237,148 {BOT}" fill="#a9d8b1"/>'
     + ''.join(f'<path d="M{x},150 L{x},{y}" stroke="{DBROWN}" stroke-width="1.8"/>' for x, y in [(40, 110), (90, 70), (150, 70), (200, 110)])
     + f'<path d="M14,120 Q50,40 120,52 Q190,64 226,120" fill="none" stroke="{GOLD}" stroke-width="5"/>'
     + f'<path d="M14,120 Q50,40 120,52 Q190,64 226,120" fill="none" stroke-width="1.4"/>'
     + car(84, 74, PINK, 160, .85) + car(150, 76, SKY, -40, .85)
     + f'<path d="M100,96 a14,14 0 1 1 6,-24" fill="none" stroke="{RED}" stroke-width="2.2"/><path d="M106,72 l-8,-2 l4,8" fill="{RED}" stroke="{RED}" stroke-width="1.6"/>'
     + f'<path d="M168,104 a14,14 0 1 0 -6,-26" fill="none" stroke="{RED}" stroke-width="2.2"/><path d="M162,78 l8,-1 l-4,8" fill="{RED}" stroke="{RED}" stroke-width="1.6"/>'
     + sparkle(36, 36) + sparkle(204, 30) + star(120, 24, 7), bg='#efe4fa')

# 4. FUJIYAMA 展望台：高 55 公尺看富士山
card('skydeck', '手繪高高的展望台，上面有人在看富士山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + fuji(170, 150, 124, 80)
     + clouds([(120, 46)])
     + f'<path d="M3,150 Q60,144 120,150 T237,148 {BOT}" fill="#a9d8b1"/>'
     + f'<path d="M50,150 L58,58 M90,150 L82,58 M52,120 L88,90 M88,120 L52,90" stroke="{DBROWN}" stroke-width="2.2" fill="none"/>'
     + f'<rect x="40" y="46" width="60" height="16" rx="4" fill="{RED}"/>'
     + f'<path d="M40,46 L100,46" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},46 L{x},34" stroke-width="1.6"/>' for x in (44, 58, 72, 86, 98))
     + f'<path d="M42,34 L100,34" stroke-width="2"/>'
     + f'<circle cx="70" cy="30" r="7" fill="#f9d9c0"/><path d="M63,44 q0,-8 7,-8 q7,0 7,8" fill="{GOLD}"/>'
     + f'<circle cx="86" cy="30" r="6" fill="#f9d9c0"/><path d="M80,44 q0,-8 6,-8 q6,0 6,8" fill="{GREEN}"/>'
     + f'<path d="M94,26 l8,-4" stroke-width="1.6"/>'
     + sparkle(130, 24) + star(30, 28, 6), bg=SKYB)

# 5. 戰慄迷宮：廢棄醫院主題的鬼屋，畫成可愛的小幽靈
card('senritsu', '手繪鬼屋的醫院走廊，有一隻可愛的小幽靈',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#4a4470"/>'
     f'<circle cx="200" cy="38" r="14" fill="{GOLD}"/><circle cx="206" cy="34" r="12" fill="#4a4470" stroke="none"/>'
     f'<rect x="26" y="52" width="120" height="98" rx="4" fill="#9e9ab8"/>'
     f'<path d="M20,56 L86,24 L152,56 Z" fill="#6f6a92"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="20" height="18" rx="2" fill="{c}" stroke-width="1.6"/>'
               for x, y, c in [(38, 66, '#2e2a4a'), (76, 66, '#e9e08a'), (114, 66, '#2e2a4a'), (38, 100, '#e9e08a'), (114, 100, '#2e2a4a')])
     + f'<rect x="74" y="106" width="24" height="44" rx="3" fill="#2e2a4a"/>'
     + f'<path d="M80,84 L92,84 M86,78 L86,90" stroke="{RED}" stroke-width="2.6"/>'
     + f'<path d="M3,150 L237,150 {BOT}" fill="#3a3558"/>'
     # 小幽靈
     + f'<path d="M168,128 q-2,-48 22,-48 q24,0 22,48 l-7,-6 l-7,6 l-8,-6 l-8,6 l-7,-6 Z" fill="{WHITE}"/>'
     + face(190, 100, .9)
     + f'<path d="M166,108 q-10,-2 -12,-10 M214,108 q10,-2 12,-10" fill="none" stroke-width="1.8"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(20, 30), (120, 22), (160, 40), (226, 70)]),
     bg='#4a4470')


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('fq-' + name, 120, 120, label, inner, bg='#fff3c4')


# 入園閘門：藍色門簾＝臉部辨識，紅色門簾＝QR 發券
rem('r-gate', '手繪提醒：藍色門簾和紅色門簾兩種閘門',
    f'<rect x="12" y="30" width="44" height="60" rx="4" fill="{GRAY}"/>'
    f'<path d="M16,36 L52,36 L52,62 q-6,4 -9,0 q-4,4 -9,0 q-4,4 -9,0 q-5,4 -9,0 Z" fill="#7fa9d6"/>'
    f'<rect x="64" y="30" width="44" height="60" rx="4" fill="{GRAY}"/>'
    f'<path d="M68,36 L104,36 L104,62 q-6,4 -9,0 q-4,4 -9,0 q-4,4 -9,0 q-5,4 -9,0 Z" fill="{RED}"/>'
    f'<circle cx="34" cy="76" r="7" fill="{WHITE}" stroke-width="1.6"/><circle cx="31.5" cy="75" r="1" fill="{INK}" stroke="none"/><circle cx="36.5" cy="75" r="1" fill="{INK}" stroke="none"/>'
    f'<rect x="78" y="70" width="16" height="16" fill="{WHITE}" stroke-width="1.4"/>'
    f'<path d="M81,73 h4 v4 h-4 Z M87,79 h4 v4 h-4 Z" fill="{INK}" stroke="none"/>'
    f'<path d="M12,100 L108,100" stroke-width="2"/>')

# 巴士站在隔壁飯店的停車場裡
rem('r-bus', '手繪提醒：巴士停在飯店旁邊的停車場',
    f'<rect x="56" y="18" width="48" height="62" rx="3" fill="#e9dcc8"/>'
    + ''.join(f'<rect x="{x}" y="{y}" width="9" height="9" fill="{SKY}" stroke-width="1.2"/>' for x in (62, 76, 90) for y in (26, 42, 58))
    + f'<rect x="10" y="62" width="62" height="32" rx="7" fill="{GREEN}"/>'
    f'<rect x="16" y="68" width="14" height="10" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    f'<rect x="34" y="68" width="14" height="10" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    f'<rect x="52" y="68" width="14" height="10" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    f'<circle cx="24" cy="96" r="5" fill="{INK}"/><circle cx="58" cy="96" r="5" fill="{INK}"/>'
    f'<path d="M8,104 L112,104" stroke-width="2" stroke-dasharray="6 5"/>'
    f'<path d="M84,94 L104,94 M98,88 L104,94 L98,100" stroke="{RED}" stroke-width="3" fill="none"/>')

# 摩天輪整修停駛
rem('r-wheel', '手繪提醒：摩天輪旁邊放了施工三角錐',
    f'<circle cx="54" cy="52" r="34" fill="none" stroke-width="2.6"/>'
    + ''.join(f'<path d="M54,52 L{54+34*__import__("math").cos(a*0.785):.1f},{52+34*__import__("math").sin(a*0.785):.1f}" stroke-width="1.4"/>' for a in range(8))
    + ''.join(f'<rect x="{54+34*__import__("math").cos(a*0.785)-5:.1f}" y="{52+34*__import__("math").sin(a*0.785)-4:.1f}" width="10" height="9" rx="2" fill="{c}" stroke-width="1.3"/>'
              for a, c in zip(range(8), [PINK, GOLD, SKY, GREEN, PINK, GOLD, SKY, GREEN]))
    + f'<path d="M54,52 L40,104 M54,52 L68,104" stroke-width="2.4"/>'
    f'<path d="M94,70 L104,104 L84,104 Z" fill="#f2a46b"/><path d="M88,90 L100,90" stroke="{WHITE}" stroke-width="3"/>'
    f'<path d="M10,106 L112,106" stroke-width="2"/>')

print(save(F, OUT), 'files')
