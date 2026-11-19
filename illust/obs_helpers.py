# 觀景台城市頁插圖共用的小零件（仙台、廣島、沖繩用；名古屋那支腳本自己帶一份）。
import math
from kit import *

W, H = 240, 180
SKYB = '#cfe8f7'
DUSK = '#f7d9b8'
NIGHT = '#3d4a78'
SEA = '#9fd0ea'
MTN = '#9cc59a'
SNOWB = '#eef3f8'
BOX = '<rect x="3" y="3" width="234" height="174" rx="22" fill="{c}"/>'
GROUND = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def band(y, col, sw=1.6):
    # 從 y 到卡片底部的一塊地面或水面（下緣跟著卡片圓角）
    return f'<path d="M3,{y} L237,{y} {GROUND}" fill="{col}" stroke-width="{sw}"/>'


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def town(base, n=9, col='#e9e1d3', x0=14, step=24):
    t = ''
    for i in range(n):
        x = x0 + i * step
        h = 10 + (i * 7) % 14
        t += f'<rect x="{x}" y="{base-h}" width="18" height="{h}" fill="{col}" stroke-width="1.2"/>'
    return t


def wheel(cx, cy, r, n=12, hub=WHITE):
    t = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="2.2"/>'
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        t += (f'<path d="M{cx},{cy} L{x:.1f},{y:.1f}" stroke-width="1"/>'
              f'<rect x="{x-4:.1f}" y="{y-3:.1f}" width="8" height="7" rx="2" fill="{PINK if i % 2 else GOLD}" stroke-width="1"/>')
    return t + f'<circle cx="{cx}" cy="{cy}" r="{r*.18:.1f}" fill="{hub}" stroke-width="1.6"/>'


def castle(cx, base, s=1.0, wall=WHITE, roof='#5d6b7a', tiers=(26, 20, 14)):
    t = f'<path d="M{cx-34*s},{base} L{cx-28*s},{base-18*s} L{cx+28*s},{base-18*s} L{cx+34*s},{base} Z" fill="#c9c2b4" stroke-width="1.6"/>'
    y = base - 18 * s
    for w in tiers:
        h = 14 * s
        t += f'<rect x="{cx-w*s}" y="{y-h}" width="{2*w*s}" height="{h}" fill="{wall}" stroke-width="1.4"/>'
        t += f'<path d="M{cx-(w+8)*s},{y-h} L{cx-(w-4)*s},{y-h-8*s} L{cx+(w-4)*s},{y-h-8*s} L{cx+(w+8)*s},{y-h} Z" fill="{roof}" stroke-width="1.4"/>'
        y = y - h - 8 * s
    return t + f'<path d="M{cx-6*s},{y} L{cx+6*s},{y}" stroke="{GOLD}" stroke-width="3"/>'


def ropeway(x0, y0, x1, y1, col=RED, k=0.5):
    x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return (f'<path d="M{x0},{y0} L{x1},{y1}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} L{x},{y+8}" stroke-width="1.2"/><rect x="{x-10}" y="{y+8}" width="20" height="14" rx="3" fill="{col}" stroke-width="1.4"/>')


def islands(y, xs=((40, 30), (110, 22), (180, 34)), col=DGREEN):
    t = ''
    for x, w in xs:
        t += f'<path d="M{x-w},{y} Q{x},{y-w*0.9} {x+w},{y} Z" fill="{col}" stroke-width="1.4"/>'
        t += ''.join(f'<path d="M{x+dx},{y-w*0.5} l0,-10" stroke="{DBROWN}" stroke-width="2"/><circle cx="{x+dx}" cy="{y-w*0.5-12}" r="5" fill="{GREEN}" stroke-width="1"/>' for dx in (-6, 6))
    return t


def tower(cx, top, base, w=8, col=WHITE, cab=SKY):
    return (f'<path d="M{cx-w},{base} L{cx-w*0.6},{top} L{cx+w*0.6},{top} L{cx+w},{base} Z" fill="{col}" stroke-width="1.8"/>'
            f'<rect x="{cx-w*2}" y="{top-6}" width="{w*4}" height="12" rx="4" fill="{cab}" stroke-width="1.6"/>')


class Cards:
    def __init__(self, prefix):
        self.F, self.prefix = {}, prefix

    def card(self, name, label, inner, bg=CREAM):
        self.F[name] = svg(self.prefix + '-' + name, W, H, label, inner, bg=bg)

    def hero(self, label, body):
        self.F['hero'] = svg(self.prefix + '-hero', 720, 330, label, body)
