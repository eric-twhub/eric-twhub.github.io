# 雲台相機價差頁的插圖與提醒卡（2026-11-13）。
# 只畫一般的手持雲台相機、配件與充電線，不畫任何品牌的造型特徵、商標或字。
# 輸出 illust/sp/japan-camera-price/*.svg，說明文字在 illust/spots/japan-camera-price.json。
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


PFX = 'cam-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-camera-price')
# 商品只畫一般的手持雲台相機外型，不畫任何品牌的按鍵配置、商標或字。


def gimbal(x, y, s=1.0, col='#4a4f5c'):
    # 一般的手持雲台相機：(x,y) 是握把左上角
    p = lambda v: v * s
    return (f'<rect x="{x+p(9):.1f}" y="{y-p(10):.1f}" width="{p(6):.1f}" height="{p(12):.1f}" rx="{p(2):.1f}" fill="{GRAY}"/>'
            f'<rect x="{x+p(1):.1f}" y="{y-p(30):.1f}" width="{p(22):.1f}" height="{p(20):.1f}" rx="{p(6):.1f}" fill="{col}"/>'
            f'<circle cx="{x+p(12):.1f}" cy="{y-p(20):.1f}" r="{p(6):.1f}" fill="{SKY}"/>'
            f'<circle cx="{x+p(12):.1f}" cy="{y-p(20):.1f}" r="{p(2.4):.1f}" fill="{INK}" stroke="none"/>'
            f'<rect x="{x}" y="{y}" width="{p(24):.1f}" height="{p(72):.1f}" rx="{p(10):.1f}" fill="{col}"/>'
            f'<rect x="{x+p(4):.1f}" y="{y+p(8):.1f}" width="{p(16):.1f}" height="{p(20):.1f}" rx="{p(3):.1f}" fill="{WHITE}" stroke-width="1.6"/>'
            + face(x + p(12), y + p(17), .45 * s, False)
            + f'<circle cx="{x+p(12):.1f}" cy="{y+p(40):.1f}" r="{p(4):.1f}" fill="{RED}" stroke-width="1.4"/>')


def usbplug(x, y, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x-6}" y="{y}" width="12" height="18" rx="3" fill="{WHITE}"/>'
            f'<rect x="{x-3.5}" y="{y-6}" width="7" height="7" rx="1.5" fill="{GRAY}" stroke-width="1.4"/></g>')


# 1. 手持雲台相機
card('gimbal', '手繪一台手持雲台相機，小螢幕上有笑臉，旁邊是錄影的紅點',
     floor(152)
     + f'<ellipse cx="96" cy="150" rx="40" ry="6" fill="#e2d3bb" stroke="none"/>'
     + gimbal(84, 66, 1.05)
     + f'<path d="M136,48 q16,-6 30,0 M136,62 q22,-8 44,0" fill="none" stroke="{SKY}" stroke-width="3"/>'
     + f'<circle cx="182" cy="96" r="7" fill="{RED}"/>' + txt(204, 101, 'REC', 12, RED)
     + sparkle(40, 40) + star(46, 112, 7) + sparkle(190, 30) + star(214, 136, 6))

# 2. 單機與套裝
card('combo', '手繪打開的盒子裡有相機、小腳架、廣角鏡頭和傳輸線',
     floor(150)
     + f'<path d="M30,150 L30,84 L210,84 L210,150 Z" fill="{BROWN}"/>'
     + f'<path d="M30,84 L48,60 L192,60 L210,84 Z" fill="#d9a77a"/>'
     + f'<path d="M30,84 L14,102 M210,84 L226,102" stroke-width="2.4"/>'
     + gimbal(48, 92, .6)
     + f'<path d="M96,140 L104,112 L112,140 M104,112 L104,140" fill="none" stroke-width="2.6"/>'
     + f'<rect x="98" y="104" width="12" height="9" rx="2" fill="{INK}" stroke="none"/>'
     + f'<circle cx="136" cy="118" r="11" fill="{GRAY}"/><circle cx="136" cy="118" r="6" fill="{SKY}"/>'
     + f'<path d="M160,140 q0,-26 16,-26 q16,0 16,14 q0,10 -10,10" fill="none" stroke="{WHITE}" stroke-width="5"/>'
     + f'<path d="M160,140 q0,-26 16,-26 q16,0 16,14 q0,10 -10,10" fill="none" stroke-width="1.4"/>'
     + face(120, 74, .6)
     + sparkle(28, 30) + star(212, 30, 7) + sparkle(120, 26))

# 3. 第三方配件（同一個貨架，點數不一樣）
card('accessory', '手繪貨架上的濾鏡和外接鏡頭，旁邊一枚點數金幣',
     floor(150)
     + shelf(22, 100, 150, rows=1, gap=60)
     + f'<rect x="34" y="62" width="34" height="38" rx="4" fill="{WHITE}"/>'
     + f'<circle cx="51" cy="78" r="11" fill="{GRAY}"/><circle cx="51" cy="78" r="6" fill="#9fb6d6"/>'
     + f'<rect x="80" y="62" width="34" height="38" rx="4" fill="{WHITE}"/>'
     + f'<rect x="88" y="70" width="18" height="16" rx="4" fill="#4a4f5c"/><circle cx="97" cy="78" r="5" fill="{SKY}"/>'
     + f'<rect x="126" y="62" width="34" height="38" rx="4" fill="{WHITE}"/>'
     + f'<circle cx="143" cy="80" r="11" fill="none" stroke-width="3"/><circle cx="143" cy="80" r="7" fill="#c8dcef" stroke-width="1.2"/>'
     + f'<circle cx="198" cy="70" r="20" fill="{GOLD}"/><circle cx="198" cy="70" r="14" fill="none" stroke-width="1.6"/>'
     + txt(198, 76, 'P', 17, INK)
     + kid(198, 116, SKY, .9)
     + sparkle(30, 30) + sparkle(222, 36) + star(120, 30, 7))

# 4. USB 充電
card('usb', '手繪相機接著 USB 線，另一頭插在充電頭上',
     floor(150)
     + gimbal(46, 64, .95)
     + f'<path d="M58,134 Q60,150 100,146 Q150,140 170,120 Q180,110 176,96" fill="none" stroke-width="3"/>'
     + usbplug(176, 96, 0)
     + f'<rect x="160" y="54" width="36" height="38" rx="7" fill="{WHITE}"/>'
     + f'<rect x="172" y="88" width="12" height="4" fill="{GRAY}" stroke="none"/>'
     + f'<path d="M171,54 L171,42 M185,54 L185,42" stroke-width="3"/>'
     + face(178, 72, .7)
     + f'<path d="M210,96 l-6,12 l8,0 l-6,12" fill="none" stroke="{GOLD}" stroke-width="2.6"/>'
     + sparkle(120, 40) + star(36, 36, 7) + sparkle(214, 40))

# ---- 提醒卡小圖 ----
rem('r-online', '手繪提醒：網購畫面打叉，實體店打勾',
    f'<rect x="10" y="22" width="56" height="40" rx="4" fill="{WHITE}"/>'
    + f'<path d="M6,66 L70,66" stroke-width="3"/>'
    + f'<path d="M22,34 L28,34 L33,48 L52,48 L56,38 L30,38" fill="none" stroke-width="2"/>'
    + f'<circle cx="35" cy="53" r="2" fill="{INK}" stroke="none"/><circle cx="50" cy="53" r="2" fill="{INK}" stroke="none"/>'
    + f'<circle cx="62" cy="22" r="10" fill="{WHITE}"/><path d="M57,17 L67,27 M67,17 L57,27" stroke="{RED}" stroke-width="3"/>'
    + f'<rect x="64" y="72" width="44" height="34" fill="{PINK}"/>'
    + awning(60, 66, 52, RED, WHITE, 4, 9)
    + f'<rect x="80" y="86" width="12" height="20" rx="2" fill="{BROWN}" stroke-width="1.4"/>'
    + f'<circle cx="104" cy="66" r="10" fill="{WHITE}"/><path d="M99,66 l4,4 l7,-8" stroke="{GREEN}" stroke-width="3" fill="none"/>')

rem('r-ship', '手繪提醒：紙箱坐飛機寄來，旁邊一張報關單',
    f'<rect x="14" y="56" width="50" height="42" rx="3" fill="{BROWN}"/>'
    + f'<path d="M14,70 L64,70 M39,56 L39,70" stroke-width="1.8"/>'
    + face(39, 84, .7)
    + f'<path d="M30,30 L74,26 Q82,26 76,32 L34,38 Z" fill="{WHITE}"/>'
    + f'<path d="M50,30 L44,44 L50,44 L60,30 Z" fill="{SKY}" stroke-width="1.4"/>'
    + f'<path d="M18,40 q6,-4 10,-6" fill="none" stroke-width="1.6" stroke-dasharray="3 3"/>'
    + f'<rect x="74" y="50" width="34" height="48" rx="3" fill="{WHITE}"/>'
    + ''.join(f'<path d="M80,{60+8*i} L102,{60+8*i}" stroke-width="1.6"/>' for i in range(4))
    + f'<circle cx="98" cy="90" r="8" fill="none" stroke="{RED}" stroke-width="2.4"/>')

print(save(F, OUT), 'files')
