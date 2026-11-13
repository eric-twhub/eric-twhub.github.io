# 吉卜力美術館頁的「館內有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網 Welcome! 頁（ghibli-museum.jp/en/welcome/）的介紹畫成一般的可愛建築與場景，不描照片構圖。
# 角色 IP：不畫任何角色、角色的招牌元素（館內的大型角色、公車、屋頂機器兵都不畫）或 logo。
# 輸出 illust/sp/japan-ghibli-museum/*.svg。說明文字放在 illust/spots/japan-ghibli-museum.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-ghibli-museum')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('gm-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def roundtree(x, base, r=16, col=GREEN, trunk=14):
    return (f'<rect x="{x-3}" y="{base-trunk}" width="6" height="{trunk}" fill="{DBROWN}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{base-trunk-r*.8:.1f}" r="{r}" fill="{col}"/>')


def glass(x, y, r):
    # 一扇圓形彩繪玻璃窗：花瓣
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SKY}"/>'
    for i, c in enumerate([PINK, GOLD, '#b6e3c6', '#c9b6e8']):
        ang = i * 90
        s += f'<ellipse cx="{x}" cy="{y-r*.45:.1f}" rx="{r*.28:.1f}" ry="{r*.42:.1f}" fill="{c}" stroke-width="1.2" transform="rotate({ang} {x} {y})"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r*.22:.1f}" fill="{RED}" stroke-width="1.2"/>'
    return s


# 1. 井之頭公園大樹旁的彩色建築，窗戶是彩繪玻璃
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(140, '#b9dca0')
     + roundtree(24, 140, 24, DGREEN, 30) + roundtree(218, 140, 22, DGREEN, 34)
     + f'<rect x="56" y="70" width="70" height="70" fill="#f6c27a"/>'
     + f'<rect x="126" y="56" width="58" height="84" fill="#f4a6a0"/>'
     + f'<path d="M126,56 Q155,24 184,56 Z" fill="#7fb59a"/>'
     + f'<rect x="40" y="96" width="24" height="44" fill="#8fc0e0"/>'
     + f'<path d="M50,70 L120,70" stroke-width="2"/>'
     + f'<path d="M52,70 L91,44 L130,70 Z" fill="{BRICK}"/>'
     + glass(80, 96, 13) + glass(155, 84, 14) + glass(108, 118, 9)
     + f'<rect x="146" y="108" width="20" height="32" rx="9" fill="{DBROWN}"/>'
     + f'<path d="M52,128 l0,-8 M58,124 l0,-6" stroke="{GREEN}" stroke-width="2"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{c}" stroke-width="1"/>' for x, y, c in [(46, 140, PINK), (60, 142, GOLD), (196, 140, PINK), (184, 144, GOLD)])
     + sparkle(110, 24) + star(206, 22, 6))
card('building', '手繪三鷹森林裡的彩色美術館建築，窗戶是花朵圖案的彩繪玻璃', t, bg=SKY)

# 2. 用 35 毫米電影膠片做的入場券，對著光看
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf0d8"/>'
     f'<circle cx="190" cy="50" r="24" fill="{GOLD}" opacity=".9"/>'
     + ''.join(f'<path d="M190,50 L{x},{y}" stroke="{GOLD}" stroke-width="2.4" opacity=".6"/>' for x, y in [(150, 20), (226, 20), (140, 60), (220, 92)])
     + f'<g transform="rotate(-12 110 100)">'
     f'<rect x="40" y="62" width="140" height="74" rx="4" fill="#4a4048"/>'
     + ''.join(f'<rect x="{x}" y="66" width="7" height="7" rx="1.5" fill="{CREAM}" stroke="none"/>'
               f'<rect x="{x}" y="125" width="7" height="7" rx="1.5" fill="{CREAM}" stroke="none"/>' for x in range(46, 176, 14))
     + f'<rect x="60" y="78" width="100" height="42" fill="{SKY}" stroke-width="1.6"/>'
     f'<path d="M60,108 Q90,92 110,104 T160,98 L160,120 L60,120 Z" fill="{GREEN}" stroke-width="1.4"/>'
     f'<circle cx="140" cy="88" r="5" fill="{WHITE}" stroke-width="1.2"/>'
     f'<path d="M110,78 L110,120" stroke-width="1.4"/>'
     f'</g>'
     + f'<path d="M30,162 q10,-26 26,-30 q8,0 8,8 l-10,22 Z" fill="#f9d9c0"/>'
     + f'<path d="M210,160 q-8,-24 -22,-30 q-8,0 -8,8 l8,22 Z" fill="#f9d9c0"/>'
     + sparkle(40, 30) + sparkle(70, 22, 4))
# 2026-11 起改 QR 票務，還發不發膠片入場券查不到，先不放
# card('ticket', '手繪一段電影膠片做的入場券，對著太陽光看得到裡面的風景畫面', t, bg='#fdf0d8')

# 3. 中央大廳：挑高空間、螺旋樓梯、空中走道、玻璃圓頂和大風扇
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f6e8d2"/>'
     f'<path d="M60,48 Q120,-6 180,48 Z" fill="{SKY}"/>'
     + ''.join(f'<path d="M120,48 L{x},{y}" stroke-width="1.2"/>' for x, y in [(70, 36), (90, 22), (120, 16), (150, 22), (170, 36)])
     + f'<path d="M72,36 Q120,20 168,36" fill="none" stroke-width="1.2"/>'
     + f'<path d="M60,48 L180,48" stroke-width="2.4"/>'
     # 大風扇
     + f'<circle cx="120" cy="62" r="4" fill="{DBROWN}"/>'
     + ''.join(f'<ellipse cx="120" cy="62" rx="24" ry="4.4" fill="{BROWN}" stroke-width="1.4" transform="rotate({a} 120 62) translate(22 0)"/>' for a in (10, 130, 250))
     # 左右的樓層與欄杆
     + f'<path d="M3,48 L47,48 L47,177 L25,177 Q3,177 3,155 Z" fill="#e8c9a0" stroke="none"/>'
     + f'<path d="M237,48 L193,48 L193,177 L215,177 Q237,177 237,155 Z" fill="#e8c9a0" stroke="none"/>'
     + f'<path d="M47,48 L47,177 M193,48 L193,177" stroke-width="2"/>'
     + f'<path d="M47,104 L193,104 M47,114 L193,114" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},104 L{x},94" stroke-width="1.4"/>' for x in range(55, 193, 12))
     + f'<path d="M47,94 L193,94" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="99" r="2.4" fill="{c}" stroke="none"/>' for x, c in zip(range(61, 193, 24), [PINK, SKY, GOLD, '#b6e3c6', PINK, GOLD]))
     # 螺旋樓梯
     + ''.join(f'<path d="M{16 + (i % 2) * 14},{168 - i * 12} L{30 - (i % 2) * 14},{162 - i * 12}" stroke-width="2.6"/>' for i in range(10))
     + f'<path d="M23,172 L23,52" stroke-width="2" opacity=".6"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="14" height="16" rx="7" fill="{GOLD}" stroke-width="1.4"/>' for x, y in [(206, 60), (206, 128), (14 + 190, 150)])
     + person(100, 120, PINK, .7) + person(140, 122, SKY, .7)
     + sparkle(36, 24) + sparkle(204, 24))
card('hall', '手繪美術館的中央大廳：玻璃圓頂、大風扇、螺旋樓梯和空中走道', t, bg='#f6e8d2')

# 4. 地下的小劇場：天花板與牆上畫著藍天和花，紅色小長椅
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#cfe6f7"/>'
     + ''.join(f'<path d="M{x},{y} q6,-6 12,0 q6,-6 12,0" fill="{WHITE}" stroke-width="1.4"/>' for x, y in [(30, 26), (170, 22), (110, 16)])
     + ''.join(f'<g>' + ''.join(f'<circle cx="{x+dx}" cy="{y+dy}" r="4.4" fill="{c}" stroke-width="1.2"/>' for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5)])
               + f'<circle cx="{x}" cy="{y}" r="3" fill="{GOLD}" stroke-width="1.2"/></g>'
               for x, y, c in [(22, 70, PINK), (24, 108, '#c9b6e8'), (218, 66, PINK), (216, 104, '#f7c9a0')])
     + f'<rect x="58" y="36" width="124" height="64" rx="4" fill="{WHITE}"/>'
     + f'<path d="M58,92 Q100,70 140,84 T182,78 L182,96 Q182,100 178,100 L62,100 Q58,100 58,96 Z" fill="#b6e3c6"/>'
     + f'<circle cx="160" cy="54" r="7" fill="{GOLD}"/>'
     + bottom(140, '#e8d6bb'))
for row, (y, n, x0) in enumerate([(118, 3, 40), (142, 3, 30)]):
    for k in range(n):
        x = x0 + k * 62
        t += (f'<rect x="{x}" y="{y}" width="52" height="10" rx="4" fill="{RED}"/>'
              f'<path d="M{x+6},{y+10} L{x+6},{y+20} M{x+46},{y+10} L{x+46},{y+20}" stroke-width="2.4"/>')
t += person(66, 102, SKY, .6) + person(150, 126, GOLD, .6) + person(100, 126, PINK, .6)
card('theater', '手繪地下的小劇場：牆上畫著藍天和花，前面一排排紅色小長椅', t, bg='#cfe6f7')

# 5. 中庭的手壓井
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fbeedd"/>'
     + bottom(140, '#e3d3b2')
     + f'<path d="M40,60 L120,22 L200,60 Z" fill="{BRICK}"/>'
     + ''.join(f'<path d="M{60+i*20},{50-i*0} q10,6 20,0" fill="none" stroke-width="1.2" opacity=".6"/>' for i in range(6))
     + f'<path d="M58,60 L58,140 M182,60 L182,140" stroke-width="4"/>'
     # 手壓幫浦
     + f'<rect x="104" y="80" width="22" height="60" rx="4" fill="{NAVY}"/>'
     + f'<rect x="100" y="74" width="30" height="10" rx="4" fill="{NAVY}"/>'
     + f'<path d="M126,90 L146,90 L146,98" fill="none" stroke-width="6" stroke="{NAVY}"/>'
     + f'<path d="M104,82 L74,64" stroke-width="5"/><circle cx="72" cy="63" r="4" fill="{NAVY}"/>'
     + f'<path d="M146,104 q-4,8 0,12 q4,-4 0,-12 Z" fill="#8fd0f0"/>'
     + f'<path d="M134,124 L158,124 L154,144 L138,144 Z" fill="{SKY}"/>'
     + f'<ellipse cx="146" cy="126" rx="10" ry="3" fill="#8fd0f0" stroke-width="1.2"/>'
     # 花
     + ''.join(f'<path d="M{x},154 L{x},140" stroke="{GREEN}" stroke-width="2"/><circle cx="{x}" cy="138" r="5" fill="{c}" stroke-width="1.2"/>'
               for x, c in [(30, PINK), (44, GOLD), (196, PINK), (210, '#c9b6e8'), (222, GOLD)])
     + sparkle(28, 30) + sparkle(214, 30))
card('well', '手繪中庭涼亭裡的手壓井，壓下把手就有水流到水桶', t, bg='#fbeedd')

# 6. 咖啡廳：橘色牆、紅窗框，露台上的大草帽
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(140, '#d9c2a0')
     + f'<rect x="30" y="56" width="180" height="84" fill="#f2a04e"/>'
     + ''.join(f'<rect x="{x}" y="70" width="26" height="30" rx="2" fill="#fff4d8" stroke="{RED}" stroke-width="3"/>'
               f'<path d="M{x+13},70 L{x+13},100 M{x},85 L{x+26},85" stroke="{RED}" stroke-width="2"/>' for x in (46, 106, 166))
     + f'<path d="M30,56 L210,56" stroke-width="2.6"/>'
     # 大草帽
     + f'<ellipse cx="120" cy="44" rx="58" ry="12" fill="#f3d27a"/>'
     + f'<path d="M90,44 Q90,14 120,14 Q150,14 150,44 Z" fill="#f3d27a"/>'
     + f'<path d="M90,38 Q120,46 150,38 L150,44 Q120,52 90,44 Z" fill="{DBROWN}" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},20 L{x+2},40" stroke-width="1" opacity=".5"/>' for x in range(98, 146, 8))
     # 露台與桌子
     + f'<rect x="20" y="132" width="200" height="8" rx="2" fill="{DBROWN}"/>'
     + f'<ellipse cx="80" cy="148" rx="30" ry="6" fill="{WHITE}"/><path d="M80,154 L80,172" stroke-width="3"/>'
     + f'<ellipse cx="80" cy="142" rx="16" ry="6" fill="#e4a95e"/><path d="M66,140 Q80,134 94,140" fill="none" stroke="{RED}" stroke-width="2.4"/>'
     + f'<ellipse cx="166" cy="148" rx="30" ry="6" fill="{WHITE}"/><path d="M166,154 L166,172" stroke-width="3"/>'
     + f'<rect x="156" y="124" width="14" height="20" rx="3" fill="#f7c9a0"/><path d="M166,124 L172,112" stroke-width="1.6"/>'
     + f'<circle cx="182" cy="140" r="6" fill="{PINK}"/>'
     + sparkle(28, 28) + star(214, 26, 6))
card('cafe', '手繪橘色牆的咖啡廳，露台上方有一頂大草帽，桌上放著熱狗和飲料', t, bg=SKY)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('gm-' + name, 120, 120, label, inner, bg='#fff3c4')


# 館內不能拍照
rem('r-nophoto', '手繪提醒：相機打叉，旁邊一隻眼睛',
    f'<rect x="14" y="36" width="58" height="40" rx="8" fill="{GRAY}"/>'
    f'<rect x="24" y="28" width="18" height="10" rx="3" fill="{GRAY}"/>'
    f'<circle cx="43" cy="56" r="13" fill="{WHITE}"/><circle cx="43" cy="56" r="7" fill="{NAVY}"/>'
    f'<path d="M10,26 L78,86 M78,26 L10,86" stroke="{RED}" stroke-width="5"/>'
    f'<path d="M70,100 Q90,82 110,100 Q90,118 70,100 Z" fill="{WHITE}"/>'
    f'<circle cx="90" cy="100" r="6" fill="{DBROWN}"/>'
    + star(96, 24, 8))

# 社區巴士只在開館時間跑
rem('r-bus', '手繪提醒：社區巴士和時鐘',
    f'<rect x="10" y="44" width="72" height="42" rx="10" fill="{GOLD}"/>'
    f'<rect x="18" y="52" width="16" height="14" rx="2" fill="{SKY}" stroke-width="1.6"/>'
    f'<rect x="38" y="52" width="16" height="14" rx="2" fill="{SKY}" stroke-width="1.6"/>'
    f'<rect x="58" y="52" width="16" height="14" rx="2" fill="{SKY}" stroke-width="1.6"/>'
    f'<circle cx="26" cy="88" r="7" fill="{GRAY}"/><circle cx="66" cy="88" r="7" fill="{GRAY}"/>'
    f'<circle cx="92" cy="30" r="18" fill="{WHITE}"/><path d="M92,30 L92,18 M92,30 L101,34" stroke-width="2.4"/>'
    '')

print(save(F, OUT), 'files')
