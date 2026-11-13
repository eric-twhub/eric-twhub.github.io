# 買 iPhone 刷哪張卡頁的「從下單到回饋入帳」插圖與提醒卡（2026-11-13）。
# 手機畫一般圓角長方形，信用卡畫一般卡片，不畫蘋果標誌、銀行或卡組織標誌。
# 說明依 gen.py 本頁內文與常見問題（依據 Apple 台灣購物協助 apple.com/tw/shop/help/payments、
# 國泰世華 CUBE 卡權益說明）。輸出 illust/sp/iphone-card/*.svg。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'iphone-card')
W, H = 240, 180
GLASS = '#e6f2fa'
LILAC = '#e7defa'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('icd-' + name, W, H, label, inner, bg=bg)


def phone(x, y, w=44, h=80, body=LILAC, scr=SKY, smile=True):
    # 一般的圓角長方形手機：外殼＋螢幕＋上方一條小膠囊，不畫任何品牌細節
    r = w * .2
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r:.1f}" fill="{body}"/>'
         f'<rect x="{x+4}" y="{y+5}" width="{w-8}" height="{h-10}" rx="{r*.7:.1f}" fill="{scr}" stroke-width="1.6"/>'
         f'<rect x="{x+w/2-5:.1f}" y="{y+8}" width="10" height="3" rx="1.5" fill="{INK}" stroke="none"/>')
    if smile:
        t += face(x + w / 2, y + h * .52, .7 * w / 44)
    return t


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-6*s},{y-1*s} q{6*s},{-10*s} {12*s},0 q{-6*s},{-4*s} {-12*s},0 Z" fill="{hair}" stroke-width="1.4"/>')


def passport(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{28*s}" height="{38*s}" rx="{3*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+14*s}" cy="{y+17*s}" r="{6.5*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+8*s},{y+31*s} L{x+20*s},{y+31*s}" stroke="{GOLD}" stroke-width="1.6"/>')


def suitcase(x, y, col=SKY, s=1.0):
    return (f'<path d="M{x+10*s},{y} L{x+10*s},{y-8*s} L{x+22*s},{y-8*s} L{x+22*s},{y}" fill="none" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{32*s}" height="{40*s}" rx="{5*s}" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+4*s} L{x+10*s},{y+36*s} M{x+22*s},{y+4*s} L{x+22*s},{y+36*s}" stroke-width="1.4" opacity=".6"/>'
            f'<circle cx="{x+6*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+26*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>')


def floor(y=150, col='#e9dcc8'):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def check(x, y, s=1.0, col=GREEN):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{col}"/>'
            f'<path d="M{x-5*s},{y} L{x-1*s},{y+4*s} L{x+6*s},{y-5*s}" fill="none" stroke="{WHITE}" stroke-width="3"/>')


def cross(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{RED}"/>'
            f'<path d="M{x-5*s},{y-5*s} L{x+5*s},{y+5*s} M{x+5*s},{y-5*s} L{x-5*s},{y+5*s}" stroke="{WHITE}" stroke-width="3"/>')


def label(x, y, txt, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="bold" '
            f'text-anchor="middle" fill="{col}" stroke="none">{txt}</text>')


def ccard(x, y, s=1.0, col=GOLD, rot=0):
    # 一般的信用卡：圓角長方形＋晶片＋一條磁條，不畫任何標誌
    t = (f'<rect x="{x}" y="{y}" width="{60*s}" height="{38*s}" rx="{5*s}" fill="{col}"/>'
         f'<rect x="{x+8*s}" y="{y+12*s}" width="{12*s}" height="{9*s}" rx="{2*s}" fill="{WHITE}" stroke-width="1.4"/>'
         f'<path d="M{x+8*s},{y+29*s} L{x+40*s},{y+29*s}" stroke-width="1.6"/>')
    if rot:
        t = f'<g transform="rotate({rot} {x+30*s} {y+19*s})">{t}</g>'
    return t


def truck(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{70*s}" height="{40*s}" rx="{4*s}" fill="{WHITE}"/>'
            f'<path d="M{x+70*s},{y+12*s} L{x+90*s},{y+12*s} L{x+100*s},{y+26*s} L{x+100*s},{y+40*s} L{x+70*s},{y+40*s} Z" fill="{SKY}"/>'
            f'<rect x="{x+76*s}" y="{y+16*s}" width="{14*s}" height="{10*s}" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
            f'<circle cx="{x+20*s}" cy="{y+42*s}" r="{8*s}" fill="{INK}"/><circle cx="{x+20*s}" cy="{y+42*s}" r="{3*s}" fill="{GRAY}" stroke="none"/>'
            f'<circle cx="{x+84*s}" cy="{y+42*s}" r="{8*s}" fill="{INK}"/><circle cx="{x+84*s}" cy="{y+42*s}" r="{3*s}" fill="{GRAY}" stroke="none"/>')


def cal(x, y, w, h, top=RED):
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{WHITE}"/>'
         f'<path d="M{x},{y+16} L{x+w},{y+16}" stroke-width="1.6"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="16" rx="6" fill="{top}"/>'
         f'<path d="M{x+12},{y-5} L{x+12},{y+6} M{x+w-12},{y-5} L{x+w-12},{y+6}" stroke-width="3"/>')
    return t


# 1. 下單：手機畫面上一台購物車，旁邊一張卡和一個小小的「授權中」沙漏
card('order', '手繪手機畫面上的購物車和一張信用卡，旁邊有個小沙漏',
     phone(34, 34, 64, 116, LILAC, '#fdf2e0', smile=False)
     + f'<path d="M48,70 L56,70 L64,96 L86,96 L90,78 L60,78" fill="none" stroke-width="2.4"/>'
     + f'<circle cx="66" cy="104" r="3.4" fill="{INK}" stroke="none"/><circle cx="84" cy="104" r="3.4" fill="{INK}" stroke="none"/>'
     + f'<rect x="46" y="118" width="40" height="12" rx="6" fill="{GREEN}"/>'
     + ccard(118, 70, 1.3, GOLD, -8)
     + f'<path d="M178,30 L198,30 L188,44 L198,58 L178,58 L188,44 Z" fill="{SKY}"/>'
     + f'<path d="M182,54 L194,54 L188,48 Z" fill="{GOLD}" stroke-width="1.2"/>'
     + sparkle(118, 40) + star(214, 140, 7))

# 2. 出貨：貨車載著箱子開走，箱子上冒出一張卡＝這天才請款
card('ship', '手繪載著紙箱開走的貨車，上面冒出一張信用卡和打勾',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e3e8ef"/>'
     + truck(56, 96, 1.0)
     + f'<path d="M70,96 L70,80 L104,80 L104,96" fill="#e8c597"/>'
     + f'<path d="M87,80 L87,96" stroke-width="1.4"/>'
     + ccard(118, 36, 1.0, PINK, 6) + check(186, 40, .9)
     + ''.join(f'<path d="M{x},{y} L{x-16},{y}" stroke-width="2" opacity=".6"/>' for x, y in [(46, 110), (40, 122), (48, 134)])
     + sparkle(30, 40) + star(214, 92, 6))

# 3. 日曆：下單日在這個月，出貨日翻到下個月
card('calendar', '手繪兩頁日曆，下單的日子在這個月，出貨的日子已經翻到下個月',
     cal(22, 40, 90, 104, RED) + cal(128, 40, 90, 104, GREEN)
     + ''.join(f'<circle cx="{34+(i%5)*16}" cy="{70+(i//5)*16}" r="2" fill="{INK}" stroke="none"/>' for i in range(20))
     + ''.join(f'<circle cx="{140+(i%5)*16}" cy="{70+(i//5)*16}" r="2" fill="{INK}" stroke="none"/>' for i in range(20))
     + f'<circle cx="66" cy="86" r="8" fill="none" stroke="{SKY}" stroke-width="3"/>'
     + phone(56, 112, 14, 24, smile=False)
     + f'<circle cx="172" cy="102" r="8" fill="none" stroke="{RED}" stroke-width="3"/>'
     + f'<rect x="164" y="114" width="18" height="16" rx="2" fill="#e8c597"/>'
     + f'<path d="M112,92 Q120,80 128,92" fill="none" stroke-width="2.4"/><path d="M122,88 L128,93 L131,86" fill="none" stroke-width="2.4"/>'
     + sparkle(120, 28, 5))

# 4. 帳單：一張帳單和一顆亮亮的星星（回饋），依發卡行週期入帳
card('statement', '手繪一張信用卡帳單，旁邊掉下一顆亮亮的星星代表回饋',
     f'<rect x="40" y="26" width="96" height="128" rx="6" fill="{WHITE}"/>'
     + f'<rect x="40" y="26" width="96" height="20" rx="6" fill="{SKY}"/>'
     + ''.join(f'<path d="M52,{y} L{124 if i % 2 else 108},{y}" stroke-width="1.6"/>' for i, y in enumerate((62, 76, 90, 104, 118)))
     + f'<path d="M52,136 L124,136" stroke="{RED}" stroke-width="3"/>'
     + star(176, 70, 22) + face(176, 72, .6, False)
     + ''.join(f'<path d="M{x},{y} l0,8" stroke="{GOLD}" stroke-width="2"/>' for x, y in [(160, 104), (176, 108), (192, 104)])
     + ccard(150, 120, .9, PINK)
     + sparkle(206, 36) + sparkle(28, 140, 4))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label_, inner):
    F[name] = svg('icd-' + name, 120, 120, label_, inner, bg='#fff3c4')


# 切換開關：別在請款前切回去
rem('r-switch', '手繪提醒：手機裡的方案切換開關，旁邊一個鈴鐺',
    phone(16, 14, 50, 92, LILAC, '#fdf2e0', smile=False)
    + f'<rect x="24" y="40" width="34" height="16" rx="8" fill="{GREEN}"/><circle cx="50" cy="48" r="6" fill="{WHITE}"/>'
    + f'<rect x="24" y="66" width="34" height="16" rx="8" fill="{GRAY}"/><circle cx="32" cy="74" r="6" fill="{WHITE}"/>'
    + f'<path d="M84,58 q0,-16 12,-16 q12,0 12,16 l3,8 l-30,0 Z" fill="{GOLD}"/>'
    + f'<circle cx="96" cy="70" r="3" fill="{INK}" stroke="none"/>'
    + f'<path d="M78,40 q-4,6 0,12 M114,40 q4,6 0,12" fill="none" stroke-width="1.8"/>'
    + label(96, 98, '!', 18, RED))

# App 和手機差一個字：左邊一個 App 方塊、右邊一支手機，中間不等號
rem('r-store', '手繪提醒：左邊是四個 App 小方塊，右邊是一支手機，中間畫著不等號',
    ''.join(f'<rect x="{x}" y="{y}" width="17" height="17" rx="5" fill="{c}" stroke-width="1.8"/>'
            for x, y, c in [(10, 38, SKY), (31, 38, PINK), (10, 59, GOLD), (31, 59, GREEN)])
    + f'<path d="M54,52 L66,52 M54,62 L66,62 M64,46 L56,68" stroke="{RED}" stroke-width="2.6"/>'
    + phone(74, 26, 34, 62)
    + f'<rect x="72" y="92" width="38" height="14" rx="4" fill="#e8c597"/>')

# 分期和回饋二選一：天平兩邊，一邊是好幾期的小卡、一邊是星星
rem('r-either', '手繪提醒：天平一邊是分期的小方塊，一邊是回饋的星星',
    f'<path d="M60,24 L60,98 M40,104 L80,104" stroke-width="3"/>'
    + f'<path d="M20,40 L100,40" stroke-width="3"/>'
    + f'<path d="M20,40 L10,66 L30,66 Z M100,40 L90,66 L110,66 Z" fill="none" stroke-width="1.4"/>'
    + f'<path d="M6,66 Q20,78 34,66 Z" fill="{WHITE}"/><path d="M86,66 Q100,78 114,66 Z" fill="{WHITE}"/>'
    + ''.join(f'<rect x="{10+i*7}" y="{56-i*0}" width="6" height="9" rx="1.5" fill="{PINK}" stroke-width="1.2"/>' for i in range(3))
    + star(100, 56, 9)
    + f'<circle cx="60" cy="22" r="5" fill="{GOLD}"/>')

print(save(F, OUT), 'files')
