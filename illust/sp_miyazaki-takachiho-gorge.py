# 高千穗峽划船頁的「高千穗峽長什麼樣子」插圖與提醒卡（2026-11-17）。
# 參考高千穗町觀光協會的介紹（takachiho-kanko.info /boat/detail.php、/sightseeing/18/、/kagura/information/）畫成可愛版，不描照片構圖；
# 神樂只畫一個不戴面具的簡單舞者剪影，不畫任何吉祥物或商標。
# 輸出 illust/sp/miyazaki-takachiho-gorge/*.svg（240×180 圖卡、120×120 提醒小圖）。說明文字放在 illust/spots/miyazaki-takachiho-gorge.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'miyazaki-takachiho-gorge')
W, H = 240, 180
F = {}
SKYW = '#e3f1f8'
ROCK = '#9c948a'
ROCK2 = '#b5ada2'
MOSS = '#7cc48f'
WATER = '#5fb79a'
FALL = '#e6f5fd'
NIGHT = '#2e3a63'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'
BG = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('tk-' + name, W, H, label, inner, bg=bg)


def columns(xs, tops, base, w=14):
    # 直立的岩柱（柱狀節理），頂上長青苔
    t = ''
    for i, (x, top) in enumerate(zip(xs, tops)):
        t += f'<rect x="{x}" y="{top}" width="{w}" height="{base-top}" rx="3" fill="{ROCK if i % 2 else ROCK2}"/>'
        t += f'<path d="M{x+2},{top+(base-top)*.5:.0f} l{w-4},0" stroke-width="1.2" opacity=".45"/>'
        t += f'<ellipse cx="{x+w/2}" cy="{top+1}" rx="{w/2+2}" ry="4" fill="{MOSS}" stroke-width="1.6"/>'
    return t


def water(y):
    return (f'<path d="M3,{y} q14,-6 28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t10,0 {BOT}" fill="{WATER}"/>'
            f'<path d="M30,{y+18} q8,-4 16,0 M150,{y+20} q8,-4 16,0 M96,{y+12} q6,-3 12,0" fill="none" stroke="{SKY}" stroke-width="1.6"/>')


def boat(x, y, s=1.0, col=RED, smile=True):
    # 有臉的小船（x 是船中間，y 是船舷）
    t = (f'<path d="M{x-30*s},{y} L{x+30*s},{y} Q{x+26*s},{y+18*s} {x+12*s},{y+18*s} '
         f'L{x-12*s},{y+18*s} Q{x-26*s},{y+18*s} {x-30*s},{y} Z" fill="{col}"/>'
         f'<path d="M{x-28*s},{y+4*s} L{x+28*s},{y+4*s}" stroke="{WHITE}" stroke-width="{2.2*s:.1f}"/>')
    if smile:
        t += face(x, y + 11 * s, .6 * s)
    return t


def oars(x, y, s=1.0):
    return (f'<path d="M{x-18*s},{y-4*s} L{x-40*s},{y+14*s} M{x+18*s},{y-4*s} L{x+40*s},{y+14*s}" stroke="{DBROWN}" stroke-width="2.6"/>'
            f'<ellipse cx="{x-42*s}" cy="{y+16*s}" rx="{5*s}" ry="{2.6*s}" fill="{DBROWN}" stroke-width="1.2" transform="rotate(-40 {x-42*s} {y+16*s})"/>'
            f'<ellipse cx="{x+42*s}" cy="{y+16*s}" rx="{5*s}" ry="{2.6*s}" fill="{DBROWN}" stroke-width="1.2" transform="rotate(40 {x+42*s} {y+16*s})"/>')


def person(x, y, col=RED, s=1.0, vest=False):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if vest:
        t += f'<path d="M{x-6*s},{y+12*s} L{x+6*s},{y+12*s} L{x+6*s},{y+19*s} L{x-6*s},{y+19*s} Z" fill="#f39a4a" stroke-width="1.2"/>'
    return t


def trees(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN if i % 2 else DGREEN}" stroke-width="1.8"/>'
                   for i, (x, y, r) in enumerate(pts))


def fall(x1, x2, top, bot):
    # 從崖上落下的瀑布＋落水處的水花
    return (f'<path d="M{x1},{top} Q{(x1+x2)/2},{top-3} {x2},{top} L{x2+4},{bot} L{x1-2},{bot} Z" fill="{FALL}" stroke-width="2"/>'
            f'<path d="M{x1+5},{top+10} L{x1+6},{bot-8} M{x2-4},{top+14} L{x2-2},{bot-6}" stroke="#9fd0ea" stroke-width="1.6"/>'
            + ''.join(f'<circle cx="{x}" cy="{bot}" r="{r}" fill="{WHITE}" stroke-width="1.4"/>'
                      for x, r in [(x1 - 4, 5), ((x1 + x2) / 2, 7), (x2 + 6, 5)]))


# 1. 柱狀節理：阿蘇火山噴發的熔岩冷卻後形成
cols = columns(list(range(88, 230, 16)), [58, 48, 62, 44, 54, 40, 50, 60, 46], 150)
cols += face(159, 104, 1.0)
card('columns', '手繪遠處冒煙的火山，和峽谷邊一根根直立的岩柱',
     BG
     + f'<path d="M14,98 L44,48 Q52,40 60,48 L92,98 Z" fill="#c9b8a4"/>'
     + f'<path d="M44,48 Q52,40 60,48 L56,58 Q52,52 48,58 Z" fill="{RED}" stroke-width="1.6"/>'
     + f'<path d="M48,38 q-8,-8 0,-14 q4,-10 14,-6 q10,-2 8,8 q4,8 -6,10 Z" fill="{GRAY}" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{RED}" stroke-width="1.2"/>' for x, y in [(66, 62), (76, 74), (84, 88)])
     + f'<path d="M3,104 Q30,92 56,100 Q76,94 90,102 L90,150 L3,150 Z" fill="{MOSS}"/>'
     + trees([(20, 100, 9), (44, 96, 10), (70, 100, 9)])
     + cols
     + water(150)
     + star(120, 26, 5) + sparkle(200, 24))

# 2. 真名井瀑布：從崖上直接落進峽谷，小船只能划到附近
card('manai', '手繪從崖上落進綠色水面的瀑布，小船停在稍遠的地方',
     BG
     + trees([(16, 30, 12), (36, 22, 13), (58, 28, 11)])
     + columns([6, 22, 38, 54], [36, 30, 34, 40], 150, 16)
     + fall(72, 88, 44, 140)
     + columns([186, 202, 218], [46, 38, 50], 150, 16)
     + trees([(196, 34, 12), (222, 40, 10)])
     + water(140)
     + oars(156, 140, .8) + person(150, 120, NAVY, .7, True) + person(164, 122, PINK, .7, True) + boat(156, 136, .9)
     + sparkle(130, 30) + star(150, 50, 5))

# 3. 小船：一艘 30 分鐘、最多 3 人、國中以上才能划
clock = (f'<circle cx="196" cy="44" r="24" fill="{WHITE}"/>'
         f'<path d="M196,44 L196,22 A22,22 0 0,1 196,66 Z" fill="{GOLD}" stroke-width="1.6"/>'
         f'<path d="M196,44 L196,28 M196,44 L208,44" stroke-width="2.4"/>'
         f'<circle cx="196" cy="44" r="2.4" fill="{INK}" stroke="none"/>')
card('boat', '手繪一艘小船坐了三個人，中間的人在划槳，旁邊有一個走了半圈的時鐘',
     BG + clock
     + columns([6, 22], [50, 60], 132, 16) + trees([(14, 46, 10), (34, 52, 9)])
     + water(132)
     + oars(110, 128, 1.15)
     + person(84, 102, RED, .85, True) + person(110, 98, NAVY, .95, True) + person(136, 104, GREEN, .8, True)
     + boat(110, 124, 1.5)
     + sparkle(60, 30) + star(150, 30, 5))

# 4. 報到：第 1 御塩井停車場裡的受付小屋，報到後再走到乘船處
def car(x, y, col):
    return (f'<rect x="{x}" y="{y}" width="36" height="18" rx="6" fill="{col}"/>'
            f'<path d="M{x+6},{y} L{x+10},{y-10} L{x+26},{y-10} L{x+30},{y} Z" fill="{SKY}" stroke-width="1.6"/>'
            f'<circle cx="{x+9}" cy="{y+18}" r="4.4" fill="{INK}"/><circle cx="{x+27}" cy="{y+18}" r="4.4" fill="{INK}"/>')


card('uketsuke', '手繪停車場裡的小屋，旁邊停著車，一條小路通往水邊的小船',
     BG
     + trees([(30, 46, 14), (54, 38, 16), (210, 40, 15)])
     + f'<path d="M3,74 L237,74 L237,124 L3,124 Z" fill="#c7ccd4" stroke="none"/>'
     + ''.join(f'<path d="M{x},80 L{x},118" stroke="{WHITE}" stroke-width="2.4"/>' for x in (18, 62, 106))
     + car(22, 96, GOLD) + car(66, 96, SKY)
     # 受付小屋
     + f'<rect x="132" y="66" width="62" height="42" rx="3" fill="{BROWN}"/>'
     + f'<path d="M124,68 L163,40 L202,68 Z" fill="{RED}"/>'
     + f'<rect x="142" y="76" width="42" height="16" rx="3" fill="{CREAM}" stroke-width="1.6"/>'
     + f'<rect x="140" y="92" width="46" height="5" rx="2" fill="{DBROWN}"/>'
     + person(163, 76, NAVY, .55)
     + f'<path d="M210,108 L210,58" stroke-width="2.4"/><path d="M210,58 L232,64 L210,72 Z" fill="{GOLD}" stroke-width="1.6"/>'
     + f'<path d="M163,112 Q150,134 120,140" fill="none" stroke="{DBROWN}" stroke-width="2.4" stroke-dasharray="2 6"/>'
     + water(140)
     + boat(76, 150, .75)
     + sparkle(100, 30))

# 5. 遊步道的觀瀑台：不划船也看得到瀑布
card('walk', '手繪沿著峽谷的步道，有人站在欄杆邊看對面的瀑布',
     BG
     + trees([(20, 34, 12), (42, 26, 13), (66, 34, 11)])
     + columns([8, 26, 44, 62], [40, 34, 38, 44], 150, 18)
     + fall(82, 96, 48, 150)
     + water(150)
     # 右邊崖上的步道與欄杆
     + f'<path d="M140,106 L237,96 L237,155 Q237,177 215,177 L140,177 Z" fill="{ROCK2}"/>'
     + ''.join(f'<path d="M{x},{110 - (x-140)*.1:.0f} L{x},176" stroke-width="1.2" opacity=".4"/>' for x in (160, 182, 204, 226))
     + f'<path d="M136,108 L237,98" stroke="{DBROWN}" stroke-width="5"/>'
     + f'<path d="M140,88 L232,78" stroke="{DBROWN}" stroke-width="3"/>'
     + ''.join(f'<path d="M{x},{108 - (x-136)*.1:.0f} L{x},{88 - (x-140)*.11:.0f}" stroke="{DBROWN}" stroke-width="3"/>' for x in (146, 176, 206, 230))
     + person(186, 66, PINK, .9) + person(204, 68, NAVY, .8)
     + trees([(212, 30, 13), (228, 40, 9)])
     + f'<path d="M168,60 Q140,48 110,56" fill="none" stroke-width="1.6" stroke-dasharray="3 5"/>'
     + sparkle(130, 26) + star(160, 30, 5))

# 6. 高千穗神社的夜神樂：不戴面具的簡單舞者剪影
dancer = (f'<circle cx="120" cy="78" r="9" fill="#f9d9c0"/>'
          + face(120, 79, .45, blush=False)
          + f'<path d="M110,74 Q120,62 130,74" fill="{INK}" stroke-width="1.4"/>'
          f'<path d="M106,120 L112,90 Q120,84 128,90 L134,120 Z" fill="{WHITE}"/>'
          f'<path d="M108,120 L134,120 L136,132 L104,132 Z" fill="{RED}"/>'
          f'<path d="M112,94 Q96,92 88,80" fill="none" stroke-width="2.6"/>'
          f'<path d="M128,94 Q144,96 150,86" fill="none" stroke-width="2.6"/>'
          f'<path d="M150,86 L160,72 L166,90 Z" fill="{GOLD}" stroke-width="1.6"/>'
          + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{GOLD}" stroke-width="1"/>' for x, y in [(84, 76), (88, 72), (82, 70), (86, 66)]))
card('kagura', '手繪晚上木頭舞台上，一位穿白衣紅褲的舞者拿著扇子跳舞，兩邊掛著燈籠',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + f'<path d="M194,14 a10,10 0 1,0 12,14 a8,8 0 1,1 -12,-14 Z" fill="{GOLD}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(28, 24), (70, 18), (160, 22), (190, 60)])
     # 舞台：屋頂、柱子、木地板
     + f'<path d="M30,52 Q120,30 210,52 L200,60 L40,60 Z" fill="{DBROWN}"/>'
     + f'<rect x="44" y="60" width="152" height="74" fill="#f3e2c0"/>'
     + f'<rect x="44" y="60" width="10" height="80" fill="{BROWN}"/><rect x="186" y="60" width="10" height="80" fill="{BROWN}"/>'
     + f'<path d="M54,64 Q120,72 186,64" fill="none" stroke="{RED}" stroke-width="3"/>'
     + f'<rect x="34" y="132" width="172" height="10" rx="2" fill="{BROWN}"/>'
     + dancer
     # 燈籠
     + ''.join(f'<path d="M{x},60 L{x},70" stroke-width="1.6"/><ellipse cx="{x}" cy="80" rx="8" ry="11" fill="{GOLD}"/>'
               f'<path d="M{x-8},80 L{x+8},80" stroke-width="1" opacity=".5"/>' for x in (26, 214))
     # 觀眾的頭
     + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#4a557e"/>' for x, y in [(40, 162), (70, 158), (100, 164), (140, 160), (170, 164), (200, 158)])
     + sparkle(150, 22))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('tk-' + name, 120, 120, label, inner, bg='#fff3c4')


# 救生衣碰水自動充氣，弄到充氣要付 3,000 円
rem('r-vest', '手繪提醒：救生衣碰到水會膨起來',
    f'<path d="M30,34 Q38,22 50,26 L60,40 L70,26 Q82,22 90,34 L96,94 Q60,106 24,94 Z" fill="#f39a4a"/>'
    + f'<path d="M60,40 L60,98" stroke-width="2"/>'
    + f'<path d="M34,62 L86,62" stroke="{WHITE}" stroke-width="3"/>'
    + face(60, 78, .7)
    + f'<path d="M14,40 q-4,-8 2,-14 M106,40 q4,-8 -2,-14 M10,64 l-6,0 M110,64 l6,0" fill="none" stroke-width="2"/>'
    + ''.join(f'<path d="M{x},{y} q-4,6 0,9 q4,-3 0,-9 Z" fill="#7fc1e8" stroke-width="1.2"/>' for x, y in [(18, 86), (100, 82), (60, 104)]))

# 下雨照開，划船的人要穿雨衣
rem('r-rain', '手繪提醒：下雨天穿雨衣划船',
    f'<path d="M20,34 Q20,16 40,18 Q48,6 66,12 Q86,8 90,26 Q104,28 100,40 L26,40 Q16,40 20,34 Z" fill="{GRAY}"/>'
    + ''.join(f'<path d="M{x},{y} l-3,8" stroke="#7fa6c8" stroke-width="2.2"/>' for x, y in [(30, 48), (54, 52), (80, 46), (100, 56), (16, 66)])
    + f'<circle cx="60" cy="62" r="9" fill="#f9d9c0"/>'
    + f'<path d="M48,62 Q48,46 60,46 Q72,46 72,62 L76,98 L44,98 Z" fill="{GOLD}"/>'
    + f'<circle cx="60" cy="63" r="8" fill="#f9d9c0" stroke-width="1.6"/>'
    + face(60, 63, .45, blush=False)
    + f'<path d="M78,82 L102,104" stroke="{DBROWN}" stroke-width="3"/><ellipse cx="104" cy="106" rx="6" ry="3" fill="{DBROWN}" stroke-width="1.2" transform="rotate(42 104 106)"/>'
    + f'<path d="M10,104 q12,-6 24,0 t24,0 t24,0" fill="none" stroke="{WATER}" stroke-width="3"/>')

# 沒有小船專用停車場，常常連第 2 停車場都停滿
def mini_car(x, y, col):
    return (f'<rect x="{x}" y="{y}" width="26" height="14" rx="5" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+5},{y} L{x+8},{y-7} L{x+18},{y-7} L{x+21},{y} Z" fill="{SKY}" stroke-width="1.2"/>'
            f'<circle cx="{x+7}" cy="{y+14}" r="3" fill="{INK}" stroke="none"/><circle cx="{x+19}" cy="{y+14}" r="3" fill="{INK}" stroke="none"/>')


rem('r-parking', '手繪提醒：停車場停滿了車',
    f'<rect x="10" y="12" width="28" height="28" rx="5" fill="#4f78c4"/>'
    f'<path d="M20,34 L20,18 L27,18 Q33,18 33,24 Q33,30 27,30 L20,30" fill="none" stroke="{WHITE}" stroke-width="3"/>'
    f'<path d="M24,40 L24,52" stroke-width="2.4"/>'
    f'<rect x="8" y="56" width="104" height="54" rx="6" fill="#c7ccd4" stroke-width="1.6"/>'
    + mini_car(14, 66, RED) + mini_car(46, 66, GOLD) + mini_car(78, 66, GREEN)
    + mini_car(14, 90, SKY) + mini_car(46, 90, PINK) + mini_car(78, 90, WHITE)
    + f'<circle cx="92" cy="28" r="14" fill="{WHITE}"/><path d="M85,21 L99,35 M99,21 L85,35" stroke="{RED}" stroke-width="3"/>')

print(save(F, OUT), 'files')
