# 銀山溫泉頁的「溫泉街有什麼」插圖與提醒卡（2026-11-13）。
# 參考銀山温泉官網散策頁（ginzanonsen.jp/ginzan/walk.html）與 2026–2027 冬季交通案内（winter/2026/）畫成可愛版，不描照片構圖。
# 輸出 illust/sp/japan-ginzan-onsen/*.svg（240×180）。說明文字放在 illust/spots/japan-ginzan-onsen.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-ginzan-onsen')
W, H = 240, 180
SKYW = '#e3eef7'
NIGHT = '#2e3a63'
RIVER = '#9fc3dc'
SLATE = '#6c7a8c'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('gz-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def inn(x, base, w, floors=3, fh=24, win=GOLD):
    # 多層木造旅館：每層一排亮燈的窗，屋簷積雪
    t = ''
    for i in range(floors):
        y = base - (i + 1) * fh
        ww = w - i * 6
        x0 = x - ww / 2
        t += (f'<rect x="{x0:.0f}" y="{y}" width="{ww}" height="{fh}" fill="{BROWN}"/>'
              + ''.join(f'<rect x="{x0 + 5 + j*((ww-10)/3):.0f}" y="{y+6}" width="{(ww-10)/3 - 4:.0f}" height="{fh-12}" rx="1.5" '
                        f'fill="{win}" stroke-width="1.2"/>' for j in range(3))
              + f'<path d="M{x0-5:.0f},{y+1} L{x0+ww+5:.0f},{y+1} L{x0+ww-2:.0f},{y-5} L{x0+2:.0f},{y-5} Z" fill="{SLATE}"/>'
              + f'<path d="M{x0-3:.0f},{y-4} Q{x:.0f},{y-9} {x0+ww+3:.0f},{y-4}" stroke="{WHITE}" stroke-width="3.4" fill="none"/>')
    return t


def lamp(x, base, h=40):
    return (f'<circle cx="{x}" cy="{base-h+6}" r="11" fill="{GOLD}" stroke="none" opacity=".3"/>'
            f'<path d="M{x},{base} L{x},{base-h+12}" stroke-width="2.6"/>'
            f'<path d="M{x-6},{base-h+2} L{x+6},{base-h+2} L{x+4},{base-h+13} L{x-4},{base-h+13} Z" fill="{GOLD}" stroke-width="1.6"/>'
            f'<path d="M{x-7},{base-h+2} L{x},{base-h-4} L{x+7},{base-h+2} Z" fill="{INK}"/>')


def person(x, y, col=RED, s=1.0, hat=None):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if hat:
        t += f'<path d="M{x-6.5*s},{y-1*s} q{6.5*s},{-11*s} {13*s},0 Z" fill="{hat}" stroke-width="1.4"/>'
    return t


# 1. 溫泉街：銀山川兩岸排滿旅館
card('street', '手繪雪夜裡沿著小河兩岸排開的木造溫泉旅館',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + inn(40, 128, 62, 3) + inn(200, 128, 62, 3)
     + inn(96, 112, 34, 2, 18) + inn(146, 112, 34, 2, 18)
     + f'<path d="M3,128 L237,128 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e6eefa"/>'
     + f'<path d="M96,177 L112,114 L130,114 L146,177 Z" fill="{RIVER}"/>'
     + f'<path d="M110,140 q6,-3 12,0 M106,158 q8,-3 16,0" stroke="{WHITE}" stroke-width="2" fill="none"/>'
     + lamp(80, 150, 34) + lamp(162, 150, 34)
     + face(40, 82, .6)
     + snow([(24, 22), (70, 30), (120, 18), (170, 34), (220, 20), (120, 60)], 2.2, WHITE)
     + f'<path d="M214,40 a8,8 0 1,0 10,11 a6,6 0 1,1 -10,-11 Z" fill="{GOLD}"/>')

# 2. 白銀橋：溫泉街入口的橋
card('bridge', '手繪雪中一座拱起來的橋，橋下是小河，橋頭有可以坐的地方',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,124 L237,124 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{RIVER}"/>'
     + f'<path d="M3,100 L40,100 L50,124 L3,124 Z M237,100 L200,100 L190,124 L237,124 Z" fill="{WHITE}"/>'
     + f'<path d="M30,100 Q120,56 210,100 L210,110 Q120,70 30,110 Z" fill="{GRAY}"/>'
     + ''.join(f'<path d="M{x},{y} L{x},{y-16}" stroke-width="2"/>' for x, y in [(52, 92), (76, 82), (100, 76), (120, 74), (140, 76), (164, 82), (188, 92)])
     + f'<path d="M30,86 Q120,42 210,86" fill="none" stroke-width="2.4"/>'
     + f'<path d="M28,84 Q120,38 212,84" fill="none" stroke="{WHITE}" stroke-width="4"/>'
     + f'<rect x="196" y="80" width="34" height="8" rx="3" fill="{BROWN}"/><path d="M200,88 L200,98 M226,88 L226,98" stroke-width="2.4"/>'
     + person(110, 54, RED, .8, GOLD) + person(134, 56, SKY, .75, PINK)
     + f'<path d="M80,150 q8,-3 16,0 M150,160 q8,-3 16,0" stroke="{WHITE}" stroke-width="2" fill="none"/>'
     + flake(30, 30) + flake(210, 30) + star(170, 40, 5))

# 3. 和楽足湯：河邊的泡腳池
card('ashiyu', '手繪河邊冒著熱氣的泡腳池，有人坐著泡腳',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{RIVER}"/>'
     + floor(118, WHITE)
     + f'<rect x="40" y="108" width="160" height="34" rx="10" fill="{BROWN}"/>'
     + f'<rect x="54" y="114" width="132" height="22" rx="8" fill="#bfe3f5"/>'
     + f'<path d="M80,104 q-6,-8 0,-16 q6,-8 0,-16 M120,100 q-6,-8 0,-16 q6,-8 0,-16 M160,104 q-6,-8 0,-16 q6,-8 0,-16" '
       f'fill="none" stroke-width="1.8" opacity=".5"/>'
     + person(90, 86, RED, 1.0, GOLD) + person(146, 86, GREEN, 1.0, PINK)
     + f'<path d="M84,108 L82,124 M96,108 L98,124 M140,108 L138,124 M152,108 L154,124" stroke="#f9d9c0" stroke-width="5"/>'
     + face(120, 128, .6)
     + flake(30, 30) + flake(210, 34) + star(200, 70, 5))

# 4. 共同浴場：大湯（かじか湯）與しろがね湯
card('baths', '手繪兩間小小的公共澡堂，門口掛著布簾',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<rect x="20" y="70" width="90" height="74" rx="2" fill="{BROWN}"/>'
     + f'<path d="M12,74 L65,40 L118,74 Z" fill="{SLATE}"/><path d="M16,72 Q65,62 114,72" stroke="{WHITE}" stroke-width="5" fill="none"/>'
     + f'<rect x="44" y="96" width="42" height="48" rx="2" fill="{GOLD}" stroke-width="1.6"/>'
     + f'<path d="M44,96 L86,96 L86,118 L44,118 Z" fill="{DGREEN}" stroke-width="1.6"/><path d="M58,96 L58,118 M72,96 L72,118" stroke-width="1.4"/>'
     + f'<rect x="132" y="80" width="88" height="64" rx="10" fill="#e9e4dc"/>'
     + f'<path d="M126,84 L226,84 L226,76 L126,76 Z" fill="{SLATE}"/>'
     + f'<rect x="146" y="94" width="60" height="22" rx="3" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<rect x="162" y="118" width="28" height="26" rx="2" fill="{SKY}" stroke-width="1.4"/>'
     + f'<path d="M154,64 q-6,-8 0,-16 q6,-8 0,-16 M176,64 q-6,-8 0,-16 q6,-8 0,-16" fill="none" stroke-width="1.8" opacity=".5"/>'
     + face(65, 84, .6) + face(176, 104, .6)
     + floor(144, WHITE)
     + flake(30, 30) + flake(120, 22, 4) + star(214, 40, 5))

# 5. 白銀之瀑（落差 22 公尺）與前面的地藏
card('falls', '手繪溫泉街盡頭的瀑布，前面有一尊小地藏',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,40 Q60,20 100,30 L100,150 L3,150 Z" fill="#b8c4d2"/>'
     + f'<path d="M237,40 Q180,20 150,30 L150,150 L237,150 Z" fill="#b8c4d2"/>'
     + f'<path d="M100,30 Q125,24 150,30 L156,146 L94,146 Z" fill="#dff1fb"/>'
     + ''.join(f'<path d="M{x},34 L{x+2},140" stroke="{RIVER}" stroke-width="2.4"/>' for x in (108, 120, 132, 142))
     + f'<ellipse cx="125" cy="150" rx="46" ry="10" fill="{RIVER}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="{WHITE}" stroke-width="1.2"/>' for x, y in [(98, 142), (152, 140), (110, 150), (140, 152)])
     + f'<path d="M20,48 q20,-8 40,-2 M180,46 q20,-6 40,0" stroke="{WHITE}" stroke-width="5" fill="none"/>'
     + floor(154, WHITE)
     + f'<path d="M190,154 L190,134 Q190,122 200,122 Q210,122 210,134 L210,154 Z" fill="#b9bfc8"/>'
     + f'<circle cx="200" cy="118" r="9" fill="#b9bfc8"/>' + face(200, 118, .45)
     + f'<path d="M192,130 L208,130 L206,140 L194,140 Z" fill="{RED}" stroke-width="1.4"/>'
     + flake(40, 70, 4) + flake(214, 70) + star(60, 100, 5))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('gz-' + name, 120, 120, label, inner, bg='#fff3c4')


# 路中間的菱形是中線，走靠河那一半
rem('r-diamond', '手繪提醒：路中間的菱形標記，走靠河那一邊',
    f'<clipPath id="gz-rclip"><rect x="4.5" y="4.5" width="111" height="111" rx="20.5"/></clipPath><g clip-path="url(#gz-rclip)">'
    f'<rect x="0" y="0" width="38" height="120" fill="{BROWN}"/>'
    f'<path d="M14,20 L32,20 M14,40 L32,40" stroke-width="1.4"/>'
    f'<path d="M38,0 L90,0 L90,120 L38,120 Z" fill="{WHITE}" stroke-width="1.4"/>'
    f'<path d="M90,0 L120,0 L120,120 L90,120 Z" fill="{RIVER}" stroke-width="1.4"/>'
    + ''.join(f'<path d="M64,{y-7} L70,{y} L64,{y+7} L58,{y} Z" fill="{GOLD}" stroke-width="1.4"/>' for y in (26, 60, 94))
    + f'<path d="M40,12 L50,12 M40,16 L46,16" stroke="{RED}" stroke-width="2"/>'
    + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="5" fill="{DBROWN}" stroke-width="1.1"/>' for x, y in [(78, 100), (82, 84), (78, 68), (82, 52), (78, 36)])
    + f'<path d="M12,52 q6,-8 12,0 q6,-8 12,0" fill="{WHITE}" stroke-width="1.4"/>'
    + '</g>')

# 回程的優先班次印在票上
rem('r-return', '手繪提醒：票上印著回程班次的時間',
    f'<rect x="12" y="28" width="96" height="58" rx="6" fill="{WHITE}"/>'
    f'<path d="M80,28 L80,86" stroke-width="1.6" stroke-dasharray="4 4"/>'
    f'<rect x="20" y="38" width="50" height="10" rx="2" fill="{SKY}" stroke-width="1.2"/>'
    f'<rect x="20" y="56" width="50" height="16" rx="3" fill="{GOLD}" stroke-width="1.4"/>'
    f'<circle cx="94" cy="57" r="10" fill="{WHITE}"/><path d="M94,57 L94,50 M94,57 L99,60" stroke-width="2"/>'
    f'<rect x="30" y="94" width="60" height="18" rx="6" fill="{GREEN}"/>'
    f'<circle cx="42" cy="112" r="4" fill="{INK}"/><circle cx="78" cy="112" r="4" fill="{INK}"/>'
    f'<rect x="36" y="98" width="10" height="7" rx="1" fill="{SKY}" stroke-width="1"/><rect x="52" y="98" width="10" height="7" rx="1" fill="{SKY}" stroke-width="1"/>')

print(save(F, OUT), 'files')
