# KIDDY LAND 頁的「店裡長怎樣」插圖與提醒卡（2026-11-13）。
# 依官網原宿店與店舖一覽（kiddyland.co.jp/shoplist/）的介紹畫成一般玩具店的可愛版。
# 角色店：不畫任何角色、角色剪影或角色招牌元素，只畫一般絨毛熊、兔子、禮物盒與層架。
# 輸出 illust/sp/japan-coupon-kiddy-land/*.svg，說明文字在 illust/spots/japan-coupon-kiddy-land.json。
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


PFX = 'kdl-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-kiddy-land')
# 角色店：不畫任何角色、角色剪影或角色招牌元素，只畫一般的玩具店、絨毛熊、兔子、禮物盒與購物袋。


def tree_round(x, base, r=18, col=GREEN):
    return (f'<rect x="{x-3}" y="{base-22}" width="6" height="22" fill="{DBROWN}"/>'
            f'<circle cx="{x}" cy="{base-22-r*.7:.1f}" r="{r}" fill="{col}"/>')


# 1. 表參道上整棟好幾層的原宿店
card('harajuku', '手繪大馬路旁一整棟好幾層樓的玩具店，路邊有行道樹',
     f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{GRAY}"/>'
     + f'<path d="M3,146 L237,146" stroke-width="1.6" stroke-dasharray="10 8"/>'
     + f'<rect x="64" y="22" width="112" height="118" rx="4" fill="{LEMON}"/>'
     + ''.join(f'<path d="M64,{48+24*i} L176,{48+24*i}" stroke-width="1.8"/>' for i in range(3))
     + ''.join(f'<rect x="{72+26*j}" y="{28+24*i}" width="18" height="14" rx="2" fill="{SKY}" stroke-width="1.3"/>' for i in range(3) for j in range(4))
     + bear(85, 34, BROWN, .3) + bunny(137, 58, PEACH, .3) + bear(163, 82, PINK, .3)
     + f'<rect x="72" y="104" width="44" height="36" rx="3" fill="{WHITE}"/>'
     + bear(92, 118, '#f2c6a0', .5) + gift(104, 126, 9, 8, PINK, RED)
     + f'<rect x="126" y="108" width="40" height="32" rx="3" fill="{BROWN}"/><path d="M146,108 L146,140" stroke-width="1.6"/>'
     + tree_round(36, 140, 20) + tree_round(206, 140, 20, DGREEN)
     + kid(48, 116, RED, .7) + kid(190, 116, SKY, .7)
     + sparkle(24, 30) + star(214, 28, 7))

# 2. 很多角色的周邊，一區一區排開
card('corners', '手繪玩具店裡一區一區的層架，擺著絨毛熊、兔子和禮物盒',
     floor(150)
     + f'<rect x="18" y="30" width="62" height="114" rx="6" fill="#fde3ea"/>'
     + f'<rect x="89" y="30" width="62" height="114" rx="6" fill="{MINT}"/>'
     + f'<rect x="160" y="30" width="62" height="114" rx="6" fill="#e3e9fb"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="58" height="5" rx="2" fill="{BROWN}"/>' for x in (20, 91, 162) for y in (84, 134))
     + bear(49, 60, BROWN, .62) + gift(38, 116, 22, 14, GOLD, RED)
     + bunny(120, 62, PEACH, .62) + bear(108, 120, '#f2c6a0', .4) + bear(132, 120, PINK, .4)
     + bear(191, 60, '#f2c6a0', .62) + bunny(179, 120, PINK, .42) + gift(196, 116, 16, 14, SKY, GOLD)
     + sparkle(120, 16) + star(40, 18, 6) + star(206, 18, 6))

# 3. 開在購物中心裡的分店，時間跟著商場
card('mall', '手繪購物中心裡的一家玩具店，牆上一個時鐘',
     floor(150)
     + f'<rect x="14" y="20" width="212" height="130" rx="4" fill="#ece6f6"/>'
     + f'<path d="M14,52 L226,52" stroke-width="2"/>'
     + ''.join(f'<rect x="{24+40*j}" y="28" width="28" height="16" rx="2" fill="{SKY}" stroke-width="1.3"/>' for j in range(5))
     + f'<rect x="34" y="66" width="120" height="84" fill="{WHITE}"/>'
     + awning(30, 62, 128, GOLD, WHITE, 6, 12)
     + f'<rect x="44" y="90" width="58" height="46" rx="4" fill="{SKY}"/>'
     + bear(62, 110, BROWN, .5) + bunny(86, 112, PEACH, .46)
     + f'<rect x="112" y="90" width="32" height="60" rx="3" fill="{BROWN}"/>'
     + f'<circle cx="190" cy="92" r="22" fill="{WHITE}"/>'
     + f'<path d="M190,92 L190,78 M190,92 L201,98" stroke-width="2.6"/>'
     + ''.join(f'<circle cx="{190+17*c}" cy="{92+17*s}" r="1.6" fill="{INK}" stroke="none"/>' for c, s in [(0, -1), (1, 0), (0, 1), (-1, 0)])
     + person(176, 128, PINK, .9) + person(202, 130, GREEN, .9))

# ---- 提醒卡小圖 ----
rem('r-counter', '手繪提醒：從玩具店走到另一棟的免稅櫃台，旁邊是今天的日曆',
    f'<rect x="10" y="44" width="34" height="40" fill="{PINK}"/>'
    + awning(8, 40, 38, RED, WHITE, 3, 8)
    + f'<rect x="18" y="60" width="12" height="24" rx="2" fill="{BROWN}" stroke-width="1.4"/>'
    + ''.join(f'<circle cx="{50+8*i}" cy="{88-2*i}" r="2" fill="{RED}" stroke="none"/>' for i in range(4))
    + f'<rect x="76" y="54" width="34" height="30" rx="3" fill="{SKY}"/>'
    + f'<rect x="72" y="50" width="42" height="8" rx="3" fill="{NAVY}"/>'
    + passport(84, 60, .5)
    + f'<rect x="60" y="12" width="42" height="30" rx="4" fill="{WHITE}"/>'
    + f'<rect x="60" y="12" width="42" height="9" rx="4" fill="{RED}"/>'
    + f'<path d="M72,30 l4,4 l8,-9" stroke="{GREEN}" stroke-width="2.6" fill="none"/>'
    + f'<path d="M10,96 L110,96" stroke-width="1.8"/>')

rem('r-receipt', '手繪提醒：一張收據，對應的三份禮物少了一份',
    receipt(12, 16, 36, 60)
    + gift(62, 62, 18, 14, PINK, RED) + gift(88, 62, 18, 14, GOLD, WHITE)
    + f'<rect x="61" y="86" width="20" height="18" rx="3" fill="none" stroke-dasharray="4 3" stroke-width="1.8"/>'
    + f'<path d="M66,90 L76,100 M76,90 L66,100" stroke="{RED}" stroke-width="2.6"/>')

rem('r-mall', '手繪提醒：購物中心大樓和一張信用卡，旁邊一個問號',
    f'<rect x="12" y="20" width="62" height="86" rx="4" fill="{LILAC}"/>'
    + ''.join(f'<path d="M12,{40+20*i} L74,{40+20*i}" stroke-width="1.6"/>' for i in range(3))
    + ''.join(f'<rect x="{20+18*j}" y="{26+20*i}" width="10" height="8" rx="1" fill="{SKY}" stroke-width="1.2"/>' for i in range(4) for j in range(3))
    + f'<rect x="58" y="70" width="52" height="34" rx="5" fill="{GREEN}"/>'
    + f'<rect x="64" y="78" width="12" height="9" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    + f'<path d="M64,96 L100,96" stroke-width="1.6"/>'
    + f'<circle cx="96" cy="36" r="15" fill="{WHITE}"/>' + txt(96, 43, '?', 20, RED))

print(save(F, OUT), 'files')
