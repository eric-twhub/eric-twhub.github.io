# 日本買 Dyson 頁的插圖與提醒卡（2026-11-13）。
# 只畫一般的吹風機、直髮器、無線吸塵器、空氣清淨機與插座外型，不畫任何品牌的造型特徵、商標或字。
# 輸出 illust/sp/japan-dyson-price/*.svg，說明文字在 illust/spots/japan-dyson-price.json。
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


PFX = 'dy-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-dyson-price')
# 只畫一般的吹風機、直髮器、無線吸塵器與空氣清淨機外型，不畫任何品牌的造型特徵（環形吹風機、氣旋筒等）、商標或字。


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


def straightener(x, y, col=LILAC):
    return (f'<g transform="rotate(-24 {x} {y})">'
            f'<rect x="{x}" y="{y}" width="12" height="74" rx="6" fill="{col}"/>'
            f'<rect x="{x+15}" y="{y+4}" width="12" height="70" rx="6" fill="{col}"/>'
            f'<rect x="{x+2}" y="{y+42}" width="8" height="28" rx="3" fill="{GRAY}" stroke-width="1.4"/>'
            f'<rect x="{x+17}" y="{y+46}" width="8" height="26" rx="3" fill="{GRAY}" stroke-width="1.4"/>'
            f'<path d="M{x+6},{y} q8,-10 15,4" fill="none" stroke-width="2.4"/></g>')


def stickvac(x, y, col=GOLD):
    # 一般的無線直立吸塵器：(x,y) 是吸頭底部左端
    return (f'<path d="M{x+26},{y-14} L{x+52},{y-102}" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M{x+26},{y-14} L{x+52},{y-102}" stroke="{GRAY}" stroke-width="5"/>'
            f'<rect x="{x}" y="{y-16}" width="54" height="16" rx="7" fill="{col}"/>'
            f'<path d="M{x+4},{y} L{x+50},{y}" stroke="{DBROWN}" stroke-width="3"/>'
            f'<g transform="rotate(16 {x+56} {y-118})">'
            f'<path d="M{x+60},{y-138} q16,0 16,14 q0,12 -10,14" fill="none" stroke-width="5"/>'
            f'<rect x="{x+44}" y="{y-138}" width="24" height="40" rx="8" fill="{col}"/>'
            f'<rect x="{x+48}" y="{y-112}" width="16" height="10" rx="3" fill="{WHITE}" stroke-width="1.4"/></g>'
            + face(x + 27, y - 8, .55))


def purifier(x, y, col=WHITE, h=100):
    # 一般的直立式空氣清淨機：(x,y) 是左上角
    return (f'<rect x="{x}" y="{y}" width="48" height="{h}" rx="12" fill="{col}"/>'
            f'<rect x="{x+6}" y="{y+8}" width="36" height="8" rx="4" fill="{GRAY}" stroke-width="1.4"/>'
            + ''.join(f'<path d="M{x+10},{y+30+7*i} L{x+38},{y+30+7*i}" stroke-width="1.4"/>' for i in range(int((h-44)/7)))
            + f'<circle cx="{x+24}" cy="{y+12}" r="2" fill="{GREEN}" stroke="none"/>')


# 1. 頭髮護理
card('hair', '手繪一支吹風機和一支直髮夾，旁邊飄著風',
     floor(150)
     + dryer(34, 66, PINK, 1.15)
     + ''.join(f'<path d="M{118},{56+10*i} q12,-4 24,0" fill="none" stroke="{SKY}" stroke-width="2.6"/>' for i in range(3))
     + straightener(166, 52, LILAC)
     + sparkle(30, 30) + star(118, 26, 7) + sparkle(214, 136))

# 2. 無線吸塵器
card('vacuum', '手繪無線直立吸塵器，插座上插著充電器',
     floor(146)
     + stickvac(52, 146, GOLD)
     + outlet(170, 60, .9)
     + f'<rect x="174" y="88" width="28" height="24" rx="5" fill="{GRAY}"/>'
     + f'<path d="M188,112 Q190,140 150,140 Q130,140 126,128" fill="none" stroke-width="2"/>'
     + sparkle(36, 40) + star(140, 30, 7) + sparkle(214, 36)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{GRAY}" stroke="none"/>' for x, y in [(30, 138), (40, 141), (122, 140)]))

# 3. 空氣清淨機
card('purifier', '手繪直立式空氣清淨機，吹出乾淨的風',
     floor(150)
     + purifier(70, 40, WHITE, 108)
     + face(94, 132, .8)
     + ''.join(f'<path d="M{128},{60+16*i} q14,-8 28,0 q10,6 20,0" fill="none" stroke="{SKY}" stroke-width="2.6"/>' for i in range(3))
     + f'<path d="M188,110 q10,-14 22,-10 q-2,14 -22,10 Z" fill="{GREEN}"/><path d="M188,110 L204,102" stroke-width="1.2"/>'
     + f'<path d="M30,128 q6,-18 20,-14 q-2,16 -20,14 Z" fill="{GREEN}"/>'
     + sparkle(36, 40) + star(200, 34, 7) + sparkle(154, 136))

# 4. 電壓不一樣
card('volt', '手繪兩個插座，左邊標日本 100V、右邊標台灣 110V',
     floor(150)
     + outlet(40, 56, 1.3, WHITE) + outlet(148, 56, 1.3, WHITE)
     + txt(66, 48, '日本', 15) + txt(174, 48, '台灣', 15)
     + f'<rect x="38" y="132" width="56" height="22" rx="11" fill="{SKY}"/>' + txt(66, 148, '100V', 14)
     + f'<rect x="146" y="132" width="56" height="22" rx="11" fill="{PEACH}"/>' + txt(174, 148, '110V', 14)
     + f'<path d="M110,94 L130,94 M110,104 L130,104 M126,86 L114,112" stroke="{RED}" stroke-width="2.6"/>'
     + sparkle(22, 30) + star(120, 30, 7) + sparkle(220, 30))

# ---- 提醒卡小圖 ----
rem('r-checkin', '手繪提醒：抱著大紙箱先到機台刷護照，再去託運',
    bigbox(8, 40, 46, 56)
    + face(31, 76, .7)
    + f'<path d="M58,66 L68,66 M63,61 L68,66 L63,71" stroke="{RED}" stroke-width="3" fill="none"/>'
    + kiosk(72, 22))

rem('r-ship', '手繪提醒：紙箱要自己寄出國，被打了一個叉',
    bigbox(16, 44, 54, 50)
    + face(43, 78, .7)
    + f'<path d="M76,30 L108,26 Q114,26 110,31 L80,36 Z" fill="{WHITE}"/>'
    + f'<path d="M92,30 L88,40 L93,40 L100,30 Z" fill="{SKY}" stroke-width="1.4"/>'
    + f'<circle cx="92" cy="80" r="14" fill="{WHITE}"/><path d="M85,73 L99,87 M99,73 L85,87" stroke="{RED}" stroke-width="3.2"/>')

print(save(F, OUT), 'files')
