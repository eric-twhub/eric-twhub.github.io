# SHIBUYA SKY 頁的「上面有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網施設介紹（shibuya-scramble-square.com/sky/ 的「SHIBUYA SKYで出来ること」「空間構成」）
# 畫成可愛版，不描照片構圖；不畫商標。輸出 illust/sp/japan-shibuya-sky/*.svg，
# 說明文字在 illust/spots/japan-shibuya-sky.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-shibuya-sky')
W, H = 240, 180
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
TURF = '#9fd39a'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ss-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


# 1. SKY EDGE：屋頂的角落，往下看得到十字路口
zebra = ''.join(f'<path d="M{132+k*12},{160} L{128+k*12},{172}" stroke="{WHITE}" stroke-width="5"/>' for k in range(8))
zebra += ''.join(f'<path d="M{150+k*8},{150} L{196+k*6},{150}" stroke="none"/>' for k in range(0))
card('edge', '手繪站在高樓屋頂邊緣往下看的人，樓下是有斑馬線的十字路口',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(150, 40, .9) + cloud(196, 70, .6)
     + f'<path d="M108,150 L237,150 L237,155 Q237,177 215,177 L108,177 Z" fill="#b9bfc9"/>'
     + zebra
     + ''.join(f'<rect x="{x}" y="{150-h}" width="{w}" height="{h}" rx="2" fill="{c}" stroke-width="1.4"/>'
               for x, w, h, c in [(118, 14, 22, GRAY), (204, 14, 30, PINK), (220, 12, 18, GRAY)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{c}" stroke="none"/>' for x, y, c in [(150, 164, RED), (168, 168, NAVY), (186, 162, GOLD), (204, 170, GREEN)])
     + f'<path d="M24,74 L100,74 L100,177 L25,177 Q24,177 24,170 Z" fill="#c9cfdb"/>'
     + ''.join(f'<path d="M30,{y} L94,{y}" stroke-width="1.2" opacity=".45"/>' for y in range(86, 176, 10))
     + f'<rect x="96" y="50" width="8" height="24" rx="2" fill="#e6f4fb"/>'
     + back(56, 50, PINK, 1.0) + back(80, 52, SKY, .9)
     + f'<path d="M90,62 Q130,100 160,150" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="4 4"/>'
     + sparkle(40, 30, 4) + star(120, 24, 6))

# 2. 雲朵吊床：躺著看天空的休息區
card('hammock', '手繪屋頂草皮上的網狀吊床，有人躺著看雲',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 46, 1.0) + cloud(150, 36, 1.2) + cloud(96, 70, .6)
     + f'<path d="M3,120 Q120,108 237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}"/>'
     + f'<path d="M30,128 L30,104 M110,128 L110,104 M130,136 L130,112 M210,136 L210,112" stroke-width="3"/>'
     + f'<path d="M30,106 Q70,140 110,106" fill="{WHITE}" stroke-width="2.2"/>'
     + f'<path d="M130,114 Q170,148 210,114" fill="{WHITE}" stroke-width="2.2"/>'
     + ''.join(f'<path d="M{x},{y1} L{x+6},{y2}" stroke-width="1" opacity=".5"/>' for x, y1, y2 in [(44, 114, 124), (60, 120, 128), (76, 120, 128), (92, 114, 122), (144, 122, 132), (160, 128, 136), (176, 128, 136), (192, 122, 130)])
     + f'<circle cx="54" cy="112" r="7" fill="#f9d9c0"/>' + face(54, 112, .55)
     + f'<path d="M60,118 Q76,124 94,114" fill="none" stroke="{RED}" stroke-width="6"/>'
     + f'<circle cx="186" cy="120" r="7" fill="#f9d9c0"/>' + face(186, 120, .55)
     + f'<path d="M180,126 Q164,132 146,122" fill="none" stroke="{GOLD}" stroke-width="6"/>'
     + sparkle(210, 70, 4) + star(120, 22, 6))

# 3. 地理羅盤：屋頂最高點，站在中間看四面八方
dirs = ''
import math
for k in range(16):
    a = k * math.pi / 8
    r1, r2 = (8, 64) if k % 4 == 0 else (8, 46)
    dirs += (f'<path d="M{120+r1*math.cos(a):.1f},{132+r1*math.sin(a)*.32:.1f} '
             f'L{120+r2*math.cos(a):.1f},{132+r2*math.sin(a)*.32:.1f}" stroke-width="{1.8 if k % 4 == 0 else 1}"/>')
card('compass', '手繪屋頂上畫在地面的大圓形羅盤，小人站在正中間',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(22, 50, .9) + cloud(170, 44, 1.0)
     + f'<path d="M3,110 L237,110 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#d9cdb8"/>'
     + f'<ellipse cx="120" cy="132" rx="80" ry="26" fill="{WHITE}"/>'
     + f'<ellipse cx="120" cy="132" rx="62" ry="20" fill="none" stroke-width="1.4"/>'
     + dirs
     + f'<path d="M120,132 L190,132" stroke="{RED}" stroke-width="2.4"/>'
     + kid(120, 100, GREEN, 1.1)
     + f'<path d="M104,88 l-8,-6 M136,88 l8,-6" stroke-width="1.6"/>'
     + sparkle(60, 86, 4) + sparkle(184, 84, 4) + star(120, 26, 6))

# 4. 光柱：每天晚上 7 點起每個整點和半點
beams = ''.join(f'<path d="M{x},{142} L{x+dx-10},{8} L{x+dx+10},{8} Z" fill="#fff3b0" opacity=".8" stroke="none"/>'
                for x, dx in [(40, -16), (80, -6), (120, 0), (160, 6), (200, 16)])
card('lights', '手繪夜晚屋頂往天空打出好幾道光柱',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + beams
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{WHITE}" stroke="none"/>' for x, y in [(22, 30), (60, 60), (100, 24), (140, 50), (190, 30), (220, 64)])
     + f'<path d="M3,142 L237,142 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#4a557f"/>'
     + ''.join(f'<ellipse cx="{x}" cy="142" rx="8" ry="3" fill="{GOLD}"/>' for x in (40, 80, 120, 160, 200))
     + back(60, 148, PINK, .8) + back(178, 148, GOLD, .8)
     + star(212, 24, 5), bg=NIGHT)

# 5. SKY GATE：天花板有影像的電梯
card('elevator', '手繪電梯裡的人抬頭看天花板的星空影像',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6e1f5"/>'
     + f'<path d="M40,16 L200,16 L176,58 L64,58 Z" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="none"/>' for x, y, r, c in [(80, 30, 2, WHITE), (110, 24, 2.4, GOLD), (140, 36, 2, WHITE), (168, 26, 2, '#8ff0ff'), (96, 46, 1.6, GOLD), (150, 48, 1.8, WHITE)])
     + f'<path d="M64,58 L64,160 M176,58 L176,160" stroke-width="2.4"/>'
     + f'<path d="M40,16 L40,170 M200,16 L200,170" stroke-width="1.4" opacity=".5"/>'
     + f'<path d="M64,58 L40,16 M176,58 L200,16" stroke-width="2"/>'
     + f'<path d="M64,160 L176,160" stroke-width="2"/>'
     + kid(96, 112, RED, 1.15) + kid(142, 116, SKY, 1.05)
     + f'<path d="M96,92 l0,-10 M90,94 l-4,-8 M142,96 l0,-10 M148,98 l4,-8" stroke-width="1.4"/>'
     + ''.join(f'<path d="M{x},{y} q4,-4 8,0" fill="none" stroke-width="1.6"/>' for x, y in [(206, 80), (212, 100), (22, 90), (28, 110)])
     + sparkle(120, 72, 4))

# 6. 46 樓室內迴廊：屋頂關閉時照常開放
card('gallery', '手繪下雨天的室內展望迴廊，玻璃窗外在下雨，裡面的人在看風景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e9e4f2"/>'
     + f'<rect x="16" y="16" width="208" height="104" rx="8" fill="#b9c7d8"/>'
     + ''.join(f'<rect x="{x}" y="{120-h}" width="{w}" height="{h}" rx="2" fill="#9fb0c4" stroke-width="1.4"/>'
               for x, w, h in [(22, 14, 26), (40, 12, 40), (54, 20, 20), (120, 12, 34), (134, 18, 22), (156, 12, 44), (172, 22, 18), (198, 18, 30)])
     + cloud(40, 40, 1.0, '#dfe5ee') + cloud(140, 36, 1.2, '#dfe5ee')
     + ''.join(f'<path d="M{x},{y} l-4,10" stroke="#5b86c5" stroke-width="2"/>' for x, y in [(36, 52), (64, 66), (90, 50), (118, 62), (150, 54), (178, 68), (204, 50), (76, 88), (132, 84), (196, 86)])
     + f'<path d="M86,16 L86,120 M156,16 L156,120" stroke-width="3"/>'
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#d9cdb8"/>'
     + back(70, 126, PINK, 1.1) + kid(170, 124, GOLD, 1.0)
     + sparkle(120, 140, 4))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ss-' + name, 120, 120, label, inner, bg='#fff3c4')


# 時段是到 14 樓入口的時間
rem('r-14f', '手繪提醒：時鐘和 14 樓的入口',
    f'<circle cx="40" cy="44" r="24" fill="{WHITE}"/><path d="M40,44 L40,28 M40,44 L52,50" stroke-width="2.6"/>'
    + f'<rect x="66" y="40" width="40" height="64" rx="4" fill="{GRAY}"/>'
    + f'<rect x="70" y="46" width="32" height="18" rx="2" fill="{GOLD}"/>'
    + f'<text x="86" y="60" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">14F</text>'
    + f'<rect x="78" y="84" width="16" height="20" rx="2" fill="{WHITE}"/>'
    + f'<path d="M30,92 L58,92 M50,84 L58,92 L50,100" fill="none" stroke="{RED}" stroke-width="3.4"/>')

# 帽子和耳機也要寄放
rem('r-locker', '手繪提醒：置物櫃裡放著帽子和耳機',
    f'<rect x="14" y="18" width="92" height="88" rx="4" fill="{GRAY}"/>'
    + f'<path d="M60,18 L60,106 M14,62 L106,62" stroke-width="2"/>'
    + f'<path d="M22,52 q0,-20 16,-20 q16,0 16,20 Z" fill="{RED}"/><path d="M18,52 L58,52" stroke-width="3"/>'
    + f'<path d="M70,52 q0,-22 14,-22 q14,0 14,22" fill="none" stroke-width="3"/>'
    + f'<rect x="66" y="46" width="8" height="12" rx="3" fill="{NAVY}"/><rect x="94" y="46" width="8" height="12" rx="3" fill="{NAVY}"/>'
    + f'<rect x="24" y="72" width="26" height="24" rx="4" fill="{GOLD}"/><path d="M30,72 q7,-8 14,0" fill="none" stroke-width="2"/>'
    + f'<circle cx="84" cy="84" r="5" fill="{WHITE}"/>')

print(save(F, OUT), 'files')
