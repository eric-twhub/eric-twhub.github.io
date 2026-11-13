# SUNDRUG 優惠券頁（/japan-coupon/sundrug/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依 LIVE JAPAN 官方發券頁（livejapan.com/public/operation/coupon/sundrug/zh-tw.html）介紹的商品畫成可愛版；
# 招牌留白、不畫任何品牌與商標。輸出 illust/sp/japan-coupon-sundrug/*.svg，說明在 illust/spots/japan-coupon-sundrug.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-sundrug')
PFX = 'sd-'

W, H = 240, 180
F = {}
LAV = '#c9b8e8'
MINT = '#bfe8d6'
PEACH = '#f9d2b4'
TEAL = '#7cc7c2'
ORANGE = '#f2a46b'
BEIGE = '#e9dcc8'
YEL = '#fff3c4'
SKIN = '#f9d9c0'


def card(name, label, inner, bg=CREAM):
    F[name] = svg(PFX + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg(PFX + name, 120, 120, label, inner, bg=YEL)


def floor(y=150, col=BEIGE):
    # 卡片底部的地面，順著外框的圓角
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def awning(x, y, w, c1, c2, n=6, h=14):
    sw = w / n
    t = ''
    for i in range(n):
        c = c1 if i % 2 == 0 else c2
        t += (f'<path d="M{x+sw*i:.1f},{y} L{x+sw*(i+1):.1f},{y} L{x+sw*(i+1):.1f},{y+h} '
              f'q{-sw/2:.1f},{h*.8:.1f} {-sw:.1f},0 Z" fill="{c}" stroke-width="1.8"/>')
    return t


def shop(x, y, w, h, wall, a1, a2, sign, door=SKY, smile=True, icon=''):
    """空白招牌的可愛店面：招牌只畫臉或商品小圖示，不寫字。"""
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{wall}"/>'
         f'<rect x="{x+10}" y="{y+8}" width="{w-20}" height="24" rx="8" fill="{sign}"/>')
    if smile:
        t += face(x + w / 2, y + 18, .8)
    t += icon
    t += awning(x - 4, y + 38, w + 8, a1, a2, n=max(4, int(w // 26)))
    dw = min(34, w * .26)
    t += (f'<rect x="{x+w/2-dw/2:.1f}" y="{y+h-40}" width="{dw:.1f}" height="40" rx="3" fill="{door}"/>'
          f'<path d="M{x+w/2:.1f},{y+h-40} L{x+w/2:.1f},{y+h}" stroke-width="1.6"/>')
    return t


def win(x, y, w, h, col=SKY):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{col}"/>'


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    # 正面小人（有臉）
    return (f'<path d="M{x-8*s},{y+26*s} q0,{-16*s} {8*s},{-16*s} q{8*s},0 {8*s},{16*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{8*s}" fill="{SKIN}"/>'
            f'<path d="M{x-8*s},{y-1*s} q{1*s},{-9*s} {8*s},{-9*s} q{7*s},0 {8*s},{9*s} q{-8*s},{-4*s} {-16*s},0 Z" fill="{hair}" stroke-width="1.4"/>'
            + face(x, y + 1.5 * s, .5 * s))


def shelf(x, y, w, n=2, gap=34, col=BROWN):
    return ''.join(f'<rect x="{x}" y="{y+gap*i}" width="{w}" height="6" rx="2" fill="{col}"/>' for i in range(n))


def lipstick(x, y, col=RED, s=1.0):
    return (f'<path d="M{x+2*s},{y} L{x+2*s},{y-12*s} L{x+12*s},{y-18*s} L{x+12*s},{y} Z" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{14*s}" height="{8*s}" rx="1" fill="{GOLD}" stroke-width="1.6"/>'
            f'<rect x="{x-1*s}" y="{y+8*s}" width="{16*s}" height="{18*s}" rx="2" fill="{NAVY}" stroke-width="1.6"/>')


def jar(x, y, col=PINK, s=1.0, smile=True):
    return (f'<rect x="{x}" y="{y}" width="{30*s}" height="{10*s}" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
            f'<rect x="{x-2*s}" y="{y+9*s}" width="{34*s}" height="{20*s}" rx="{6*s}" fill="{col}" stroke-width="1.8"/>'
            + (face(x + 15 * s, y + 18 * s, .5 * s) if smile else ''))


def pump(x, y, col=MINT, s=1.0):
    # 按壓瓶（化妝水、洗髮精）
    return (f'<path d="M{x+8*s},{y-12*s} l{12*s},0" stroke-width="2.4"/>'
            f'<rect x="{x+6*s}" y="{y-12*s}" width="{6*s}" height="{14*s}" fill="{WHITE}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{18*s}" height="{40*s}" rx="{5*s}" fill="{col}" stroke-width="1.8"/>'
            f'<rect x="{x+3*s}" y="{y+12*s}" width="{12*s}" height="{14*s}" rx="2" fill="{WHITE}" stroke-width="1.2"/>')


def pillbox(x, y, w=34, h=26, col=WHITE, mark=RED):
    # 藥盒：只畫十字，不畫任何品牌
    return (f'<path d="M{x},{y} l8,-8 l{w},0 l-8,8 Z" fill="{GRAY}" stroke-width="1.6"/>'
            f'<path d="M{x+w},{y} l8,-8 l0,{h} l-8,8 Z" fill="{GRAY}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x+w/2},{y+6} L{x+w/2},{y+h-6} M{x+w/2-7},{y+h/2} L{x+w/2+7},{y+h/2}" stroke="{mark}" stroke-width="3.2"/>')


def eyedrop(x, y, col=SKY, s=1.0):
    return (f'<path d="M{x+3*s},{y} L{x+5*s},{y-10*s} L{x+9*s},{y-10*s} L{x+11*s},{y} Z" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x}" y="{y}" width="{14*s}" height="{28*s}" rx="{5*s}" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x+3*s}" y="{y+8*s}" width="{8*s}" height="{10*s}" rx="1" fill="{WHITE}" stroke-width="1"/>')


def tube(x, y, col=MINT, s=1.0):
    return (f'<path d="M{x},{y} L{x+44*s},{y} L{x+50*s},{y+7*s} L{x+44*s},{y+14*s} L{x},{y+14*s} Z" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x+50*s}" y="{y+3*s}" width="{8*s}" height="{8*s}" rx="1" fill="{WHITE}" stroke-width="1.4"/>'
            f'<path d="M{x+4*s},{y} L{x+4*s},{y+14*s}" stroke-width="1.2"/>')


def snack(x, y, col=GOLD, s=1.0, smile=True):
    # 零食袋：上下鋸齒封口
    w, h = 40 * s, 50 * s
    zz = ''.join(f'l{w/8:.1f},{(-3 if i % 2 == 0 else 3)*s:.1f} ' for i in range(8))
    zb = ''.join(f'l{-w/8:.1f},{(3 if i % 2 == 0 else -3)*s:.1f} ' for i in range(8))
    return (f'<path d="M{x},{y} {zz} q{4*s},{h/2:.1f} 0,{h:.1f} {zb} q{-4*s},{-h/2:.1f} 0,{-h:.1f} Z" fill="{col}" stroke-width="1.8"/>'
            f'<ellipse cx="{x+w/2:.1f}" cy="{y+h/2+2*s:.1f}" rx="{13*s:.1f}" ry="{11*s:.1f}" fill="{WHITE}" stroke-width="1.4"/>'
            + (face(x + w / 2, y + h / 2 + 1 * s, .55 * s) if smile else ''))


def phone(x, y, s=1.0, col=NAVY, screen=WHITE, coupon=True):
    # 手機畫面上是一張沒有字的券
    t = (f'<rect x="{x}" y="{y}" width="{40*s}" height="{70*s}" rx="{7*s}" fill="{col}"/>'
         f'<rect x="{x+4*s}" y="{y+8*s}" width="{32*s}" height="{54*s}" rx="2" fill="{screen}" stroke-width="1.4"/>')
    if coupon:
        t += ticket(x + 7 * s, y + 18 * s, .45 * s)
        t += ''.join(f'<path d="M{x+9*s:.1f},{y+(40+i*6)*s:.1f} L{x+31*s:.1f},{y+(40+i*6)*s:.1f}" stroke-width="1.4" opacity=".5"/>' for i in range(3))
    return t


def ticket(x, y, s=1.0, col=PINK):
    # 兩側有缺口的券，中間虛線，不寫字
    w, h = 58 * s, 30 * s
    r = 5 * s
    return (f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h/2-r} a{r},{r} 0 0 0 0,{2*r} L{x+w},{y+h} L{x},{y+h} '
            f'L{x},{y+h/2+r} a{r},{r} 0 0 0 0,{-2*r} Z" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+w*.68:.1f},{y+3*s:.1f} L{x+w*.68:.1f},{y+h-3*s:.1f}" stroke-width="1.4" stroke-dasharray="3 3"/>'
            + star(x + w * .34, y + h / 2, 7 * s, GOLD))


def passport(x, y, s=1.0, col='#3b5a8c'):
    # 護照：只畫一個圓，不畫任何國徽
    return (f'<rect x="{x}" y="{y}" width="{34*s}" height="{46*s}" rx="{4*s}" fill="{col}"/>'
            f'<circle cx="{x+17*s}" cy="{y+20*s}" r="{8*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+9*s},{y+36*s} L{x+25*s},{y+36*s}" stroke="{GOLD}" stroke-width="1.8"/>')


def receipt(x, y, s=1.0, n=4):
    w, h = 34 * s, (18 + n * 7) * s
    return (
            f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h} '
            + ''.join(f'L{x+w-w/6*(i+1):.1f},{y+h+(4 if i % 2 == 0 else 0)*s:.1f} ' for i in range(6))
            + f'Z" fill="{WHITE}" stroke-width="1.6"/>'
            + ''.join(f'<path d="M{x+6*s:.1f},{y+(10+i*7)*s:.1f} L{x+w-6*s:.1f},{y+(10+i*7)*s:.1f}" stroke-width="1.4" opacity=".55"/>' for i in range(n)))


def basket(x, y, s=1.0, col=RED):
    return (f'<path d="M{x+6*s},{y} q{24*s},{-26*s} {48*s},0" fill="none" stroke-width="3"/>'
            f'<path d="M{x},{y} L{x+60*s},{y} L{x+54*s},{y+30*s} L{x+6*s},{y+30*s} Z" fill="{col}"/>'
            + ''.join(f'<path d="M{x+(12+i*12)*s},{y+4*s} L{x+(12+i*12)*s},{y+26*s}" stroke-width="1.4" opacity=".6"/>' for i in range(4)))


def suitcase(x, y, s=1.0, col=ORANGE):
    return (f'<rect x="{x+12*s}" y="{y-10*s}" width="{16*s}" height="{12*s}" rx="3" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{40*s}" height="{54*s}" rx="{7*s}" fill="{col}"/>'
            f'<path d="M{x+13*s},{y+6*s} L{x+13*s},{y+48*s} M{x+27*s},{y+6*s} L{x+27*s},{y+48*s}" stroke-width="1.6"/>'
            f'<circle cx="{x+8*s}" cy="{y+58*s}" r="{3.5*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+32*s}" cy="{y+58*s}" r="{3.5*s}" fill="{INK}" stroke="none"/>')


def nope(x, y, r=14):
    # 紅色禁止圈
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{RED}" stroke-width="4"/>'
            f'<path d="M{x-r*.7:.1f},{y+r*.7:.1f} L{x+r*.7:.1f},{y-r*.7:.1f}" stroke="{RED}" stroke-width="4"/>')


def cross(x, y, r=10):
    return f'<path d="M{x-r},{y-r} L{x+r},{y+r} M{x+r},{y-r} L{x-r},{y+r}" stroke="{RED}" stroke-width="4.5"/>'


def ok(x, y, r=12):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN}"/>'
            f'<path d="M{x-r*.45:.1f},{y} L{x-r*.1:.1f},{y+r*.4:.1f} L{x+r*.5:.1f},{y-r*.4:.1f}" stroke="{WHITE}" stroke-width="3" fill="none"/>')


def arrow(x1, y1, x2, y2, col=RED, w=3):
    a = math.atan2(y2 - y1, x2 - x1)
    l = 8
    p1 = (x2 - l * math.cos(a - .5), y2 - l * math.sin(a - .5))
    p2 = (x2 - l * math.cos(a + .5), y2 - l * math.sin(a + .5))
    return (f'<path d="M{x1},{y1} L{x2},{y2} M{p1[0]:.1f},{p1[1]:.1f} L{x2},{y2} L{p2[0]:.1f},{p2[1]:.1f}" '
            f'stroke="{col}" stroke-width="{w}" fill="none"/>')


def register(x, y, s=1.0, col=GRAY):
    return (f'<rect x="{x}" y="{y+20*s}" width="{60*s}" height="{30*s}" rx="4" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+20*s} L{x+16*s},{y} L{x+44*s},{y} L{x+50*s},{y+20*s} Z" fill="{WHITE}"/>'
            f'<rect x="{x+20*s}" y="{y+4*s}" width="{20*s}" height="{8*s}" rx="1" fill="{SKY}" stroke-width="1.2"/>'
            + ''.join(f'<rect x="{x+(8+i*12)*s}" y="{y+28*s}" width="{8*s}" height="{6*s}" rx="1" fill="{WHITE}" stroke-width="1"/>' for i in range(4)))


def creditcard(x, y, s=1.0, col=TEAL):
    # 沒有任何品牌的卡：只有晶片和一條線
    return (f'<rect x="{x}" y="{y}" width="{46*s}" height="{30*s}" rx="{4*s}" fill="{col}"/>'
            f'<rect x="{x+6*s}" y="{y+8*s}" width="{10*s}" height="{8*s}" rx="1.5" fill="{GOLD}" stroke-width="1.2"/>'
            f'<path d="M{x+6*s},{y+23*s} L{x+30*s},{y+23*s}" stroke-width="1.6" opacity=".6"/>')


def wagon(x, y, col=PEACH):
    # 店門口的小貨架，上面擺盒子和瓶子
    return (f'<rect x="{x}" y="{y}" width="40" height="44" rx="3" fill="{col}"/>'
            f'<path d="M{x},{y+22} L{x+40},{y+22}" stroke-width="1.8"/>'
            f'<rect x="{x+4}" y="{y+8}" width="12" height="14" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x+20}" y="{y+4}" width="14" height="18" rx="2" fill="{MINT}" stroke-width="1.4"/>'
            f'<rect x="{x+5}" y="{y+28}" width="10" height="16" rx="3" fill="{PINK}" stroke-width="1.4"/>'
            f'<rect x="{x+20}" y="{y+30}" width="14" height="14" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
            f'<circle cx="{x+6}" cy="{y+48}" r="3" fill="{INK}" stroke="none"/><circle cx="{x+34}" cy="{y+48}" r="3" fill="{INK}" stroke="none"/>')


def mask(x, y, s=1.0):
    # 面膜：白色臉形，挖空眼睛和嘴巴，自己也在笑
    return (f'<path d="M{x},{y} q{22*s},{-6*s} {44*s},0 q{4*s},{30*s} {-6*s},{46*s} q{-16*s},{14*s} {-32*s},0 q{-10*s},{-16*s} {-6*s},{-46*s} Z" '
            f'fill="{WHITE}" stroke-width="1.8"/>'
            f'<ellipse cx="{x+12*s}" cy="{y+16*s}" rx="{5*s}" ry="{3*s}" fill="{CREAM}" stroke-width="1.4"/>'
            f'<ellipse cx="{x+32*s}" cy="{y+16*s}" rx="{5*s}" ry="{3*s}" fill="{CREAM}" stroke-width="1.4"/>'
            f'<path d="M{x+15*s},{y+33*s} q{7*s},{6*s} {14*s},0" fill="none" stroke-width="1.6"/>'
            f'<ellipse cx="{x+8*s}" cy="{y+26*s}" rx="{3*s}" ry="{1.8*s}" fill="{PINK}" stroke="none"/>'
            f'<ellipse cx="{x+36*s}" cy="{y+26*s}" rx="{3*s}" ry="{1.8*s}" fill="{PINK}" stroke="none"/>')


def matcha_box(x, y, s=1.0):
    # 抹茶點心的盒子：綠色盒子＋一塊抹茶色的小點心
    return (f'<rect x="{x}" y="{y}" width="{54*s}" height="{30*s}" rx="{4*s}" fill="#9ccf8e"/>'
            f'<rect x="{x+4*s}" y="{y+5*s}" width="{46*s}" height="{20*s}" rx="{3*s}" fill="{CREAM}" stroke-width="1.4"/>'
            f'<rect x="{x+8*s}" y="{y+9*s}" width="{16*s}" height="{12*s}" rx="2" fill="#7fb36b" stroke-width="1.2"/>'
            f'<rect x="{x+30*s}" y="{y+9*s}" width="{16*s}" height="{12*s}" rx="2" fill="#7fb36b" stroke-width="1.2"/>'
            + face(x + 16 * s, y + 15 * s, .35 * s, blush=False) + face(x + 38 * s, y + 15 * s, .35 * s, blush=False))


# 1. 店面：門口擺著小貨架
card('front', '手繪藥妝店店面，門口擺著放滿商品的小貨架',
     floor(152)
     + shop(56, 28, 128, 124, '#fdf6f0', PEACH, WHITE, LAV)
     + win(66, 92, 30, 34) + win(144, 92, 30, 34)
     + wagon(10, 106) + wagon(190, 106, MINT)
     + person(100, 133, PINK, .7) + person(140, 131, SKY, .75, INK) + sparkle(24, 32) + star(214, 30, 6) + sparkle(222, 70))

# 2. 保養美妝：面膜、防曬、化妝水
card('skincare', '手繪保養品貨架：面膜、防曬乳和化妝水',
     floor(156, '#f3e6d6')
     + shelf(16, 98, 208, 2, 52)
     + mask(30, 40, 1.0)
     + tube(92, 80, '#ffe08a', .9) + pump(160, 58, MINT, .95) + pump(188, 64, PINK, .8)
     + jar(28, 120, PINK, .9) + jar(80, 122, SKY, .8) + tube(126, 134, '#ffe08a', .7) + pump(196, 124, LAV, .6)
     + sparkle(140, 32) + star(214, 28, 6))

# 3. 藥品區：腸胃藥、眼藥水
card('medicine', '手繪藥品貨架，有藥盒和眼藥水',
     floor(156, '#e9eef5')
     + shelf(16, 92, 208, 2, 54)
     + pillbox(24, 62, 36, 28) + pillbox(72, 58, 34, 32, '#fde8e8', RED) + pillbox(124, 64, 30, 26, '#e8f4ec', GREEN)
     + eyedrop(176, 62, SKY, .95) + eyedrop(198, 62, PINK, .95)
     + pillbox(24, 118, 30, 26, '#eef', NAVY) + eyedrop(70, 116, '#c8f0e0', .9) + eyedrop(92, 116, SKY, .9)
     + pillbox(124, 118, 34, 28) + pillbox(176, 120, 30, 24, '#fff6d8', ORANGE)
     + sparkle(214, 30) + star(30, 30, 6))

# 4. 零食與抹茶點心
card('snack', '手繪零食區，有零食袋、糖果和抹茶點心盒',
     floor(156, '#f3e6d6')
     + shelf(16, 102, 208, 2, 50)
     + snack(24, 50, GOLD) + snack(72, 52, ORANGE, .9) + matcha_box(124, 70, 1.0) + snack(186, 54, PINK, .8, False)
     + matcha_box(24, 126, .8) + jar(92, 124, '#ffe08a', .8) + snack(140, 118, MINT, .7) + snack(180, 120, GOLD, .65, False)
     + sparkle(120, 30) + star(214, 26, 6))

# ---- 提醒小圖 ----
# 只認免稅結帳：護照＋手機券，一起出示
rem('r-taxfree', '手繪提醒：護照和手機上的券一起出示',
    passport(14, 40, 1.0) + phone(62, 26, 1.0) + ok(98, 90, 12) + sparkle(20, 22) + sparkle(56, 104))

# 專櫃化妝品和部分藥品不折
rem('r-cosme', '手繪提醒：專櫃化妝品和部分藥品不在折扣裡',
    lipstick(18, 62, RED, 1.2) + jar(44, 78, LAV, .8, False) + pillbox(70, 74, 28, 22)
    + nope(90, 34, 16) + sparkle(24, 24))

# 一筆只用一次、不疊別張券
rem('r-once', '手繪提醒：一張券可以，兩張疊在一起不行',
    ticket(12, 22, 1.0) + ok(84, 26, 10)
    + ticket(14, 66, .9, SKY) + ticket(26, 76, .9, GOLD) + nope(94, 84, 13))

print(save(F, OUT), 'files')
