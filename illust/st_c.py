# 主題貼紙 C 組（2026-11-13）：雪景、溫泉、季節、住宿與雜項頁面用的手繪貼紙。
# 共用工具在 kit.py。改圖就改這支，跑 `python3 illust/st_c.py` 重新輸出 illust/st/*.svg。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st')

THATCH = '#d9b36c'
ORANGE = '#f08a4b'
AMBER = '#f0b37a'
MILK = '#eef2f7'
SEA = '#9fcbe8'
WALL = '#f6dcc4'
SLATE = '#6c7a8c'
LIGHTBLUE = '#a8d1ef'

FILES = {}


def snowfloor(y=118):
    # 框內底部的積雪地面（不超出圓角框）
    return (f'<path d="M6,{y} Q50,{y-10} 90,{y-2} T174,{y-4} L174,136 Q174,144 166,144 '
            f'L14,144 Q6,144 6,136 Z" fill="{WHITE}"/>')


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def heart(x, y, s=1.0, col=RED):
    return (f'<path d="M{x},{y+6*s} C{x-10*s},{y-1*s} {x-7*s},{y-9*s} {x},{y-4*s} '
            f'C{x+7*s},{y-9*s} {x+10*s},{y-1*s} {x},{y+6*s} Z" fill="{col}" stroke-width="1.4"/>')


def add(name, label, inner, bg=CREAM, dots=True):
    FILES[name] = sticker(name, label, inner, bg=bg, dots=dots)


# ---- gassho：雪中的合掌造 ----
def gassho_house(x, base, w, h):
    # 尖三角茅草屋頂、深色木牆、屋頂積雪
    top = base - h
    roof_bot = base - h * .38
    t = (f'<rect x="{x - w*.38:.0f}" y="{roof_bot:.0f}" width="{w*.76:.0f}" height="{base-roof_bot:.0f}" fill="{DBROWN}"/>'
         f'<path d="M{x - w/2:.0f},{roof_bot+2:.0f} L{x},{top} L{x + w/2:.0f},{roof_bot+2:.0f} Z" fill="{THATCH}"/>'
         f'<path d="M{x - w*.3:.0f},{top + (roof_bot-top)*.6:.0f} L{x},{top} L{x + w*.3:.0f},{top + (roof_bot-top)*.6:.0f} '
         f'Q{x + w*.15:.0f},{top + (roof_bot-top)*.5:.0f} {x},{top + (roof_bot-top)*.58:.0f} '
         f'Q{x - w*.15:.0f},{top + (roof_bot-top)*.5:.0f} {x - w*.3:.0f},{top + (roof_bot-top)*.6:.0f} Z" fill="{WHITE}"/>'
         f'<rect x="{x - w*.1:.0f}" y="{top + (roof_bot-top)*.7:.0f}" width="{w*.2:.0f}" height="{w*.12:.0f}" rx="1" fill="{GOLD}" stroke-width="1.4"/>')
    return t


add('gassho', '手繪雪中的合掌造房子',
    gassho_house(72, 124, 92, 92)
    + f'<rect x="48" y="104" width="12" height="12" rx="1.5" fill="{GOLD}" stroke-width="1.4"/>'
    + f'<rect x="84" y="104" width="12" height="12" rx="1.5" fill="{GOLD}" stroke-width="1.4"/>'
    + face(72, 112, .75)
    + gassho_house(140, 124, 54, 60)
    + f'<rect x="134" y="108" width="12" height="11" rx="1.5" fill="{GOLD}" stroke-width="1.4"/>'
    + snowfloor(124)
    + flake(30, 40) + flake(118, 34, 4) + flake(160, 64, 4) + star(160, 22, 5))

# ---- ginzan：雪夜的木造溫泉旅館加煤氣燈 ----
_g = ''
for i, (y, w) in enumerate([(50, 74), (78, 82), (106, 88)]):
    x0 = 76 - w / 2
    _g += (f'<rect x="{x0:.0f}" y="{y}" width="{w}" height="28" fill="{BROWN}"/>'
           + ''.join(f'<rect x="{x0 + 8 + j*((w-16)/3):.0f}" y="{y+8}" width="{(w-16)/3 - 6:.0f}" height="13" rx="1.5" '
                     f'fill="{GOLD}" stroke-width="1.3"/>' for j in range(3))
           + f'<path d="M{x0-8:.0f},{y+1} L{x0+w+8:.0f},{y+1} L{x0+w:.0f},{y-7} L{x0:.0f},{y-7} Z" fill="{SLATE}"/>'
           + f'<path d="M{x0-6:.0f},{y-6} Q{x0+w/2:.0f},{y-12} {x0+w+6:.0f},{y-6}" stroke="{WHITE}" stroke-width="4"/>')
add('ginzan', '手繪雪夜的木造溫泉旅館和煤氣燈',
    _g
    + f'<path d="M64,50 L76,30 L88,50 Z" fill="{SLATE}"/>'
    + f'<circle cx="146" cy="66" r="15" fill="{GOLD}" stroke="none" opacity=".35"/>'
    + f'<path d="M146,80 L146,128" stroke-width="3.4"/>'
    + f'<path d="M138,58 L154,58 L151,76 L141,76 Z" fill="{GOLD}"/>'
    + f'<path d="M136,58 L146,50 L156,58 Z" fill="{INK}"/>'
    + face(146, 66, .55, blush=False)
    + snowfloor(126)
    + snow([(24, 30), (40, 70), (112, 26), (164, 40), (128, 100), (22, 104)], 2.2, WHITE)
    + f'<path d="M30,22 a10,10 0 1,0 12,14 a8,8 0 1,1 -12,-14 Z" fill="{GOLD}"/>',
    bg=NAVY, dots=False)

# ---- rotenburo：乳白色露天溫泉 ----
add('rotenburo', '手繪乳白色的露天溫泉、茅草屋頂和木桶',
    f'<path d="M40,52 L40,100 M140,52 L140,100" stroke-width="3.4"/>'
    + f'<path d="M24,54 L90,20 L156,54 Q90,46 24,54 Z" fill="{THATCH}"/>'
    + f'<path d="M50,40 L90,20 L130,40" fill="none" stroke-width="1.4" opacity=".6"/>'
    + f'<ellipse cx="86" cy="112" rx="66" ry="22" fill="{GRAY}"/>'
    + f'<ellipse cx="86" cy="110" rx="54" ry="14" fill="{MILK}"/>'
    + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="6" fill="#b9c3cf" stroke-width="1.6"/>'
              for x, y in [(28, 112), (42, 126), (66, 132), (106, 132), (130, 126), (146, 114)])
    + face(86, 108, .9)
    + f'<path d="M62,92 q-6,-8 0,-16 q6,-8 0,-16 M86,90 q-6,-8 0,-16 q6,-8 0,-16 M110,92 q-6,-8 0,-16 q6,-8 0,-16" '
      f'fill="none" stroke-width="1.8" opacity=".55"/>'
    + f'<path d="M140,102 L166,102 L162,128 L144,128 Z" fill="{BROWN}"/>'
    + f'<path d="M142,110 L164,110 M143,120 L163,120" stroke-width="1.6"/>'
    + sparkle(160, 76, 4))

# ---- icebreaker：流冰中的破冰船加小海豹 ----
add('icebreaker', '手繪流冰中的破冰船和小海豹',
    f'<path d="M6,94 L174,94 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="{SEA}"/>'
    + f'<path d="M100,46 L112,46 L112,64 L100,64 Z" fill="{GOLD}"/>'
    + f'<rect x="64" y="62" width="58" height="26" rx="4" fill="{WHITE}"/>'
    + ''.join(f'<rect x="{x}" y="68" width="8" height="7" rx="1.5" fill="{SKY}" stroke-width="1.3"/>' for x in (70, 82))
    + face(103, 74, .7)
    + f'<path d="M34,88 L150,88 L140,112 L50,112 Q40,104 34,88 Z" fill="{RED}"/>'
    + f'<path d="M40,96 L146,96" stroke="{WHITE}" stroke-width="3"/>'
    + f'<path d="M152,106 L170,104 L168,116 L148,118 Z" fill="{WHITE}"/>'
    + f'<path d="M110,118 L138,114 L144,124 L114,128 Z" fill="{WHITE}"/>'
    + f'<path d="M10,118 L58,114 L64,130 L12,134 Z" fill="{WHITE}"/>'
    + f'<ellipse cx="34" cy="116" rx="17" ry="9" fill="#cfd6de"/>'
    + f'<path d="M48,120 q8,-2 10,4" fill="#cfd6de" stroke-width="1.6"/>'
    + face(28, 114, .6, blush=True)
    + flake(30, 36) + flake(146, 30, 4) + star(60, 30, 5))

# ---- snowman：圍圍巾的雪人 ----
add('snowman', '手繪圍圍巾的雪人',
    snowfloor(124)
    + f'<path d="M58,92 L34,74 M40,79 L32,82 M122,92 L146,74 M140,79 L148,82" stroke="{DBROWN}" stroke-width="2.6"/>'
    + f'<circle cx="90" cy="104" r="30" fill="{WHITE}"/>'
    + f'<circle cx="90" cy="60" r="22" fill="{WHITE}"/>'
    + face(90, 58, .9)
    + f'<path d="M90,62 L101,64 L90,66 Z" fill="{ORANGE}" stroke-width="1.3"/>'
    + f'<path d="M68,44 Q90,22 112,44 Z" fill="{GREEN}"/>'
    + f'<path d="M66,44 L114,44" stroke-width="5" stroke="{DGREEN}"/>'
    + f'<circle cx="90" cy="26" r="5" fill="{WHITE}"/>'
    + f'<path d="M68,78 Q90,88 112,78 L112,86 Q90,96 68,86 Z" fill="{RED}"/>'
    + f'<path d="M100,88 L106,110 L96,112 L92,90 Z" fill="{RED}"/>'
    + ''.join(f'<circle cx="90" cy="{y}" r="2.6" fill="{INK}" stroke="none"/>' for y in (100, 112))
    + flake(28, 40) + flake(150, 50, 4) + star(144, 22, 5))

# ---- juhyo：一排有臉的樹冰 ----
def monster(x, base, h, w):
    return (f'<path d="M{x-w/2},{base} Q{x-w*.66:.0f},{base-h*.45:.0f} {x-w*.32:.0f},{base-h*.62:.0f} '
            f'Q{x-w*.48:.0f},{base-h*.86:.0f} {x-w*.12:.0f},{base-h*.9:.0f} Q{x},{base-h-6} {x+w*.14:.0f},{base-h*.9:.0f} '
            f'Q{x+w*.5:.0f},{base-h*.84:.0f} {x+w*.32:.0f},{base-h*.6:.0f} Q{x+w*.66:.0f},{base-h*.42:.0f} {x+w/2},{base} Z" '
            f'fill="{WHITE}"/>'
            f'<path d="M{x-w*.3:.0f},{base-h*.4:.0f} l-7,-4 M{x+w*.3:.0f},{base-h*.5:.0f} l7,-5" stroke="{DGREEN}" stroke-width="2"/>'
            + face(x, base - h * .55, .75))
add('juhyo', '手繪雪坡上一排有臉的樹冰',
    f'<path d="M6,116 Q60,96 110,108 T174,100 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="{WHITE}"/>'
    + monster(46, 120, 66, 40) + monster(96, 114, 84, 46) + monster(144, 112, 58, 36)
    + flake(30, 30) + flake(130, 26, 4) + flake(162, 52, 4),
    bg=SKY, dots=False)

# ---- lights：燈光隧道加花 ----
def arc_bulbs(cx, base, rx, ry, n, r):
    t = (f'<path d="M{cx-rx},{base} A{rx},{ry} 0 0 1 {cx+rx},{base}" fill="none" stroke="{GOLD}" '
         f'stroke-width="2" opacity=".7"/>')
    for i in range(n + 1):
        a = math.pi - math.pi * i / n
        t += (f'<circle cx="{cx + rx*math.cos(a):.1f}" cy="{base - ry*math.sin(a):.1f}" r="{r}" '
              f'fill="{GOLD}" stroke="none"/>')
    return t
add('lights', '手繪金色燈光隧道和花',
    arc_bulbs(90, 128, 76, 104, 18, 3.4) + arc_bulbs(90, 128, 54, 76, 14, 2.8)
    + arc_bulbs(90, 128, 34, 50, 10, 2.3) + arc_bulbs(90, 128, 18, 28, 7, 1.8)
    + f'<path d="M6,128 L174,128 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="{DGREEN}"/>'
    + ''.join(f'<path d="M{x},{136} L{x},{126}" stroke="{GREEN}" stroke-width="2"/>'
              f'<circle cx="{x}" cy="122" r="5" fill="{c}" stroke-width="1.4"/>'
              for x, c in [(22, PINK), (38, RED), (138, PINK), (154, GOLD), (166, RED)])
    + f'<circle cx="90" cy="118" r="11" fill="{PINK}"/>' + face(90, 117, .65)
    + f'<path d="M90,129 L90,136" stroke="{GREEN}" stroke-width="2.4"/>'
    + sparkle(30, 30, 4) + sparkle(152, 26, 4),
    bg=NAVY, dots=False)

# ---- teamlab：暗色背景裡發光的花 ----
def glow_flower(x, y, r, col, with_face=False):
    t = f'<circle cx="{x}" cy="{y}" r="{r*2.1:.1f}" fill="{col}" stroke="none" opacity=".22"/>'
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        t += (f'<circle cx="{x + r*math.cos(a):.1f}" cy="{y + r*math.sin(a):.1f}" r="{r*.72:.1f}" '
              f'fill="{col}" stroke-width="1.5"/>')
    t += f'<circle cx="{x}" cy="{y}" r="{r*.62:.1f}" fill="{WHITE}" stroke-width="1.5"/>'
    if with_face:
        t += face(x, y - 1, r / 18)
    return t
add('teamlab', '手繪暗色背景裡發光的花朵',
    glow_flower(88, 76, 22, PINK, True) + glow_flower(40, 46, 12, GOLD) + glow_flower(142, 44, 13, SKY)
    + glow_flower(36, 116, 11, GREEN) + glow_flower(144, 112, 14, GOLD)
    + sparkle(64, 26, 4) + sparkle(116, 124, 4) + sparkle(160, 78, 3)
    + snow([(20, 80), (112, 30), (70, 128), (164, 20)], 1.8, WHITE),
    bg=NAVY, dots=False)

# ---- maple：楓葉加小鳥居 ----
def maple_leaf(x, y, r, col, rot=0, with_face=False):
    # 五裂的楓葉：每一裂有主尖和兩側的小鋸齒，底下留葉柄的缺口
    lobes = [(152, .55), (210, .78), (270, 1.0), (330, .78), (388, .55)]
    pts = []
    def P(ang, rr):
        a = math.radians(ang + rot)
        pts.append(f'{x + r*rr*math.cos(a):.1f},{y + r*rr*math.sin(a):.1f}')
    P(90, .18)
    for i, (ang, L) in enumerate(lobes):
        P(ang - 13, L * .7)
        P(ang - 5, L * .82)
        P(ang, L)
        P(ang + 5, L * .82)
        P(ang + 13, L * .7)
        if i < len(lobes) - 1:
            P((ang + lobes[i+1][0]) / 2, .36)
    sx = x + r * .95 * math.cos(math.radians(90 + rot))
    sy = y + r * .95 * math.sin(math.radians(90 + rot))
    t = (f'<path d="M{x},{y} L{sx:.1f},{sy:.1f}" stroke-width="2"/>'
         f'<polygon points="{" ".join(pts)}" fill="{col}" stroke-width="1.6"/>'
         + ''.join(f'<path d="M{x},{y} L{x + r*.6*math.cos(math.radians(a + rot)):.1f},{y + r*.6*math.sin(math.radians(a + rot)):.1f}" '
                   f'stroke-width="1" opacity=".5"/>' for a, _ in lobes))
    if with_face:
        t += face(x, y - r * .1, r / 26)
    return t


add('maple', '手繪紅葉和小鳥居',
    f'<path d="M58,62 L56,128 M102,62 L104,128" stroke="{RED}" stroke-width="7"/>'
    + f'<path d="M58,62 L56,128 M102,62 L104,128" fill="none" stroke-width="1.2" opacity=".0"/>'
    + f'<rect x="52" y="72" width="56" height="7" rx="1" fill="{RED}"/>'
    + f'<path d="M38,50 Q80,42 122,50 L120,60 L40,60 Z" fill="{RED}"/>'
    + f'<path d="M36,48 Q80,38 124,48 L124,52 Q80,43 36,52 Z" fill="{INK}"/>'
    + f'<path d="M20,130 L160,130"/>'
    + maple_leaf(136, 92, 24, RED, 12, True) + maple_leaf(30, 34, 13, ORANGE, -20)
    + maple_leaf(150, 36, 11, GOLD, 30) + maple_leaf(30, 104, 12, ORANGE, 40)
    + maple_leaf(88, 112, 8, RED, -30))

# ---- ginkgo：黃色銀杏樹並排的步道 ----
def ginkgo_tree(x, base, h, w, with_face=False):
    t = (f'<rect x="{x - w*.07:.1f}" y="{base - h*.18:.1f}" width="{w*.14:.1f}" height="{h*.18:.1f}" fill="{DBROWN}" stroke-width="1.6"/>'
         f'<path d="M{x},{base - h} Q{x + w*.5:.1f},{base - h*.5:.1f} {x + w/2:.1f},{base - h*.22:.1f} '
         f'Q{x},{base - h*.1:.1f} {x - w/2:.1f},{base - h*.22:.1f} Q{x - w*.5:.1f},{base - h*.5:.1f} {x},{base - h} Z" fill="{GOLD}"/>')
    if with_face:
        t += face(x, base - h * .45, w / 44)
    return t
add('ginkgo', '手繪黃色銀杏樹並排的步道',
    f'<path d="M6,128 L174,128 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="#e9dcc0"/>'
    + f'<path d="M62,144 L86,84 L94,84 L118,144 Z" fill="{THATCH}" stroke-width="1.8"/>'
    + ginkgo_tree(80, 88, 20, 10) + ginkgo_tree(100, 88, 20, 10)
    + ginkgo_tree(68, 104, 36, 18) + ginkgo_tree(112, 104, 36, 18)
    + ginkgo_tree(38, 132, 74, 42, True) + ginkgo_tree(142, 132, 74, 42)
    + ''.join(f'<path d="M{x},{y} l-4,-6 q4,-3 8,0 Z" fill="{GOLD}" stroke-width="1.2"/>'
              for x, y in [(84, 130), (96, 118), (82, 104), (104, 138), (20, 140), (162, 140)])
    + sparkle(90, 34, 4) + star(28, 28, 5))

# ---- seasonal：南瓜燈加小聖誕樹 ----
add('seasonal', '手繪南瓜燈和小聖誕樹',
    f'<path d="M14,130 L166,130"/>'
    + f'<path d="M62,74 q2,-10 10,-14" fill="none" stroke="{DGREEN}" stroke-width="4"/>'
    + f'<ellipse cx="46" cy="104" rx="20" ry="25" fill="{ORANGE}"/>'
    + f'<ellipse cx="80" cy="104" rx="20" ry="25" fill="{ORANGE}"/>'
    + f'<ellipse cx="63" cy="104" rx="20" ry="27" fill="{ORANGE}"/>'
    + f'<path d="M80,64 q8,-4 12,4 q-8,4 -12,-4 Z" fill="{GREEN}" stroke-width="1.4"/>'
    + face(63, 104, 1.1)
    + tree(132, 120, 72, 54, smile=True)
    + star(30, 34, 5) + sparkle(100, 30, 4))

# ---- hotel：小旅館（招牌是床的圖示）----
add('hotel', '手繪小旅館建築，招牌是一張床的圖示',
    f'<path d="M20,132 L160,132"/>'
    + f'<rect x="44" y="46" width="92" height="86" rx="3" fill="{WALL}"/>'
    + f'<rect x="58" y="20" width="64" height="24" rx="5" fill="{GOLD}"/>'
    + f'<path d="M68,38 L68,28 M68,34 L112,34 L112,38" stroke-width="2"/>'
    + f'<rect x="72" y="28" width="10" height="5" rx="2" fill="{WHITE}" stroke-width="1.3"/>'
    + f'<path d="M84,34 L84,30 Q96,28 108,30 L108,34" fill="{PINK}" stroke-width="1.4"/>'
    + ''.join(f'<rect x="{x}" y="{y}" width="16" height="13" rx="2" fill="{SKY}" stroke-width="1.5"/>'
              for x in (54, 110) for y in (56, 78, 100))
    + face(90, 66, .85)
    + f'<rect x="78" y="100" width="24" height="32" rx="3" fill="{DBROWN}"/>'
    + f'<path d="M72,98 L108,98 L104,90 L76,90 Z" fill="{RED}"/>'
    + f'<circle cx="97" cy="117" r="1.8" fill="{GOLD}" stroke="none"/>'
    + f'<path d="M24,132 L24,118 Q30,108 36,118 L36,132 Z" fill="{GREEN}"/>'
    + f'<path d="M144,132 L144,118 Q150,108 156,118 L156,132 Z" fill="{GREEN}"/>'
    + star(28, 30, 5) + sparkle(152, 64, 4))

# ---- bunk：上下舖 ----
def bunk_level(y):
    return (f'<rect x="40" y="{y}" width="92" height="12" rx="3" fill="{WHITE}"/>'
            f'<rect x="72" y="{y-4}" width="60" height="14" rx="5" fill="{PINK}"/>'
            f'<rect x="44" y="{y-7}" width="24" height="10" rx="4" fill="{SKY}" stroke-width="1.6"/>'
            f'<circle cx="62" cy="{y-10}" r="9" fill="#f6d2b8"/>'
            f'<path d="M57,{y-11} q2,2 4,0 M64,{y-11} q2,2 4,0" fill="none" stroke-width="1.4"/>'
            f'<ellipse cx="56" cy="{y-7}" rx="2.4" ry="1.4" fill="{PINK}" stroke="none"/>')
add('bunk', '手繪上下舖，上下各睡一個小人',
    f'<path d="M36,30 L36,134 M136,30 L136,134" stroke="{DBROWN}" stroke-width="5"/>'
    + f'<path d="M36,66 L136,66 M36,118 L136,118" stroke="{DBROWN}" stroke-width="4"/>'
    + bunk_level(56) + bunk_level(108)
    + f'<path d="M144,58 L144,134 M160,58 L160,134" stroke="{BROWN}" stroke-width="3"/>'
    + ''.join(f'<path d="M144,{y} L160,{y}" stroke="{BROWN}" stroke-width="2.4"/>' for y in (72, 88, 104, 120))
    + f'<path d="M136,60 L160,58" stroke="{BROWN}" stroke-width="2.4"/>'
    + star(156, 24, 5) + sparkle(22, 40, 4) + sparkle(88, 26, 3))

# ---- ghosthouse：小房子和可愛小幽靈 ----
add('ghosthouse', '手繪小房子和一隻可愛的小幽靈',
    f'<path d="M14,132 L166,132"/>'
    + f'<rect x="24" y="76" width="66" height="56" fill="{WALL}"/>'
    + f'<path d="M16,80 L57,44 L98,80 Z" fill="{DBROWN}"/>'
    + f'<rect x="34" y="88" width="16" height="14" rx="2" fill="{GOLD}" stroke-width="1.5"/>'
    + f'<path d="M42,88 L42,102 M34,95 L50,95" stroke-width="1.2"/>'
    + f'<rect x="60" y="100" width="18" height="32" rx="2" fill="{BROWN}"/>'
    + f'<path d="M106,108 L106,70 Q106,40 132,40 Q158,40 158,70 L158,108 '
      f'Q152,100 146,108 Q140,116 132,108 Q126,100 119,108 Q112,116 106,108 Z" fill="{WHITE}"/>'
    + face(132, 70, 1.05)
    + f'<path d="M106,80 q-10,2 -12,-8 M158,80 q10,2 12,-8" fill="none" stroke-width="2.2"/>'
    + f'<path d="M30,20 a10,10 0 1,0 12,14 a8,8 0 1,1 -12,-14 Z" fill="{GOLD}"/>'
    + star(80, 26, 5) + sparkle(164, 22, 3))

# ---- medicine：藥瓶加化妝品 ----
add('medicine', '手繪藥瓶、口紅和乳霜罐',
    f'<path d="M14,132 L166,132"/>'
    + f'<rect x="30" y="56" width="52" height="76" rx="9" fill="{AMBER}"/>'
    + f'<rect x="34" y="40" width="44" height="18" rx="4" fill="{WHITE}"/>'
    + f'<path d="M38,46 L74,46 M38,52 L74,52" stroke-width="1.2" opacity=".6"/>'
    + f'<rect x="36" y="72" width="40" height="26" rx="3" fill="{WHITE}"/>'
    + f'<path d="M53,78 L59,78 L59,82 L63,82 L63,88 L59,88 L59,92 L53,92 L53,88 L49,88 L49,82 L53,82 Z" fill="{GREEN}" stroke-width="1.3"/>'
    + face(56, 112, .85)
    + f'<rect x="96" y="92" width="18" height="40" rx="3" fill="{GOLD}"/>'
    + f'<path d="M98,92 L98,74 Q105,64 112,72 L112,92 Z" fill="{RED}"/>'
    + f'<rect x="122" y="108" width="38" height="24" rx="5" fill="{WHITE}"/>'
    + f'<rect x="120" y="98" width="42" height="12" rx="4" fill="{PINK}"/>'
    + face(141, 120, .6, blush=False)
    + ''.join(f'<g transform="rotate({r} {x} {y})"><rect x="{x-8}" y="{y-4}" width="16" height="8" rx="4" fill="{WHITE}" stroke-width="1.4"/>'
              f'<path d="M{x},{y-4} L{x},{y+4}" stroke-width="1.2"/><rect x="{x}" y="{y-4}" width="8" height="8" rx="0" fill="{PINK}" stroke="none" opacity=".9"/></g>'
              for x, y, r in [(132, 40, -20), (152, 62, 25)])
    + sparkle(110, 30, 4) + star(28, 26, 5))

# ---- speech：對話泡泡 ----
add('speech', '手繪幾個對話泡泡',
    f'<path d="M22,26 L104,26 Q114,26 114,36 L114,62 Q114,72 104,72 L50,72 L36,86 L38,72 L32,72 Q22,72 22,62 L22,36 Q22,26 32,26 Z" fill="{SKY}"/>'
    + ''.join(f'<circle cx="{x}" cy="49" r="4" fill="{INK}" stroke="none"/>' for x in (52, 68, 84))
    + f'<path d="M74,82 L148,82 Q158,82 158,92 L158,112 Q158,122 148,122 L144,122 L148,136 L132,122 L84,122 Q74,122 74,112 L74,92 Q74,82 84,82 Z" fill="{PINK}"/>'
    + face(116, 100, .95)
    + f'<ellipse cx="44" cy="114" rx="24" ry="16" fill="{GOLD}"/>'
    + f'<path d="M30,126 L22,138 L40,129" fill="{GOLD}" stroke-width="2"/>'
    + heart(44, 114, 1.0, RED)
    + sparkle(150, 40, 4) + star(132, 56, 5))

# ---- shirt：掛在衣架上的 T 恤 ----
add('shirt', '手繪掛在衣架上的 T 恤',
    f'<path d="M90,30 Q90,20 98,20 Q106,20 104,28 Q102,34 90,38" fill="none" stroke-width="2.4"/>'
    + f'<path d="M90,38 L40,58 L140,58 Z" fill="none" stroke-width="2.4"/>'
    + f'<path d="M58,52 L74,46 Q90,58 106,46 L122,52 L148,72 L134,88 L122,80 L122,132 L58,132 L58,80 L46,88 L32,72 Z" fill="{LIGHTBLUE}"/>'
    + f'<path d="M74,46 Q90,62 106,46" fill="none" stroke-width="2"/>'
    + face(90, 92, 1.0)
    + star(90, 116, 6, GOLD)
    + sparkle(30, 36, 4) + star(152, 30, 5))

# ---- shop：有遮雨棚的小店面 ----
_aw = ''.join(f'<rect x="{30 + i*15}" y="50" width="15" height="16" fill="{RED if i % 2 == 0 else WHITE}" stroke-width="1.4"/>' for i in range(8))
_aw += ''.join(f'<path d="M{30 + i*15},66 q7.5,10 15,0" fill="{RED if i % 2 == 0 else WHITE}" stroke-width="1.4"/>' for i in range(8))
add('shop', '手繪有紅白遮雨棚的小店面',
    f'<path d="M14,132 L166,132"/>'
    + f'<rect x="34" y="50" width="112" height="82" fill="{WALL}"/>'
    + f'<rect x="44" y="20" width="92" height="28" rx="6" fill="{GOLD}"/>'
    + face(90, 32, .9)
    + _aw
    + f'<rect x="44" y="82" width="56" height="38" rx="2" fill="{SKY}"/>'
    + f'<rect x="52" y="102" width="12" height="18" rx="2" fill="{PINK}" stroke-width="1.4"/>'
    + f'<rect x="68" y="96" width="12" height="24" rx="2" fill="{GREEN}" stroke-width="1.4"/>'
    + f'<circle cx="90" cy="110" r="7" fill="{GOLD}" stroke-width="1.4"/>'
    + f'<rect x="110" y="82" width="28" height="50" rx="2" fill="{DBROWN}"/>'
    + f'<circle cx="132" cy="108" r="2" fill="{GOLD}" stroke="none"/>'
    + f'<path d="M150,132 L150,118 Q156,108 162,118 L162,132 Z" fill="{GREEN}"/>'
    + sparkle(24, 30, 4) + star(154, 30, 5))

# ---- search：放大鏡 ----
add('search', '手繪放大鏡',
    f'<path d="M106,96 L142,132" stroke="{DBROWN}" stroke-width="13"/>'
    + f'<path d="M106,96 L142,132" stroke="{BROWN}" stroke-width="8"/>'
    + f'<circle cx="80" cy="68" r="38" fill="{SKY}" stroke-width="7"/>'
    + f'<circle cx="80" cy="68" r="38" fill="none" stroke="{GOLD}" stroke-width="3"/>'
    + f'<path d="M58,50 Q66,38 80,36" fill="none" stroke="{WHITE}" stroke-width="4"/>'
    + face(80, 72, 1.1)
    + star(150, 34, 6) + sparkle(30, 120, 4) + sparkle(140, 76, 3))

# ---- notebook：筆記本和鉛筆 ----
add('notebook', '手繪筆記本和鉛筆',
    f'<g transform="rotate(-6 80 80)">'
    f'<rect x="38" y="24" width="86" height="108" rx="6" fill="{WHITE}"/>'
    + ''.join(f'<path d="M50,{y} L114,{y}" stroke="{SKY}" stroke-width="2"/>' for y in range(48, 128, 12))
    + ''.join(f'<circle cx="38" cy="{y}" r="5" fill="{CREAM}" stroke-width="1.8"/>' for y in range(36, 128, 16))
    + face(82, 66, .95)
    + heart(98, 104, .8, PINK)
    + '</g>'
    + f'<g transform="rotate(35 140 84)">'
      f'<rect x="132" y="40" width="16" height="70" fill="{GOLD}"/>'
      f'<rect x="132" y="32" width="16" height="10" rx="3" fill="{PINK}"/>'
      f'<path d="M132,110 L140,126 L148,110 Z" fill="{WALL}"/>'
      f'<path d="M137,120 L140,126 L143,120 Z" fill="{INK}"/></g>'
    + sparkle(150, 26, 4) + star(28, 132, 5))

if __name__ == '__main__':
    print(save(FILES, OUT), 'files')
