# 流冰物語號頁的「沿途看得到什麼」插圖與提醒卡（2026-11-13）。
# 參考 JR 北海道流氷物語号頁（jrhokkaido.co.jp/travel/ryuhyo/）的車廂、停靠站與減速區間介紹畫成可愛版，不描照片構圖。
# 破冰船畫一般外型，不畫船公司標誌。
# 輸出 illust/sp/japan-ryuhyo-monogatari/*.svg（240×180）。說明文字放在 illust/spots/japan-ryuhyo-monogatari.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-ryuhyo-monogatari')
W, H = 240, 180
OCEAN = '#9fc3dc'
SKYW = '#e3eef7'
ICE = '#f7fbff'
TRAIN_G = '#3f8a73'
TRAIN_P = '#7a5a8e'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('rm-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def floes(pts):
    # 一片片的流冰（扁扁的白色多邊形）
    t = ''
    for x, y, w in pts:
        t += (f'<path d="M{x},{y} l{w*.45:.1f},{-w*.12:.1f} l{w*.5:.1f},{w*.05:.1f} l{-w*.1:.1f},{w*.18:.1f} '
              f'l{-w*.7:.1f},{w*.04:.1f} Z" fill="{ICE}" stroke-width="1.5"/>')
    return t


def car(x, y, w, col, front=None, s=1.0):
    # 一節柴油車廂（側面），front='l' / 'r' 畫圓弧車頭
    h = 34 * s
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{7*s}" fill="{col}"/>'
         f'<path d="M{x+3},{y+h*.68:.1f} L{x+w-3},{y+h*.68:.1f}" stroke="{GOLD}" stroke-width="2"/>')
    n = int((w - 16) // (14 * s))
    for i in range(n):
        wx = x + 8 + i * 14 * s
        t += f'<rect x="{wx:.1f}" y="{y+7*s:.1f}" width="{10*s:.1f}" height="{9*s:.1f}" rx="2" fill="{SKY}" stroke-width="1.3"/>'
    if front == 'r':
        t += (f'<rect x="{x+w-12*s:.1f}" y="{y+5*s:.1f}" width="{9*s:.1f}" height="{12*s:.1f}" rx="2" fill="{SKY}" stroke-width="1.3"/>'
              f'<circle cx="{x+w-6*s:.1f}" cy="{y+26*s:.1f}" r="{2.6*s:.1f}" fill="{GOLD}" stroke-width="1.2"/>')
    t += (f'<circle cx="{x+12*s:.1f}" cy="{y+h+3:.1f}" r="{5*s:.1f}" fill="{INK}"/>'
          f'<circle cx="{x+w-12*s:.1f}" cy="{y+h+3:.1f}" r="{5*s:.1f}" fill="{INK}"/>')
    return t


def person(x, y, col=RED, s=1.0, hat=None):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if hat:
        t += f'<path d="M{x-6.5*s},{y-1*s} q{6.5*s},{-11*s} {13*s},0 Z" fill="{hat}" stroke-width="1.4"/>'
    return t


# 1. 綠色＋紫色兩節車廂，沿著有流冰的海岸
card('train', '手繪綠色和紫色兩節車廂的觀光列車，沿著有流冰的海邊開',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,56 L237,56 L237,92 L3,92 Z" fill="{OCEAN}" stroke="none"/>'
     + floes([(12, 70, 30), (52, 80, 24), (92, 66, 36), (150, 76, 28), (190, 64, 34), (128, 86, 20)])
     + floor(96, WHITE)
     + f'<path d="M3,142 L237,142" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},142 L{x+6},150" stroke-width="1.6"/>' for x in range(10, 236, 16))
     + car(24, 100, 98, TRAIN_P) + car(124, 100, 98, TRAIN_G, 'r')
     + face(208, 124, .6)
     + flake(30, 24) + flake(120, 18, 4) + flake(208, 30) + star(70, 30, 5))

# 2. 濤沸川的橋附近放慢速度
card('slow', '手繪列車慢慢開過河上的橋，窗外是海',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,50 L237,50 L237,84 L3,84 Z" fill="{OCEAN}" stroke="none"/>'
     + floes([(20, 62, 26), (80, 70, 30), (140, 58, 24), (196, 68, 30)])
     + floor(88, WHITE)
     + f'<path d="M60,177 Q90,140 110,130 L150,130 Q170,140 190,177 Z" fill="{OCEAN}"/>'
     + f'<path d="M30,112 L210,112 L210,120 L30,120 Z" fill="{GRAY}"/>'
     + ''.join(f'<path d="M{x},120 L{x},146" stroke-width="3"/>' for x in (70, 120, 170))
     + car(56, 74, 90, TRAIN_G, 'r', .9)
     + face(132, 94, .55)
     + f'<path d="M166,84 q8,-4 16,0 q-8,4 -16,0 Z M178,96 q8,-4 16,0" fill="none" stroke-width="1.6"/>'
     + f'<path d="M20,98 q10,-6 20,0 M28,90 q8,-5 16,0" fill="none" stroke-width="1.6" opacity=".7"/>'
     + flake(30, 24) + flake(200, 22, 4) + sparkle(120, 26))

# 3. 北濱站：木造小站，月台就看得到海
card('kitahama', '手繪雪中的木造小車站，旁邊就是海',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M140,62 L237,62 L237,120 L140,120 Z" fill="{OCEAN}" stroke="none"/>'
     + floes([(150, 80, 24), (190, 92, 30), (176, 72, 20), (204, 106, 22)])
     + f'<rect x="28" y="74" width="104" height="62" rx="2" fill="{DBROWN}"/>'
     + ''.join(f'<path d="M32,{y} L128,{y}" stroke-width="1.2" opacity=".55"/>' for y in range(84, 136, 9))
     + f'<path d="M16,78 L44,46 L116,46 L144,78 Z" fill="#6c7a8c"/>'
     + f'<path d="M20,74 Q80,64 140,74" stroke="{WHITE}" stroke-width="5" fill="none"/>'
     + f'<path d="M46,48 Q80,40 114,48" stroke="{WHITE}" stroke-width="4" fill="none"/>'
     + f'<rect x="60" y="78" width="40" height="10" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
     + f'<rect x="36" y="94" width="20" height="18" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<rect x="104" y="94" width="20" height="18" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<rect x="68" y="98" width="24" height="38" rx="2" fill="{SKY}" stroke-width="1.4"/>'
     + face(80, 114, .6)
     + floor(136, WHITE)
     + person(170, 128, RED, .9, GOLD) + person(194, 132, GREEN, .8, PINK)
     + f'<path d="M176,124 l10,-10" stroke-width="1.6"/>'
     + flake(26, 28) + flake(130, 24, 4) + flake(214, 30) + star(180, 40, 5))

# 4. 濱小清水：車站旁邊的公路休息站
card('roadside', '手繪車站旁邊的公路休息站，有人提著購物袋',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<rect x="36" y="64" width="120" height="70" rx="3" fill="#f3e2c0"/>'
     + f'<path d="M26,68 L96,30 L166,68 Z" fill="{BRICK}"/>'
     + f'<path d="M32,66 Q96,56 160,66" stroke="{WHITE}" stroke-width="5" fill="none"/>'
     + f'<rect x="52" y="82" width="34" height="26" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<rect x="106" y="82" width="34" height="26" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<rect x="86" y="96" width="20" height="38" rx="2" fill="{SKY}" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{c}" stroke-width="1.2"/>' for x, y, c in [(60, 100, RED), (70, 98, GREEN), (78, 101, PINK), (114, 100, SKY), (124, 98, RED), (132, 101, GREEN)])
     + floor(134, WHITE)
     + person(186, 120, GREEN, 1.0, RED)
     + f'<path d="M196,136 L214,136 L212,156 L198,156 Z" fill="{PINK}"/><path d="M200,136 q5,-8 10,0" fill="none" stroke-width="1.6"/>'
     + f'<path d="M190,134 L198,140" stroke-width="1.8"/>'
     + flake(28, 26) + flake(200, 30) + star(214, 70, 5) + sparkle(110, 20))

# 5. 網走港的破冰船（一般外型，不畫標誌）
card('icebreaker', '手繪破冰船推開流冰往前開',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,104 L237,104 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{OCEAN}"/>'
     + f'<rect x="120" y="36" width="12" height="20" rx="2" fill="{GOLD}"/>'
     + f'<rect x="78" y="52" width="80" height="22" rx="4" fill="{WHITE}"/>'
     + f'<rect x="92" y="38" width="44" height="16" rx="3" fill="{WHITE}"/>'
     + ''.join(f'<rect x="{x}" y="58" width="9" height="8" rx="1.5" fill="{SKY}" stroke-width="1.3"/>' for x in (86, 100, 114, 128, 142))
     + ''.join(f'<rect x="{x}" y="42" width="8" height="7" rx="1.5" fill="{SKY}" stroke-width="1.3"/>' for x in (98, 110, 122))
     + f'<path d="M40,74 L196,74 L182,110 L62,110 Q48,96 40,74 Z" fill="{RED}"/>'
     + f'<path d="M46,84 L192,84" stroke="{WHITE}" stroke-width="3"/>'
     + face(70, 94, .7)
     + floes([(6, 112, 34), (190, 108, 38), (150, 126, 30), (40, 132, 36), (96, 140, 30), (180, 150, 30), (20, 156, 26)])
     + f'<path d="M30,98 L14,92 M32,104 L12,104" stroke-width="2" stroke="{WHITE}"/>'
     + flake(30, 30) + flake(206, 28) + star(180, 48, 5))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('rm-' + name, 120, 120, label, inner, bg='#fff3c4')


# 指定席券和乘車券是兩張
rem('r-tickets', '手繪提醒：座位票和車票是兩張不同的票',
    f'<g transform="rotate(-10 44 56)"><rect x="12" y="36" width="62" height="38" rx="4" fill="{SKY}"/>'
    f'<path d="M20,48 L64,48 M20,58 L52,58" stroke-width="2"/></g>'
    f'<g transform="rotate(8 78 78)"><rect x="46" y="60" width="62" height="38" rx="4" fill="{GOLD}"/>'
    f'<path d="M54,72 L98,72 M54,82 L84,82" stroke-width="2"/></g>'
    f'<path d="M58,24 L58,40 M50,32 L66,32" stroke="{RED}" stroke-width="4"/>')

# 停車時間：下車前先記發車時間
rem('r-clock', '手繪提醒：下車逛之前先看時鐘',
    f'<circle cx="60" cy="58" r="34" fill="{WHITE}"/>'
    f'<path d="M60,58 L60,36 M60,58 L76,66" stroke-width="3.4"/>'
    + ''.join(f'<circle cx="{60+28*__import__("math").cos(a*0.5236):.1f}" cy="{58+28*__import__("math").sin(a*0.5236):.1f}" r="2" fill="{INK}" stroke="none"/>' for a in range(12))
    + f'<rect x="20" y="96" width="80" height="12" rx="4" fill="{TRAIN_G}"/>'
    f'<rect x="28" y="98" width="10" height="6" rx="1" fill="{SKY}" stroke-width="1"/><rect x="44" y="98" width="10" height="6" rx="1" fill="{SKY}" stroke-width="1"/>')

print(save(F, OUT), 'files')
