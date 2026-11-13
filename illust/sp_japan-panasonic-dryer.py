# 日本買 Panasonic 吹風機頁的插圖與提醒卡（2026-11-13）。
# 只畫一般的吹風機、紙盒、規格標籤與插座外型，不畫任何品牌的造型特徵、商標或字。
# 輸出 illust/sp/japan-panasonic-dryer/*.svg，說明文字在 illust/spots/japan-panasonic-dryer.json。
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


PFX = 'pn-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-panasonic-dryer')
# 只畫一般的吹風機、紙盒、規格標籤與插座外型，不畫任何品牌的造型特徵、商標或字。


def dryer(x, y, col=PINK, s=1.0, rot=0, cord=True):
    # 一般的吹風機（筒身朝右），(x,y) 是筒身後端中心
    p = lambda v: v * s
    t = (f'<g transform="rotate({rot} {x} {y})">'
         + (f'<path d="M{x+p(24):.1f},{y+p(52):.1f} q{p(4):.1f},{p(16):.1f} {p(-12):.1f},{p(20):.1f} q{p(-14):.1f},{p(4):.1f} {p(-22):.1f},{p(-6):.1f}" fill="none" stroke-width="2"/>' if cord else '')
         + f'<g transform="rotate(-10 {x+p(24):.1f} {y+p(10):.1f})"><rect x="{x+p(15):.1f}" y="{y+p(6):.1f}" width="{p(18):.1f}" height="{p(48):.1f}" rx="{p(8):.1f}" fill="{col}"/>'
         f'<rect x="{x+p(20):.1f}" y="{y+p(18):.1f}" width="{p(8):.1f}" height="{p(12):.1f}" rx="{p(3):.1f}" fill="{WHITE}" stroke-width="1.4"/></g>'
         f'<path d="M{x+p(52):.1f},{y-p(11):.1f} L{x+p(68):.1f},{y-p(8):.1f} L{x+p(68):.1f},{y+p(8):.1f} L{x+p(52):.1f},{y+p(11):.1f} Z" fill="{GRAY}"/>'
         f'<rect x="{x}" y="{y-p(16):.1f}" width="{p(56):.1f}" height="{p(32):.1f}" rx="{p(16):.1f}" fill="{col}"/>'
         f'<ellipse cx="{x+p(5):.1f}" cy="{y}" rx="{p(5):.1f}" ry="{p(13):.1f}" fill="{WHITE}" stroke-width="1.6"/>'
         + face(x + p(32), y - p(1), .65 * s)
         + '</g>')
    return t


def outlet(x, y, s=1.0, col=WHITE):
    # 日本與台灣常見的兩孔扁腳插座（一般外型）
    p = lambda v: v * s
    return (f'<rect x="{x}" y="{y}" width="{p(40):.1f}" height="{p(52):.1f}" rx="{p(8):.1f}" fill="{col}"/>'
            f'<rect x="{x+p(12):.1f}" y="{y+p(16):.1f}" width="{p(4):.1f}" height="{p(12):.1f}" rx="1" fill="{INK}" stroke="none"/>'
            f'<rect x="{x+p(24):.1f}" y="{y+p(16):.1f}" width="{p(4):.1f}" height="{p(12):.1f}" rx="1" fill="{INK}" stroke="none"/>'
            f'<path d="M{x+p(14):.1f},{y+p(38):.1f} q{p(6):.1f},{p(5):.1f} {p(12):.1f},0" fill="none" stroke-width="1.8"/>')


def bigbox(x, y, w, h, col=BROWN):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
            f'<path d="M{x},{y+12} L{x+w},{y+12} M{x+w/2:.1f},{y} L{x+w/2:.1f},{y+12}" stroke-width="1.8"/>'
            f'<rect x="{x+w/2-10:.1f}" y="{y}" width="20" height="12" fill="#e9c79a" stroke-width="1.4"/>')


def dbox(x, y, col, label, lab_col):
    # 吹風機的盒子，側面貼著規格標籤
    return (f'<rect x="{x}" y="{y}" width="72" height="92" rx="4" fill="{col}"/>'
            f'<path d="M{x},{y+10} L{x+72},{y+10}" stroke-width="1.6"/>'
            + dryer(x + 10, y + 34, WHITE, .62, 0, False)
            + f'<rect x="{x+8}" y="{y+70}" width="56" height="16" rx="3" fill="{WHITE}" stroke-width="1.6"/>'
            + txt(x + 36, y + 82, label, 11, lab_col))


# 1. 高階機種：一樣的型號兩地都有
card('dryer', '手繪一支吹風機吹出帶著小水滴的風',
     floor(150)
     + dryer(36, 70, '#b9a4d6', 1.15)
     + ''.join(f'<path d="M{120},{60+10*i} q12,-4 24,0" fill="none" stroke="{SKY}" stroke-width="2.6"/>' for i in range(3))
     + ''.join(f'<path d="M{x},{y} q-4,6 0,8 q4,-2 0,-8 Z" fill="#9fd3ef" stroke-width="1.2"/>' for x, y in [(160, 54), (176, 66), (166, 80), (186, 50), (192, 78), (204, 62)])
     + sparkle(30, 30) + star(120, 26, 7) + sparkle(214, 128))

# 2. 盒子長得像，規格標籤不一樣
card('label', '手繪兩個一樣的吹風機盒子，標籤一個寫 AC100V、一個寫 110V',
     floor(150)
     + dbox(34, 46, PEACH, 'AC100V', NAVY) + dbox(134, 46, PEACH, '110V', RED)
     + txt(70, 36, '日本版', 13) + txt(170, 36, '台灣版', 13)
     + f'<circle cx="120" cy="92" r="12" fill="{WHITE}"/>' + txt(120, 98, '≠', 18, RED)
     + sparkle(20, 120) + sparkle(222, 120))

# 3. 要單獨插一個 15A 以上的插座
card('outlet', '手繪牆上插座只插著一支吹風機，旁邊標著 15A',
     floor(150)
     + outlet(56, 50, 1.2)
     + f'<rect x="64" y="64" width="32" height="26" rx="5" fill="{GRAY}"/>'
     + f'<path d="M80,90 Q82,128 120,128 Q160,128 168,112" fill="none" stroke-width="2.4"/>'
     + dryer(150, 72, PINK, .78, 0, False)
     + f'<rect x="40" y="118" width="40" height="22" rx="11" fill="{GOLD}"/>' + txt(60, 134, '15A', 13)
     + f'<path d="M200,40 l-6,12 l8,0 l-6,12" fill="none" stroke="{GOLD}" stroke-width="2.6"/>'
     + sparkle(34, 30) + star(214, 136, 6))

# 4. 旗艦機不給點數，入門機反而有
card('points', '手繪兩支吹風機，大支的旁邊點數金幣打叉，小支的旁邊有點數金幣',
     floor(150)
     + dryer(22, 70, '#b9a4d6', .95)
     + f'<circle cx="62" cy="34" r="15" fill="{GOLD}"/>' + txt(62, 40, 'P', 15)
     + f'<path d="M50,22 L74,46 M74,22 L50,46" stroke="{RED}" stroke-width="3"/>'
     + dryer(148, 88, MINT, .7)
     + f'<circle cx="176" cy="44" r="15" fill="{GOLD}"/>' + txt(176, 50, 'P', 15)
     + sparkle(118, 30) + sparkle(222, 74) + star(120, 130, 6))

# ---- 提醒卡小圖 ----
rem('r-gift', '手繪提醒：一張收據對應三個盒子，少了一個',
    receipt(10, 14, 36, 60)
    + f'<rect x="56" y="58" width="22" height="28" rx="3" fill="{PEACH}"/><rect x="84" y="58" width="22" height="28" rx="3" fill="{PEACH}"/>'
    + f'<rect x="70" y="92" width="22" height="20" rx="3" fill="none" stroke-dasharray="4 3" stroke-width="1.8"/>'
    + f'<path d="M76,96 L86,106 M86,96 L76,106" stroke="{RED}" stroke-width="2.6"/>')

rem('r-checkin', '手繪提醒：先到機台刷護照，再把行李箱拿去託運',
    kiosk(10, 18)
    + f'<circle cx="18" cy="12" r="8" fill="{WHITE}"/>' + txt(18, 16, '1', 11)
    + f'<path d="M56,58 L70,58 M64,52 L70,58 L64,64" stroke="{RED}" stroke-width="3" fill="none"/>'
    + suitcase(74, 50, 38, 46, MINT)
    + f'<circle cx="62" cy="90" r="8" fill="{WHITE}"/>' + txt(62, 94, '2', 11))

print(save(F, OUT), 'files')
