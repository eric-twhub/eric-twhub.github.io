# 旭山動物園頁的「冬天看得到什麼」插圖與提醒卡（2026-11-13）。
# 參考官網施設紹介（city.asahikawa.hokkaido.jp/asahiyamazoo/facilityinformation/）各館的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/japan-asahiyama-zoo/*.svg（240×180）。說明文字放在 illust/spots/japan-asahiyama-zoo.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-asahiyama-zoo')
W, H = 240, 180
SEA = '#bfe3f5'
WATER = '#8fc8e8'
SNOWBG = '#e8f3fb'
ORANGE = '#f4a24a'
BEAR = '#fbf6ea'
SEAL = '#c9ced6'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('az-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    # 框內底部的地面（不超出圓角框）
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def king(x, y, s=1.0):
    # 正面站著的國王企鵝：深色背、白肚子、頭兩側橘色
    return (f'<ellipse cx="{x-10*s}" cy="{y+4*s}" rx="{5*s}" ry="{12*s}" fill="{NAVY}" transform="rotate(16 {x-10*s} {y+4*s})"/>'
            f'<ellipse cx="{x+10*s}" cy="{y+4*s}" rx="{5*s}" ry="{12*s}" fill="{NAVY}" transform="rotate(-16 {x+10*s} {y+4*s})"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{14*s}" ry="{23*s}" fill="{NAVY}"/>'
            f'<ellipse cx="{x}" cy="{y+6*s}" rx="{10*s}" ry="{15*s}" fill="{WHITE}" stroke-width="1.4"/>'
            f'<path d="M{x-8*s},{y-4*s} Q{x},{y+1*s} {x+8*s},{y-4*s} Q{x},{y-1*s} {x-8*s},{y-4*s} Z" fill="{ORANGE}" stroke="none"/>'
            f'<ellipse cx="{x-10*s}" cy="{y-12*s}" rx="{2.4*s}" ry="{4*s}" fill="{ORANGE}" stroke="none"/>'
            f'<ellipse cx="{x+10*s}" cy="{y-12*s}" rx="{2.4*s}" ry="{4*s}" fill="{ORANGE}" stroke="none"/>'
            f'<circle cx="{x-4.5*s}" cy="{y-12*s}" r="{2*s}" fill="{WHITE}" stroke="none"/>'
            f'<circle cx="{x+4.5*s}" cy="{y-12*s}" r="{2*s}" fill="{WHITE}" stroke="none"/>'
            f'<path d="M{x-2.5*s},{y-8*s} L{x+2.5*s},{y-8*s} L{x},{y-3*s} Z" fill="{ORANGE}" stroke-width="1.1"/>'
            f'<ellipse cx="{x-5*s}" cy="{y+23*s}" rx="{5*s}" ry="{2.6*s}" fill="{ORANGE}" stroke-width="1.3"/>'
            f'<ellipse cx="{x+5*s}" cy="{y+23*s}" rx="{5*s}" ry="{2.6*s}" fill="{ORANGE}" stroke-width="1.3"/>')


def swim_peng(x, y, s=1.0, rot=0):
    # 在水裡游、像在飛的企鵝（側面，頭朝右）
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-6,-4 L-22,-14 L-14,0 Z" fill="{NAVY}" stroke-width="1.4"/>'
            f'<ellipse cx="0" cy="0" rx="24" ry="10" fill="{NAVY}"/>'
            f'<path d="M-18,3 Q0,12 20,3 Q2,8 -18,3 Z" fill="{WHITE}" stroke-width="1.2"/>'
            f'<path d="M22,-2 L32,0 L22,3 Z" fill="{ORANGE}" stroke-width="1.2"/>'
            f'<circle cx="16" cy="-3" r="1.8" fill="{WHITE}" stroke="none"/>'
            f'<path d="M-24,0 L-32,-5 L-31,5 Z" fill="{NAVY}" stroke-width="1.3"/>'
            f'</g>')


def person(x, y, col=RED, s=1.0, hat=None):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if hat:
        t += f'<path d="M{x-6.5*s},{y-1*s} q{6.5*s},{-11*s} {13*s},0 Z" fill="{hat}" stroke-width="1.4"/>'
    return t


def seal(x, y, s=1.0, rot=0, col=SEAL):
    # 有斑點的海豹，頭朝右
    t = (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
         f'<path d="M-30,0 L-42,-8 L-40,8 Z" fill="{col}" stroke-width="1.6"/>'
         f'<ellipse cx="0" cy="0" rx="32" ry="13" fill="{col}"/>'
         f'<ellipse cx="2" cy="10" rx="7" ry="3.4" fill="{col}" transform="rotate(30 2 10)" stroke-width="1.4"/>')
    for dx, dy in [(-18, -4), (-10, 2), (-2, -6), (6, 3), (-22, 4), (12, -6)]:
        t += f'<circle cx="{dx}" cy="{dy}" r="1.6" fill="#7d8796" stroke="none"/>'
    t += (f'<circle cx="22" cy="-4" r="2.2" fill="{INK}" stroke="none"/>'
          f'<circle cx="28" cy="1" r="1.6" fill="{INK}" stroke="none"/>'
          f'<ellipse cx="20" cy="3" rx="3" ry="1.8" fill="{PINK}" stroke="none" opacity=".85"/>'
          f'<path d="M30,4 l6,-1 M30,6 l6,2" stroke-width="1"/>'
          f'</g>')
    return t


def bear(x, y, s=1.0):
    # 正面的北極熊頭＋身體（可愛版）
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<ellipse cx="0" cy="26" rx="30" ry="24" fill="{BEAR}"/>'
            f'<circle cx="-17" cy="-16" r="7" fill="{BEAR}"/><circle cx="17" cy="-16" r="7" fill="{BEAR}"/>'
            f'<circle cx="0" cy="0" r="22" fill="{BEAR}"/>'
            f'<ellipse cx="0" cy="8" rx="9" ry="6.5" fill="{WHITE}" stroke-width="1.4"/>'
            f'<ellipse cx="0" cy="5" rx="3.6" ry="2.6" fill="{INK}" stroke="none"/>'
            f'<circle cx="-8" cy="-3" r="2.2" fill="{INK}" stroke="none"/><circle cx="8" cy="-3" r="2.2" fill="{INK}" stroke="none"/>'
            f'<path d="M-2.6,11 q2.6,2.6 5.2,0" fill="none" stroke-width="1.4"/>'
            f'<ellipse cx="-14" cy="5" rx="3.4" ry="2" fill="{PINK}" stroke="none" opacity=".8"/>'
            f'<ellipse cx="14" cy="5" rx="3.4" ry="2" fill="{PINK}" stroke="none" opacity=".8"/>'
            f'</g>')


# 1. 企鵝散步（國王企鵝走在紅線內側）
card('walk', '手繪國王企鵝在雪地步道上排隊走路，旁邊有紅線和觀眾',
     floor(96, WHITE)
     + f'<path d="M3,112 Q120,104 237,112" fill="none" stroke="{RED}" stroke-width="2.6" stroke-dasharray="7 5"/>'
     + f'<path d="M3,160 Q120,152 237,160" fill="none" stroke="{RED}" stroke-width="2.6" stroke-dasharray="7 5"/>'
     + king(190, 124, .82) + king(150, 128, .78) + king(110, 132, .74) + king(72, 134, .7)
     + person(40, 70, RED, .85, GREEN) + person(66, 66, SKY, .8, PINK) + person(176, 66, GOLD, .85, RED) + person(202, 70, GREEN, .8, GOLD)
     + flake(30, 30) + flake(120, 24, 4) + flake(214, 34) + star(100, 40, 5),
     bg=SNOWBG)

# 2. 企鵝館的 360 度水中隧道
card('tunnel', '手繪企鵝館的水中隧道，企鵝在頭頂上像飛一樣游泳',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{WATER}"/>'
     + swim_peng(70, 46, .9, -8) + swim_peng(170, 36, .75, 10) + swim_peng(196, 82, .7, -14) + swim_peng(44, 92, .65, 6)
     + f'<path d="M40,177 L40,132 A80,62 0 0,1 200,132 L200,177" fill="{SEA}" stroke-width="2.6"/>'
     + f'<path d="M58,177 L58,136 A62,46 0 0,1 182,136 L182,177" fill="none" stroke="{WHITE}" stroke-width="2" opacity=".8"/>'
     + person(100, 140, RED, .9, GOLD) + person(132, 144, GREEN, .85) + person(156, 138, PINK, .9, SKY)
     + f'<path d="M100,124 l-4,-8 M156,122 l4,-8" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke="{WHITE}" stroke-width="1.4"/>' for x, y in [(120, 20), (128, 30), (24, 40), (218, 120)]),
     bg=WATER)

# 3. 海豹館的圓柱水槽（海洋通道）
card('marineway', '手繪海豹館的圓柱水槽，海豹從中間往上游，小朋友在旁邊看',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SNOWBG}"/>'
     + f'<rect x="88" y="14" width="64" height="150" rx="6" fill="{WATER}"/>'
     + f'<ellipse cx="120" cy="16" rx="32" ry="7" fill="{SEA}"/>'
     + f'<path d="M98,30 L98,150" stroke="{WHITE}" stroke-width="3" opacity=".75"/>'
     + seal(120, 88, .95, -90)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="none" stroke="{WHITE}" stroke-width="1.3"/>' for x, y in [(138, 40), (134, 28), (108, 140)])
     + floor(160, '#e9dcc8')
     + person(52, 120, RED, 1.0, GOLD) + person(184, 122, GREEN, .95, PINK) + person(208, 132, GOLD, .75)
     + f'<path d="M60,116 l12,-10 M178,118 l-12,-10" stroke-width="1.6"/>'
     + flake(34, 36) + flake(206, 40, 4) + star(40, 76, 5))

# 4. 北極熊館的大泳池（跳水）
card('dive', '手繪北極熊從岩石上跳進大泳池，水花四濺',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SNOWBG}"/>'
     + f'<path d="M3,40 Q30,30 60,46 L82,92 L3,92 Z" fill="#d9dee6"/>'
     + f'<path d="M3,92 L237,92 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WATER}"/>'
     + f'<path d="M3,92 q20,-6 40,0 t40,0 t40,0 t40,0 t40,0 t34,0" fill="none" stroke="{WHITE}" stroke-width="2.4"/>'
     + bear(140, 60, .85)
     + f'<path d="M110,82 q-8,-16 2,-22 M170,82 q8,-16 -2,-22" fill="none" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},{y} q{dx},-12 {dx*2},-2" fill="none" stroke="{WHITE}" stroke-width="2.6"/>'
               for x, y, dx in [(100, 96, -6), (180, 96, 6), (90, 104, -8), (190, 104, 8)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{WHITE}" stroke-width="1.2"/>' for x, y in [(96, 76), (186, 74), (204, 86), (80, 86)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke="{WHITE}" stroke-width="1.4"/>' for x, y in [(60, 130), (70, 150), (196, 140)])
     + flake(30, 22, 4) + flake(214, 30) + sparkle(110, 24))

# 5. 北極熊館的「海豹之眼」膠囊
card('sealseye', '手繪從地面冒出來的透明膠囊，小朋友在裡面和北極熊對看',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SNOWBG}"/>'
     + floor(128, WHITE)
     + f'<path d="M150,132 a36,36 0 0,1 72,0 Z" fill="{SEA}" opacity=".9"/>'
     + f'<path d="M160,120 a26,26 0 0,1 18,-18" fill="none" stroke="{WHITE}" stroke-width="3" opacity=".9"/>'
     + person(186, 112, PINK, .95, RED)
     + bear(92, 82, .95)
     + f'<path d="M126,74 q14,-10 24,4" fill="none" stroke-width="1.6" stroke-dasharray="3 4"/>'
     + flake(30, 30) + flake(214, 28, 4) + star(150, 34, 5) + sparkle(40, 150))

# 6. 猛獸館：懸在半空的籠子，從正下方看雪豹
leo = ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="none" stroke="#7d8796" stroke-width="1.4"/>'
              for x, y in [(96, 64), (110, 58), (124, 64), (138, 58), (152, 64), (104, 72), (132, 72)])
card('snowleopard', '手繪趴在空中籠子上的雪豹，下面的人抬頭看',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SNOWBG}"/>'
     + f'<path d="M40,30 L40,88 M200,30 L200,88" stroke-width="3"/>'
     + f'<rect x="40" y="80" width="160" height="12" rx="3" fill="{GRAY}"/>'
     + ''.join(f'<path d="M{x},80 L{x},92" stroke-width="1.2"/>' for x in range(52, 200, 12))
     + f'<path d="M150,72 q40,-4 46,-24 q4,-10 -4,-10 q-2,14 -42,24 Z" fill="#eef0f2"/>'
     + f'<ellipse cx="122" cy="68" rx="40" ry="13" fill="#eef0f2"/>'
     + leo
     + f'<circle cx="80" cy="62" r="15" fill="#eef0f2"/>'
     + f'<path d="M68,54 l1,-9 l7,5 Z M92,54 l-1,-9 l-7,5 Z" fill="#eef0f2" stroke-width="1.8"/>'
     + face(80, 62, .75)
     + f'<path d="M77,64 l3,2 l3,-2 Z" fill="{PINK}" stroke-width="1"/>'
     + f'<path d="M66,66 l-9,-1 M66,68 l-9,2 M94,66 l9,-1 M94,68 l9,2" stroke-width="1"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="none" stroke="#7d8796" stroke-width="1.3"/>' for x, y in [(170, 66), (184, 56), (192, 44)])
     + f'<ellipse cx="72" cy="78" rx="8" ry="3.4" fill="#eef0f2" stroke-width="1.6"/><ellipse cx="94" cy="78" rx="7" ry="3.4" fill="#eef0f2" stroke-width="1.6"/>'
     + floor(150, '#e9dcc8')
     + person(90, 128, RED, .9, GOLD) + person(124, 132, SKY, .85, GREEN) + person(160, 128, GOLD, .9)
     + f'<path d="M90,118 l0,-10 M124,122 l0,-10 M160,118 l0,-10" stroke-width="1.4" stroke-dasharray="2 3"/>'
     + flake(22, 30, 4) + flake(220, 22, 4) + star(120, 22, 5))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('az-' + name, 120, 120, label, inner, bg='#fff3c4')


def nocircle(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RED}" stroke-width="4"/>'
            f'<path d="M{cx-r*.7:.1f},{cy-r*.7:.1f} L{cx+r*.7:.1f},{cy+r*.7:.1f}" stroke="{RED}" stroke-width="4"/>')


# 拍照：閃光燈先關
rem('r-flash', '手繪提醒：相機的閃光燈要關掉',
    f'<rect x="22" y="44" width="76" height="50" rx="8" fill="{GRAY}"/>'
    f'<rect x="40" y="36" width="24" height="10" rx="3" fill="{GRAY}"/>'
    f'<circle cx="60" cy="69" r="16" fill="{WHITE}"/><circle cx="60" cy="69" r="8" fill="{NAVY}"/>'
    f'<path d="M86,22 L78,36 L86,36 L80,48" fill="none" stroke="{GOLD}" stroke-width="3"/>'
    + nocircle(84, 34, 16))

# 雪橇、雪球夾不能帶進園
rem('r-sled', '手繪提醒：雪橇和雪球夾不能帶進動物園',
    f'<path d="M14,74 L74,74 Q86,74 86,62" fill="none" stroke="{RED}" stroke-width="3.4"/>'
    f'<rect x="18" y="58" width="54" height="10" rx="3" fill="{RED}"/>'
    f'<path d="M26,68 L26,74 M64,68 L64,74" stroke-width="2.4"/>'
    f'<path d="M78,92 L102,92 M78,92 L74,104 M102,92 L106,104" stroke-width="2.6"/>'
    f'<circle cx="74" cy="106" r="5" fill="{SKY}"/><circle cx="106" cy="106" r="5" fill="{SKY}"/>'
    + nocircle(60, 60, 50))

# 東門和くもざる・かぴばら館之間的免費小巴
rem('r-shuttle', '手繪提醒：園內的免費接駁小巴',
    f'<path d="M6,100 Q60,70 114,52" fill="none" stroke="#e9dcc8" stroke-width="10"/>'
    f'<g transform="rotate(-16 60 66)">'
    f'<rect x="28" y="46" width="64" height="34" rx="8" fill="{GREEN}"/>'
    f'<rect x="36" y="52" width="12" height="11" rx="2" fill="{SKY}" stroke-width="1.3"/>'
    f'<rect x="54" y="52" width="12" height="11" rx="2" fill="{SKY}" stroke-width="1.3"/>'
    f'<rect x="72" y="52" width="12" height="11" rx="2" fill="{SKY}" stroke-width="1.3"/>'
    f'<circle cx="42" cy="82" r="6" fill="{INK}"/><circle cx="80" cy="82" r="6" fill="{INK}"/>'
    f'</g>'
    + snow([(20, 26), (60, 18), (100, 28)], 2.6, '#cfe3f3'))

print(save(F, OUT), 'files')
