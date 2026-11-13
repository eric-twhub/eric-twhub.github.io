# ちゅらさん6（Churasun6）頁的「店裡看得到什麼」插圖與提醒卡（2026-11-13）。
# 參考官網首頁（churasun6.com）的文字介紹畫成可愛版：官網自稱「宇宙船造型的表演俱樂部」，
# 只畫一般的舞台與 Q 版表演女孩，不畫成任何真實成員的樣子、不畫店家或團體 logo。
# Q 版女孩的畫法與 sp_tokyo-63angel.py 相同。
# 輸出 illust/sp/okinawa-churasun6/*.svg。說明文字放在 illust/spots/okinawa-churasun6.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'okinawa-churasun6')
W, H = 240, 180
F = {}
SPACE = '#24305a'
STAGE = '#2f3a6e'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('cs-' + name, W, H, label, inner, bg=bg)


def girl(x, y, hair=DBROWN, dress=PINK, s=1.0, arms='up', bun=False):
    # Q 版表演女孩：大頭、蓬蓬裙、手舉起來；y 是頭的中心
    t = ''
    if arms == 'up':
        t += (f'<path d="M{x-8*s},{y+18*s} L{x-20*s},{y+4*s} M{x+8*s},{y+18*s} L{x+20*s},{y+4*s}" stroke-width="{2.6*s}"/>'
              f'<circle cx="{x-20*s}" cy="{y+4*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>'
              f'<circle cx="{x+20*s}" cy="{y+4*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>')
    elif arms == 'wave':
        t += (f'<path d="M{x-8*s},{y+18*s} L{x-18*s},{y+30*s} M{x+8*s},{y+18*s} L{x+22*s},{y+6*s}" stroke-width="{2.6*s}"/>'
              f'<circle cx="{x+22*s}" cy="{y+6*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>')
    t += (f'<path d="M{x-4*s},{y+40*s} L{x-5*s},{y+52*s} M{x+4*s},{y+40*s} L{x+5*s},{y+52*s}" stroke-width="{2.4*s}"/>'
          f'<ellipse cx="{x-6*s}" cy="{y+53*s}" rx="{4*s}" ry="{2*s}" fill="{dress}" stroke-width="1.2"/>'
          f'<ellipse cx="{x+6*s}" cy="{y+53*s}" rx="{4*s}" ry="{2*s}" fill="{dress}" stroke-width="1.2"/>'
          f'<path d="M{x-8*s},{y+14*s} L{x+8*s},{y+14*s} L{x+9*s},{y+26*s} L{x+20*s},{y+42*s} Q{x},{y+46*s} {x-20*s},{y+42*s} L{x-9*s},{y+26*s} Z" fill="{dress}"/>'
          f'<path d="M{x-18*s},{y+40*s} q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0" fill="none" stroke="{WHITE}" stroke-width="1.4"/>')
    # 頭髮（後）＋臉＋瀏海
    t += f'<path d="M{x-14*s},{y+12*s} Q{x-16*s},{y-14*s} {x},{y-15*s} Q{x+16*s},{y-14*s} {x+14*s},{y+12*s} Z" fill="{hair}"/>'
    t += f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="#f9e0cc"/>'
    t += f'<path d="M{x-12*s},{y-2*s} Q{x-10*s},{y-14*s} {x},{y-13*s} Q{x+10*s},{y-14*s} {x+12*s},{y-2*s} Q{x+6*s},{y-8*s} {x},{y-6*s} Q{x-6*s},{y-8*s} {x-12*s},{y-2*s} Z" fill="{hair}"/>'
    if bun:
        t += f'<circle cx="{x-10*s}" cy="{y-13*s}" r="{5*s}" fill="{hair}"/><circle cx="{x+10*s}" cy="{y-13*s}" r="{5*s}" fill="{hair}"/>'
    t += face(x, y + 2 * s, .55 * s)
    t += star(x + 9 * s, y - 11 * s, 3.4 * s)
    return t


def spot(x1, x2, top=8, bottom=150, col='#46518a'):
    return f'<path d="M{(x1+x2)/2-6},{top} L{(x1+x2)/2+6},{top} L{x2},{bottom} L{x1},{bottom} Z" fill="{col}" stroke="none"/>'


def stars_bg(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in pts)



# 1. 宇宙船造型的店
card('ship', '手繪飛碟造型的表演廳，圓窗裡透出舞台的燈光',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="none"/>' for x, y, r, c in
               [(24, 24, 1.8, WHITE), (60, 40, 1.4, GOLD), (210, 30, 2, WHITE), (190, 60, 1.4, '#8ff0ff'), (30, 130, 1.6, WHITE), (220, 130, 1.8, GOLD)])
     + f'<circle cx="200" cy="140" r="14" fill="#7fc4e8"/><path d="M188,136 q12,6 24,0" fill="none" stroke-width="1.4"/>'
     + f'<path d="M84,74 Q86,34 120,32 Q154,34 156,74 Z" fill="#bfe3f5"/>'
     + f'<path d="M100,70 Q102,50 120,48 Q138,50 140,70" fill="none" stroke="{WHITE}" stroke-width="2" opacity=".8"/>'
     + f'<ellipse cx="120" cy="88" rx="96" ry="26" fill="{GRAY}"/>'
     + f'<ellipse cx="120" cy="80" rx="74" ry="12" fill="#e6ecf5"/>'
     + ''.join(f'<circle cx="{x}" cy="92" r="6" fill="{c}" stroke-width="1.4"/>' for x, c in [(48, GOLD), (84, PINK), (120, '#8ff0ff'), (156, PINK), (192, GOLD)])
     + f'<path d="M80,112 L64,150 M160,112 L176,150" stroke="#fff6c8" stroke-width="8" opacity=".5"/>'
     + f'<path d="M80,112 L64,150 M160,112 L176,150" stroke-width="2"/>'
     + girl(120, 52, DBROWN, PINK, .55, 'up')
     + star(30, 70, 6) + star(212, 90, 5) + sparkle(160, 24), bg=SPACE)

# 2. 舞台上的唱跳
card('stage', '手繪舞台上兩個可愛女孩在跳舞，頭上有星星燈',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + spot(50, 120) + spot(120, 190)
     + ''.join(star(x, y, 5, c) for x, y, c in [(40, 24, GOLD), (90, 18, '#8ff0ff'), (150, 18, PINK), (200, 26, GOLD)])
     + f'<path d="M3,134 L237,134 {BOT}" fill="#46518a"/>'
     + f'<ellipse cx="120" cy="138" rx="80" ry="9" fill="#8fd0e8"/>'
     + girl(84, 76, INK, '#8fd0e8', 1.0, 'up', True) + girl(156, 76, '#c27a4a', GOLD, 1.0, 'wave')
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(20, 60), (222, 70), (30, 110)]), bg=SPACE)

# 3. 和表演者聊天、拍照
card('chat', '手繪表演女孩和觀眾一起比耶拍照',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e3e8f7"/>'
     + f'<path d="M3,140 L237,140 {BOT}" fill="#cfd8ee"/>'
     + girl(92, 66, DBROWN, PINK, 1.05, 'wave')
     # 觀眾
     + f'<circle cx="142" cy="74" r="12" fill="#f9d9c0"/>'
     + f'<path d="M130,72 Q130,58 142,58 Q154,58 154,72 Q148,64 142,66 Q136,64 130,72 Z" fill="{INK}"/>'
     + face(142, 76, .55)
     + f'<path d="M126,120 q0,-34 16,-34 q16,0 16,34 Z" fill="{GREEN}"/>'
     + f'<path d="M156,96 L166,80" stroke-width="2.4"/><path d="M164,78 l-2,-8 M168,80 l4,-7" stroke-width="2"/>'
     + f'<g transform="rotate(8 196 60)"><rect x="176" y="46" width="40" height="28" rx="6" fill="{GRAY}"/>'
     f'<circle cx="196" cy="60" r="8" fill="{NAVY}"/><circle cx="196" cy="60" r="3.4" fill="{SKY}" stroke-width="1"/></g>'
     + f'<path d="M178,36 l-4,-6 M196,32 l0,-8 M214,36 l4,-6" stroke="{GOLD}" stroke-width="2"/>'
     + f'<path d="M102,40 q10,-14 24,-6" fill="none" stroke-width="1.6"/><path d="M110,30 l4,-6" stroke-width="1.4"/>'
     + ''.join(f'<path d="M{x},{y} q-6,-8 0,-12 q6,4 0,12 Z M{x},{y} q6,-8 12,-4 q-2,8 -12,4" fill="{PINK}" stroke-width="1.2"/>' for x, y in [(30, 40), (40, 120)])
     + star(214, 120, 6), bg='#e3e8f7')

# 4. 前排方案附螢光棒
card('front', '手繪前排觀眾舉著發光的螢光棒看表演',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + spot(60, 180, 8, 100)
     + f'<path d="M3,96 L237,96 L237,108 L3,108 Z" fill="#8fd0e8"/>'
     + girl(120, 34, INK, PINK, .8, 'up', True)
     + f'<path d="M3,108 L237,108 {BOT}" fill="#1c2546"/>'
     + ''.join(f'<circle cx="{x}" cy="150" r="13" fill="{c}"/>' for x, c in [(48, DBROWN), (96, INK), (144, '#8a5c3a'), (192, INK)])
     + ''.join(f'<path d="M{x},{y1} L{x+d},{y2}" stroke="{c}" stroke-width="5"/>'
               f'<path d="M{x},{y1} L{x+d},{y2}" stroke="{WHITE}" stroke-width="1.6"/>'
               for x, y1, d, y2, c in [(60, 140, 8, 112, '#8ff0ff'), (110, 140, -6, 112, PINK), (156, 140, 6, 112, '#b6f5c8'), (204, 140, -8, 112, GOLD)])
     + stars_bg([(20, 20, WHITE), (220, 22, GOLD), (16, 70, '#8ff0ff'), (224, 76, WHITE)]), bg=SPACE)

# 5. 生日拍照
card('birthday', '手繪生日蛋糕、相機和星星彩帶',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + spot(70, 170, 8, 140)
     + f'<path d="M3,132 L237,132 {BOT}" fill="#46518a"/>'
     + f'<rect x="88" y="96" width="64" height="36" rx="6" fill="{WHITE}"/>'
     + f'<path d="M88,108 q8,6 16,0 q8,6 16,0 q8,6 16,0 q8,6 16,0" fill="none" stroke="#8fd0e8" stroke-width="3"/>'
     + f'<rect x="96" y="76" width="48" height="22" rx="5" fill="#8fd0e8"/>'
     + ''.join(f'<path d="M{x},76 L{x},64" stroke-width="2"/><path d="M{x},62 q-3,-4 0,-8 q3,4 0,8 Z" fill="{GOLD}" stroke-width="1.2"/>' for x in (108, 120, 132))
     + star(120, 88, 5, GOLD)
     + f'<g transform="rotate(-12 44 64)"><rect x="24" y="52" width="44" height="30" rx="6" fill="{GRAY}"/>'
     f'<circle cx="46" cy="67" r="9" fill="{NAVY}"/><circle cx="46" cy="67" r="4" fill="{SKY}" stroke-width="1"/>'
     f'<rect x="54" y="46" width="10" height="7" rx="2" fill="{GRAY}"/></g>'
     + f'<path d="M30,40 l-6,-8 M44,36 l0,-10 M58,40 l6,-8" stroke="{GOLD}" stroke-width="2"/>'
     + ''.join(star(x, y, 4, c) for x, y, c in [(180, 36, PINK), (204, 56, GOLD), (220, 30, '#8ff0ff'), (172, 76, '#b6f5c8'), (200, 100, PINK)])
     + stars_bg([(20, 20, WHITE), (110, 20, GOLD), (60, 120, WHITE)]), bg=SPACE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('cs-' + name, 120, 120, label, inner, bg='#fff3c4')


# 開演前 10 分鐘沒到，位子就讓出去
rem('r-late', '手繪提醒：時鐘差 10 分鐘，空出來的椅子',
    f'<circle cx="44" cy="46" r="30" fill="{WHITE}"/>'
    + ''.join(f'<circle cx="{44+24*math.cos(k*math.pi/6):.1f}" cy="{46+24*math.sin(k*math.pi/6):.1f}" r="1.5" fill="{INK}" stroke="none"/>' for k in range(12))
    + f'<path d="M44,46 L44,26" stroke-width="2.6"/><path d="M44,46 L{44-18*math.cos(math.radians(30)):.1f},{46-18*math.sin(math.radians(30)):.1f}" stroke-width="2.6"/>'
    f'<path d="M44,16 A30,30 0 0 0 {44-30*math.sin(math.radians(60)):.1f},{46-30*math.cos(math.radians(60)):.1f}" fill="none" stroke="{RED}" stroke-width="4"/>'
    f'<rect x="80" y="66" width="28" height="12" rx="3" fill="{RED}"/>'
    f'<rect x="80" y="50" width="8" height="18" rx="2" fill="{RED}"/>'
    f'<path d="M84,78 L84,98 M104,78 L104,98" stroke-width="2.6"/>'
    f'<path d="M78,40 L110,40 M102,32 L110,40 L102,48" stroke="{RED}" stroke-width="2.6" fill="none"/>'
    f'<path d="M8,104 L112,104" stroke-width="2"/>')

# 當天預約打另一支電話
rem('r-phone', '手繪提醒：兩支電話，一支旁邊寫著今天',
    f'<rect x="12" y="28" width="38" height="66" rx="8" fill="{GRAY}"/>'
    f'<rect x="17" y="36" width="28" height="44" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
    f'<rect x="66" y="28" width="38" height="66" rx="8" fill="{PINK}"/>'
    f'<rect x="71" y="36" width="28" height="44" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
    f'<rect x="74" y="44" width="22" height="20" rx="2" fill="{GOLD}" stroke-width="1.2"/>'
    f'<path d="M74,50 L96,50" stroke-width="1.2"/>'
    + star(85, 58, 4, RED)
    + f'<path d="M100,14 q8,4 10,12 M94,20 q6,2 8,8" fill="none" stroke-width="1.8"/>'
    f'<path d="M8,106 L112,106" stroke-width="2"/>')

print(save(F, OUT), 'files')
