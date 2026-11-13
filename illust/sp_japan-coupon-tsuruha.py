# 鶴羽藥妝優惠券頁（/japan-coupon/tsuruha/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依鶴羽官網（tsuruha.co.jp）首頁的商品活動與 coupons.json 的分店說明畫成可愛版，招牌留白、不畫商標；
# 提醒卡依 MATCHA 發券頁（matcha-jp.com/tw/coupon/74）與鶴羽官網繁中免稅說明（tsuruha.co.jp/tw/）。
# 輸出 illust/sp/japan-coupon-tsuruha/*.svg，說明在 illust/spots/japan-coupon-tsuruha.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-tsuruha')
PFX = 'th-'

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


def snowroof(x, y, w):
    # 屋頂上一層圓滾滾的積雪
    n = int(w // 14)
    return (f'<path d="M{x-4},{y+4} ' + ''.join(f'q{w/n/2+.4:.1f},{-12} {w/n+.8:.1f},0 ' for _ in range(n))
            + f'L{x+w+4},{y+8} L{x-4},{y+8} Z" fill="{WHITE}" stroke-width="1.8"/>')


def compact(x, y, s=1.0, col=PINK):
    # 粉餅盒：打開的蓋子有鏡子
    return (f'<ellipse cx="{x}" cy="{y}" rx="{18*s}" ry="{8*s}" fill="{col}"/>'
            f'<ellipse cx="{x}" cy="{y-2*s}" rx="{12*s}" ry="{4.5*s}" fill="#f6d2c0" stroke-width="1.4"/>'
            f'<path d="M{x-18*s},{y} q{0},{-30*s} {18*s},{-30*s} q{18*s},0 {18*s},{30*s}" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x-12*s},{y-4*s} q0,{-20*s} {12*s},{-20*s} q{12*s},0 {12*s},{20*s} Z" fill="{SKY}" stroke-width="1.4"/>'
            f'<path d="M{x-4*s},{y-16*s} l{6*s},{-4*s}" stroke="{WHITE}" stroke-width="2"/>')


def spray(x, y, s=1.0, col=LAV):
    # 髮型噴霧罐
    return (f'<rect x="{x+3*s}" y="{y-10*s}" width="{12*s}" height="{10*s}" rx="2" fill="{WHITE}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{18*s}" height="{46*s}" rx="{5*s}" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x},{y+12*s} L{x+18*s},{y+12*s} M{x},{y+34*s} L{x+18*s},{y+34*s}" stroke-width="1.4"/>'
            + ''.join(f'<circle cx="{x+20*s+i*5*s:.1f}" cy="{y-12*s-i*2*s:.1f}" r="1.6" fill="{SKY}" stroke="none"/>' for i in range(3)))


def diapers(x, y, s=1.0, col=SKY):
    # 一大包尿布：袋子上畫一個小寶寶的臉
    return (f'<rect x="{x}" y="{y}" width="{56*s}" height="{50*s}" rx="{8*s}" fill="{col}"/>'
            f'<path d="M{x+4*s},{y+6*s} L{x+52*s},{y+6*s}" stroke-width="1.4" opacity=".5"/>'
            f'<circle cx="{x+28*s}" cy="{y+28*s}" r="{14*s}" fill="{SKIN}" stroke-width="1.6"/>'
            f'<path d="M{x+24*s},{y+15*s} q{4*s},{-5*s} {6*s},{1*s}" fill="none" stroke-width="1.4"/>'
            + face(x + 28 * s, y + 29 * s, .55 * s))


def tissue(x, y, s=1.0, col=MINT):
    return (f'<rect x="{x}" y="{y}" width="{46*s}" height="{24*s}" rx="{3*s}" fill="{col}"/>'
            f'<ellipse cx="{x+23*s}" cy="{y+4*s}" rx="{12*s}" ry="{3*s}" fill="{WHITE}" stroke-width="1.2"/>'
            f'<path d="M{x+17*s},{y+4*s} q{6*s},{-16*s} {12*s},0" fill="{WHITE}" stroke-width="1.4"/>'
            + ''.join(f'<circle cx="{x+(8+i*10)*s:.1f}" cy="{y+16*s:.1f}" r="{2*s:.1f}" fill="{WHITE}" stroke="none"/>' for i in range(4)))


def bottle(x, y, s=1.0, col='#f6c28b', cap=RED):
    # 調味料或飲料的瓶子
    return (f'<rect x="{x+6*s}" y="{y-8*s}" width="{8*s}" height="{8*s}" rx="1.5" fill="{cap}" stroke-width="1.4"/>'
            f'<path d="M{x+6*s},{y} L{x+14*s},{y} q{6*s},{6*s} {6*s},{14*s} L{x+20*s},{y+36*s} q0,{4*s} {-4*s},{4*s} '
            f'L{x+4*s},{y+40*s} q{-4*s},0 {-4*s},{-4*s} L{x},{y+14*s} q0,{-8*s} {6*s},{-14*s} Z" fill="{col}" stroke-width="1.8"/>'
            f'<rect x="{x+3*s}" y="{y+18*s}" width="{14*s}" height="{12*s}" rx="2" fill="{WHITE}" stroke-width="1.2"/>')


# 1. 下雪的街上的藥妝店
card('front', '手繪下雪街道上的藥妝店，屋頂積著雪',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e3eef8"/>'
     + floor(150, WHITE)
     + shop(52, 34, 136, 116, '#fbf7f2', SKY, WHITE, MINT)
     + snowroof(52, 26, 136)
     + win(62, 96, 32, 32, '#fff3c4') + win(146, 96, 32, 32, '#fff3c4')
     + person(28, 122, RED, 1.0) + f'<path d="M19,134 q9,5 18,0" stroke="{GOLD}" stroke-width="3.4" fill="none"/>'
     + f'<circle cx="212" cy="140" r="12" fill="{WHITE}"/><circle cx="212" cy="120" r="9" fill="{WHITE}"/>' + face(212, 120, .5)
     + f'<path d="M206,112 L218,112 L216,104 L208,104 Z" fill="{RED}" stroke-width="1.4"/>'
     + snow([(20, 30), (40, 60), (210, 40), (226, 90), (196, 20), (30, 100), (120, 18)], 2.6)
     + snow([(80, 162), (160, 166), (200, 158)], 2.2, GRAY), bg='#e3eef8')

# 2. 彩妝與美髮造型
card('beauty', '手繪彩妝與美髮貨架：粉餅、口紅和造型噴霧',
     floor(156, '#f3e6d6')
     + shelf(16, 100, 208, 2, 52)
     + compact(52, 96, 1.0) + lipstick(92, 74, RED, 1.0) + lipstick(114, 74, PINK, 1.0)
     + spray(150, 52, 1.0) + spray(178, 56, .9, MINT)
     + compact(44, 148, .7, LAV) + tube(80, 134, PINK, .7) + jar(140, 124, PEACH, .8) + lipstick(196, 128, ORANGE, .8)
     + sparkle(30, 34) + star(212, 26, 6))

# 3. 日用品：尿布、面紙、調味料
card('daily', '手繪日用品貨架：尿布、面紙和瓶裝調味料',
     floor(156, '#e9eef5')
     + shelf(16, 104, 208, 2, 48)
     + diapers(24, 54, 1.0) + diapers(88, 58, .9, PINK) + tissue(150, 80, 1.0)
     + bottle(42, 120, .8) + bottle(66, 120, .8, '#cfe6a8', GREEN) + tissue(100, 133, .8, PEACH) + bottle(158, 120, .8, '#f9d2b4', NAVY) + bottle(184, 120, .8)
     + sparkle(170, 36) + star(212, 28, 6))

# ---- 提醒小圖 ----
# 部分商品不折、不能疊其他優惠
rem('r-combo', '手繪提醒：購物籃裡有些商品不適用折扣',
    basket(14, 64, 1.0, SKY)
    + pillbox(22, 44, 22, 18) + lipstick(52, 46, RED, .9) + jar(66, 50, PINK, .5, False)
    + nope(94, 30, 14) + sparkle(14, 20))

# 官網繁中免稅說明還是舊制
rem('r-oldinfo', '手繪提醒：舊的免稅說明打叉，改成出境時辦確認',
    f'<path d="M14,22 L54,22 L54,74 L14,74 Z" fill="#f3e2c0" stroke-width="1.8"/>'
    + ''.join(f'<path d="M20,{32+i*9} L48,{32+i*9}" stroke-width="1.4" opacity=".55"/>' for i in range(5))
    + cross(34, 48, 14)
    + suitcase(66, 46, .8, ORANGE) + passport(20, 84, .55) + ok(98, 30, 11))

print(save(F, OUT), 'files')
