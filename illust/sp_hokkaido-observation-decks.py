# 北海道觀景台懶人包（/hokkaido/observation-decks/）與札幌觀景台頁的手繪插圖（2026-11-18）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。
# 輸出 illust/sp/kyushu-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'hokkaido-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
TURF = '#9fd08a'
SEA = '#9fd0ea'
F = {}
BOX = '<rect x="3" y="3" width="234" height="174" rx="22" fill="{c}"/>'
FLOOR = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('hk-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def bldg(x, base, w, h, col=GRAY):
    t = f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{col}" stroke-width="1.6"/>'
    if w >= 14:
        for yy in range(int(base - h + 8), int(base - 6), 12):
            t += f'<path d="M{x+4},{yy} L{x+w-4},{yy}" stroke-width="1" opacity=".45"/>'
    return t


def stars(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in pts)


def citylights(y0, y1, step=10):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{GOLD}" stroke="none"/>'
                   for x in range(14, 230, step) for y in (y0, y1) if (x + y) % 3)


def window(inner_bg, inner, people):
    # 室內展望大廳：窗框、地板、背對的人
    return (BOX.format(c=inner_bg) + inner
            + ''.join(f'<path d="M{x},3 L{x},128" stroke-width="3"/>' for x in (80, 160))
            + f'<path d="M3,128 L237,128 {FLOOR}" fill="#e9dcc8"/><path d="M3,128 L237,128" stroke-width="2.4"/>'
            + people)


def fktower(cx, base, h, s=1.0):
    # 福岡塔：細長三角柱，玻璃帷幕，上面展望室
    top = base - h
    t = (f'<path d="M{cx-9*s},{base} L{cx-5*s},{top+12*s} L{cx+5*s},{top+12*s} L{cx+9*s},{base} Z" fill="#a9c7e3" stroke-width="1.8"/>'
         + ''.join(f'<path d="M{cx-8*s},{y} L{cx+8*s},{y}" stroke="{WHITE}" stroke-width="1" opacity=".8"/>' for y in [base - h * k / 9 for k in range(1, 8)])
         + f'<rect x="{cx-8*s}" y="{top+14*s}" width="{16*s}" height="{8*s}" rx="{2*s}" fill="{WHITE}" stroke-width="1.4"/>'
         + f'<path d="M{cx},{top+12*s} L{cx},{top}" stroke-width="2"/>')
    return t


def castle(cx, base, s=1.0, wall=WHITE, roof='#3d3d4a', stone='#b9a68c'):
    t = (f'<path d="M{cx-60*s},{base} L{cx-48*s},{base-36*s} L{cx+48*s},{base-36*s} L{cx+60*s},{base} Z" fill="{stone}" stroke-width="1.8"/>'
         + ''.join(f'<path d="M{cx-(50-i*2)*s},{base-28*s+i*8*s} L{cx+(50-i*2)*s},{base-28*s+i*8*s}" stroke-width="1" opacity=".5"/>' for i in range(3)))
    for w, y in ((70, 52), (54, 70), (40, 88), (26, 104)):
        t += (f'<rect x="{cx-w*s/2}" y="{base-y*s}" width="{w*s}" height="{16*s}" fill="{wall}" stroke-width="1.6"/>'
              f'<path d="M{cx-w*s/2-8*s},{base-y*s} Q{cx},{base-y*s-10*s} {cx+w*s/2+8*s},{base-y*s} Z" fill="{roof}" stroke-width="1.6"/>')
    return t


def gondola(x, y, col=RED):
    return (f'<path d="M{x},{y-14} L{x},{y}" stroke-width="1.4"/>'
            f'<rect x="{x-14}" y="{y}" width="28" height="20" rx="4" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x-10}" y="{y+4}" width="20" height="8" rx="2" fill="{SKY}" stroke-width="1.2"/>')


def volcano(cx, base, s=1.0, smoke=True):
    t = (f'<path d="M{cx-70*s},{base} Q{cx-30*s},{base-50*s} {cx-12*s},{base-62*s} L{cx+10*s},{base-64*s} '
         f'Q{cx+34*s},{base-48*s} {cx+74*s},{base} Z" fill="#8f8aa8" stroke-width="1.8"/>'
         f'<path d="M{cx-40*s},{base-30*s} Q{cx},{base-44*s} {cx+44*s},{base-28*s}" fill="none" stroke-width="1" opacity=".5"/>')
    if smoke:
        t += cloud(cx - 6 * s, base - 70 * s, .7 * s, '#eeeeee') + cloud(cx + 8 * s, base - 88 * s, .55 * s, '#f5f5f5')
    return t


def sea(y, col=SEA):
    return f'<path d="M3,{y} L237,{y} {FLOOR}" fill="{col}"/>'


def ship(x, y):
    return (f'<path d="M{x},{y} L{x+40},{y} L{x+34},{y+10} L{x+6},{y+10} Z" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x+14}" y="{y-10}" width="14" height="10" rx="2" fill="{SKY}" stroke-width="1.2"/>')



SNOW = '#f4f7fb'
WINTER = '#dbe9f5'


def snowground(y, col=SNOW):
    return f'<path d="M3,{y} Q60,{y-6} 120,{y} T237,{y-4} {FLOOR}" fill="{col}"/><path d="M3,{y} Q60,{y-6} 120,{y} T237,{y-4}" fill="none" stroke-width="2"/>'


def snowmtn(x0, x1, base, peak, col='#c9d6e6'):
    m = (x0 + x1) / 2
    return (f'<path d="M{x0},{base} L{m},{peak} L{x1},{base} Z" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{m-(m-x0)*.3},{peak+(base-peak)*.3} L{m},{peak} L{m+(x1-m)*.3},{peak+(base-peak)*.3} '
            f'q{-(x1-m)*.15},6 {-(x1-m)*.3},0 q{-(m-x0)*.15},6 {-(m-x0)*.3},0 Z" fill="{WHITE}" stroke-width="1.2"/>')


def flakes(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{WHITE}" stroke="none"/>' for x, y in pts)


def tvtower(cx, base, s=1.0):
    t = (f'<path d="M{cx-22*s},{base} L{cx-7*s},{base-90*s} L{cx+7*s},{base-90*s} L{cx+22*s},{base} Z" fill="none" stroke="{RED}" stroke-width="2.4"/>'
         + ''.join(f'<path d="M{cx-22*s+k*1.6*s},{base-k*10*s} L{cx+22*s-k*1.6*s},{base-k*10*s}" stroke="{RED}" stroke-width="1.6"/>' for k in range(1, 9))
         + f'<rect x="{cx-12*s}" y="{base-104*s}" width="{24*s}" height="{14*s}" rx="{2*s}" fill="{WHITE}" stroke-width="1.6"/>'
         + f'<circle cx="{cx}" cy="{base-62*s}" r="{7*s}" fill="{WHITE}" stroke-width="1.4"/>'
         + f'<path d="M{cx},{base-62*s} L{cx},{base-66*s} M{cx},{base-62*s} L{cx+3*s},{base-62*s}" stroke-width="1"/>'
         + f'<path d="M{cx},{base-104*s} L{cx},{base-130*s}" stroke="{RED}" stroke-width="2"/>')
    return t


def wheel(cx, cy, r, col=PINK):
    t = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="2"/>'
    for i in range(12):
        a = math.pi * 2 * i / 12
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        t += f'<path d="M{cx},{cy} L{x:.1f},{y:.1f}" stroke-width="1"/><rect x="{x-4:.1f}" y="{y-3:.1f}" width="8" height="7" rx="2" fill="{col if i % 2 else GOLD}" stroke-width="1"/>'
    return t + f'<circle cx="{cx}" cy="{cy}" r="4" fill="{WHITE}" stroke-width="1.4"/>'


def star5(cx, cy, r, col='#cfe3c0'):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * .55
        pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a)*.55:.1f}')
    return f'<path d="M{" L".join(pts)} Z" fill="{col}" stroke-width="1.6"/>'


def pine(x, base, h=24, col=DGREEN, snow=True):
    t = f'<path d="M{x},{base-h} L{x+h*.4},{base} L{x-h*.4},{base} Z" fill="{col}" stroke-width="1.2"/>'
    if snow:
        t += f'<path d="M{x},{base-h} L{x+h*.15},{base-h*.62} L{x-h*.15},{base-h*.62} Z" fill="{WHITE}" stroke-width="1"/>'
    return t


def ropeline(x0, y0, x1, y1, gx, col=RED):
    gy = y0 + (y1 - y0) * (gx - x0) / (x1 - x0)
    return f'<path d="M{x0},{y0} L{x1},{y1}" stroke-width="1.4"/>' + gondola(gx, gy + 14, col)


# 0. 封面
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{WINTER}"/>'
         + f'<path d="M3,150 Q3,3 25,3 L695,3 Q717,3 717,25 L717,150 Z" fill="#c9dcef" stroke="none"/>'
         + cloud(80, 60, 1.2) + cloud(560, 50, 1.0)
         + snowmtn(470, 717, 262, 90) + snowmtn(380, 560, 262, 140, '#d4dfec')
         + f'<path d="M20,90 L250,200" stroke-width="1.4"/>' + gondola(130, 156, RED)
         + tvtower(300, 262, 1.25)
         + bldg(350, 262, 30, 150, '#c7c2dc') + bldg(384, 262, 24, 90)
         + wheel(470, 196, 46, PINK)
         + pine(40, 262, 40) + pine(70, 262, 30) + pine(660, 262, 36)
         + f'<path d="M3,262 L717,262 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="{SNOW}"/>'
         + f'<path d="M3,262 L717,262" stroke-width="2.4"/>'
         + f'<rect x="60" y="270" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(200, 232, RED, 1.6) + back(380, 236, SKY, 1.5) + back(560, 232, GOLD, 1.6)
         + flakes([(120, 40), (220, 110), (330, 60), (420, 30), (600, 130), (690, 80), (40, 180)]))
F['hero'] = svg('hk-hero', 720, 330, '手繪插圖：下雪的北海道，有紅色鐵塔、摩天輪、雪山和纜車，三個人站在窗邊看景色', _hero)

# 付費
card('t38', '手繪車站上方高樓的展望室，窗外是覆雪的城市和遠方的山',
     window(WINTER, snowmtn(150, 237, 80, 34) + ''.join(bldg(x, 112, w, h, '#d6dbe6') for x, w, h in ((10, 16, 30), (30, 12, 20), (50, 18, 38), (80, 14, 24), (120, 16, 30)))
            + flakes([(40, 30), (90, 50), (200, 20)]),
            back(80, 120, RED, 1.0) + back(160, 122, SKY, .95)))
card('tvtower', '手繪紅色鐵塔，中間有一個時鐘，前面是覆雪的長條形公園',
     BOX.format(c=WINTER) + cloud(30, 40, .8) + cloud(190, 30, .7)
     + tvtower(120, 150, 1.0)
     + snowground(150)
     + ''.join(pine(x, 152, 18) for x in (30, 56, 184, 210))
     + kid(80, 136, PINK, .8) + flakes([(40, 70), (200, 80), (170, 30)]))
card('moiwa', '手繪纜車往雪山山頂開，山下是一片閃亮的城市夜景',
     BOX.format(c=NIGHT) + stars([(30, 24, WHITE), (200, 20, GOLD)])
     + f'<path d="M3,120 Q120,138 237,118 L237,160 L3,160 Z" fill="#3f4a78" stroke-width="1.4"/>' + citylights(134, 148, 9)
     + f'<path d="M3,120 Q40,100 80,90 Q140,30 237,100 L237,120 L3,120 Z" fill="#c9d6e6" stroke-width="1.6"/>'
     + ropeline(30, 110, 200, 46, 120, GOLD)
     + back(196, 40, PINK, .55) + star(60, 50, 5), bg=NIGHT)
card('hitsuji', '手繪一大片雪原的山丘，遠方是城市，有人站在展望台上',
     BOX.format(c=WINTER) + cloud(40, 36, .8)
     + ''.join(bldg(x, 100, w, h, '#d6dbe6') for x, w, h in ((150, 12, 18), (166, 14, 26), (184, 10, 14), (198, 16, 22)))
     + f'<path d="M3,100 Q120,80 237,100 L237,177 L3,177 Z" fill="{SNOW}" stroke-width="1.6"/>'
     + f'<path d="M3,130 Q80,110 237,128" fill="none" stroke-width="1" opacity=".5"/>'
     + f'<rect x="40" y="132" width="80" height="8" fill="{BROWN}" stroke-width="1.4"/>'
     + back(60, 112, RED, .9) + back(96, 114, GOLD, .9) + pine(200, 150, 26) + flakes([(30, 70), (120, 40), (210, 60)]))
card('noria', '手繪大樓屋頂上的摩天輪，下面是霓虹燈的鬧區夜景',
     BOX.format(c=NIGHT) + stars([(24, 24, WHITE), (210, 30, GOLD)])
     + bldg(70, 160, 100, 70, '#4a5488')
     + wheel(120, 62, 40, PINK)
     + f'<path d="M108,90 L104,102 M132,90 L136,102" stroke-width="2"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="10" height="6" rx="1" fill="{c}" stroke="none"/>' for x, y, c in ((78, 112, PINK), (100, 124, GOLD), (140, 116, SKY), (152, 136, PINK), (86, 140, GOLD)))
     + bldg(10, 160, 40, 60, '#3d466f') + bldg(186, 160, 44, 50, '#3d466f')
     + f'<path d="M3,160 L237,160 {FLOOR}" fill="#2a3152"/>', bg=NIGHT)
card('dome', '手繪銀色圓頂的大型體育館，屋頂上有一個小小的展望台，後面是雪山',
     BOX.format(c=WINTER) + cloud(40, 34, .8)
     + snowmtn(120, 237, 110, 50)
     + f'<path d="M20,150 Q120,60 220,150 Z" fill="#d6dbe6" stroke-width="2"/>'
     + ''.join(f'<path d="M{20+i*25},150 Q120,{60+i*3} {120+i*12},{70+i*2}" fill="none" stroke-width="1" opacity=".4"/>' for i in range(4))
     + f'<rect x="104" y="80" width="32" height="12" rx="3" fill="{SKY}" stroke-width="1.6"/>'
     + back(114, 74, GOLD, .45) + back(126, 74, PINK, .45)
     + snowground(150))
card('goryokaku', '手繪從高塔往下看，雪地裡有一座星形的城郭，周圍是護城河',
     BOX.format(c=WINTER)
     + f'<ellipse cx="120" cy="110" rx="100" ry="46" fill="{SEA}" stroke-width="1.6"/>'
     + star5(120, 110, 86, SNOW)
     + ''.join(pine(x, y, 12) for x, y in ((100, 110), (130, 104), (118, 124)))
     + ''.join(bldg(x, 60, w, h, '#d6dbe6') for x, w, h in ((14, 14, 22), (34, 12, 16), (190, 16, 24), (210, 12, 18)))
     + f'<rect x="3" y="150" width="234" height="27" fill="#e9dcc8" stroke="none"/>'
     + f'<path d="M3,150 L237,150" stroke-width="2.4"/>' + back(60, 132, RED, .9) + back(180, 132, SKY, .9))
card('hakodateyama', '手繪山頂往下看，兩邊是海、中間細腰的港口城市夜景',
     BOX.format(c=NIGHT) + stars([(30, 24, WHITE), (120, 18, GOLD), (210, 28, WHITE)])
     + f'<path d="M3,60 L237,60 L237,150 L3,150 Z" fill="#2a3a66" stroke="none"/>'
     + f'<path d="M40,60 Q100,90 110,120 Q120,150 130,150 Q140,120 150,100 Q170,70 237,62 L237,60 L40,60 Z" fill="#3f4a78" stroke-width="1.2"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{GOLD}" stroke="none"/>' for x, y in ((70, 70), (90, 80), (100, 96), (110, 110), (118, 126), (128, 140), (140, 116), (150, 96), (170, 80), (190, 70), (210, 66), (60, 66), (130, 104), (160, 88), (120, 92)))
     + f'<path d="M3,150 Q120,134 237,152 {FLOOR}" fill="#22284a"/>'
     + back(100, 142, PINK, .9) + back(136, 144, GOLD, .9), bg=NIGHT)
card('tengu', '手繪纜車開上雪山，山下是港口城市和海',
     BOX.format(c=WINTER) + cloud(190, 30, .7)
     + f'<path d="M3,120 L237,120 L237,140 L3,140 Z" fill="{SEA}" stroke-width="1.2"/>'
     + ''.join(bldg(x, 120, w, h, '#d6dbe6') for x, w, h in ((120, 12, 14), (136, 14, 20), (156, 10, 12), (170, 16, 18)))
     + f'<path d="M3,140 L3,60 Q60,40 110,130 L110,140 Z" fill="{SNOW}" stroke-width="1.6"/>'
     + ''.join(pine(x, y, 16) for x, y in ((30, 74), (54, 88), (80, 112)))
     + ropeline(40, 50, 120, 136, 80, RED)
     + snowground(150) + kid(190, 136, PINK, .8))
card('usuzan', '手繪纜車開往冒著白煙的火山，旁邊是湖和湖中的小島',
     BOX.format(c=SKYB) + cloud(40, 30, .8)
     + f'<path d="M3,120 L237,120 L237,140 L3,140 Z" fill="{SEA}" stroke-width="1.2"/>' + f'<ellipse cx="60" cy="128" rx="20" ry="5" fill="{GREEN}" stroke-width="1.2"/>'
     + volcano(170, 120, .9)
     + ropeline(100, 136, 180, 70, 140, RED)
     + snowground(150) + back(40, 140, SKY, .9))
card('asahidake', '手繪雪白的高山和冒出的白色噴氣，纜車往山腰開',
     BOX.format(c=SKYB)
     + snowmtn(30, 230, 150, 30, '#d4dfec')
     + cloud(150, 60, .5, '#f5f5f5') + cloud(160, 46, .4, '#f5f5f5')
     + ropeline(10, 160, 120, 90, 60, RED)
     + snowground(156) + pine(200, 160, 20) + pine(220, 160, 16))
card('kurodake', '手繪峽谷中的雪山，纜車開到山腰車站，屋頂有人看景',
     BOX.format(c=SKYB) + cloud(40, 30, .7)
     + snowmtn(60, 237, 150, 26, '#c9d6e6') + snowmtn(3, 120, 150, 70, '#d4dfec')
     + f'<rect x="150" y="76" width="34" height="20" fill="{WHITE}" stroke-width="1.6"/>'
     + back(160, 70, PINK, .5) + back(174, 70, GOLD, .5)
     + ropeline(20, 160, 160, 90, 90, RED)
     + snowground(158))
card('otower', '手繪海上的塔，周圍漂著白色的流冰，塔下有海中觀察窗',
     BOX.format(c=WINTER) + cloud(40, 34, .8)
     + f'<path d="M3,96 L237,96 L237,177 L25,177 Q3,177 3,155 Z" fill="#7fb3d5" stroke="none"/>'
     + f'<rect x="100" y="30" width="44" height="26" rx="4" fill="{WHITE}" stroke-width="1.8"/><rect x="108" y="56" width="28" height="90" fill="#e8e2d4" stroke-width="1.8"/>'
     + ''.join(f'<circle cx="122" cy="{y}" r="5" fill="{SKY}" stroke-width="1.2"/>' for y in (118, 134))
     + ''.join(f'<path d="M{x},{y} l14,-3 l10,3 l-6,5 l-16,0 Z" fill="{WHITE}" stroke-width="1.2"/>' for x, y in ((20, 104), (50, 112), (170, 108), (196, 118), (30, 130)))
     + back(116, 32, RED, .5) + back(130, 32, SKY, .5))
card('kushiro', '手繪展望台建築前面一大片濕原，河流彎彎曲曲，遠方有山',
     BOX.format(c=WINTER) + cloud(190, 30, .7)
     + snowmtn(120, 237, 70, 34, '#c9d6e6')
     + f'<path d="M3,70 L237,70 L237,150 L3,150 Z" fill="#c8c6a0" stroke="none"/>'
     + f'<path d="M3,100 Q60,80 90,110 T170,96 T237,110" fill="none" stroke="{SEA}" stroke-width="5"/>'
     + f'<rect x="20" y="104" width="60" height="40" rx="6" fill="#b48a64" stroke-width="1.6"/><rect x="30" y="94" width="40" height="12" rx="4" fill="{SKY}" stroke-width="1.4"/>'
     + snowground(150) + back(140, 140, GOLD, .9))

# 不用門票
card('asahiyama', '手繪公園的展望台，往下看雪後的城市和遠方的海',
     BOX.format(c=WINTER) + cloud(40, 30, .8)
     + f'<path d="M3,70 L237,70 L237,80 L3,80 Z" fill="{SEA}" stroke-width="1.2"/>'
     + ''.join(bldg(x, 112, w, h, '#d6dbe6') for x, w, h in ((14, 14, 24), (32, 10, 16), (50, 16, 30), (140, 12, 20), (160, 18, 32), (190, 12, 22), (208, 16, 18)))
     + f'<path d="M3,130 Q120,110 237,132 {FLOOR}" fill="{SNOW}"/><path d="M3,130 Q120,110 237,132" fill="none" stroke-width="2"/>'
     + f'<rect x="80" y="116" width="80" height="8" fill="{BROWN}" stroke-width="1.4"/>'
     + back(100, 112, PINK, .9) + back(136, 112, SKY, .9) + pine(20, 160, 24) + pine(220, 160, 22))
card('moerenuma', '手繪雪原上一座圓圓的人工小山，有人坐雪橇滑下來',
     BOX.format(c=WINTER) + cloud(60, 34, .9) + cloud(190, 40, .7)
     + f'<path d="M20,150 Q120,40 220,150 Z" fill="{SNOW}" stroke-width="1.8"/>'
     + ''.join(f'<path d="M{70+i*10},{150-i*0} Q120,{60+i*12} {170-i*10},150" fill="none" stroke-width="1" opacity=".35"/>' for i in range(3))
     + f'<path d="M150,108 l18,6 l-2,4 l-18,-6 Z" fill="{RED}" stroke-width="1.2"/>' + kid(160, 96, GOLD, .6)
     + back(120, 58, PINK, .55) + snowground(152))
card('motomachi', '手繪坡上的公園和洋館，往下看港口和海',
     BOX.format(c=SKYB) + cloud(190, 30, .7)
     + f'<path d="M3,90 L237,90 L237,120 L3,120 Z" fill="{SEA}" stroke-width="1.2"/>' + ship(150, 98)
     + f'<path d="M3,177 L3,110 Q120,130 237,150 L237,177 Z" fill="{SNOW}" stroke-width="1.8"/>'
     + f'<rect x="30" y="80" width="50" height="34" fill="#f2e6c9" stroke-width="1.6"/><path d="M24,80 L55,62 L86,80 Z" fill="#7aa0c4" stroke-width="1.6"/>'
     + ''.join(f'<rect x="{x}" y="90" width="8" height="12" fill="{SKY}" stroke-width="1"/>' for x in (38, 52, 66))
     + back(150, 140, RED, .9) + pine(200, 160, 22))
card('silo', '手繪紅色屋頂的圓筒形穀倉，前面是湖和湖中的島，遠方有冒煙的山',
     BOX.format(c=SKYB) + cloud(40, 30, .8)
     + volcano(190, 96, .6)
     + f'<path d="M3,96 L237,96 L237,126 L3,126 Z" fill="{SEA}" stroke-width="1.2"/>' + f'<ellipse cx="110" cy="110" rx="26" ry="7" fill="{GREEN}" stroke-width="1.2"/>'
     + f'<rect x="30" y="80" width="28" height="70" fill="#e8e2d4" stroke-width="1.6"/><path d="M28,80 Q44,62 60,80 Z" fill="{RED}" stroke-width="1.6"/>'
     + snowground(150) + back(150, 140, GOLD, .9))
card('tomakomai', '手繪市政府高樓的展望迴廊，窗外是港口的大船和飛過的飛機',
     window(SKYB, f'<path d="M3,90 L237,90 L237,120 L3,120 Z" fill="{SEA}" stroke-width="1.2"/>' + ship(60, 96) + ship(150, 102)
            + f'<path d="M170,40 l26,-6 l4,3 l-26,8 Z M184,36 l-6,-8 l4,0 l8,7" fill="{WHITE}" stroke-width="1.2"/>' + snowmtn(3, 90, 90, 56),
            back(110, 120, GOLD, 1.0)))
card('asahikawa', '手繪市政府新大樓高樓層的休息區，窗外是雪中的城市和遠方的山',
     window(WINTER, snowmtn(100, 237, 92, 44) + ''.join(bldg(x, 112, w, h, '#d6dbe6') for x, w, h in ((14, 14, 20), (34, 12, 28), (56, 16, 16), (150, 14, 22), (176, 18, 18)))
            + flakes([(40, 30), (120, 40), (210, 24)]),
            back(110, 120, SKY, 1.0) + kid(160, 120, PINK, .85)))
card('obihiro', '手繪辦公大樓高樓層的展望大廳，窗外是平坦的城市和遠方的山脈',
     window(SKYB, snowmtn(3, 120, 84, 52, '#c9d6e6') + snowmtn(100, 237, 84, 46, '#d4dfec')
            + f'<path d="M3,84 L237,84 L237,120 L3,120 Z" fill="#e9eef3" stroke="none"/>'
            + ''.join(bldg(x, 112, w, h, '#d6dbe6') for x, w, h in ((14, 12, 14), (30, 14, 20), (60, 12, 12), (150, 16, 18), (190, 14, 14))),
            back(110, 120, GOLD, 1.0)))
card('tentozan', '手繪山上建築的屋頂展望台，往下看兩個湖和遠方的海與雪山',
     BOX.format(c=SKYB) + snowmtn(150, 237, 64, 30, '#c9d6e6')
     + f'<path d="M3,64 L237,64 L237,80 L3,80 Z" fill="{SEA}" stroke-width="1.2"/>'
     + f'<ellipse cx="60" cy="100" rx="40" ry="9" fill="{SEA}" stroke-width="1.2"/><ellipse cx="170" cy="104" rx="34" ry="8" fill="{SEA}" stroke-width="1.2"/>'
     + f'<path d="M3,120 Q120,110 237,124 L237,177 L3,177 Z" fill="{SNOW}" stroke-width="1.6"/>'
     + f'<rect x="70" y="124" width="100" height="30" rx="4" fill="#e8e2d4" stroke-width="1.6"/><path d="M70,124 L170,124" stroke-width="2"/>'
     + back(100, 116, RED, .7) + back(136, 116, PINK, .7))
card('kaiyodai', '手繪台地上的展望館屋頂，四周是一望無際的雪原，天上有星星',
     BOX.format(c=NIGHT) + stars([(20, 20, WHITE), (60, 40, GOLD), (100, 16, WHITE), (150, 34, WHITE), (190, 22, GOLD), (220, 44, WHITE), (130, 54, WHITE)])
     + f'<path d="M3,110 Q120,100 237,112 L237,177 L3,177 Z" fill="#e6ecf4" stroke-width="1.6"/>'
     + ''.join(f'<path d="M3,{y} Q120,{y-8} 237,{y+2}" fill="none" stroke-width="1" opacity=".4"/>' for y in (130, 150))
     + f'<rect x="90" y="96" width="60" height="26" rx="4" fill="#b48a64" stroke-width="1.6"/><path d="M90,96 L150,96" stroke-width="2"/>'
     + back(110, 88, PINK, .6) + back(130, 88, SKY, .6) + star(200, 70, 5), bg=NIGHT)

print(save(F, OUT), 'files')
