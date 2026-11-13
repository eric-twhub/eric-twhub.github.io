# 主題貼紙 B 組（2026-11-13）：人物、樂園、建築、動物類。共用工具在 kit.py。
# 跑 `python3 illust/st_b.py` 輸出 illust/st/*.svg。
# 不畫任何既有角色或 IP，只畫通用的東西。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st')

SKIN = '#ffdcc2'
HAIR = '#7a5340'
DARK = '#3b3550'
BLUE = '#7fb0de'
LBLUE = '#b9d6f2'
LILAC = '#c7b5ea'
ORANGE = '#f3a25f'
SUNSET = '#ffd9b0'
LAKE = '#9cc7ea'
STONE = '#b9b4ac'
ROOF = '#5fa08a'

FILES = {}


def add(name, label, inner, **kw):
    FILES[name] = sticker(name, label, inner, **kw)


# ---- girl：偶像風女孩拿麥克風 ----
add('girl', '手繪拿著麥克風的可愛女孩',
    # 雙馬尾與後髮
    f'<circle cx="56" cy="72" r="13" fill="{HAIR}"/><circle cx="124" cy="72" r="13" fill="{HAIR}"/>'
    f'<path d="M60,70 Q58,30 90,30 Q122,30 120,70 Z" fill="{HAIR}"/>'
    # 洋裝
    f'<path d="M74,88 L60,132 L120,132 L106,88 Z" fill="{PINK}"/>'
    f'<path d="M64,122 Q90,128 116,122" fill="none" stroke="{WHITE}" stroke-width="3"/>'
    # 頭
    f'<circle cx="90" cy="64" r="25" fill="{SKIN}"/>'
    # 瀏海
    f'<path d="M65,60 Q66,36 90,36 Q114,36 115,60 Q104,48 96,54 Q90,46 84,54 Q76,48 65,60 Z" fill="{HAIR}"/>'
    # 蝴蝶結
    f'<circle cx="66" cy="66" r="4" fill="{PINK}" stroke-width="1.4"/><circle cx="114" cy="66" r="4" fill="{PINK}" stroke-width="1.4"/>'
    f'<path d="M108,38 L97,30 L97,46 Z M108,38 L119,30 L119,46 Z" fill="{RED}" stroke-width="1.6"/>'
    f'<circle cx="108" cy="38" r="3.4" fill="{RED}" stroke-width="1.4"/>'
    + face(90, 68, 1.0)
    # 手與麥克風
    + f'<path d="M108,96 L124,84" stroke-width="3"/>'
    f'<circle cx="126" cy="80" r="7" fill="{GRAY}"/>'
    f'<path d="M121,77 L131,83 M120,82 L130,86" stroke-width="1.2" opacity=".6"/>'
    f'<circle cx="110" cy="96" r="5" fill="{SKIN}"/>'
    + star(38, 34, 8) + star(146, 30, 7, PINK) + sparkle(152, 108) + sparkle(28, 106)
    + f'<path d="M140,52 q4,-6 8,0 q4,-6 8,0 l-8,10 z" fill="{PINK}" stroke-width="1.6"/>')

# ---- skier：滑雪的人 ----
add('skier', '手繪滑雪的人，戴毛帽和護目鏡',
    f'<path d="M8,126 Q90,98 172,84 L172,124 Q172,144 152,144 L28,144 Q8,144 8,126 Z" fill="{WHITE}"/>'
    # 雪杖
    f'<path d="M72,80 L56,110 M106,76 L124,100" stroke-width="2.4"/>'
    f'<circle cx="56" cy="110" r="3" fill="{GRAY}" stroke-width="1.4"/><circle cx="124" cy="100" r="3" fill="{GRAY}" stroke-width="1.4"/>'
    # 雪板
    f'<path d="M46,116 L130,96" stroke="{RED}" stroke-width="5"/>'
    f'<path d="M46,116 L130,96" stroke-width="1" opacity=".4"/>'
    # 腿
    f'<path d="M80,90 L80,110 M96,88 L100,104" stroke="{DARK}" stroke-width="7"/>'
    # 外套
    f'<ellipse cx="88" cy="80" rx="18" ry="15" fill="{BLUE}"/>'
    f'<rect x="78" y="66" width="22" height="6" rx="3" fill="{GREEN}" stroke-width="1.6"/>'
    f'<circle cx="72" cy="80" r="4.5" fill="{RED}" stroke-width="1.6"/><circle cx="106" cy="76" r="4.5" fill="{RED}" stroke-width="1.6"/>'
    # 頭
    f'<circle cx="90" cy="54" r="14" fill="{SKIN}"/>'
    f'<path d="M75,52 Q75,32 90,32 Q105,32 105,52 Z" fill="{RED}"/>'
    f'<rect x="74" y="46" width="32" height="7" rx="3.5" fill="{WHITE}" stroke-width="1.6"/>'
    f'<rect x="80" y="38" width="20" height="8" rx="4" fill="{GOLD}" stroke-width="1.6"/>'
    f'<circle cx="90" cy="29" r="5" fill="{WHITE}"/>'
    + face(90, 60, .75)
    + snow([(30, 40), (52, 26), (140, 50), (156, 70), (128, 26)], 2.8, LBLUE)
    + star(150, 36, 6))

# ---- sumo：可愛相撲力士 ----
add('sumo', '手繪胖胖的可愛相撲力士',
    f'<path d="M22,134 Q90,122 158,134" fill="none" stroke-width="2"/>'
    f'<ellipse cx="66" cy="128" rx="15" ry="8" fill="{SKIN}"/><ellipse cx="114" cy="128" rx="15" ry="8" fill="{SKIN}"/>'
    f'<ellipse cx="44" cy="88" rx="11" ry="15" fill="{SKIN}" transform="rotate(25 44 88)"/>'
    f'<ellipse cx="136" cy="88" rx="11" ry="15" fill="{SKIN}" transform="rotate(-25 136 88)"/>'
    f'<ellipse cx="90" cy="96" rx="42" ry="34" fill="{SKIN}"/>'
    f'<path d="M50,104 Q90,114 130,104 L128,118 Q90,126 52,118 Z" fill="{NAVY}"/>'
    f'<rect x="84" y="114" width="12" height="18" rx="2" fill="{NAVY}"/>'
    f'<path d="M86,118 L86,130 M90,118 L90,131 M94,118 L94,130" stroke="{WHITE}" stroke-width="1.4"/>'
    f'<circle cx="80" cy="92" r="2" fill="{INK}" stroke="none" opacity=".5"/><circle cx="100" cy="92" r="2" fill="{INK}" stroke="none" opacity=".5"/>'
    f'<circle cx="90" cy="52" r="22" fill="{SKIN}"/>'
    f'<path d="M69,46 Q90,24 111,46 Q90,38 69,46 Z" fill="{DARK}"/>'
    f'<path d="M84,28 Q90,16 96,28 Q90,32 84,28 Z" fill="{DARK}"/>'
    + face(90, 56, 1.0)
    + star(30, 34, 7) + sparkle(152, 40) + sparkle(148, 108, 4))

# ---- forest：大樹下的小木屋 ----
add('forest', '手繪大樹下的森林小木屋',
    f'<path d="M14,132 L166,132" />'
    f'<rect x="40" y="70" width="18" height="62" rx="3" fill="{DBROWN}"/>'
    f'<circle cx="30" cy="62" r="18" fill="{DGREEN}"/><circle cx="68" cy="60" r="20" fill="{DGREEN}"/>'
    f'<circle cx="49" cy="42" r="26" fill="{GREEN}"/>'
    f'<circle cx="40" cy="38" r="3" fill="{RED}" stroke-width="1.2"/><circle cx="58" cy="52" r="3" fill="{RED}" stroke-width="1.2"/>'
    f'<rect x="126" y="40" width="10" height="20" fill="{BRICK}"/>'
    f'<path d="M132,34 q-5,-5 0,-10 q5,-5 0,-10" fill="none" stroke-width="1.6" opacity=".6"/>'
    f'<rect x="88" y="78" width="62" height="54" rx="2" fill="{CREAM}"/>'
    f'<path d="M80,82 L119,46 L158,82 Z" fill="{RED}"/>'
    f'<path d="M110,132 L110,110 Q119,100 128,110 L128,132" fill="{BROWN}"/>'
    f'<circle cx="140" cy="96" r="6" fill="{GOLD}" stroke-width="1.6"/>'
    + face(102, 96, .7)
    + f'<path d="M66,132 L66,124" stroke-width="2"/><path d="M58,125 Q66,112 74,125 Z" fill="{RED}" stroke-width="1.6"/>'
    f'<circle cx="63" cy="120" r="1.4" fill="{WHITE}" stroke="none"/><circle cx="69" cy="121" r="1.4" fill="{WHITE}" stroke="none"/>'
    + sparkle(152, 26, 4), dots=False)

# ---- cafe：拉花咖啡加蛋糕 ----
add('cafe', '手繪拉花愛心咖啡和一塊草莓蛋糕',
    f'<ellipse cx="68" cy="126" rx="42" ry="8" fill="{WHITE}"/>'
    f'<path d="M100,92 q16,0 16,13 q0,13 -16,11" fill="none" stroke-width="3.4"/>'
    f'<path d="M36,84 L100,84 Q98,124 68,124 Q38,124 36,84 Z" fill="{WHITE}"/>'
    f'<ellipse cx="68" cy="84" rx="32" ry="8" fill="{BROWN}"/>'
    f'<path d="M68,88 q-9,-6 -5,-9 q3,-2 5,2 q2,-4 5,-2 q4,3 -5,9 z" fill="{CREAM}" stroke-width="1.2"/>'
    + face(68, 104, .85)
    + f'<path d="M56,72 q-5,-6 0,-12 q5,-6 0,-12 M76,72 q-5,-6 0,-12 q5,-6 0,-12" fill="none" stroke-width="1.8" opacity=".55"/>'
    f'<ellipse cx="140" cy="128" rx="28" ry="6" fill="{WHITE}"/>'
    f'<path d="M116,126 L116,100 L164,110 L164,126 Z" fill="#fde7b8"/>'
    f'<path d="M116,100 L164,110 L164,116 L116,106 Z" fill="{PINK}"/>'
    f'<path d="M116,113 L164,120" stroke="{PINK}" stroke-width="3"/>'
    f'<circle cx="136" cy="96" r="7" fill="{RED}"/>'
    f'<path d="M132,90 L136,86 L140,90" fill="{GREEN}" stroke-width="1.6"/>'
    + sparkle(152, 40) + star(30, 34, 6))

# ---- ferris：摩天輪加雲霄飛車 ----
_g = ''
import math as _m
_cols = [RED, GOLD, BLUE, PINK, GREEN, LILAC, ORANGE, BLUE]
for i in range(8):
    a = i * _m.pi / 4
    gx, gy = 66 + 42 * _m.cos(a), 66 + 42 * _m.sin(a)
    _g += f'<path d="M66,66 L{gx:.1f},{gy:.1f}" stroke-width="1.4"/>'
    _g += f'<rect x="{gx-6:.1f}" y="{gy-3:.1f}" width="12" height="11" rx="4" fill="{_cols[i]}" stroke-width="1.6"/>'
add('ferris', '手繪摩天輪和雲霄飛車',
    f'<path d="M14,134 L166,134" />'
    f'<path d="M66,66 L44,134 M66,66 L88,134" stroke-width="3"/>'
    f'<circle cx="66" cy="66" r="42" fill="none" stroke-width="2.6"/>'
    + _g
    + f'<circle cx="66" cy="66" r="10" fill="{GOLD}"/>' + face(66, 65, .55, blush=False)
    + f'<path d="M116,134 L116,96 M136,134 L136,78 M156,134 L156,104" stroke-width="1.6"/>'
    f'<path d="M104,124 Q122,70 140,80 Q154,88 166,106" fill="none" stroke="{RED}" stroke-width="4"/>'
    f'<rect x="126" y="70" width="16" height="10" rx="3" fill="{GOLD}" transform="rotate(10 134 75)" stroke-width="1.6"/>'
    + sparkle(150, 30) + star(124, 40, 6), dots=False)

# ---- gamepad：可愛遊戲手把 ----
add('gamepad', '手繪有笑臉的遊戲手把',
    f'<path d="M42,62 Q42,50 58,50 L122,50 Q138,50 138,62 L150,102 Q154,124 136,124 Q124,124 116,106 L64,106 Q56,124 44,124 Q26,124 30,102 Z" fill="{LILAC}"/>'
    f'<path d="M52,78 L72,78 M62,68 L62,88" stroke-width="7"/>'
    f'<path d="M52,78 L72,78 M62,68 L62,88" stroke="{DARK}" stroke-width="4.5"/>'
    f'<circle cx="122" cy="68" r="5" fill="{RED}" stroke-width="1.6"/>'
    f'<circle cx="133" cy="79" r="5" fill="{GOLD}" stroke-width="1.6"/>'
    f'<circle cx="111" cy="79" r="5" fill="{BLUE}" stroke-width="1.6"/>'
    f'<circle cx="122" cy="90" r="5" fill="{GREEN}" stroke-width="1.6"/>'
    + face(90, 80, .9)
    + star(34, 32, 7) + sparkle(150, 30) + sparkle(90, 136, 4))

# ---- museum：柱子小博物館加氣球 ----
add('museum', '手繪有柱子的小博物館和氣球',
    f'<path d="M150,44 Q148,80 140,112 M162,62 Q158,92 146,114 M24,48 Q28,80 34,112" fill="none" stroke-width="1.4"/>'
    f'<ellipse cx="150" cy="36" rx="10" ry="12" fill="{RED}"/>'
    f'<ellipse cx="162" cy="54" rx="8" ry="10" fill="{GOLD}"/>'
    f'<ellipse cx="24" cy="40" rx="9" ry="11" fill="{PINK}"/>'
    f'<rect x="32" y="118" width="116" height="10" rx="2" fill="{STONE}"/>'
    f'<rect x="40" y="110" width="100" height="8" rx="2" fill="{GRAY}"/>'
    + ''.join(f'<rect x="{x}" y="72" width="12" height="38" fill="{WHITE}"/>' for x in (48, 70, 98, 120))
    + f'<rect x="38" y="64" width="104" height="9" rx="2" fill="{CREAM}"/>'
    f'<path d="M34,64 L90,36 L146,64 Z" fill="{CREAM}"/>'
    + face(90, 54, .7)
    + sparkle(110, 24, 4), dots=False)

# ---- rooftop：頂樓觀景台＋夕陽 ----
add('rooftop', '手繪高樓頂樓觀景台和夕陽',
    f'<rect x="10" y="10" width="160" height="130" rx="18" fill="{SUNSET}" stroke="none"/>'
    f'<circle cx="132" cy="76" r="20" fill="{GOLD}" stroke-width="1.8"/>'
    f'<path d="M24,40 q8,-8 18,-2 q8,-6 14,2 q6,6 -2,8 l-28,0 q-8,-2 -2,-8 z" fill="{WHITE}" stroke-width="1.6"/>'
    f'<rect x="50" y="72" width="80" height="68" fill="{LBLUE}"/>'
    + ''.join(f'<rect x="{x}" y="{y}" width="10" height="8" rx="1.5" fill="{CREAM}" stroke-width="1.2"/>'
              for x in (60, 76, 92, 108) for y in (86, 104, 122))
    + f'<path d="M46,72 L134,72" stroke-width="3"/>'
    f'<path d="M48,62 L132,62 M52,62 L52,72 M72,62 L72,72 M92,62 L92,72 M112,62 L112,72 M128,62 L128,72" stroke-width="1.6"/>'
    f'<rect x="73" y="53" width="14" height="14" rx="5" fill="{RED}" stroke-width="1.6"/><circle cx="80" cy="47" r="6" fill="{SKIN}" stroke-width="1.6"/>'
    f'<rect x="91" y="53" width="14" height="14" rx="5" fill="{BLUE}" stroke-width="1.6"/><circle cx="98" cy="47" r="6" fill="{SKIN}" stroke-width="1.6"/>'
    f'<path d="M86,58 L92,58" stroke-width="1.8"/>'
    + sparkle(150, 32) + star(34, 66, 5), dots=False)

# ---- harukas：階梯狀超高大樓 ----
add('harukas', '手繪階梯狀的超高大樓',
    f'<path d="M14,136 L166,136" />'
    f'<rect x="48" y="96" width="84" height="40" fill="{LBLUE}"/>'
    f'<rect x="56" y="62" width="68" height="34" fill="{SKY}"/>'
    f'<rect x="64" y="30" width="52" height="32" fill="{LBLUE}"/>'
    f'<path d="M90,30 L90,14" stroke-width="2.4"/><circle cx="90" cy="13" r="2.5" fill="{RED}" stroke-width="1.2"/>'
    + ''.join(f'<path d="M{x},{y1} L{x},{y2}" stroke-width="1.2" opacity=".5"/>'
              for x, y1, y2 in [(66, 100, 134), (84, 100, 134), (102, 100, 134), (120, 100, 134),
                                (74, 66, 94), (106, 66, 94), (78, 34, 60), (102, 34, 60)])
    + face(90, 76, .85)
    + f'<path d="M18,60 q6,-8 16,-3 q6,-5 12,1 q6,6 -2,7 l-24,0 q-8,-1 -2,-5 z" fill="{WHITE}" stroke-width="1.6"/>'
    f'<path d="M136,44 q6,-8 16,-3 q6,-5 12,1 q4,5 -2,7 l-24,0 q-8,-1 -2,-5 z" fill="{WHITE}" stroke-width="1.6"/>'
    + sparkle(150, 96) + star(32, 98, 6), dots=False)

# ---- castle：大阪城 ----
add('castle', '手繪大阪城，白牆綠屋頂加石牆',
    f'<path d="M40,104 L140,104 L150,136 L30,136 Z" fill="{STONE}"/>'
    f'<path d="M36,116 L144,116 M33,126 L147,126 M60,104 L58,116 M90,104 L90,116 M120,104 L122,116 M74,116 L72,126 M106,116 L108,126 M50,126 L48,136 M90,126 L90,136 M130,126 L132,136" stroke-width="1.2" opacity=".6"/>'
    f'<rect x="54" y="86" width="72" height="18" fill="{WHITE}"/>'
    f'<path d="M42,88 L56,76 L124,76 L138,88 Q90,82 42,88 Z" fill="{ROOF}"/>'
    f'<rect x="62" y="62" width="56" height="14" fill="{WHITE}"/>'
    f'<path d="M52,64 L64,54 L116,54 L128,64 Q90,59 52,64 Z" fill="{ROOF}"/>'
    f'<rect x="72" y="42" width="36" height="12" fill="{WHITE}"/>'
    f'<path d="M62,44 L90,24 L118,44 Q90,39 62,44 Z" fill="{ROOF}"/>'
    f'<path d="M58,76 L122,76 M66,54 L114,54" stroke="{GOLD}" stroke-width="2"/>'
    f'<path d="M64,44 l-4,-7 l6,3 z M116,44 l4,-7 l-6,3 z" fill="{GOLD}" stroke-width="1.2"/>'
    + ''.join(f'<rect x="{x}" y="66" width="6" height="6" fill="{DARK}" stroke-width="1"/>' for x in (70, 87, 104))
    + ''.join(f'<rect x="{x}" y="46" width="5" height="5" fill="{DARK}" stroke-width="1"/>' for x in (80, 95))
    + face(90, 94, .7)
    + f'<path d="M136,40 q6,-8 16,-3 q6,-5 12,1 q4,5 -2,7 l-24,0 q-8,-1 -2,-5 z" fill="{WHITE}" stroke-width="1.6"/>'
    + sparkle(30, 40) + star(150, 78, 5), dots=False)

# ---- hakone：湖上的船＋纜車＋富士山 ----
add('hakone', '手繪湖上觀光船、纜車和遠方的富士山',
    f'<path d="M24,94 L64,48 L104,94 Z" fill="{LBLUE}"/>'
    f'<path d="M52,62 L64,48 L76,62 Q70,58 67,64 Q64,58 61,64 Q58,58 52,62 Z" fill="{WHITE}" stroke-width="1.6"/>'
    f'<path d="M10,94 L170,94 L170,128 Q170,140 158,140 L22,140 Q10,140 10,128 Z" fill="{LAKE}"/>'
    f'<path d="M24,112 q6,-4 12,0 M128,130 q6,-4 12,0 M30,130 q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>'
    f'<path d="M66,104 L136,104 L128,122 L74,122 Z" fill="{RED}"/>'
    f'<rect x="80" y="90" width="40" height="14" rx="2" fill="{CREAM}"/>'
    + ''.join(f'<circle cx="{x}" cy="97" r="2.6" fill="{SKY}" stroke-width="1.1"/>' for x in (88, 100, 112))
    + f'<path d="M100,90 L100,70" stroke-width="2"/><path d="M100,70 L114,75 L100,80 Z" fill="{GOLD}" stroke-width="1.4"/>'
    + face(101, 111, .7, blush=False)
    + f'<path d="M96,14 L170,46" stroke-width="1.8"/>'
    f'<path d="M136,31 L136,38" stroke-width="1.6"/>'
    f'<rect x="126" y="38" width="20" height="16" rx="4" fill="{GOLD}"/>'
    f'<rect x="130" y="42" width="12" height="6" rx="1.5" fill="{SKY}" stroke-width="1.2"/>'
    + sparkle(30, 30, 4), dots=False)

# ---- fujicoaster：富士山前的雲霄飛車 ----
add('fujicoaster', '手繪富士山前面的雲霄飛車',
    f'<path d="M20,118 L90,34 L160,118 Z" fill="{BLUE}"/>'
    f'<path d="M70,58 L90,34 L110,58 Q102,52 97,60 Q90,52 84,60 Q78,52 70,58 Z" fill="{WHITE}"/>'
    f'<path d="M10,120 Q50,108 90,118 Q130,128 170,116 L170,132 Q170,142 160,142 L20,142 Q10,142 10,132 Z" fill="{GREEN}"/>'
    f'<path d="M28,134 L28,104 M54,134 L54,118 M118,134 L118,96 M146,134 L146,110" stroke-width="1.6"/>'
    f'<path d="M14,124 Q34,72 60,116 Q84,150 116,98 Q132,72 166,112" fill="none" stroke="{RED}" stroke-width="4.5"/>'
    f'<rect x="26" y="88" width="20" height="12" rx="4" fill="{GOLD}" transform="rotate(-28 36 94)" stroke-width="1.8"/>'
    + face(36, 93, .5, blush=False)
    + sparkle(150, 32) + star(30, 34, 6), dots=False)

# ---- windmill：荷蘭風車加鬱金香 ----
_bl = ''.join(
    f'<g transform="rotate({a} 90 56)"><rect x="84" y="8" width="12" height="46" rx="2" fill="{CREAM}"/>'
    f'<path d="M84,20 L96,20 M84,32 L96,32 M84,44 L96,44 M90,8 L90,54" stroke-width="1" opacity=".55"/></g>'
    for a in (20, 110, 200, 290))
add('windmill', '手繪荷蘭風車和鬱金香',
    f'<path d="M10,124 Q90,114 170,124 L170,132 Q170,142 160,142 L20,142 Q10,142 10,132 Z" fill="{GREEN}"/>'
    f'<path d="M72,62 L108,62 L116,128 L64,128 Z" fill="{BROWN}"/>'
    f'<path d="M68,64 L90,44 L112,64 Z" fill="{DBROWN}"/>'
    f'<path d="M84,128 L84,114 Q90,106 96,114 L96,128" fill="{DBROWN}"/>'
    + face(90, 88, .8)
    + _bl
    + f'<circle cx="90" cy="56" r="5" fill="{GOLD}" stroke-width="1.6"/>'
    + ''.join(f'<path d="M{x},128 L{x},114" stroke="{DGREEN}" stroke-width="2"/>'
              f'<path d="M{x-6},108 L{x-6},116 Q{x},121 {x+6},116 L{x+6},108 L{x+3},112 L{x},107 L{x-3},112 Z" fill="{c}" stroke-width="1.5"/>'
              for x, c in [(26, RED), (40, PINK), (140, GOLD), (154, RED)])
    + sparkle(150, 30) + star(30, 36, 6), dots=False)

# ---- whaleshark：可愛鯨鯊 ----
_spots = [(72, 62), (86, 58), (100, 60), (114, 64), (128, 70), (80, 72), (96, 70), (110, 76), (124, 82), (66, 74)]
add('whaleshark', '手繪藍底白點的可愛鯨鯊和泡泡',
    f'<path d="M14,124 q8,-5 16,0 q8,5 16,0 M120,132 q8,-5 16,0 q8,5 16,0" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
    f'<path d="M84,100 L96,124 L106,100 Z" fill="{BLUE}"/>'
    f'<path d="M28,82 Q36,50 96,52 Q136,54 148,72 L170,54 L164,80 L170,106 L148,90 Q136,108 96,110 Q36,110 28,82 Z" fill="{BLUE}"/>'
    f'<path d="M34,90 Q60,106 104,106 Q130,104 146,90 Q118,96 80,94 Q50,92 34,90 Z" fill="{LBLUE}" stroke-width="1.6"/>'
    f'<path d="M92,52 L102,36 L112,54" fill="{BLUE}"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{WHITE}" stroke="none"/>' for x, y in _spots)
    + f'<circle cx="48" cy="76" r="2.4" fill="{INK}" stroke="none"/>'
    f'<path d="M32,86 Q42,92 54,88" fill="none" stroke-width="1.8"/>'
    f'<ellipse cx="54" cy="84" rx="4" ry="2.4" fill="{PINK}" stroke="none" opacity=".8"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{WHITE}" stroke-width="1.8"/>'
              for x, y, r in [(22, 54, 5), (30, 38, 3.5), (18, 28, 2.5)])
    + sparkle(150, 30), bg='#dceefa', dots=False)

# ---- penguin：雪地上排隊走路的企鵝 ----


def penguin(x, y, s, scarf=None):
    t = (f'<ellipse cx="{x-9*s}" cy="{y+4*s}" rx="{5*s}" ry="{11*s}" fill="{NAVY}" transform="rotate(18 {x-9*s} {y+4*s})"/>'
         f'<ellipse cx="{x+9*s}" cy="{y+4*s}" rx="{5*s}" ry="{11*s}" fill="{NAVY}" transform="rotate(-18 {x+9*s} {y+4*s})"/>'
         f'<ellipse cx="{x}" cy="{y}" rx="{14*s}" ry="{21*s}" fill="{NAVY}"/>'
         f'<ellipse cx="{x}" cy="{y+5*s}" rx="{9.5*s}" ry="{14*s}" fill="{WHITE}" stroke-width="1.4"/>'
         f'<ellipse cx="{x-5*s}" cy="{y+21*s}" rx="{5*s}" ry="{2.6*s}" fill="{GOLD}" stroke-width="1.4"/>'
         f'<ellipse cx="{x+5*s}" cy="{y+21*s}" rx="{5*s}" ry="{2.6*s}" fill="{GOLD}" stroke-width="1.4"/>')
    t += (f'<circle cx="{x-4.5*s}" cy="{y-9*s}" r="{1.9*s}" fill="{WHITE}" stroke="none"/>'
          f'<circle cx="{x+4.5*s}" cy="{y-9*s}" r="{1.9*s}" fill="{WHITE}" stroke="none"/>'
          f'<path d="M{x-3*s},{y-5*s} L{x+3*s},{y-5*s} L{x},{y-1*s} Z" fill="{GOLD}" stroke-width="1.2"/>'
          f'<ellipse cx="{x-8*s}" cy="{y-3*s}" rx="{2.6*s}" ry="{1.6*s}" fill="{PINK}" stroke="none" opacity=".85"/>'
          f'<ellipse cx="{x+8*s}" cy="{y-3*s}" rx="{2.6*s}" ry="{1.6*s}" fill="{PINK}" stroke="none" opacity=".85"/>')
    if scarf:
        t += f'<path d="M{x-11*s},{y+1*s} Q{x},{y+6*s} {x+11*s},{y+1*s} L{x+10*s},{y+6*s} Q{x},{y+11*s} {x-10*s},{y+6*s} Z" fill="{scarf}" stroke-width="1.4"/>'
    return t


add('penguin', '手繪在雪地上排成一列走路的企鵝',
    f'<path d="M10,118 Q90,106 170,118 L170,132 Q170,142 160,142 L20,142 Q10,142 10,132 Z" fill="{WHITE}"/>'
    + penguin(140, 92, 1.0, RED) + penguin(104, 98, .85, GOLD) + penguin(72, 102, .75, GREEN) + penguin(44, 106, .65)
    + snow([(30, 40), (60, 28), (120, 34), (150, 50), (90, 50)], 2.6, LBLUE)
    + star(154, 26, 5), dots=False)

# ---- owl：戴巫師帽、圍圍巾的貓頭鷹 ----
add('owl', '手繪戴巫師帽、圍圍巾的貓頭鷹',
    f'<path d="M30,128 L150,128" stroke="{DBROWN}" stroke-width="5"/>'
    f'<ellipse cx="56" cy="98" rx="10" ry="22" fill="{DBROWN}" transform="rotate(14 56 98)"/>'
    f'<ellipse cx="124" cy="98" rx="10" ry="22" fill="{DBROWN}" transform="rotate(-14 124 98)"/>'
    f'<ellipse cx="90" cy="92" rx="36" ry="36" fill="{BROWN}"/>'
    f'<ellipse cx="90" cy="106" rx="22" ry="18" fill="{CREAM}" stroke-width="1.6"/>'
    f'<path d="M82,100 l4,4 l4,-4 M92,100 l4,4 l4,-4 M86,110 l4,4 l4,-4" fill="none" stroke-width="1.3"/>'
    f'<circle cx="76" cy="82" r="11" fill="{WHITE}"/><circle cx="104" cy="82" r="11" fill="{WHITE}"/>'
    f'<circle cx="77" cy="83" r="5" fill="{INK}" stroke="none"/><circle cx="103" cy="83" r="5" fill="{INK}" stroke="none"/>'
    f'<circle cx="78.5" cy="81" r="1.6" fill="{WHITE}" stroke="none"/><circle cx="104.5" cy="81" r="1.6" fill="{WHITE}" stroke="none"/>'
    f'<path d="M86,92 L94,92 L90,99 Z" fill="{GOLD}" stroke-width="1.4"/>'
    f'<ellipse cx="64" cy="96" rx="4" ry="2.4" fill="{PINK}" stroke="none" opacity=".85"/>'
    f'<ellipse cx="116" cy="96" rx="4" ry="2.4" fill="{PINK}" stroke="none" opacity=".85"/>'
    f'<path d="M58,118 Q90,128 122,118 L120,126 Q90,134 60,126 Z" fill="{RED}"/>'
    f'<path d="M110,122 L118,140 L128,136 L120,120" fill="{RED}"/>'
    f'<path d="M72,121 L72,129 M86,123 L86,131 M100,123 L100,131 M114,138 L124,135" stroke="{GOLD}" stroke-width="2.4"/>'
    f'<ellipse cx="80" cy="128" rx="5" ry="3" fill="{GOLD}" stroke-width="1.4"/><ellipse cx="100" cy="128" rx="5" ry="3" fill="{GOLD}" stroke-width="1.4"/>'
    f'<ellipse cx="90" cy="62" rx="40" ry="8" fill="{NAVY}"/>'
    f'<path d="M64,60 Q74,36 92,14 Q100,10 104,18 Q100,26 112,58 Z" fill="{NAVY}"/>'
    + star(88, 42, 6) + sparkle(36, 40) + star(148, 32, 5) + sparkle(150, 70, 4), dots=False)

if __name__ == '__main__':
    print(save(FILES, OUT), 'files')
