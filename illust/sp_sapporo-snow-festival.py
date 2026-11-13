# 札幌雪祭頁的「三個會場長什麼樣子」插圖與提醒卡（2026-11-13）。
# 參考雪祭官網各會場頁與「凍った路面の歩き方」（snowfes.com）畫成可愛版，不描照片構圖。
# 不畫任何真實雪像的主題（角色、建築、作品），只畫一般的大雪像、冰雕與會場風景。
# 輸出 illust/sp/sapporo-snow-festival/*.svg（240×180）。說明文字放在 illust/spots/sapporo-snow-festival.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'sapporo-snow-festival')
W, H = 240, 180
SKYW = '#e3eef7'
NIGHT = '#2e3a63'
ICE = '#dff3fb'
ICE2 = '#bfe6f5'
SNOWS = '#f4f8fc'
SHADE = '#d6e2ee'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sf-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def person(x, y, col=RED, s=1.0, hat=None):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if hat:
        t += f'<path d="M{x-6.5*s},{y-1*s} q{6.5*s},{-11*s} {13*s},0 Z" fill="{hat}" stroke-width="1.4"/>'
    return t


def big_sculpture(x, base, col=SNOWS, shade=SHADE):
    # 一般的大雪像：台座＋階梯＋圓頂和兩座小塔（不對應任何真實作品）
    return (f'<rect x="{x-86}" y="{base-14}" width="172" height="14" rx="2" fill="{shade}"/>'
            f'<rect x="{x-70}" y="{base-70}" width="140" height="56" rx="4" fill="{col}"/>'
            + ''.join(f'<rect x="{x-58+i*24}" y="{base-58}" width="12" height="30" rx="6" fill="{shade}" stroke-width="1.5"/>' for i in range(6))
            + f'<rect x="{x-22}" y="{base-30}" width="44" height="16" rx="2" fill="{shade}" stroke-width="1.5"/>'
            + f'<path d="M{x-24},{base-30} L{x+24},{base-30} M{x-26},{base-22} L{x+26},{base-22}" stroke-width="1.3"/>'
            + f'<path d="M{x-40},{base-70} Q{x},{base-128} {x+40},{base-70} Z" fill="{col}"/>'
            + f'<rect x="{x-82}" y="{base-96}" width="20" height="82" rx="3" fill="{col}"/>'
            + f'<path d="M{x-84},{base-96} L{x-72},{base-114} L{x-60},{base-96} Z" fill="{col}"/>'
            + f'<rect x="{x+62}" y="{base-96}" width="20" height="82" rx="3" fill="{col}"/>'
            + f'<path d="M{x+60},{base-96} L{x+72},{base-114} L{x+84},{base-96} Z" fill="{col}"/>'
            + f'<circle cx="{x}" cy="{base-84}" r="7" fill="{shade}" stroke-width="1.5"/>')


# 1. 大通會場：沿著公園排下去的大雪像
card('odori', '手繪大通公園的大雪像，前面有很多人在看',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + big_sculpture(120, 140)
     + floor(140, WHITE)
     + person(40, 140, RED, .8, GOLD) + person(62, 144, GREEN, .75, PINK) + person(176, 142, GOLD, .8, RED)
     + person(200, 146, SKY, .75, GREEN) + person(110, 148, PINK, .75, SKY)
     + flake(24, 24) + flake(210, 20) + flake(36, 70, 4) + star(214, 64, 5))

# 2. 大通會場晚上點燈
card('night', '手繪晚上打了彩色燈光的大雪像',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<path d="M{x},176 L{x+dx},40" stroke="{c}" stroke-width="10" opacity=".22" stroke-linecap="round"/>'
               for x, dx, c in [(40, 40, '#8fd8ff'), (200, -40, '#f6a5ad'), (120, 0, GOLD)])
     + big_sculpture(120, 140, '#d9e9ff', '#a9c4ea')
     + floor(140, '#e6eefa')
     + person(46, 140, RED, .8, GOLD) + person(190, 142, GREEN, .8, PINK)
     + snow([(24, 22), (70, 30), (180, 20), (220, 40), (40, 66), (210, 80)], 2.2, WHITE)
     + star(150, 24, 5))

# 3. 薄野會場：霓虹燈街上的冰雕
card('susukino', '手繪霓虹燈街上透明的冰雕',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + f'<rect x="12" y="18" width="50" height="100" rx="3" fill="#4b5a8a"/>'
     + f'<rect x="178" y="12" width="50" height="106" rx="3" fill="#4b5a8a"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="34" height="9" rx="4" fill="{c}" stroke-width="1.4"/>'
               for x, y, c in [(20, 30, PINK), (20, 52, GOLD), (20, 74, '#8fd8ff'), (186, 26, '#8fd8ff'), (186, 48, PINK), (186, 70, GOLD)])
     + f'<path d="M3,124 L237,124 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#5d6a94"/>'
     + f'<rect x="84" y="116" width="72" height="12" rx="2" fill="{ICE2}"/>'
     + f'<path d="M100,116 Q92,80 110,64 Q102,50 120,40 Q138,50 130,64 Q148,80 140,116 Z" fill="{ICE}" opacity=".95"/>'
     + f'<path d="M110,100 Q114,80 120,72" fill="none" stroke="{WHITE}" stroke-width="2.4"/>'
     + face(120, 88, .7)
     + f'<path d="M100,70 Q80,60 76,44 Q92,52 106,62 Z" fill="{ICE}"/><path d="M140,70 Q160,60 164,44 Q148,52 134,62 Z" fill="{ICE}"/>'
     + sparkle(90, 44) + sparkle(152, 96, 4) + sparkle(70, 104, 4)
     + person(54, 140, RED, .8, GOLD) + person(184, 140, GREEN, .8, PINK))

# 4. 薄野：把魚凍在裡面的冰雕
card('fish', '手繪一塊透明冰塊，裡面凍著魚',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + floor(146, WHITE)
     + f'<rect x="56" y="34" width="128" height="112" rx="8" fill="{ICE}" opacity=".95"/>'
     + f'<path d="M66,46 L66,96 M74,46 L74,70" stroke="{WHITE}" stroke-width="3"/>'
     + ''.join(f'<g transform="translate({x},{y}) rotate({r})">'
               f'<path d="M-14,0 q14,-10 28,0 q-14,10 -28,0 Z" fill="{c}" stroke-width="1.5"/>'
               f'<path d="M-14,0 l-8,-7 l0,14 Z" fill="{c}" stroke-width="1.5"/>'
               f'<circle cx="7" cy="-1" r="1.6" fill="{INK}" stroke="none"/></g>'
               for x, y, r, c in [(100, 66, -10, '#9fb4cf'), (150, 80, 8, '#f2a46b'), (110, 108, 4, '#c7d3e2'), (152, 120, -6, '#9fb4cf'), (128, 92, 0, GOLD)])
     + f'<path d="M48,146 L192,146" stroke-width="2"/>'
     + sparkle(196, 40) + sparkle(46, 60, 4) + flake(24, 24) + flake(214, 120, 4))

# 5. 薄野：冰雕製作中
card('carving', '手繪拿鑿子雕冰塊的人',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + floor(146, WHITE)
     + f'<rect x="100" y="52" width="80" height="94" rx="4" fill="{ICE}"/>'
     + f'<path d="M100,52 L130,52 Q122,74 130,96 Q118,110 128,146 L100,146 Z" fill="{ICE2}" opacity=".7" stroke="none"/>'
     + f'<path d="M150,66 Q166,74 160,92 Q172,104 158,118" fill="none" stroke="{WHITE}" stroke-width="2.6"/>'
     + person(66, 82, GREEN, 1.3, RED)
     + f'<path d="M78,102 L100,92" stroke-width="3"/>'
     + f'<path d="M96,86 L110,96 L106,100 L94,90 Z" fill="{GRAY}" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},{y} l4,-4" stroke="{ICE2}" stroke-width="2.2"/>' for x, y in [(112, 86), (118, 92), (114, 80)])
     + snow([(118, 140), (130, 142), (108, 143)], 3, ICE2)
     + sparkle(196, 34) + flake(30, 30) + flake(60, 20, 4) + star(214, 70, 5))

# 6. Tsudome 會場：大型管狀溜滑梯
card('slider', '手繪坐著充氣圈從雪坡滑下來的人',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,60 L60,48 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WHITE}"/>'
     + f'<path d="M30,70 L224,170 M54,58 L237,140" stroke="{SHADE}" stroke-width="3"/>'
     + f'<path d="M40,64 L232,156" stroke="{SHADE}" stroke-width="2" stroke-dasharray="6 6"/>'
     + f'<g transform="rotate(28 130 108)">'
     + f'<ellipse cx="130" cy="112" rx="24" ry="9" fill="{RED}"/>'
     + f'<ellipse cx="130" cy="110" rx="12" ry="4" fill="#b8443e" stroke-width="1.4"/>'
     + f'</g>'
     + person(128, 86, SKY, 1.0, GOLD)
     + f'<path d="M120,96 l-12,-8 M136,96 l12,-8" stroke-width="2"/>'
     + f'<ellipse cx="54" cy="52" rx="14" ry="5" fill="{GOLD}" transform="rotate(20 54 52)"/>'
     + person(52, 32, GREEN, .7, PINK)
     + ''.join(f'<path d="M{x},{y} l-8,-3" stroke="{SHADE}" stroke-width="2"/>' for x, y in [(100, 96), (96, 104), (104, 88)])
     + flake(200, 30) + flake(160, 22, 4) + star(214, 64, 5))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('sf-' + name, 120, 120, label, inner, bg='#fff3c4')


# 斑馬線白線特別滑
rem('r-crosswalk', '手繪提醒：結冰的斑馬線很滑',
    f'<rect x="10" y="20" width="100" height="84" rx="6" fill="#8a94a6"/>'
    + ''.join(f'<rect x="20" y="{y}" width="80" height="10" rx="2" fill="{WHITE}" stroke-width="1.4"/>' for y in (30, 52, 74))
    + sparkle(30, 26, 5) + sparkle(96, 48, 5) + sparkle(60, 96, 5)
    + f'<path d="M70,62 q10,-6 22,0" fill="none" stroke="{SKY}" stroke-width="2.4"/>'
    + f'<path d="M90,12 L108,44 L72,44 Z" fill="{GOLD}" stroke-width="2"/>'
    + f'<path d="M90,22 L90,33" stroke-width="3.4"/><circle cx="90" cy="39" r="1.8" fill="{INK}" stroke="none"/>')

# Tsudome 的遊樂設施要戴帽子和手套
rem('r-hatgloves', '手繪提醒：毛帽和手套',
    f'<path d="M22,62 Q22,24 54,24 Q86,24 86,62 Z" fill="{RED}"/>'
    f'<rect x="18" y="58" width="72" height="14" rx="5" fill="{WHITE}"/>'
    f'<circle cx="54" cy="20" r="7" fill="{WHITE}"/>'
    f'<path d="M66,84 L66,104 Q66,112 74,112 L92,112 Q100,112 100,104 L100,84 Q100,76 92,76 L74,76 Q66,76 66,84 Z" fill="{SKY}"/>'
    f'<path d="M66,92 Q56,90 56,82 Q58,74 66,80" fill="{SKY}"/>'
    f'<path d="M24,84 L24,104 Q24,112 32,112 L50,112 Q58,112 58,104 L58,84 Q58,76 50,76 L32,76 Q24,76 24,84 Z" fill="{SKY}"/>'
    f'<path d="M58,92 Q68,90 68,82 Q66,74 58,80" fill="{SKY}"/>')

print(save(F, OUT), 'files')
