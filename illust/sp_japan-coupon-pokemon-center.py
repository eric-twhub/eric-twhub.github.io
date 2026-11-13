# 寶可夢中心頁的「店裡長怎樣」插圖與提醒卡（2026-11-13）。
# 依官網店舖一覽（pokemon.co.jp/shop/）的店址與介紹畫成一般玩具店的可愛版。
# 角色店：不畫任何角色、角色剪影或角色招牌元素，只畫一般絨毛熊、兔子、禮物盒與層架。
# 輸出 illust/sp/japan-coupon-pokemon-center/*.svg，說明文字在 illust/spots/japan-coupon-pokemon-center.json。
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


PFX = 'pkc-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-pokemon-center')
# 角色店：不畫任何角色、角色剪影或角色招牌元素，只畫一般玩具店、一般絨毛熊與兔子、禮物盒。


def plane(x, y, s=1.0):
    return (f'<path d="M{x-16*s},{y+2*s} L{x+16*s},{y-2*s} Q{x+22*s},{y} {x+16*s},{y+3*s} L{x-14*s},{y+6*s} Z" fill="{WHITE}"/>'
            f'<path d="M{x-2*s},{y+1*s} L{x-10*s},{y+14*s} L{x-4*s},{y+14*s} L{x+6*s},{y+1*s} Z" fill="{SKY}" stroke-width="1.6"/>'
            f'<path d="M{x-14*s},{y+2*s} L{x-19*s},{y-7*s} L{x-14*s},{y-6*s} L{x-9*s},{y+1*s} Z" fill="{SKY}" stroke-width="1.6"/>')


def cardpack(x, y, col):
    return (f'<rect x="{x}" y="{y}" width="16" height="24" rx="2" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x},{y+5} L{x+16},{y+5}" stroke-width="1.2"/>' + star(x + 8, y + 15, 4, WHITE))


# 1. 開在百貨或購物中心裡的某一層
card('mall', '手繪購物中心大樓，其中一層是玩具店，窗邊坐著絨毛熊',
     floor(150)
     + f'<rect x="40" y="26" width="140" height="124" rx="4" fill="{GRAY}"/>'
     + ''.join(f'<path d="M40,{57+31*i} L180,{57+31*i}" stroke-width="2"/>' for i in range(3))
     + ''.join(f'<rect x="{50+30*j}" y="{33+31*i}" width="20" height="16" rx="2" fill="{SKY}" stroke-width="1.4"/>'
               for i in (0, 2, 3) for j in range(4))
     + f'<rect x="40" y="88" width="140" height="31" fill="{PINK}"/>'
     + f'<rect x="50" y="93" width="68" height="22" rx="3" fill="{WHITE}" stroke-width="1.6"/>'
     + bear(66, 101, BROWN, .42) + bunny(86, 102, PEACH, .4) + gift(100, 104, 12, 9, GOLD, RED)
     + f'<rect x="128" y="92" width="44" height="27" rx="3" fill="{WHITE}" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{136+10*k}" cy="106" r="3" fill="{c}" stroke-width="1.2"/>' for k, c in enumerate([RED, GOLD, GREEN, LILAC]))
     + f'<rect x="96" y="132" width="28" height="18" rx="2" fill="{BROWN}"/>'
     + plane(210, 34, .9)
     + sparkle(22, 40) + star(206, 92, 7) + sparkle(24, 120))

# 2. 層架上的絨毛娃娃、遊戲和卡牌
card('shelf', '手繪玩具店層架，上層是絨毛熊和兔子，下層是遊戲盒和卡牌',
     floor(152)
     + shelf(20, 78, 200, rows=2, gap=52)
     + bear(46, 55, BROWN, .78) + bunny(92, 56, PEACH, .78) + bear(138, 55, '#f2c6a0', .78) + bunny(184, 56, PINK, .72)
     + f'<rect x="32" y="98" width="40" height="32" rx="4" fill="{RED}"/>'
     + f'<rect x="38" y="104" width="28" height="14" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
     + f'<circle cx="46" cy="124" r="2.4" fill="{WHITE}" stroke="none"/><circle cx="58" cy="124" r="2.4" fill="{WHITE}" stroke="none"/>'
     + f'<rect x="82" y="98" width="40" height="32" rx="4" fill="{SKY}"/>'
     + f'<rect x="88" y="104" width="28" height="14" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
     + cardpack(136, 106, GOLD) + cardpack(156, 104, GREEN) + cardpack(176, 106, LILAC)
     + sparkle(28, 24) + star(212, 22, 7) + sparkle(120, 20))

# 3. 附設的咖啡廳與甜點店
card('cafe', '手繪一杯拉花咖啡和一塊草莓蛋糕',
     floor(140, '#f6e6d0')
     + f'<ellipse cx="80" cy="136" rx="52" ry="8" fill="{WHITE}"/>'
     + f'<path d="M110,92 q22,0 22,16 q0,16 -22,16" fill="none" stroke-width="5"/>'
     + f'<path d="M44,80 L116,80 L110,126 Q108,134 98,134 L62,134 Q52,134 50,126 Z" fill="{WHITE}"/>'
     + f'<ellipse cx="80" cy="80" rx="36" ry="9" fill="{BROWN}"/>'
     + f'<path d="M80,86 q-10,-8 -4,-12 q4,-2 4,3 q0,-5 4,-3 q6,4 -4,12 Z" fill="{WHITE}" stroke-width="1.4"/>'
     + face(80, 108, .8)
     + ''.join(f'<path d="M{x},62 q-5,-7 0,-14 q5,-7 0,-14" fill="none" stroke-width="1.8" opacity=".6"/>' for x in (68, 80, 92))
     + f'<path d="M150,128 L208,128 L208,98 L150,112 Z" fill="{LEMON}"/>'
     + f'<path d="M150,112 L208,98 L208,92 L150,106 Z" fill="{WHITE}"/>'
     + f'<path d="M150,120 L208,110" stroke="{PINK}" stroke-width="3"/>'
     + f'<path d="M190,92 q-2,-14 8,-14 q10,0 8,14 Z" fill="{RED}"/><path d="M196,78 l2,-6 l4,4" fill="{GREEN}" stroke-width="1.4"/>'
     + sparkle(30, 30) + star(210, 30, 7) + sparkle(150, 40))

# ---- 提醒卡小圖 ----
rem('r-stock', '手繪提醒：手機上一個問號，旁邊是店面',
    f'<rect x="16" y="16" width="40" height="72" rx="7" fill="{NAVY}"/>'
    + f'<rect x="21" y="24" width="30" height="52" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
    + txt(36, 58, '?', 24, RED)
    + f'<rect x="64" y="56" width="44" height="44" fill="{PINK}"/>'
    + awning(60, 50, 52, RED, WHITE, 4, 10)
    + f'<rect x="72" y="70" width="16" height="16" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    + f'<rect x="92" y="70" width="10" height="30" rx="2" fill="{BROWN}" stroke-width="1.4"/>')

rem('r-lottery', '手繪提醒：抽選箱和一張籤',
    f'<rect x="22" y="44" width="62" height="56" rx="6" fill="{GOLD}"/>'
    + f'<rect x="38" y="44" width="30" height="7" rx="3" fill="{INK}" stroke="none"/>'
    + face(53, 74, .9)
    + f'<g transform="rotate(14 88 30)"><rect x="70" y="16" width="38" height="26" rx="3" fill="{WHITE}"/>'
    + f'<circle cx="80" cy="29" r="5" fill="{RED}" stroke-width="1.2"/><path d="M90,25 L102,25 M90,33 L100,33" stroke-width="1.6"/></g>'
    + sparkle(18, 24) + sparkle(104, 84))

rem('r-mall', '手繪提醒：百貨大樓和一張信用卡，旁邊一個問號',
    f'<rect x="12" y="20" width="62" height="86" rx="4" fill="{LILAC}"/>'
    + ''.join(f'<path d="M12,{40+20*i} L74,{40+20*i}" stroke-width="1.6"/>' for i in range(3))
    + ''.join(f'<rect x="{20+18*j}" y="{26+20*i}" width="10" height="8" rx="1" fill="{SKY}" stroke-width="1.2"/>' for i in range(4) for j in range(3))
    + f'<rect x="58" y="70" width="52" height="34" rx="5" fill="{GREEN}"/>'
    + f'<rect x="64" y="78" width="12" height="9" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    + f'<path d="M64,96 L100,96" stroke-width="1.6"/>'
    + f'<circle cx="96" cy="36" r="15" fill="{WHITE}"/>' + txt(96, 43, '?', 20, RED))

print(save(F, OUT), 'files')
