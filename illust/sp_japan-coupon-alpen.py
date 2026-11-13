# Alpen 頁的「店裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考 TAXFREESHOPS.JP 上 Alpen 旅客券的店型與照片（只看有什麼），畫成可愛版，不畫店家招牌與商標。
# 輸出 illust/sp/japan-coupon-alpen/*.svg，說明文字在 illust/spots/japan-coupon-alpen.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

W, H = 240, 180
F = {}
SKIN = '#f9d9c0'
LILAC = '#c9b3e6'
MINT = '#bfe6d0'
PEACH = '#f9c9a4'
LEMON = '#fbe39a'
FLOOR = '#efe2cc'


def card(name, label, inner, bg=CREAM):
    F[name] = svg(PFX + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg(PFX + name, 120, 120, label, inner, bg='#fff3c4')


def floor(y=148, col=FLOOR):
    # 卡片下緣的地板，底部跟著外框的圓角
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def txt(x, y, s, size=12, col=INK, bold=True):
    fw = ' font-weight="bold"' if bold else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}" stroke="none" '
            f'font-family="sans-serif"{fw}>{s}</text>')


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    # 背影的小人
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{hair}"/>')


def kid(x, y, col=RED, s=1.0, hair=DBROWN):
    # 正面的小人（有臉）
    return (f'<path d="M{x-8*s},{y+24*s} q0,{-15*s} {8*s},{-15*s} q{8*s},0 {8*s},{15*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7.5*s}" fill="{SKIN}"/>'
            f'<path d="M{x-7.5*s},{y-1*s} q0,{-8.5*s} {7.5*s},{-8.5*s} q{7.5*s},0 {7.5*s},{8.5*s} q{-4*s},{-4*s} {-7.5*s},{-3*s} q{-4*s},{-1*s} {-7.5*s},{3*s} Z" fill="{hair}" stroke-width="1.4"/>'
            + face(x, y + 1.5 * s, .5 * s))


def bag(x, y, w=26, h=30, col=PINK, s=1.0):
    # 購物袋：(x,y) 是袋子左上角
    w, h = w * s, h * s
    return (f'<path d="M{x+w*.28:.1f},{y} q0,{-12*s:.1f} {w*.22:.1f},{-12*s:.1f} q{w*.22:.1f},0 {w*.22:.1f},{12*s:.1f}" fill="none" stroke-width="2"/>'
            f'<path d="M{x},{y} L{x+w},{y} L{x+w-2*s:.1f},{y+h} L{x+2*s:.1f},{y+h} Z" fill="{col}"/>')


def gift(x, y, w=30, h=24, col=PINK, rib=RED):
    # 禮物盒：(x,y) 是盒身左上角
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
            f'<rect x="{x-3}" y="{y-7}" width="{w+6}" height="9" rx="3" fill="{col}"/>'
            f'<rect x="{x+w/2-3:.1f}" y="{y-7}" width="6" height="{h+7}" fill="{rib}" stroke-width="1.4"/>'
            f'<path d="M{x+w/2:.1f},{y-7} q-12,-12 -12,-2 q0,6 12,2 q12,4 12,-2 q0,-10 -12,2 Z" fill="{rib}" stroke-width="1.6"/>')


def receipt(x, y, w=34, h=48):
    zig = ''.join(f' l{-w/8:.2f},4 l{-w/8:.2f},-4' for _ in range(4))
    lines = ''.join(f'<path d="M{x+6},{y+10+8*i} L{x+w-6-(8 if i % 2 else 0)},{y+10+8*i}" stroke-width="1.6"/>'
                    for i in range(int((h - 12) / 8)))
    return f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h}{zig} Z" fill="{WHITE}"/>' + lines


def passport(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{26*s}" height="{36*s}" rx="{3*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+13*s}" cy="{y+15*s}" r="{6*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+7*s},{y+28*s} L{x+19*s},{y+28*s}" stroke="{GOLD}" stroke-width="1.6"/>')


def suitcase(x, y, w=44, h=56, col=SKY):
    return (f'<path d="M{x+w*.32:.1f},{y} L{x+w*.32:.1f},{y-10} L{x+w*.68:.1f},{y-10} L{x+w*.68:.1f},{y}" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{col}"/>'
            f'<path d="M{x+w*.3:.1f},{y+4} L{x+w*.3:.1f},{y+h-4} M{x+w*.7:.1f},{y+4} L{x+w*.7:.1f},{y+h-4}" stroke-width="1.6"/>'
            f'<circle cx="{x+8}" cy="{y+h+4}" r="3.5" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+w-8}" cy="{y+h+4}" r="3.5" fill="{INK}" stroke="none"/>')


def kiosk(x, y, ok=True):
    # 機場的免稅手續機台：螢幕亮綠燈（或紅燈）
    return (f'<rect x="{x}" y="{y}" width="40" height="70" rx="6" fill="{GRAY}"/>'
            f'<rect x="{x+6}" y="{y+8}" width="28" height="22" rx="3" fill="{WHITE}"/>'
            f'<circle cx="{x+20}" cy="{y+19}" r="7" fill="{GREEN if ok else RED}" stroke-width="1.6"/>'
            f'<rect x="{x+8}" y="{y+38}" width="24" height="5" rx="2" fill="{INK}" stroke="none"/>'
            f'<rect x="{x+4}" y="{y+70}" width="32" height="6" rx="2" fill="{DBROWN}"/>')


def awning(x, y, w, c1=RED, c2=WHITE, n=6, h=14):
    sw = w / n
    t = ''
    for i in range(n):
        c = c1 if i % 2 == 0 else c2
        t += (f'<path d="M{x+i*sw:.1f},{y} L{x+(i+1)*sw:.1f},{y} L{x+(i+1)*sw:.1f},{y+h} '
              f'Q{x+(i+.5)*sw:.1f},{y+h+9} {x+i*sw:.1f},{y+h} Z" fill="{c}" stroke-width="1.8"/>')
    return t


def bear(x, y, col=BROWN, s=1.0, muz='#f3dcc0'):
    # 一般的絨毛熊（不是任何角色）
    return (f'<ellipse cx="{x}" cy="{y+21*s:.1f}" rx="{13*s:.1f}" ry="{12*s:.1f}" fill="{col}"/>'
            f'<circle cx="{x-11*s:.1f}" cy="{y-10*s:.1f}" r="{5.5*s:.1f}" fill="{col}"/>'
            f'<circle cx="{x+11*s:.1f}" cy="{y-10*s:.1f}" r="{5.5*s:.1f}" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{14*s:.1f}" fill="{col}"/>'
            f'<ellipse cx="{x}" cy="{y+5*s:.1f}" rx="{6.5*s:.1f}" ry="{5*s:.1f}" fill="{muz}" stroke-width="1.4"/>'
            + face(x, y + 1 * s, .62 * s, blush=True))


def bunny(x, y, col=PEACH, s=1.0):
    # 一般的兔子娃娃（不是任何角色）
    return (f'<ellipse cx="{x}" cy="{y+20*s:.1f}" rx="{12*s:.1f}" ry="{11*s:.1f}" fill="{col}"/>'
            f'<ellipse cx="{x-6*s:.1f}" cy="{y-18*s:.1f}" rx="{4.5*s:.1f}" ry="{12*s:.1f}" fill="{col}"/>'
            f'<ellipse cx="{x+6*s:.1f}" cy="{y-18*s:.1f}" rx="{4.5*s:.1f}" ry="{12*s:.1f}" fill="{col}"/>'
            f'<ellipse cx="{x-6*s:.1f}" cy="{y-17*s:.1f}" rx="{2*s:.1f}" ry="{8*s:.1f}" fill="{PINK}" stroke="none"/>'
            f'<ellipse cx="{x+6*s:.1f}" cy="{y-17*s:.1f}" rx="{2*s:.1f}" ry="{8*s:.1f}" fill="{PINK}" stroke="none"/>'
            f'<circle cx="{x}" cy="{y}" r="{12.5*s:.1f}" fill="{col}"/>'
            + face(x, y + 1 * s, .58 * s))


def shelf(x, y, w, rows=2, gap=40, col=BROWN):
    # 木頭層架：(x,y) 是最上層板子的位置
    t = f'<rect x="{x}" y="{y-gap+6}" width="6" height="{gap*rows}" fill="{DBROWN}"/>' \
        f'<rect x="{x+w-6}" y="{y-gap+6}" width="6" height="{gap*rows}" fill="{DBROWN}"/>'
    for r in range(rows):
        t += f'<rect x="{x-2}" y="{y+r*gap}" width="{w+4}" height="6" rx="2" fill="{col}"/>'
    return t


PFX = 'alp-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-alpen')
SNOW = '#eaf4fb'


def ball(x, y, r=12):
    # 一般的足球（黑白塊）
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}"/>'
            f'<polygon points="{x},{y-r*.45:.1f} {x+r*.43:.1f},{y-r*.14:.1f} {x+r*.27:.1f},{y+r*.36:.1f} '
            f'{x-r*.27:.1f},{y+r*.36:.1f} {x-r*.43:.1f},{y-r*.14:.1f}" fill="{INK}" stroke="none"/>')


def racket(x, y, col=RED, rot=-20):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-3}" y="{y+16}" width="6" height="26" rx="3" fill="{DBROWN}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="13" ry="17" fill="{WHITE}" stroke="{col}" stroke-width="3.4"/>'
            + ''.join(f'<path d="M{x-12},{y-12+6*i} L{x+12},{y-12+6*i}" stroke-width=".8" opacity=".5"/>' for i in range(5))
            + '</g>')


# 1. 大型運動用品店
card('front', '手繪大型運動用品店的門口，櫥窗有足球、球拍和球鞋',
     floor(150)
     + f'<rect x="16" y="46" width="208" height="104" fill="#e3effa"/>'
     + f'<rect x="56" y="18" width="128" height="22" rx="6" fill="{WHITE}"/>'
     + ball(120, 29, 8)
     + awning(12, 44, 216, '#4f8fd6', WHITE, 9)
     + f'<rect x="26" y="72" width="128" height="70" rx="4" fill="{WHITE}"/>'
     + f'<path d="M30,132 L150,132" stroke-width="2"/>'
     + ball(52, 119, 13) + racket(92, 98, RED, -16)
     + f'<path d="M116,132 L116,118 Q116,112 122,112 L130,112 L134,108 L138,114 Q146,120 150,124 L150,132 Z" fill="{GOLD}"/>'
     + face(52, 118, .5, False)
     + f'<rect x="166" y="72" width="46" height="78" rx="3" fill="{GRAY}"/>'
     + f'<path d="M189,72 L189,150" stroke-width="1.8"/>'
     + sparkle(28, 26) + star(206, 22, 7))

# 2. 冬天的雪具
card('snow', '手繪雪板、雙板和護目鏡，旁邊飄著雪',
     floor(150, '#f3f7fb')
     + f'<g transform="rotate(-8 70 90)"><rect x="54" y="26" width="30" height="120" rx="15" fill="{RED}"/>'
     + f'<rect x="58" y="62" width="22" height="10" rx="3" fill="{INK}" stroke="none"/>'
     + f'<rect x="58" y="100" width="22" height="10" rx="3" fill="{INK}" stroke="none"/>' + face(69, 84, .7) + '</g>'
     + f'<rect x="104" y="30" width="11" height="118" rx="5" fill="{SKY}"/>'
     + f'<rect x="120" y="30" width="11" height="118" rx="5" fill="{SKY}"/>'
     + f'<path d="M104,36 q5,-12 11,0 M120,36 q5,-12 11,0" fill="{SKY}"/>'
     + f'<path d="M150,96 q-2,-14 14,-14 L198,82 q16,0 14,14 q0,12 -14,12 q-6,0 -10,-6 q-4,-4 -9,0 q-4,6 -10,6 q-14,0 -15,-12 Z" fill="{GOLD}"/>'
     + f'<path d="M158,92 q0,-6 8,-6 L176,86 M188,86 L198,86" stroke="{WHITE}" stroke-width="2.4"/>'
     + f'<path d="M150,94 L144,96 M212,94 L218,96" stroke-width="2.4"/>'
     + snow([(30, 40), (200, 36), (170, 54), (222, 120), (36, 120), (150, 30), (90, 22)], 3, WHITE)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="none" stroke-width="1.2"/>' for x, y in [(30, 40), (200, 36), (222, 120)]),
     bg=SNOW)

# 3. 高爾夫球具
card('golf', '手繪高爾夫球袋和球桿，草地上有一顆球',
     f'<path d="M3,128 Q80,118 160,126 T237,122 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{GREEN}"/>'
     + f'<path d="M84,44 L76,22 M98,42 L98,18 M112,44 L122,24" stroke-width="3"/>'
     + f'<path d="M70,22 L82,20 L80,26 Z M92,14 L104,14 L104,20 L92,20 Z M118,20 L130,22 L126,28 Z" fill="{GRAY}"/>'
     + f'<rect x="70" y="40" width="58" height="104" rx="14" fill="{NAVY}"/>'
     + f'<rect x="70" y="60" width="58" height="12" fill="{RED}"/>'
     + f'<rect x="80" y="86" width="38" height="34" rx="8" fill="#4b5a8f"/>'
     + face(99, 102, .7)
     + f'<path d="M172,138 L172,126" stroke-width="2.4"/><circle cx="172" cy="120" r="7" fill="{WHITE}"/>'
     + ''.join(f'<circle cx="{170+dx}" cy="{118+dy}" r=".9" fill="{INK}" stroke="none"/>' for dx, dy in [(-2, 0), (2, -2), (3, 2), (-1, 3)])
     + f'<path d="M198,138 L198,84" stroke-width="2.4"/><path d="M198,84 L218,92 L198,100 Z" fill="{RED}"/>'
     + sparkle(36, 40) + star(160, 40, 7) + sparkle(210, 46))

# 4. 店裡搭好的帳篷
card('camp', '手繪店裡搭好展示的帳篷和營燈',
     floor(146)
     + f'<path d="M40,140 L100,52 L160,140 Z" fill="{PEACH}"/>'
     + f'<path d="M100,52 L132,140 L68,140 Z" fill="#f2a46b"/>'
     + f'<path d="M100,100 L100,140" stroke-width="2"/>'
     + f'<path d="M100,52 L100,40" stroke-width="2.4"/><path d="M100,40 L114,45 L100,50 Z" fill="{GREEN}"/>'
     + face(84, 118, .7)
     + f'<path d="M30,140 L40,140 M160,140 L172,140" stroke-width="2.4"/>'
     + f'<rect x="184" y="108" width="24" height="32" rx="5" fill="{GOLD}"/>'
     + f'<path d="M188,108 q8,-12 16,0" fill="none" stroke-width="2"/>'
     + f'<circle cx="196" cy="124" r="7" fill="{LEMON}" stroke-width="1.4"/>'
     + ''.join(f'<path d="M{196+14*dx},{124+14*dy} L{196+20*dx},{124+20*dy}" stroke="{GOLD}" stroke-width="2"/>' for dx, dy in [(1.2, 0), (.85, -.85), (0, -1.2)])
     + sparkle(36, 34) + star(200, 34, 7) + sparkle(150, 26))

# ---- 提醒卡小圖 ----
rem('r-list', '手繪提醒：一張店舖名單，有的打勾有的打叉',
    f'<rect x="24" y="14" width="64" height="88" rx="4" fill="{WHITE}"/>'
    + ''.join(f'<path d="M44,{32+16*i} L80,{32+16*i}" stroke-width="2"/>' for i in range(4))
    + ''.join((f'<path d="M30,{30+16*i} l4,4 l6,-8" stroke="{GREEN}" stroke-width="2.6" fill="none"/>' if i != 2 else
               f'<path d="M31,{26+16*i} l8,8 M39,{26+16*i} l-8,8" stroke="{RED}" stroke-width="2.6"/>') for i in range(4))
    + f'<circle cx="92" cy="92" r="16" fill="{SKY}"/><circle cx="92" cy="92" r="9" fill="{WHITE}"/>'
    + f'<path d="M100,100 L110,110" stroke-width="4"/>')

rem('r-combo', '手繪提醒：折價券和打折標籤中間一個叉',
    f'<g transform="rotate(-10 34 52)"><rect x="12" y="34" width="46" height="34" rx="4" fill="{GOLD}"/>'
    + f'<circle cx="20" cy="51" r="3" fill="#fff3c4"/><path d="M28,44 L50,44 M28,52 L50,52 M28,60 L44,60" stroke-width="1.8"/></g>'
    + f'<g transform="rotate(10 86 76)"><path d="M66,62 L96,62 L108,76 L96,90 L66,90 Z" fill="{RED}"/>'
    + f'<circle cx="96" cy="76" r="3" fill="#fff3c4"/>' + txt(80, 81, '%', 14, WHITE) + '</g>'
    + f'<circle cx="60" cy="98" r="11" fill="{WHITE}"/><path d="M54,92 L66,104 M66,92 L54,104" stroke="{RED}" stroke-width="3"/>')

rem('r-board', '手繪提醒：抱著雪板先到機台刷護照',
    f'<g transform="rotate(-14 34 62)"><rect x="24" y="12" width="20" height="96" rx="10" fill="{RED}"/>'
    + f'<rect x="27" y="40" width="14" height="7" rx="2" fill="{INK}" stroke="none"/><rect x="27" y="72" width="14" height="7" rx="2" fill="{INK}" stroke="none"/></g>'
    + kiosk(66, 22)
    + f'<path d="M48,60 L60,60 M54,54 L60,60 L54,66" stroke="{RED}" stroke-width="3" fill="none"/>')

print(save(F, OUT), 'files')
