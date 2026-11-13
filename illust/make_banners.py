# 全站每頁標題下的手繪封面（2026-11-13）。
# 使用者看過聖誕頁後說「新的頁面比較活潑可愛，全站都需要這樣」，
# 所以把每張主題貼紙（illust/st、illust/xmas）的圖案拿出來，放進一張寬版場景：
# 依主題選背景（天空、雪地、海、夜晚、暖色），兩側加雲、雪花、泡泡、燈串等手繪裝飾。
# 跑 `python3 illust/make_banners.py` 輸出 illust/banner/*.svg；gen.py 的 _sticker() 依網址挑一張。
import os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'banner')
W, H = 720, 210

THEME = {}
for n in 'lights teamlab ginzan nighttrain'.split():
    THEME[n] = 'night'
for n in 'skier snowman juhyo gassho penguin rotenburo'.split():
    THEME[n] = 'snow'
for n in 'whaleshark icebreaker'.split():
    THEME[n] = 'sea'
for n in 'plane plane-fuji seat rooftop harukas castle hakone fujicoaster ferris windmill tower skytree'.split():
    THEME[n] = 'sky'

BG = {'night': NAVY, 'snow': '#e4eefa', 'sea': '#d6edf8', 'sky': '#dff0fd', 'warm': '#fff0dc'}


def cloud(x, y, s=1.0):
    return (f'<path d="M{x},{y} q{-2*s},{-14*s} {12*s},{-14*s} q{4*s},{-12*s} {18*s},{-8*s} '
            f'q{12*s},{-8*s} {20*s},{6*s} q{12*s},{0} {10*s},{16*s} Z" fill="{WHITE}"/>')


def heart(x, y, s=1.0, col=PINK):
    return (f'<path d="M{x},{y+6*s} q{-10*s},{-8*s} {-6*s},{-13*s} q{4*s},{-4*s} {6*s},{1*s} '
            f'q{2*s},{-5*s} {6*s},{-1*s} q{4*s},{5*s} {-6*s},{13*s} Z" fill="{col}" stroke-width="1.6"/>')


def bunting(x1, y1, x2, y2, sag=20, n=10):
    # 三角旗彩帶（暖色背景用，不帶聖誕味）
    cols = [RED, GOLD, GREEN, PINK, SKY]
    my = max(y1, y2) + sag
    t = f'<path d="M{x1},{y1} Q{(x1+x2)/2},{my} {x2},{y2}" fill="none" stroke-width="1.6"/>'
    for i in range(n):
        u0, u1 = i / n, (i + .8) / n
        def pt(u):
            return ((1-u)**2*x1 + 2*(1-u)*u*(x1+x2)/2 + u*u*x2, (1-u)**2*y1 + 2*(1-u)*u*my + u*u*y2)
        ax, ay = pt(u0); bx, by = pt(u1)
        t += (f'<path d="M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f} L{(ax+bx)/2:.1f},{(ay+by)/2+15:.1f} Z" '
              f'fill="{cols[i % len(cols)]}" stroke-width="1.4"/>')
    return t


def fish(x, y, col=GOLD):
    return (f'<path d="M{x},{y} q12,-10 24,0 q-12,10 -24,0 Z" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+24},{y} l9,-7 l0,14 Z" fill="{col}" stroke-width="1.6"/>'
            f'<circle cx="{x+7}" cy="{y-1}" r="1.6" fill="{INK}" stroke="none"/>')


def scene(theme):
    t = f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="26" fill="{BG[theme]}"/>'
    if theme == 'night':
        t += snow([(60, 40), (130, 70), (200, 30), (520, 40), (600, 76), (670, 30), (90, 120), (640, 130)], 2.4)
        t += ''.join(sparkle(x, y) for x, y in [(170, 110), (560, 110), (40, 80)])
        t += f'<path d="M80,52 a20,20 0 1,0 24,28 a16,16 0 1,1 -24,-28 Z" fill="{GOLD}"/>'
        t += f'<path d="M3,178 Q180,160 360,172 T717,166 L717,184 Q717,207 694,207 L26,207 Q3,207 3,184 Z" fill="#283358"/>'
    elif theme == 'snow':
        t += snow([(50, 30), (120, 60), (190, 24), (540, 34), (610, 64), (680, 28), (80, 100), (650, 110), (240, 90), (480, 90)], 3, WHITE)
        t += f'<path d="M3,170 Q180,150 360,164 T717,156 L717,184 Q717,207 694,207 L26,207 Q3,207 3,184 Z" fill="{WHITE}"/>'
        t += tree(70, 176, 70, 50, smile=False) + tree(650, 176, 60, 44, smile=False)
    elif theme == 'sea':
        t += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke-width="1.6"/>'
                     for x, y, r in [(80, 50, 6), (96, 30, 4), (620, 60, 7), (640, 36, 4), (560, 110, 5)])
        t += fish(110, 120, GOLD) + fish(590, 140, PINK)
        t += f'<path d="M3,176 q30,-12 60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t54,0 L717,184 Q717,207 694,207 L26,207 Q3,207 3,184 Z" fill="#9fcfe9"/>'
    elif theme == 'sky':
        t += cloud(70, 70, 1.3) + cloud(560, 56, 1.1) + cloud(620, 128, .8) + cloud(150, 140, .7)
        t += ''.join(sparkle(x, y) for x, y in [(240, 40), (500, 100), (40, 120)])
        t += f'<path d="M3,180 Q160,160 330,176 T717,170 L717,184 Q717,207 694,207 L26,207 Q3,207 3,184 Z" fill="#cfe7c4"/>'
    else:  # warm
        t += bunting(20, 22, 360, 26, 22, 11) + bunting(360, 26, 700, 22, 22, 11)
        t += heart(90, 110, 1.2) + heart(620, 120, 1.0, GOLD)
        t += star(160, 150, 8) + star(560, 160, 7) + sparkle(60, 160) + sparkle(670, 76)
        t += snow([(120, 70), (600, 80), (40, 60), (680, 150)], 3, GOLD)
        t += f'<path d="M3,186 Q180,170 360,182 T717,178 L717,184 Q717,207 694,207 L26,207 Q3,207 3,184 Z" fill="#f6dcc0"/>'
    return t


def inner_of(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'<g filter="url\(#[^)]+\)"[^>]*>(.*)</g></svg>$', s, re.S)
    body = m.group(1)
    # 拿掉貼紙的米色圓角外框（第一個 x=3 y=3 的 rect），圖案本身留著
    body = re.sub(r'^<rect x="3" y="3"[^>]*/>', '', body, count=1)
    return body


FILES = {}
srcs = sorted(glob.glob(os.path.join(HERE, 'st', '*.svg'))) + \
    [os.path.join(HERE, 'xmas', n + '.svg') for n in ('tower', 'skytree', 'gift')]
for p in srcs:
    name = os.path.basename(p)[:-4]
    theme = THEME.get(name, 'warm')
    art = inner_of(p)
    cw, ch = 252, 210
    body = (scene(theme)
            + f'<svg x="{(W-cw)/2:.0f}" y="2" width="{cw}" height="{ch}" viewBox="0 0 180 150" overflow="visible">{art}</svg>')
    label = re.search(r'aria-label="([^"]*)"', open(p, encoding='utf-8').read())
    FILES[name] = svg('bn-' + name, W, H, (label.group(1) if label else ''), body, frame=False)

print(save(FILES, OUT), 'banners')
