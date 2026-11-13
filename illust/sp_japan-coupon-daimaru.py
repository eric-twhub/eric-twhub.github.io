# 大丸・松坂屋優惠券頁（/japan-coupon/daimaru/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依大丸東京店官網「外国のお客様に」（daimaru.co.jp/tokyo/service/gaikoku.html）的說明畫成可愛版；
# 百貨外觀不描任何一家分店，招牌、旗子留白，不畫商標。
# 輸出 illust/sp/japan-coupon-daimaru/*.svg，說明在 illust/spots/japan-coupon-daimaru.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-daimaru')
PFX = 'dm-'

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


STONE = '#efe4d2'


def flag(x, y, col=RED):
    return (f'<path d="M{x},{y} L{x},{y+40}" stroke-width="2"/>'
            f'<path d="M{x},{y+2} L{x+18},{y+2} L{x+18},{y+30} L{x+9},{y+24} L{x},{y+30} Z" fill="{col}" stroke-width="1.6"/>')


def mirror(x, y, s=1.0):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{12*s}" ry="{16*s}" fill="{SKY}" stroke-width="1.8"/>'
            f'<path d="M{x-4*s},{y-8*s} l{6*s},{-4*s}" stroke="{WHITE}" stroke-width="2"/>'
            f'<path d="M{x},{y+16*s} L{x},{y+26*s} M{x-8*s},{y+26*s} L{x+8*s},{y+26*s}" stroke-width="2.4"/>')


def bento(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{50*s}" height="{30*s}" rx="{4*s}" fill="{BRICK}"/>'
            f'<rect x="{x+4*s}" y="{y+4*s}" width="{42*s}" height="{22*s}" rx="2" fill="{CREAM}" stroke-width="1.2"/>'
            f'<circle cx="{x+14*s}" cy="{y+15*s}" r="{6*s}" fill="{WHITE}" stroke-width="1.2"/>'
            f'<rect x="{x+24*s}" y="{y+8*s}" width="{8*s}" height="{14*s}" rx="2" fill="{GOLD}" stroke-width="1"/>'
            f'<circle cx="{x+39*s}" cy="{y+15*s}" r="{4*s}" fill="{GREEN}" stroke-width="1"/>')


def cake(x, y, s=1.0):
    return (f'<path d="M{x},{y+20*s} L{x+30*s},{y+20*s} L{x+30*s},{y+4*s} L{x},{y} Z" fill="#fde2b8"/>'
            f'<path d="M{x},{y} q{15*s},{-6*s} {30*s},{4*s}" fill="{WHITE}" stroke-width="1.6"/>'
            f'<circle cx="{x+14*s}" cy="{y-4*s}" r="{4*s}" fill="{RED}" stroke-width="1.2"/>')


def paperticket(x, y, s=1.0):
    # 紙本折價券：一張小紙片，上面一顆星
    return (f'<rect x="{x}" y="{y}" width="{40*s}" height="{24*s}" rx="2" fill="{WHITE}" stroke-width="1.8"/>'
            f'<rect x="{x+3*s}" y="{y+3*s}" width="{34*s}" height="{18*s}" rx="1" fill="none" stroke="{PINK}" stroke-width="1.6"/>'
            + star(x + 20 * s, y + 12 * s, 6 * s))


# 1. 百貨公司外觀
card('building', '手繪百貨公司外觀，有圓柱、旗子和大門',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f2fb"/>'
     + floor(152, '#e2dccf')
     + f'<rect x="26" y="34" width="188" height="118" rx="4" fill="{STONE}"/>'
     + f'<rect x="20" y="28" width="200" height="12" rx="3" fill="#d9c8ad"/>'
     + f'<rect x="70" y="10" width="100" height="18" rx="5" fill="{WHITE}"/>' + face(120, 19, .55, blush=False)
     + ''.join(f'<rect x="{36+i*44}" y="50" width="34" height="22" rx="2" fill="{SKY}" stroke-width="1.6"/>' for i in range(4))
     + ''.join(f'<rect x="{36+i*44}" y="80" width="34" height="22" rx="2" fill="{SKY}" stroke-width="1.6"/>' for i in range(4))
     + ''.join(f'<rect x="{x}" y="108" width="10" height="44" rx="2" fill="#f7efe2"/>' for x in (44, 80, 150, 186))
     + f'<rect x="96" y="112" width="48" height="40" rx="3" fill="#fff3c4"/><path d="M120,112 L120,152" stroke-width="1.6"/>'
     + flag(14, 46, RED) + flag(206, 46, NAVY)
     + person(64, 128, PINK, .8) + person(172, 128, TEAL, .8, INK)
     + sparkle(226, 22) + sparkle(18, 22), bg='#e6f2fb')

# 2. 化妝品賣場
card('cosme', '手繪化妝品專櫃：玻璃櫃裡有口紅和乳霜，櫃上有鏡子',
     floor(150, '#f6e9ee')
     + f'<rect x="20" y="96" width="200" height="54" rx="6" fill="{WHITE}"/>'
     + f'<rect x="28" y="104" width="184" height="26" rx="3" fill="#eef7fb" stroke-width="1.4"/>'
     + lipstick(40, 112, RED, .7) + lipstick(56, 112, PINK, .7) + jar(78, 108, PINK, .55, False) + jar(110, 108, LAV, .55, False)
     + pump(150, 102, MINT, .5) + lipstick(176, 112, ORANGE, .7) + lipstick(192, 112, '#c45a7a', .7)
     + mirror(60, 68, 1.0) + pump(92, 52, PINK, .9) + jar(118, 70, GOLD, .7)
     + person(180, 58, '#2f3e5e', 1.3)
     + sparkle(30, 30) + star(140, 30, 6) + sparkle(220, 30))

# 3. 免稅櫃台：出示護照換紙本券
card('counter', '手繪免稅櫃台，旅客拿出護照，櫃台人員遞出紙本券',
     floor(152)
     + f'<rect x="20" y="96" width="200" height="56" rx="6" fill="#d9c8ad"/>'
     + f'<rect x="20" y="90" width="200" height="10" rx="3" fill="{STONE}"/>'
     + person(150, 50, NAVY, 1.4) + f'<rect x="143" y="70" width="14" height="16" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
     + person(64, 66, PINK, 1.5)
     + passport(86, 72, .6) + paperticket(118, 72, .8)
     + f'<rect x="96" y="20" width="48" height="18" rx="5" fill="{WHITE}"/>' + passport(110, 23, .25)
     + sparkle(206, 30) + star(30, 30, 6))

# 4. 地下食品賣場（不在券的範圍）
card('food', '手繪百貨地下的食品賣場，有便當和蛋糕',
     floor(150, '#efe6d6')
     + f'<rect x="16" y="86" width="208" height="64" rx="6" fill="{WHITE}"/>'
     + f'<rect x="24" y="94" width="192" height="30" rx="3" fill="#eef7fb" stroke-width="1.4"/>'
     + bento(30, 96, .9) + bento(84, 96, .9) + cake(150, 104, .8) + cake(184, 104, .8)
     + f'<path d="M16,40 q26,-12 52,0 q26,-12 52,0 q26,-12 52,0 q26,-12 52,0" fill="none" stroke-width="2"/>'
     + ''.join(f'<circle cx="{x}" cy="40" r="5" fill="{c}" stroke-width="1.4"/>' for x, c in [(42, GOLD), (94, RED), (146, GOLD), (198, RED)])
     + person(70, 54, ORANGE, .9) + person(170, 54, LAV, .9, INK)
     + sparkle(120, 66))

# ---- 提醒小圖 ----
# 免稅要在買的當天辦
rem('r-sameday', '手繪提醒：商品和當天的收據一起帶到櫃台',
    f'<rect x="12" y="18" width="46" height="40" rx="5" fill="{WHITE}"/>'
    f'<path d="M12,30 L58,30" stroke-width="1.6"/><rect x="12" y="18" width="46" height="12" rx="5" fill="{RED}"/>'
    f'<circle cx="35" cy="44" r="8" fill="{GOLD}" stroke-width="1.4"/>'
    + receipt(70, 18, .9, 4)
    + f'<path d="M30,96 L18,72 L56,72 L44,96 Z" fill="{PINK}"/><path d="M28,72 q9,-14 18,0" fill="none" stroke-width="2.4"/>'
    + ok(90, 92, 12))

# 護照和付款名義要一樣
rem('r-name', '手繪提醒：護照和卡要同一個人',
    passport(12, 26, .9) + creditcard(58, 34, 1.0)
    + f'<path d="M46,50 L56,50" stroke-width="2.4"/>' + f'<path d="M46,56 L56,56" stroke-width="2.4"/>'
    + person(34, 84, PINK, .7) + person(82, 84, TEAL, .7, INK) + cross(58, 96, 7))

# 辦完免稅就不能退換
rem('r-noreturn', '手繪提醒：辦完免稅的商品不能退貨換貨',
    lipstick(22, 58, RED, 1.2) + lipstick(46, 58, PINK, 1.2)
    + f'<path d="M78,52 q14,-10 24,4" fill="none" stroke-width="2.6"/>' + arrow(96, 40, 102, 56, INK, 2.6)
    + nope(88, 82, 16) + sparkle(20, 22))

print(save(F, OUT), 'files')
