# 吉卜力公園頁的「園區裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網各區介紹（ghibli-park.jp/en/about/）畫成一般的可愛建築與場景，不描照片構圖。
# 角色 IP：不畫任何角色、角色的招牌元素、電影裡特定造型的建物（例如會動的城堡）或 logo。
# 輸出 illust/sp/japan-ghibli-park/*.svg（240×180、提醒小圖 120×120）。說明文字放在 illust/spots/japan-ghibli-park.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-ghibli-park')
W, H = 240, 180
F = {}
FLOOR = '#e9dcc8'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('gp-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    # 卡片底部的一塊地面（貼合圓角框）
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def roundtree(x, base, r=16, col=GREEN):
    return (f'<rect x="{x-3}" y="{base-14}" width="6" height="14" fill="{DBROWN}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{base-14-r*.8:.1f}" r="{r}" fill="{col}"/>')


MOS = [PINK, SKY, GOLD, '#b6e3c6', '#c9b6e8', '#f7c9a0']

# 1. 吉卜力大倉庫：天窗下的馬賽克磁磚中央階梯
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f3e6d3"/>'
     f'<rect x="58" y="14" width="124" height="30" rx="4" fill="{SKY}"/>'
     + ''.join(f'<path d="M{58+31*i},14 L{58+31*i},44" stroke-width="1.4"/>' for i in range(1, 4))
     + f'<path d="M58,29 L182,29" stroke-width="1.4"/>'
     + ''.join(f'<polygon points="{a},44 {a+20},44 {a+34},150 {a-6},150" fill="{GOLD}" stroke="none" opacity=".18"/>'
               for a in (70, 110, 150))
     + f'<path d="M3,82 L237,82" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{x},82 L{x},64" stroke-width="1.6"/>' for x in (14, 34, 54, 74, 166, 186, 206, 226))
     + f'<path d="M10,64 L78,64 M162,64 L230,64" stroke-width="2"/>')
for i in range(7):
    y1 = 84 + i * 12
    y2 = y1 + 12
    l1, r1 = 88 - i * 5.4, 152 + i * 5.4
    l2, r2 = 88 - (i + 1) * 5.4, 152 + (i + 1) * 5.4
    t += f'<polygon points="{l1:.1f},{y1} {r1:.1f},{y1} {r2:.1f},{y2} {l2:.1f},{y2}" fill="{FLOOR}" stroke-width="1.6"/>'
    n = 5
    for k in range(n):
        cx = l1 + (r1 - l1) * (k + .5) / n
        t += f'<rect x="{cx-4:.1f}" y="{y1+3}" width="8" height="6" rx="1" fill="{MOS[(i+k) % len(MOS)]}" stroke-width="1"/>'
t += (f'<path d="M88,84 L50,168 M152,84 L190,168" stroke-width="2.6"/>'
      + person(120, 58, PINK, .8) + person(104, 118, SKY, .75) + person(142, 138, GOLD, .75)
      + sparkle(30, 30) + sparkle(210, 30))
card('warehouse', '手繪吉卜力大倉庫的中央階梯，天窗下鋪著彩色馬賽克磁磚', t)

# 2. 放映室：約 170 個座位的小電影院
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#5b4a66"/>'
     f'<rect x="40" y="20" width="160" height="70" rx="6" fill="{SKY}"/>'
     f'<path d="M40,74 Q90,50 130,66 T200,58 L200,84 Q200,90 194,90 L46,90 Q40,90 40,84 Z" fill="{GREEN}"/>'
     f'<circle cx="168" cy="38" r="9" fill="{GOLD}"/>'
     f'<path d="M64,40 q6,-6 12,0 q6,-6 12,0" fill="none" stroke-width="1.6"/>'
     f'<path d="M12,12 Q30,60 22,120 L6,120 L6,24 Q6,12 12,12 Z" fill="{RED}"/>'
     f'<path d="M228,12 Q210,60 218,120 L234,120 L234,24 Q234,12 228,12 Z" fill="{RED}"/>')
for row, (y, n, x0, sp) in enumerate([(116, 7, 42, 22), (136, 8, 32, 22), (156, 9, 22, 22)]):
    for k in range(n):
        x = x0 + k * sp
        t += (f'<path d="M{x},{y+14} L{x},{y} q0,-8 9,-8 q9,0 9,8 L{x+18},{y+14} Z" fill="{RED if (k+row) % 3 else "#f08a80"}" stroke-width="1.8"/>')
t += sparkle(120, 104, 4)
card('cinema', '手繪吉卜力大倉庫裡的小電影院，一排排紅色座位面對大銀幕', t, bg='#5b4a66')

# 3. 青春之丘：圓環中間的大杉樹與郵筒，後面是電梯塔和洋館
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(132, '#cfe8b8')
     # 電梯塔
     + f'<rect x="22" y="40" width="26" height="92" fill="#d9c7a8"/>'
     + ''.join(f'<path d="M22,{y} L48,{y}" stroke-width="1.2"/>' for y in (60, 80, 100, 120))
     + f'<path d="M22,40 L48,60 M48,40 L22,60 M22,80 L48,100 M48,80 L22,100" stroke-width="1" opacity=".5"/>'
     + f'<path d="M16,40 Q35,14 54,40 Z" fill="#7fa58c"/><circle cx="35" cy="20" r="3" fill="{GOLD}"/>'
     + f'<rect x="28" y="88" width="14" height="16" rx="2" fill="{GOLD}"/>'
     # 洋館（古董店）
     + f'<rect x="150" y="66" width="74" height="66" fill="#f5e3c8"/>'
     + f'<path d="M144,68 L187,40 L230,68 Z" fill="#6f9e88"/>'
     + f'<rect x="160" y="78" width="18" height="18" rx="2" fill="{GOLD}"/><rect x="196" y="78" width="18" height="18" rx="2" fill="{GOLD}"/>'
     + f'<path d="M150,104 L224,104" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},104 L{x},96" stroke-width="1.4"/>' for x in range(154, 224, 8))
     + f'<rect x="178" y="110" width="16" height="22" rx="2" fill="{DBROWN}"/>'
     # 圓環的杉樹
     + f'<ellipse cx="102" cy="150" rx="44" ry="10" fill="#e9dcc8"/>'
     + f'<rect x="98" y="128" width="8" height="18" fill="{DBROWN}"/>'
     + f'<path d="M102,58 L124,96 L114,96 L132,128 L72,128 L90,96 L80,96 Z" fill="{DGREEN}"/>'
     # 郵筒
     + f'<rect x="132" y="126" width="16" height="30" rx="7" fill="{RED}"/>'
     + f'<path d="M135,136 L145,136" stroke-width="2"/>'
     + f'<rect x="56" y="140" width="22" height="14" rx="2" fill="{WHITE}" transform="rotate(-10 67 147)"/>'
     + f'<path d="M57,141 L67,148 L77,139" fill="none" stroke-width="1.4" transform="rotate(-10 67 147)"/>'
     + sparkle(80, 30) + star(124, 22, 6))
card('hill', '手繪青春之丘：圓環中間的大杉樹、紅色郵筒，後面是電梯塔和洋館', t, bg=SKY)

# 4. 動動力森林：開上山頂的斜坡車
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f3dc"/>'
     f'<path d="M3,150 L200,40 L237,40 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9ccc8a"/>'
     f'<path d="M20,156 L210,48 M30,162 L220,54" stroke-width="2"/>'
     + ''.join(f'<path d="M{20+19*i:.0f},{156-10.8*i:.0f} L{30+19*i:.0f},{162-10.8*i:.0f}" stroke-width="1.4"/>' for i in range(11))
     + f'<g transform="translate(116,104) rotate(-29)">'
     f'<rect x="-34" y="-30" width="68" height="34" rx="8" fill="#f6edd0"/>'
     f'<rect x="-34" y="-8" width="68" height="12" fill="{GREEN}"/>'
     f'<rect x="-28" y="-24" width="14" height="12" rx="2" fill="{SKY}" stroke-width="1.6"/>'
     f'<rect x="-7" y="-24" width="14" height="12" rx="2" fill="{SKY}" stroke-width="1.6"/>'
     f'<rect x="14" y="-24" width="14" height="12" rx="2" fill="{SKY}" stroke-width="1.6"/>'
     f'<circle cx="-20" cy="8" r="5" fill="{GRAY}"/><circle cx="20" cy="8" r="5" fill="{GRAY}"/>'
     f'</g>'
     + roundtree(40, 112, 16, DGREEN) + roundtree(64, 98, 12, GREEN) + roundtree(180, 128, 18, DGREEN)
     + roundtree(212, 134, 13, GREEN) + roundtree(150, 40, 12, DGREEN)
     + f'<path d="M200,40 L200,22" stroke-width="2"/><path d="M200,22 L216,27 L200,32 Z" fill="{RED}"/>'
     + sparkle(40, 30) + sparkle(100, 24))
card('slopecar', '手繪動動力森林的斜坡車，沿著軌道開上種滿樹的山坡', t, bg='#e6f3dc')

# 5. 魔法公主之里：草屋頂的達達拉場與炭火烤五平餅
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef4e2"/>'
     + bottom(120, '#e3d3b2')
     + f'<rect x="20" y="70" width="104" height="52" fill="#c9a77c"/>'
     + ''.join(f'<path d="M{x},70 L{x},122" stroke-width="1.2" opacity=".6"/>' for x in range(30, 124, 12))
     + f'<path d="M8,74 Q72,10 136,74 Z" fill="#a9b86a"/>'
     + ''.join(f'<path d="M{x},{y} l4,8" stroke-width="1.2" opacity=".7"/>' for x, y in [(40, 56), (56, 44), (72, 38), (90, 44), (106, 54), (50, 64), (96, 64)])
     + f'<rect x="58" y="90" width="28" height="32" rx="2" fill="{DBROWN}"/>'
     # 炭火爐
     + f'<rect x="138" y="128" width="88" height="24" rx="6" fill="#8a8f99"/>'
     + ''.join(f'<ellipse cx="{x}" cy="128" rx="7" ry="4" fill="{c}" stroke-width="1.2"/>' for x, c in [(150, RED), (166, '#f08a3c'), (182, RED), (198, '#f08a3c'), (214, RED)])
     # 五平餅：扁平飯餅插在木籤上，塗醬
     + ''.join(f'<g transform="rotate({a} {x} 122)"><path d="M{x},126 L{x},160" stroke="{DBROWN}" stroke-width="3"/>'
               f'<ellipse cx="{x}" cy="104" rx="11" ry="20" fill="#f7efd9"/>'
               f'<ellipse cx="{x}" cy="102" rx="8" ry="15" fill="{c}" stroke="none" opacity=".85"/>'
               + ''.join(f'<ellipse cx="{x+dx}" cy="{dy}" rx="1.6" ry="1" fill="{WHITE}" stroke="none"/>' for dx, dy in [(-5, 90), (4, 96), (-3, 106), (5, 112), (-1, 118), (6, 88)])
               + '</g>'
               for x, a, c in [(156, -12, '#b8743a'), (182, 0, '#8a5a2c'), (208, 12, '#d9533f')])
     + ''.join(f'<path d="M{x},86 q-5,-6 0,-12 q5,-6 0,-12" fill="none" stroke-width="1.6" opacity=".55"/>' for x in (164, 196))
     + sparkle(200, 24) + sparkle(30, 26))
card('gohei', '手繪魔法公主之里的草屋頂建築，旁邊炭火上烤著三支五平餅', t, bg='#eef4e2')


# 6. 魔女之谷：歐洲木骨架房子的麵包店
def halftimber(x, y, w, h, roof, wall='#fbf3e4'):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}"/>'
         f'<path d="M{x-6},{y+2} L{x+w/2},{y-34} L{x+w+6},{y+2} Z" fill="{roof}"/>'
         f'<path d="M{x},{y+h/2} L{x+w},{y+h/2}" stroke="{DBROWN}" stroke-width="3"/>'
         f'<path d="M{x},{y} L{x+w/2},{y+h/2} L{x+w},{y} M{x+w/2},{y+h/2} L{x+w/2},{y+h}" stroke="{DBROWN}" stroke-width="2.4" fill="none"/>'
         f'<rect x="{x+6}" y="{y+h/2+6}" width="{w/2-12}" height="{h/2-12}" rx="2" fill="{GOLD}" stroke-width="1.6"/>')
    return s


t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(132, '#e8dccb')
     + halftimber(16, 60, 64, 72, BRICK) + halftimber(92, 48, 70, 84, '#6f9e88') + halftimber(174, 66, 54, 66, '#8a6fb0')
     + f'<path d="M124,132 L124,104 q8,-8 16,0 L140,132 Z" fill="{DBROWN}"/>'
     # 麵包籃
     + f'<path d="M70,150 L170,150 L160,172 L80,172 Z" fill="#d9a066"/>'
     + ''.join(f'<path d="M{x},150 L{x+4},172" stroke-width="1" opacity=".6"/>' for x in range(86, 160, 12))
     + f'<g transform="rotate(-18 108 140)"><ellipse cx="108" cy="140" rx="34" ry="8" fill="#e4a95e"/>'
     + ''.join(f'<path d="M{x},136 l6,7" stroke-width="1.4"/>' for x in (88, 102, 116))
     + '</g>'
     + f'<circle cx="146" cy="142" r="13" fill="#d99a52"/><path d="M138,140 q8,-6 16,0" fill="none" stroke-width="1.4"/>'
     + sparkle(40, 24) + star(210, 24, 6))
card('witches', '手繪魔女之谷的歐洲木骨架小房子和一籃長棍、圓麵包', t, bg=SKY)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('gp-' + name, 120, 120, label, inner, bg='#fff3c4')


def tiny(x, y, col):
    return (f'<circle cx="{x}" cy="{y}" r="6" fill="#f9d9c0"/>'
            f'<path d="M{x-8},{y+24} q0,-16 8,-16 q8,0 8,16 Z" fill="{col}"/>')


# 第一區換手環，之後每區都要全員和申請人一起進
rem('r-wristband', '手繪提醒：手腕上的手環和手牽手的一群人',
    f'<rect x="6" y="28" width="62" height="22" rx="10" fill="#f9d9c0"/>'
    f'<circle cx="72" cy="39" r="12" fill="#f9d9c0"/>'
    f'<rect x="34" y="23" width="14" height="32" rx="5" fill="{RED}"/>'
    f'<rect x="36" y="32" width="10" height="14" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    + tiny(36, 78, SKY) + tiny(60, 76, RED) + tiny(84, 78, GREEN)
    + f'<path d="M42,94 L54,92 M66,92 L78,94" stroke-width="2"/>'
    + star(96, 26, 8))

# 標準版：屋子內部要當天另外排隊領號碼牌
rem('r-standard', '手繪提醒：房子門口排隊和號碼牌',
    f'<rect x="18" y="40" width="50" height="50" fill="#fbf3e4"/>'
    f'<path d="M12,42 L43,14 L74,42 Z" fill="{BRICK}"/>'
    f'<rect x="36" y="64" width="14" height="26" rx="2" fill="{DBROWN}"/>'
    f'<rect x="72" y="50" width="38" height="28" rx="4" fill="{WHITE}"/>'
    f'<path d="M80,58 L102,58" stroke-width="1.6"/>'
    f'<text x="91" y="74" font-size="12" text-anchor="middle" fill="{RED}" stroke="none" font-family="sans-serif" font-weight="bold">No.7</text>'
    + ''.join(f'<circle cx="{x}" cy="104" r="5" fill="{c}"/>' for x, c in [(30, SKY), (46, PINK), (62, GOLD), (78, GREEN)]))

print(save(F, OUT), 'files')
