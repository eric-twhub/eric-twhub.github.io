# UNIQLO 頁（/japan-coupon/uniqlo/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 服飾店畫成可愛版，招牌留白，不畫商標、招牌配色與任何聯名角色。
# 提醒卡依 refund-fees.json 記錄的 UNIQLO 官方 FAQ（退稅由 J&J 處理）與觀光廳旅客問答。
# 輸出 illust/sp/japan-coupon-uniqlo/*.svg，說明在 illust/spots/japan-coupon-uniqlo.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-uniqlo')
PFX = 'uq-'

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


def folded(x, y, col, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{34*s}" height="{11*s}" rx="{3*s}" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+12*s},{y} q{5*s},{5*s} {10*s},0" fill="none" stroke-width="1.2"/>')


def tee(x, y, col, s=1.0):
    return (f'<path d="M{x-12*s},{y} L{x-26*s},{y+10*s} L{x-20*s},{y+20*s} L{x-13*s},{y+16*s} L{x-13*s},{y+46*s} '
            f'L{x+13*s},{y+46*s} L{x+13*s},{y+16*s} L{x+20*s},{y+20*s} L{x+26*s},{y+10*s} L{x+12*s},{y} '
            f'q{-12*s},{8*s} {-24*s},0 Z" fill="{col}" stroke-width="1.8"/>')


def puffer(x, y, col, s=1.0):
    # 羽絨外套：一格一格鼓鼓的
    t = (f'<path d="M{x-16*s},{y} L{x-30*s},{y+12*s} L{x-30*s},{y+50*s} L{x-20*s},{y+50*s} L{x-18*s},{y+58*s} '
         f'L{x+18*s},{y+58*s} L{x+20*s},{y+50*s} L{x+30*s},{y+50*s} L{x+30*s},{y+12*s} L{x+16*s},{y} '
         f'q{-16*s},{10*s} {-32*s},0 Z" fill="{col}" stroke-width="1.8"/>')
    for i in range(1, 5):
        t += f'<path d="M{x-28*s:.1f},{y+(4+i*10)*s:.1f} q{28*s:.1f},{4*s:.1f} {56*s:.1f},0" fill="none" stroke-width="1.3" opacity=".6"/>'
    t += f'<path d="M{x},{y+6*s} L{x},{y+58*s}" stroke-width="1.4"/>'
    return t


def hanger_rail(x1, x2, y):
    return f'<path d="M{x1},{y} L{x2},{y}" stroke-width="3"/>'


def hook(x, y):
    return f'<path d="M{x},{y} L{x},{y+6} q0,4 -4,4" fill="none" stroke-width="1.6"/>'


def mannequin(x, y, col, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f1e6d8"/>'
            + tee(x, y + 8 * s, col, .7 * s)
            + f'<rect x="{x-9*s}" y="{y+40*s}" width="{18*s}" height="{18*s}" rx="2" fill="{NAVY}"/>'
            f'<path d="M{x},{y+58*s} L{x},{y+64*s} M{x-8*s},{y+64*s} L{x+8*s},{y+64*s}" stroke-width="2"/>')


def beanie(x, y, col=RED, s=1.0):
    # 毛線帽：半圓帽身＋反摺帽緣＋毛球
    return (f'<circle cx="{x}" cy="{y-24*s}" r="{6*s}" fill="{WHITE}" stroke-width="1.6"/>'
            f'<path d="M{x-20*s},{y} q0,{-26*s} {20*s},{-26*s} q{20*s},0 {20*s},{26*s} Z" fill="{col}" stroke-width="1.8"/>'
            + ''.join(f'<path d="M{x+i*7*s},{y-22*s+abs(i)*2*s} L{x+i*7*s},{y-2*s}" stroke-width="1.1" opacity=".5"/>' for i in (-2, -1, 0, 1, 2))
            + f'<rect x="{x-22*s}" y="{y-2*s}" width="{44*s}" height="{12*s}" rx="{4*s}" fill="{col}" stroke-width="1.8"/>'
            + face(x, y + 4 * s, .4 * s, blush=False))


def scarf(x, y, col=RED, s=1.0):
    return (f'<path d="M{x},{y} q{14*s},{-8*s} {28*s},0 L{x+28*s},{y+8*s} q{-14*s},{-8*s} {-28*s},0 Z" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+18*s},{y+6*s} L{x+16*s},{y+34*s} L{x+26*s},{y+34*s} L{x+26*s},{y+6*s}" fill="{col}" stroke-width="1.6"/>'
            + ''.join(f'<path d="M{x+(17+i*3)*s},{y+34*s} L{x+(17+i*3)*s},{y+38*s}" stroke-width="1.2"/>' for i in range(4)))


# 1. 服飾店門口，櫥窗裡有人台
card('front', '手繪服飾店門口，兩邊櫥窗各站著一個穿衣服的人台',
     floor(152, '#e6e6ee')
     + shop(26, 24, 188, 128, '#f7f8fb', '#d6e4f0', WHITE, '#eef1f6', smile=True)
     + win(36, 84, 56, 62, '#fdfdfa') + win(148, 84, 56, 62, '#fdfdfa')
     + mannequin(64, 90, '#f2b8a2', .8) + mannequin(176, 90, '#a9cbe8', .8)
     + sparkle(14, 30) + star(226, 28, 5))

# 2. 摺好的衣服按顏色排
card('fold', '手繪大桌上摺好的衣服，一疊一疊按顏色排好',
     floor(150, '#ece4d8')
     + f'<rect x="14" y="108" width="212" height="42" rx="5" fill="#e9dcc8"/>'
     + ''.join(folded(20 + c * 41, 97 - r * 11, col, 1.0)
               for c, col in enumerate(['#f6a5ad', '#f4c152', '#bfe8d6', '#a9cbe8', '#c9b8e8']) for r in range(5))
     + ''.join(f'<rect x="{30+c*41}" y="116" width="16" height="10" rx="2" fill="{WHITE}" stroke-width="1.2"/>' for c in range(5))
     + sparkle(40, 30) + star(120, 26, 6) + sparkle(200, 30))

# 3. 冬天的外套與圍巾
card('winter', '手繪掛在衣架上的羽絨外套、毛衣和圍巾',
     floor(156, '#e6ecf3')
     + hanger_rail(14, 226, 26)
     + hook(50, 26) + puffer(50, 38, '#a9cbe8', .95)
     + hook(120, 26) + puffer(120, 38, '#f2b8a2', .95)
     + hook(190, 26) + tee(190, 38, '#cfe6a8', 1.1)
     + f'<rect x="14" y="136" width="212" height="8" rx="3" fill="#d9c8ad"/>'
     + beanie(50, 126, RED) + beanie(120, 126, GOLD) + beanie(190, 126, '#9fd3c7')
     + snow([(20, 60), (226, 70), (226, 120)], 2.4, GRAY))

# ---- 提醒小圖 ----
# 退稅要自己上網登錄
rem('r-refund', '手繪提醒：用手機登錄退款方式，錢才會退回卡上',
    phone(12, 22, .9, NAVY, WHITE, coupon=False)
    + f'<rect x="20" y="36" width="20" height="20" fill="{WHITE}" stroke-width="1.4"/>'
    + ''.join(f'<rect x="{22+(i%3)*6}" y="{38+(i//3)*6}" width="4" height="4" fill="{INK}" stroke="none"/>' for i in (0, 2, 4, 6, 8, 1))
    + passport(54, 34, .5) + arrow(56, 78, 74, 78, RED, 2.6)
    + creditcard(70, 66, .9) + ok(98, 30, 11))

# 衣服塞進託運行李前，先辦海關確認
rem('r-checkin', '手繪提醒：衣服先別塞進託運的大行李箱',
    suitcase(56, 46, 1.0, '#a9cbe8')
    + tee(30, 36, '#f2b8a2', .6)
    + arrow(44, 70, 54, 78, INK, 2.4) + nope(96, 26, 13))

print(save(F, OUT), 'files')
