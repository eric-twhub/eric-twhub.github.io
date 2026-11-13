# iPhone 持有成本頁的「手機的錢是怎麼花掉的」插圖與提醒卡（2026-11-13）。
# 手機畫一般圓角長方形，不畫蘋果標誌、不畫可辨識的機身設計；收購店不畫招牌。
# 說明依 resale.json（src_note）與 gen.py 本頁的內文、註腳。輸出 illust/sp/iphone-cost/*.svg。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'iphone-cost')
W, H = 240, 180
GLASS = '#e6f2fa'
LILAC = '#e7defa'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ic-' + name, W, H, label, inner, bg=bg)


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


def tired(x, y, s=1.0):
    # 累累的表情：半閉的眼睛＋一滴汗
    return (f'<path d="M{x-7*s},{y} q{2*s},{2*s} {4*s},0 M{x+3*s},{y} q{2*s},{2*s} {4*s},0" fill="none" stroke-width="1.6"/>'
            f'<path d="M{x-3*s},{y+6*s} q{3*s},{-2*s} {6*s},0" fill="none" stroke-width="1.6"/>'
            f'<path d="M{x+10*s},{y-8*s} q{3*s},{5*s} 0,{7*s} q{-3*s},{-2*s} 0,{-7*s} Z" fill="{SKY}" stroke-width="1.2"/>')


# 1. 新機從盒子裡出來，旁邊一條往下的線
card('newbox', '手繪剛從盒子裡拿出來的新手機，旁邊有一條往下掉的曲線',
     f'<rect x="28" y="110" width="80" height="40" rx="5" fill="{WHITE}"/>'
     + f'<path d="M28,120 L108,120" stroke-width="1.4"/>'
     + phone(46, 40, 44, 80)
     + sparkle(36, 40) + sparkle(100, 30, 4) + star(108, 60, 6)
     + f'<rect x="126" y="40" width="96" height="104" rx="8" fill="{WHITE}"/>'
     + f'<path d="M138,52 L138,132 L212,132" fill="none" stroke-width="2"/>'
     + f'<path d="M140,58 Q156,98 176,108 T210,122" fill="none" stroke="{RED}" stroke-width="3"/>'
     + f'<circle cx="140" cy="58" r="4" fill="{GOLD}"/>')

# 2. 三支手機排排站，越右邊越舊越累
card('years', '手繪三支手機排成一排，從閃亮的新機到用了好幾年、有點累的舊機',
     f'<path d="M3,146 L237,146 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + phone(26, 58, 46, 84) + sparkle(22, 50) + sparkle(78, 46, 4)
     + phone(98, 62, 44, 80, PINK, smile=False) + face(120, 104, .7, False)
     + phone(168, 66, 42, 76, '#d8d2c8', '#e8eef2', smile=False) + tired(189, 104, .9)
     + f'<path d="M176,84 L186,92 M198,120 L204,128" stroke-width="1.4"/>'
     + label(49, 40, '1', 15, GREEN) + label(120, 44, '2', 15, GOLD) + label(189, 50, '3', 15, RED))

# 3. 收購店的櫃台：店員拿放大鏡看手機，旁邊是盒子和充電線
card('tradein', '手繪收購櫃台，店員拿放大鏡仔細看手機，旁邊放著盒子和充電線',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<rect x="14" y="112" width="212" height="38" rx="4" fill="{BROWN}"/>'
     + person(170, 66, NAVY, 1.7, INK)
     + phone(70, 66, 30, 50)
     + f'<circle cx="122" cy="80" r="16" fill="{GLASS}" stroke-width="2.6"/>'
     + f'<path d="M133,92 L150,108" stroke-width="5"/>'
     + f'<rect x="24" y="84" width="36" height="28" rx="4" fill="{WHITE}"/>'
     + f'<path d="M24,92 L60,92" stroke-width="1.4"/>'
     + f'<path d="M106,112 q-10,-12 -20,-4 q-8,6 -16,0" fill="none" stroke-width="2.2"/>'
     + f'<rect x="102" y="104" width="10" height="8" rx="2" fill="{WHITE}" stroke-width="1.6"/>'
     + sparkle(28, 36) + star(212, 30, 6))

# 4. 容量升級：手機頭上疊著幾塊積木，多出來的那幾塊淡淡的、往下掉
card('storage', '手繪手機頭上疊著代表容量的積木，多加的幾塊顏色變淡、往下掉',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + phone(40, 70, 44, 80)
     + f'<rect x="42" y="50" width="40" height="18" rx="4" fill="{GOLD}"/>'
     + f'<rect x="42" y="30" width="40" height="18" rx="4" fill="{GOLD}"/>'
     + f'<rect x="120" y="44" width="40" height="18" rx="4" fill="{PINK}" opacity=".9"/>'
     + f'<rect x="136" y="78" width="40" height="18" rx="4" fill="{PINK}" opacity=".6" transform="rotate(14 156 87)"/>'
     + f'<rect x="166" y="118" width="40" height="18" rx="4" fill="{PINK}" opacity=".35" transform="rotate(-10 186 127)"/>'
     + f'<path d="M100,40 Q118,36 120,44" fill="none" stroke-width="1.6" stroke-dasharray="3 4"/>'
     + f'<path d="M150,64 L152,74 M178,100 L182,112" stroke="{RED}" stroke-width="2.4"/>'
     + f'<path d="M146,72 L152,76 L156,70 M176,108 L182,114 L186,106" fill="none" stroke="{RED}" stroke-width="2.4"/>'
     + label(62, 64, '+', 14) + label(140, 58, '+', 14)
     + sparkle(212, 36) + star(24, 30, 6))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label_, inner):
    F[name] = svg('ic-' + name, 120, 120, label_, inner, bg='#fff3c4')


# 報價不等於成交：價格吊牌＋放大鏡＋問號
rem('r-quote', '手繪提醒：價格吊牌旁邊有放大鏡和問號',
    f'<path d="M20,40 L56,22 L84,50 L48,86 Z" fill="{WHITE}"/>'
    + f'<circle cx="54" cy="36" r="4" fill="{GOLD}"/>'
    + f'<path d="M54,36 Q40,14 22,20" fill="none" stroke-width="1.6"/>'
    + ''.join(f'<path d="M{40+i*6},{54+i*6} L{60+i*6},{40+i*6}" stroke-width="1.4"/>' for i in range(2))
    + f'<circle cx="82" cy="78" r="15" fill="#e6f2fa" stroke-width="2.4"/><path d="M93,89 L106,102" stroke-width="5"/>'
    + label(82, 84, '?', 18, RED))

# 月成本只算機身：手機殼、保固盾牌、訊號格都打上虛線框
rem('r-extras', '手繪提醒：只算手機本體，手機殼、保固盾牌和電信訊號是虛線，不在月成本裡',
    phone(10, 22, 36, 64) + check(28, 96, .7)
    + f'<path d="M50,62 L58,62" stroke-width="2.4"/>'
    + f'<rect x="60" y="22" width="20" height="34" rx="7" fill="none" stroke-dasharray="4 4"/>'
    + f'<path d="M98,24 L108,27 L108,40 Q108,49 98,54 Q88,49 88,40 L88,27 Z" fill="none" stroke-dasharray="4 4"/>'
    + ''.join(f'<rect x="{68+i*11}" y="{104-h}" width="7" height="{h}" rx="2" fill="none" stroke-dasharray="3 3" stroke-width="1.8"/>' for i, h in enumerate((10, 18, 26, 34)))
    + label(84, 74, '?', 14, RED))

# 日版賣的時候被扣：手機掛 J/A 吊牌，旁邊一個往下的箭頭
rem('r-jpver', '手繪提醒：掛著 J/A 吊牌的手機，旁邊有往下的箭頭',
    phone(22, 24, 40, 72)
    + f'<path d="M62,40 L74,50" stroke-width="1.6"/>'
    + f'<rect x="66" y="48" width="38" height="20" rx="5" fill="{GOLD}"/>'
    + label(85, 63, 'J/A', 12)
    + f'<path d="M86,76 L86,106 M76,96 L86,108 L96,96" fill="none" stroke="{RED}" stroke-width="4"/>')

print(save(F, OUT), 'files')
