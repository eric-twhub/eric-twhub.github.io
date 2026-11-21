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

# ---- ferry（2026-11-17，石垣島離島船票頁 /ishigaki/ferry/）：藍綠色海上的白色高速船，後面一座紅瓦屋頂＋椰子樹的小島 ----
TQ = '#4fc6c0'
TQ2 = '#a8e6df'
SAND = '#f6e3b4'
fy = ''
# 太陽和一朵小雲
fy += f'<circle cx="36" cy="34" r="12" fill="{GOLD}" stroke-width="1.8"/>'
fy += f'<path d="M58,50 q-2,-10 8,-10 q4,-8 14,-4 q8,-4 12,4 q8,0 6,10 Z" fill="{WHITE}" stroke-width="1.8"/>'
# 小島：沙灘、紅瓦屋頂的小屋、椰子樹
fy += f'<path d="M98,98 Q106,80 134,78 Q162,76 174,98 Z" fill="{SAND}"/>'
fy += f'<rect x="116" y="70" width="26" height="14" rx="2" fill="{CREAM}"/>'
fy += f'<rect x="125" y="75" width="8" height="9" rx="1.5" fill="{DBROWN}" stroke-width="1.4"/>'
fy += f'<path d="M110,72 L119,58 L139,58 L148,72 Z" fill="{BRICK}"/>'
fy += f'<path d="M114,66 L144,66 M122,58 L120,72 M129,58 L129,72 M136,58 L138,72" stroke-width="1.2" opacity=".5"/>'
fy += f'<path d="M158,84 Q156,66 152,48" fill="none" stroke="{BROWN}" stroke-width="5"/>'
fy += f'<path d="M158,84 Q156,66 152,48" fill="none" stroke-width="1.2" opacity=".5" stroke-dasharray="2 4"/>'
fy += ''.join(f'<path d="M152,48 Q{x1},{y1} {x2},{y2} Q{x1},{y1+8} 152,48 Z" fill="{GREEN}" stroke-width="1.6"/>'
              for x1, y1, x2, y2 in [(140, 38, 128, 50), (146, 30, 136, 26), (160, 30, 170, 32), (166, 40, 174, 54)])
fy += f'<circle cx="150" cy="52" r="2.6" fill="{DBROWN}" stroke-width="1"/><circle cx="155" cy="52" r="2.6" fill="{DBROWN}" stroke-width="1"/>'
# 藍綠色的海
fy += (f'<path d="M6,96 q12,-6 24,0 t24,0 t24,0 t24,0 t24,0 t24,0 t24,0 L174,136 Q174,144 166,144 '
       f'L14,144 Q6,144 6,136 Z" fill="{TQ}"/>')
fy += f'<path d="M6,100 q12,-5 24,0 t24,0 t24,0 t24,0 t24,0 t24,0 t24,0" fill="none" stroke="{TQ2}" stroke-width="2"/>'
fy += f'<path d="M128,128 q8,-4 16,0 M150,136 q8,-4 16,0 M60,136 q6,-3 12,0" fill="none" stroke="{WHITE}" stroke-width="1.6"/>'
# 船尾的白浪
fy += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" stroke-width="1.4"/>'
              for x, y, r in [(12, 114, 5), (20, 120, 6), (10, 124, 4)])
fy += f'<path d="M26,124 q-8,4 -18,2 M30,128 q-10,5 -22,4" fill="none" stroke="{WHITE}" stroke-width="2"/>'
# 白色高速船：船身、藍線、船艙、窗戶、雷達
fy += f'<path d="M16,100 L124,96 Q118,116 100,120 L28,120 Q18,120 16,110 Z" fill="{WHITE}"/>'
fy += f'<path d="M18,112 L114,110" stroke="#3a8fd0" stroke-width="3.4"/>'
fy += f'<path d="M30,100 L30,82 Q30,74 38,74 L84,74 Q96,74 104,88 L108,98 Z" fill="{WHITE}"/>'
fy += ''.join(f'<rect x="{x}" y="80" width="9" height="8" rx="2" fill="{SKY}" stroke-width="1.4"/>' for x in (37, 50, 63))
fy += f'<path d="M86,78 Q96,79 100,88 L86,88 Z" fill="{SKY}" stroke-width="1.4"/>'
fy += f'<path d="M58,74 L58,64 M52,64 L64,64" stroke-width="2.2"/><circle cx="58" cy="62" r="2.4" fill="{RED}" stroke-width="1.2"/>'
fy += face(90, 101, .7)
# 船頭的水花
fy += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" stroke-width="1.4"/>'
              for x, y, r in [(126, 104, 4), (130, 112, 5), (122, 118, 4)])
fy += sparkle(84, 30) + star(108, 22, 5) + sparkle(16, 60, 4)
add('ferry', '手繪藍綠色海上一艘有臉的白色高速船，後面是有紅瓦屋頂小屋和椰子樹的小島', fy, dots=False)

# ---- ropeway（2026-11-17，函館山纜車頁 /hakodate/ropeway/）：深藍夜空裡掛在纜線上的紅白色纜車，下面是兩邊夾著海灣、亮著小燈的彎彎市街 ----
# 市街的形狀參考函館山往下看的「兩邊是海、中間變窄」簡化成沙漏形，不描照片構圖；纜車不畫公司標誌。
NSEA = '#2b3866'
NFAR = '#232b4f'
NLAND = '#3d4a7c'
LITE = [GOLD, '#ffd98a', '#ffb066', WHITE]


def _isthmus(y):
    # 回傳這一列市街的中心與半寬：遠處寬、中間窄、近處再變寬
    c = 90 + (y - 120) * 0.25
    hw = 12 + (y - 120) ** 2 * (0.1 if y < 120 else 0.0625)
    return c, min(hw, 52)


rw = ''
# 星星（不畫月亮：封面的夜晚場景已經有一個月亮）
rw += star(30, 30, 5) + star(122, 20, 4) + star(62, 66, 3.6) + star(156, 26, 5.4)
rw += sparkle(150, 76, 4) + sparkle(18, 70, 3) + sparkle(138, 12, 3)
# 兩邊的海灣與遠處的山影
rw += f'<path d="M6,96 L174,96 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="{NSEA}"/>'
rw += f'<path d="M6,100 Q30,90 62,94 Q100,86 132,92 Q156,88 174,96 L174,102 L6,102 Z" fill="{NFAR}" stroke-width="1.8"/>'
# 沙漏形的市街
_ys = list(range(100, 145, 4))
_l = [(_isthmus(y)[0] - _isthmus(y)[1], y) for y in _ys]
_r = [(_isthmus(y)[0] + _isthmus(y)[1], y) for y in _ys]
rw += ('<path d="M' + ' L'.join(f'{x:.1f},{y}' for x, y in _l) + ' L'
       + ' L'.join(f'{x:.1f},{y}' for x, y in reversed(_r)) + f' Z" fill="{NLAND}" stroke-width="1.8"/>')
# 市街裡一顆顆暖色的小燈（固定亂數，每次輸出一樣）
_seed = 11
_n = 0
while _n < 78:
    _seed = (_seed * 1103515245 + 12345) % 2147483648
    _x = 6 + (_seed % 1680) / 10
    _seed = (_seed * 1103515245 + 12345) % 2147483648
    _y = 101 + (_seed % 420) / 10
    _c, _hw = _isthmus(_y)
    if abs(_x - _c) > _hw - 2.6 or _x < 9 or _x > 171:
        continue
    rw += f'<circle cx="{_x:.1f}" cy="{_y:.1f}" r="{1.0 + (_n % 3) * 0.25:.2f}" fill="{LITE[_n % 4]}" stroke="none"/>'
    _n += 1
rw += f'<path d="M14,124 q8,-3 16,0 M146,130 q8,-3 16,0 M20,136 q6,-2 12,0" fill="none" stroke="#5b6ea6" stroke-width="1.4"/>'
# 兩條纜線（從左上斜斜往右下）
rw += f'<path d="M4,16 L176,58" stroke="{GRAY}" stroke-width="1.8"/><path d="M4,20 L176,62" stroke="{GRAY}" stroke-width="1.4" opacity=".7"/>'
# 纜車：吊架＋車廂（紅色車頂與底線、白色車身、亮燈的窗、可愛臉）
rw += (f'<g transform="rotate(13.7 95 39)"><rect x="83" y="34" width="24" height="7" rx="3" fill="{GRAY}"/>'
       f'<circle cx="88" cy="36" r="2.6" fill="{WHITE}" stroke-width="1.2"/><circle cx="102" cy="36" r="2.6" fill="{WHITE}" stroke-width="1.2"/></g>')
rw += f'<path d="M95,42 L95,52 M89,52 L101,52" stroke-width="2.4"/>'
rw += f'<rect x="72" y="52" width="46" height="42" rx="10" fill="{WHITE}"/>'
rw += f'<path d="M72,64 L72,62 Q72,52 82,52 L108,52 Q118,52 118,62 L118,64 Z" fill="{RED}"/>'
rw += f'<path d="M72,86 L118,86 Q118,94 108,94 L82,94 Q72,94 72,86 Z" fill="{RED}"/>'
rw += ''.join(f'<rect x="{x}" y="67" width="11" height="9" rx="2.4" fill="#ffe7a8" stroke-width="1.4"/>' for x in (77, 89.5, 102))
rw += face(95, 80, .62)
rw += sparkle(128, 46, 3.4)
add('ropeway', '手繪深藍夜空下掛在纜線上、有臉的紅白色纜車，下面是兩邊夾著海灣、亮著小小燈光的彎彎市街', rw, bg=NAVY, dots=False)

# ---- conan（2026-11-18，青山剛昌ふるさと館頁 /yonago/conan-museum/）：一支大放大鏡照著鄉下小車站前的路，路上有一串小腳印 ----
# 只畫一般的鄉下車站和放大鏡，不畫任何角色、角色的剪影或眼鏡＋領結、館方或店家的標誌與招牌、文字和數字。
FIELD = '#cfe7c4'
LENS = '#cfe9f7'
cn = ''
# 雲和遠山
cn += f'<path d="M20,40 q-2,-10 8,-10 q4,-8 14,-4 q8,-4 12,4 q8,0 6,10 Z" fill="{WHITE}" stroke-width="1.8"/>'
cn += f'<path d="M6,84 Q30,58 58,70 Q84,52 112,66 Q140,56 174,74 L174,92 L6,92 Z" fill="{GREEN}"/>'
cn += f'<path d="M6,90 L174,90 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="{FIELD}"/>'
# 鐵軌（車站後面橫過去）
cn += f'<path d="M6,94 L174,94 M6,99 L174,99" stroke="{DBROWN}" stroke-width="1.8"/>'
cn += ''.join(f'<path d="M{x},92 L{x},101" stroke="{DBROWN}" stroke-width="1.4" opacity=".6"/>' for x in range(12, 174, 10))
# 停在月台邊的一節小火車（沒有塗裝標誌）
cn += f'<rect x="98" y="72" width="62" height="22" rx="7" fill="{CREAM}"/>'
cn += f'<path d="M98,86 L160,86 L160,87 Q160,94 153,94 L105,94 Q98,94 98,87 Z" fill="{GREEN}"/>'
cn += ''.join(f'<rect x="{x}" y="76" width="9" height="7" rx="2" fill="{SKY}" stroke-width="1.3"/>' for x in (104, 117, 130, 143))
cn += f'<circle cx="110" cy="96" r="3.4" fill="{INK}"/><circle cx="148" cy="96" r="3.4" fill="{INK}"/>'
cn += f'<circle cx="155" cy="90" r="2" fill="{GOLD}" stroke-width="1"/>'
# 木造小車站：瓦屋頂、白牆、門和兩扇窗
cn += f'<rect x="20" y="66" width="62" height="36" rx="2" fill="{CREAM}"/>'
cn += f'<path d="M12,68 L28,50 L74,50 L90,68 Z" fill="{BRICK}"/>'
cn += f'<path d="M20,58 L82,58 M30,50 L26,68 M51,50 L51,68 M72,50 L76,68" stroke-width="1.2" opacity=".45"/>'
cn += f'<rect x="44" y="78" width="14" height="24" rx="2" fill="{DBROWN}" stroke-width="1.8"/>'
cn += ''.join(f'<rect x="{x}" y="74" width="11" height="10" rx="2" fill="{SKY}" stroke-width="1.4"/>' for x in (26, 65))
cn += f'<rect x="34" y="60" width="34" height="6" rx="1.5" fill="{WHITE}" stroke-width="1.4"/>'
cn += face(51, 92, .5, blush=False)
# 從車站門口彎出去的路，路上一串小腳印
cn += f'<path d="M44,102 Q40,114 70,122 Q104,130 112,144 L84,144 Q80,134 56,126 Q32,118 36,102 Z" fill="#eadcc4" stroke-width="1.8"/>'
_fp = [(42, 108, 10), (50, 114, -20), (60, 118, -40)]
cn += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="1.8" ry="2.8" fill="{DBROWN}" stroke="none" transform="rotate({a+90} {x} {y})"/>'
              for x, y, a in _fp)
# 路邊的小樹
cn += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DGREEN}" stroke-width="1.6"/>' for x, y, r in [(14, 114, 6), (150, 132, 7), (164, 120, 5)])
# 大放大鏡：鏡片蓋在路上，裡面的腳印被放大，握把往右下
cn += f'<path d="M119,127 L156,138" stroke="{DBROWN}" stroke-width="10"/>'
cn += f'<path d="M119,127 L156,138" stroke="{BROWN}" stroke-width="5"/>'
cn += f'<circle cx="98" cy="120" r="22" fill="{LENS}" fill-opacity=".6" stroke-width="5"/>'
cn += f'<circle cx="98" cy="120" r="22" fill="none" stroke="{GOLD}" stroke-width="2"/>'
cn += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.6" ry="5.6" fill="{DBROWN}" stroke="none" transform="rotate({a} {x} {y})"/>'
              for x, y, a in [(84, 118, 64), (98, 124, 52), (110, 132, 40)])
cn += f'<path d="M84,108 Q88,101 96,100" fill="none" stroke="{WHITE}" stroke-width="3"/>'
cn += sparkle(150, 40, 4) + star(98, 22, 5) + sparkle(160, 22, 3)
add('conan', '手繪一支大放大鏡照著鄉下小車站前彎彎的路，路上有一串小腳印', cn, dots=False)

# ---- samurai：新宿 SAMURAI RESTAURANT 頁（2026-11-21）。Q 版武士拿扇子站在太鼓旁，不畫真實表演者或 logo ----
sm = (f'<path d="M14,112 L166,112 L166,128 Q166,140 154,140 L26,140 Q14,140 14,128 Z" fill="#c49a6c"/>'
      f'<path d="M74,62 L106,62 L109,90 L71,90 Z" fill="{RED}"/>'
      f'<path d="M84,62 L90,76 L96,62" fill="{WHITE}" stroke-width="1.2"/>'
      f'<path d="M71,90 L109,90 L117,118 L63,118 Z" fill="{NAVY}"/><path d="M90,92 L90,118" stroke-width="1.4"/>'
      f'<path d="M106,68 L122,54" stroke-width="3"/>'
      f'<path d="M122,54 L112,36 Q130,28 142,42 Z" fill="{GOLD}" stroke-width="1.6"/>'
      f'<path d="M74,68 L62,80" stroke-width="3"/>'
      f'<circle cx="90" cy="42" r="17" fill="#f9e0cc"/>'
      f'<path d="M73,40 Q73,25 90,25 Q107,25 107,40 Q99,33 90,34 Q81,33 73,40 Z" fill="{INK}"/>'
      f'<path d="M86,26 L87,14 L98,12 L94,26 Z" fill="{INK}"/>'
      + face(90, 45, .8)
      + f'<ellipse cx="40" cy="122" rx="22" ry="7" fill="{DBROWN}"/><rect x="18" y="98" width="44" height="24" fill="{BRICK}"/>'
      f'<ellipse cx="40" cy="98" rx="22" ry="7" fill="#f7e7cf"/>'
      f'<path d="M30,86 L38,96 M52,84 L46,96" stroke="{BROWN}" stroke-width="3"/>'
      + star(150, 30, 6) + sparkle(30, 40, 4) + sparkle(152, 84, 3))
add('samurai', '手繪拿著金色扇子的可愛 Q 版武士，旁邊一個太鼓', sm, dots=False)

print(save(FILES, OUT), 'stickers')
