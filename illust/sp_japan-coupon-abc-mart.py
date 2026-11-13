# ABC-MART 頁的「店裡有什麼」插圖與提醒卡（2026-11-13）。
# 分類參考 ABC-MART 官網網路商店（abc-mart.net/shop/）畫成可愛版，不畫任何品牌鞋款特徵、不寫店名。
# 輸出 illust/sp/japan-coupon-abc-mart/*.svg，說明文字在 illust/spots/japan-coupon-abc-mart.json。
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


PFX = 'abc-'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-abc-mart')


def sneaker(x, y, col=PINK, s=1.0, accent=WHITE):
    # 一般的運動鞋側面（鞋頭朝右），(x,y) 是鞋跟底部
    p = lambda dx, dy: f'{x+dx*s:.1f},{y+dy*s:.1f}'
    return (f'<rect x="{x-1*s:.1f}" y="{y-1*s:.1f}" width="{58*s:.1f}" height="{7*s:.1f}" rx="{3*s:.1f}" fill="{WHITE}"/>'
            f'<path d="M{p(0,0)} L{p(0,-18)} Q{p(0,-25)} {p(7,-25)} L{p(18,-22)} L{p(24,-29)} '
            f'Q{p(28,-31)} {p(30,-25)} Q{p(42,-16)} {p(52,-11)} Q{p(58,-7)} {p(56,0)} Z" fill="{col}"/>'
            f'<path d="M{p(40,-2)} Q{p(52,-4)} {p(55,-8)}" fill="none" stroke-width="1.5"/>'
            + ''.join(f'<path d="M{p(25+5*i,-21+3*i)} L{p(31+5*i,-23+3*i)}" stroke-width="1.5"/>' for i in range(3))
            + f'<rect x="{x-1*s:.1f}" y="{y-21*s:.1f}" width="{7*s:.1f}" height="{13*s:.1f}" rx="{2*s:.1f}" fill="{accent}" stroke-width="1.4"/>')


def boot(x, y, col=BROWN, s=1.0):
    p = lambda dx, dy: f'{x+dx*s:.1f},{y+dy*s:.1f}'
    return (f'<rect x="{x-1*s:.1f}" y="{y-1*s:.1f}" width="{50*s:.1f}" height="{7*s:.1f}" rx="{2*s:.1f}" fill="{DBROWN}"/>'
            f'<path d="M{p(0,0)} L{p(0,-42)} Q{p(0,-46)} {p(4,-46)} L{p(22,-46)} Q{p(25,-46)} {p(25,-42)} '
            f'L{p(25,-18)} Q{p(40,-16)} {p(46,-9)} Q{p(49,-4)} {p(48,0)} Z" fill="{col}"/>'
            + ''.join(f'<circle cx="{x+22*s:.1f}" cy="{y-(38-8*i)*s:.1f}" r="{1.6*s:.1f}" fill="{INK}" stroke="none"/>' for i in range(3)))


def sandal(x, y, col=GOLD, s=1.0):
    p = lambda dx, dy: f'{x+dx*s:.1f},{y+dy*s:.1f}'
    return (f'<path d="M{p(0,0)} Q{p(0,-6)} {p(10,-6)} L{p(44,-6)} Q{p(54,-6)} {p(54,0)} Z" fill="{PEACH}"/>'
            f'<path d="M{p(8,-6)} Q{p(16,-20)} {p(24,-6)}" fill="none" stroke="{col}" stroke-width="{4*s:.1f}"/>'
            f'<path d="M{p(30,-6)} Q{p(38,-20)} {p(46,-6)}" fill="none" stroke="{col}" stroke-width="{4*s:.1f}"/>')


# 1. 鞋店門口
card('front', '手繪鞋子專門店的門口，櫥窗裡擺著運動鞋和靴子',
     floor(150)
     + f'<rect x="30" y="50" width="180" height="100" fill="#fdebd3"/>'
     + f'<rect x="64" y="20" width="112" height="24" rx="6" fill="{WHITE}"/>'
     + sneaker(102, 39, RED, .62)
     + awning(24, 48, 192, RED, WHITE, 8)
     + f'<rect x="40" y="76" width="104" height="66" rx="4" fill="{SKY}"/>'
     + f'<path d="M44,134 L140,134" stroke-width="2"/>'
     + sneaker(48, 132, PINK, .62) + boot(100, 132, BROWN, .62)
     + face(66, 116, .55)
     + f'<rect x="156" y="76" width="44" height="74" rx="3" fill="{BROWN}"/>'
     + f'<rect x="164" y="84" width="28" height="30" rx="3" fill="{SKY}"/>'
     + f'<circle cx="192" cy="122" r="2.6" fill="{GOLD}"/>'
     + sparkle(20, 26) + sparkle(218, 30) + star(200, 18, 6))

# 2. 童鞋（官網分類有キッズ・ジュニア）
card('kids', '手繪層架，上層是大人的運動鞋，下層是小小的童鞋',
     floor(150)
     + shelf(22, 72, 140, rows=2, gap=48)
     + sneaker(30, 71, SKY, .78) + sneaker(92, 71, PINK, .78)
     + sneaker(30, 119, GOLD, .5, RED) + sneaker(66, 119, GREEN, .5) + sneaker(102, 119, LILAC, .5)
     + kid(196, 112, RED, 1.1)
     + sparkle(150, 32) + star(190, 40, 7) + sparkle(214, 70))

# 3. 包包和鞋子保養用品
card('care', '手繪包包、鞋子保養噴霧和鞋刷',
     floor(148)
     + f'<path d="M48,82 q0,-26 24,-26 q24,0 24,26" fill="none" stroke-width="4"/>'
     + f'<rect x="34" y="80" width="76" height="62" rx="12" fill="{NAVY}"/>'
     + f'<rect x="46" y="96" width="52" height="22" rx="6" fill="#4b5a8f"/>'
     + face(72, 128, .7)
     + f'<rect x="128" y="74" width="26" height="66" rx="6" fill="{GREEN}"/>'
     + f'<rect x="133" y="62" width="16" height="14" rx="3" fill="{WHITE}"/>'
     + f'<path d="M149,66 L158,62" stroke-width="2.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{SKY}" stroke="none"/>' for x, y in [(164, 58), (168, 64), (166, 52), (172, 58)])
     + f'<rect x="138" y="94" width="6" height="26" rx="2" fill="{WHITE}" stroke="none"/>'
     + f'<rect x="168" y="114" width="52" height="16" rx="7" fill="{BROWN}"/>'
     + ''.join(f'<path d="M{172+5*i},130 L{172+5*i},140" stroke-width="1.8"/>' for i in range(10))
     + sparkle(28, 40) + star(206, 50, 7) + sparkle(120, 30))

# ---- 提醒卡小圖 ----
# 鞋碼是公分，另外標鞋寬
rem('r-size', '手繪提醒：腳踩在公分尺上量長度',
    f'<rect x="14" y="78" width="92" height="22" rx="3" fill="{GOLD}"/>'
    + ''.join(f'<path d="M{20+8*i},78 L{20+8*i},{86 if i % 2 else 90}" stroke-width="1.4"/>' for i in range(11))
    + f'<path d="M40,72 q-14,-4 -12,-24 q2,-22 18,-30 q14,-6 22,4 q8,10 2,24 q-4,10 -2,18 q2,8 -8,10 Z" fill="{SKIN}"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SKIN}" stroke-width="1.4"/>' for x, y, r in [(52, 14, 4.5), (61, 16, 3.6), (68, 21, 3), (73, 27, 2.6)])
    + f'<path d="M86,30 L104,30 M86,44 L104,44" stroke="{RED}" stroke-width="2.4"/>'
    + txt(95, 22, 'cm', 13, RED))

# 先辦海關確認，再託運
rem('r-box', '手繪提醒：先在機台刷護照，再把鞋盒放進行李託運',
    kiosk(10, 18)
    + f'<circle cx="18" cy="12" r="8" fill="{WHITE}"/>' + txt(18, 16, '1', 11)
    + f'<path d="M56,58 L70,58 M64,52 L70,58 L64,64" stroke="{RED}" stroke-width="3" fill="none"/>'
    + suitcase(74, 50, 38, 46, PINK)
    + f'<rect x="78" y="30" width="30" height="16" rx="2" fill="{BROWN}"/><path d="M78,36 L108,36" stroke-width="1.4"/>'
    + f'<circle cx="62" cy="90" r="8" fill="{WHITE}"/>' + txt(62, 94, '2', 11))

# CUBE 的加碼不含商場裡的門市
rem('r-mall', '手繪提醒：購物中心大樓和一張信用卡，旁邊一個問號',
    f'<rect x="12" y="20" width="62" height="86" rx="4" fill="{LILAC}"/>'
    + ''.join(f'<path d="M12,{40+20*i} L74,{40+20*i}" stroke-width="1.6"/>' for i in range(3))
    + ''.join(f'<rect x="{20+18*j}" y="{26+20*i}" width="10" height="8" rx="1" fill="{SKY}" stroke-width="1.2"/>' for i in range(4) for j in range(3))
    + f'<rect x="58" y="70" width="52" height="34" rx="5" fill="{GREEN}"/>'
    + f'<rect x="64" y="78" width="12" height="9" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    + f'<path d="M64,96 L100,96" stroke-width="1.6"/>'
    + f'<circle cx="96" cy="36" r="15" fill="{WHITE}"/>' + txt(96, 43, '?', 20, RED))

print(save(F, OUT), 'files')
