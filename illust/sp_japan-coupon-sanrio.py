# 三麗鷗頁的「店裡有什麼」插圖與提醒卡（2026-11-13）。
# 依官網店舖公告（sanrio.co.jp/storeslist/）列的商品類型畫成一般禮品店的可愛版。
# 角色店：不畫任何角色、角色剪影或角色招牌元素（包括頭上的蝴蝶結），只畫一般絨毛熊、文具與禮物盒。
# 輸出 illust/sp/japan-coupon-sanrio/*.svg，說明文字在 illust/spots/japan-coupon-sanrio.json。
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


PFX = 'snr-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-sanrio')
# 角色店：不畫任何角色、角色剪影或角色招牌元素（包括頭上的蝴蝶結），只畫一般的禮品店、絨毛熊、文具與禮物盒。
TEAL = '#7cc7c0'


def heart(x, y, r=8, col=PINK):
    return (f'<path d="M{x},{y+r*.9:.1f} C{x-r*1.6:.1f},{y-r*.2:.1f} {x-r*.8:.1f},{y-r*1.3:.1f} {x},{y-r*.45:.1f} '
            f'C{x+r*.8:.1f},{y-r*1.3:.1f} {x+r*1.6:.1f},{y-r*.2:.1f} {x},{y+r*.9:.1f} Z" fill="{col}"/>')


# 1. 粉紅色的禮品店
card('shop', '手繪粉紅色的禮品店門口，櫥窗有絨毛熊和禮物盒',
     floor(150)
     + f'<rect x="30" y="50" width="180" height="100" fill="#fde3ea"/>'
     + f'<rect x="76" y="18" width="88" height="26" rx="13" fill="{WHITE}"/>'
     + heart(120, 31, 8, PINK)
     + awning(24, 48, 192, PINK, WHITE, 8)
     + f'<rect x="40" y="76" width="108" height="66" rx="10" fill="{SKY}"/>'
     + f'<path d="M44,134 L144,134" stroke-width="2"/>'
     + bear(70, 104, '#f2c6a0', .62) + gift(98, 112, 20, 16, LILAC, TEAL) + gift(124, 118, 16, 12, GOLD, WHITE)
     + f'<path d="M158,150 L158,90 Q158,76 178,76 Q198,76 198,90 L198,150 Z" fill="{PINK}"/>'
     + f'<circle cx="190" cy="118" r="2.6" fill="{GOLD}"/>'
     + heart(178, 96, 6, WHITE)
     + sparkle(20, 30) + star(210, 22, 7) + sparkle(222, 64))

# 2. 文具與小周邊
card('goods', '手繪貼紙本、一張張貼紙、小包包和絨毛吊飾',
     floor(150, '#fbe9ef')
     + f'<rect x="22" y="40" width="64" height="86" rx="6" fill="{LILAC}"/>'
     + f'<rect x="22" y="40" width="12" height="86" rx="4" fill="#ab93d1"/>'
     + heart(60, 70, 10, WHITE) + star(48, 100, 6, GOLD) + f'<circle cx="72" cy="104" r="6" fill="{MINT}"/>'
     + f'<g transform="rotate(8 120 60)"><rect x="98" y="34" width="44" height="56" rx="4" fill="{WHITE}"/>'
     + heart(110, 50, 6, PINK) + star(130, 50, 6, GOLD) + f'<circle cx="110" cy="72" r="6" fill="{SKY}"/>' + heart(130, 72, 6, RED) + '</g>'
     + f'<path d="M104,110 L160,110 Q166,110 166,118 L164,140 Q163,146 156,146 L108,146 Q101,146 100,140 L98,118 Q98,110 104,110 Z" fill="{TEAL}"/>'
     + f'<path d="M100,118 L166,118" stroke-width="1.8"/><circle cx="160" cy="116" r="3" fill="{GOLD}"/>'
     + f'<path d="M196,34 L196,58" stroke-width="1.8"/><circle cx="196" cy="32" r="4" fill="{GOLD}"/>'
     + bear(196, 74, PINK, .6)
     + sparkle(30, 24) + sparkle(220, 120) + star(160, 26, 6))

# 3. 抽獎籤（当りくじ）
card('kuji', '手繪抽獎用的籤和後面一排獎品',
     floor(150)
     + shelf(26, 70, 188, rows=1, gap=40)
     + bear(52, 46, BROWN, .62) + gift(80, 50, 22, 18, PINK, TEAL) + bear(130, 46, '#f2c6a0', .62)
     + f'<rect x="152" y="40" width="26" height="28" rx="5" fill="{MINT}"/><rect x="186" y="46" width="22" height="22" rx="4" fill="{LEMON}"/>'
     + f'<rect x="58" y="96" width="124" height="48" rx="8" fill="{WHITE}"/>'
     + ''.join(f'<g transform="rotate({r} {x} 118)"><rect x="{x-11}" y="102" width="22" height="32" rx="3" fill="{c}"/>'
               f'<path d="M{x-7},{110} L{x+7},{110}" stroke-width="1.4"/></g>'
               for x, r, c in [(84, -10, PINK), (108, -3, GOLD), (132, 4, SKY), (156, 11, LILAC)])
     + sparkle(28, 120) + star(212, 112, 7) + sparkle(120, 24))

# ---- 提醒卡小圖 ----
rem('r-nextday', '手繪提醒：日曆上今天和明天兩格，明天那格畫著新商品',
    f'<rect x="12" y="24" width="96" height="76" rx="6" fill="{WHITE}"/>'
    + f'<rect x="12" y="24" width="96" height="16" rx="6" fill="{PINK}"/>'
    + f'<path d="M30,18 L30,30 M90,18 L90,30" stroke-width="3"/>'
    + f'<path d="M60,40 L60,100" stroke-width="1.8"/>'
    + txt(36, 76, '1', 26, GRAY) + gift(70, 66, 26, 20, LILAC, TEAL)
    + f'<path d="M40,104 Q60,114 80,104" fill="none" stroke="{RED}" stroke-width="2.4"/><path d="M74,100 L80,104 L74,109" fill="none" stroke="{RED}" stroke-width="2.4"/>')

rem('r-receipt', '手繪提醒：一張收據，對應的三份禮物少了一份',
    receipt(12, 16, 36, 60)
    + gift(62, 62, 18, 14, PINK, TEAL) + gift(88, 62, 18, 14, GOLD, WHITE)
    + f'<rect x="61" y="86" width="20" height="18" rx="3" fill="none" stroke-dasharray="4 3" stroke-width="1.8"/>'
    + f'<path d="M66,90 L76,100 M76,90 L66,100" stroke="{RED}" stroke-width="2.6"/>'
    + f'<path d="M50,46 L60,56" stroke-width="1.6" stroke-dasharray="3 3"/>')

rem('r-mall', '手繪提醒：百貨大樓和一張信用卡，旁邊一個問號',
    f'<rect x="12" y="20" width="62" height="86" rx="4" fill="{LILAC}"/>'
    + ''.join(f'<path d="M12,{40+20*i} L74,{40+20*i}" stroke-width="1.6"/>' for i in range(3))
    + ''.join(f'<rect x="{20+18*j}" y="{26+20*i}" width="10" height="8" rx="1" fill="{SKY}" stroke-width="1.2"/>' for i in range(4) for j in range(3))
    + f'<rect x="58" y="70" width="52" height="34" rx="5" fill="{GREEN}"/>'
    + f'<rect x="64" y="78" width="12" height="9" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    + f'<path d="M64,96 L100,96" stroke-width="1.6"/>'
    + f'<circle cx="96" cy="36" r="15" fill="{WHITE}"/>' + txt(96, 43, '?', 20, RED))

print(save(F, OUT), 'files')
