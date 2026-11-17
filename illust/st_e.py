# 主題貼紙 E 組（2026-11-17）：高千穗峽划船頁（/miyazaki/takachiho-gorge/）用的手繪貼紙。
# 柱狀節理的峽谷、從崖上落下的瀑布、綠色的水和一艘有臉的小船；參考觀光協會介紹畫成可愛版，不描照片構圖。
# 共用工具在 kit.py。跑 `python3 illust/st_e.py` 輸出 illust/st/*.svg，
# 再跑 `python3 illust/make_banners.py` 產生標題下的寬版封面。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st')
ROCK = '#9c948a'
ROCK2 = '#b5ada2'
MOSS = '#7cc48f'
WATER = '#5fb79a'
FALL = '#e6f5fd'

FILES = {}


def add(name, label, inner, bg=CREAM, dots=True):
    FILES[name] = sticker(name, label, inner, bg=bg, dots=dots)


def columns(xs, tops, base, w=12):
    # 一根根直立的岩柱（柱狀節理），頂上長青苔
    t = ''
    for i, (x, top) in enumerate(zip(xs, tops)):
        t += f'<rect x="{x}" y="{top}" width="{w}" height="{base-top}" rx="3" fill="{ROCK if i % 2 else ROCK2}"/>'
        t += f'<path d="M{x+2},{top+(base-top)*.45:.0f} l{w-4},0" stroke-width="1.2" opacity=".45"/>'
        t += f'<ellipse cx="{x+w/2}" cy="{top+1}" rx="{w/2+2}" ry="4" fill="{MOSS}" stroke-width="1.6"/>'
    return t


# ---- gorge：柱狀節理的峽谷、瀑布、綠水上的小船 ----
gz = ''
# 兩側崖頂的樹
for x, y, r in [(18, 30, 9), (34, 24, 11), (146, 26, 11), (162, 32, 9)]:
    gz += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN}" stroke-width="1.8"/>'
# 遠處的岩壁（淡色，讓峽谷有深度）
gz += (f'<path d="M50,118 L50,70 q8,-10 16,-4 q8,-10 18,-3 q8,-9 18,-2 q8,-9 16,-2 q6,-6 12,2 L130,118 Z" '
       f'fill="#cfe3c6" stroke-width="1.8"/>')
gz += f'<path d="M60,96 q20,-6 36,0 q16,6 30,-2" fill="none" stroke-width="1.2" opacity=".4"/>'
# 左右兩面柱狀節理的岩壁
gz += columns([8, 20, 32, 44], [36, 30, 38, 44], 118)
gz += columns([124, 136, 148, 160], [44, 34, 30, 38], 118)
# 從左邊崖上落下的瀑布＋水花
gz += (f'<path d="M50,46 Q58,44 62,48 L66,116 L52,116 Z" fill="{FALL}" stroke-width="2"/>'
       f'<path d="M56,58 L57,104 M61,62 L62,108" stroke="#9fd0ea" stroke-width="1.6"/>')
gz += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" stroke-width="1.4"/>'
              for x, y, r in [(50, 114, 5), (60, 112, 6), (70, 115, 5)])
# 綠色的水
gz += (f'<path d="M6,114 q12,-6 24,0 t24,0 t24,0 t24,0 t24,0 t24,0 t24,0 L174,136 Q174,144 166,144 '
       f'L14,144 Q6,144 6,136 Z" fill="{WATER}"/>')
gz += f'<path d="M20,132 q8,-4 16,0 M140,134 q8,-4 16,0 M76,138 q6,-3 12,0" fill="none" stroke="{SKY}" stroke-width="1.6"/>'
# 有臉的小船＋兩支槳
gz += (f'<path d="M90,110 L72,126 M130,110 L148,126" stroke="{DBROWN}" stroke-width="3"/>'
       f'<ellipse cx="70" cy="128" rx="6" ry="3" fill="{DBROWN}" stroke-width="1.2" transform="rotate(-42 70 128)"/>'
       f'<ellipse cx="150" cy="128" rx="6" ry="3" fill="{DBROWN}" stroke-width="1.2" transform="rotate(42 150 128)"/>')
gz += f'<path d="M80,112 L140,112 Q136,132 120,132 L100,132 Q84,132 80,112 Z" fill="{RED}"/>'
gz += f'<path d="M82,117 L138,117" stroke="{WHITE}" stroke-width="2.4"/>'
gz += face(110, 123, .8)
gz += sparkle(92, 22) + sparkle(110, 40, 4) + star(76, 28, 6)
add('gorge', '手繪柱狀節理的峽谷、瀑布和綠色水面上的小船', gz, dots=False)

print(save(FILES, OUT), 'stickers')
