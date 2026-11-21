# 新宿歌舞伎町 SAMURAI RESTAURANT 頁的插圖與提醒卡（2026-11-21）。
# 參考官網（samurai-restaurant.tokyo）的場次頁、餐點頁與 FAQ 畫成可愛版：和風舞台、白天三場、
# 便當或兩杯飲料選一種、12 月起變便宜。只畫 Q 版武士與太鼓，不畫任何真實表演者、機器人造型或 logo。
# 輸出 illust/sp/tokyo-samurai-restaurant/*.svg。說明文字放在 illust/spots/tokyo-samurai-restaurant.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-samurai-restaurant')
W, H = 240, 180
F = {}
NIGHT = '#2b2346'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sr-' + name, W, H, label, inner, bg=bg)


def samurai(x, y, s=1.0, kimono=RED, hakama=NAVY, fan=False):
    # Q 版武士：大頭、丁髷、和服＋袴；y 是頭的中心。手上拿扇子或竹刀
    t = (f'<path d="M{x-10*s},{y+16*s} L{x+10*s},{y+16*s} L{x+12*s},{y+34*s} L{x-12*s},{y+34*s} Z" fill="{kimono}"/>'
         f'<path d="M{x-4*s},{y+16*s} L{x},{y+26*s} L{x+4*s},{y+16*s}" fill="{WHITE}" stroke-width="1.2"/>'
         f'<path d="M{x-12*s},{y+34*s} L{x+12*s},{y+34*s} L{x+18*s},{y+54*s} L{x-18*s},{y+54*s} Z" fill="{hakama}"/>'
         f'<path d="M{x},{y+36*s} L{x},{y+54*s}" stroke-width="1.4"/>')
    if fan:
        t += (f'<path d="M{x+10*s},{y+20*s} L{x+24*s},{y+8*s}" stroke-width="{2.6*s}"/>'
              f'<path d="M{x+24*s},{y+8*s} L{x+16*s},{y-8*s} Q{x+30*s},{y-14*s} {x+40*s},{y-2*s} Z" fill="{GOLD}" stroke-width="1.4"/>'
              f'<path d="M{x-10*s},{y+20*s} L{x-20*s},{y+30*s}" stroke-width="{2.6*s}"/>')
    else:
        t += (f'<path d="M{x+10*s},{y+20*s} L{x+20*s},{y+14*s}" stroke-width="{2.6*s}"/>'
              f'<path d="M{x+18*s},{y+16*s} L{x+40*s},{y-14*s}" stroke="{BROWN}" stroke-width="{3.4*s}"/>'
              f'<path d="M{x+16*s},{y+12*s} L{x+22*s},{y+18*s}" stroke-width="{2*s}"/>'
              f'<path d="M{x-10*s},{y+20*s} L{x-20*s},{y+30*s}" stroke-width="{2.6*s}"/>')
    t += f'<circle cx="{x}" cy="{y}" r="{12*s}" fill="#f9e0cc"/>'
    t += f'<path d="M{x-12*s},{y-2*s} Q{x-12*s},{y-12*s} {x},{y-12*s} Q{x+12*s},{y-12*s} {x+12*s},{y-2*s} Q{x+6*s},{y-7*s} {x},{y-6*s} Q{x-6*s},{y-7*s} {x-12*s},{y-2*s} Z" fill="{INK}"/>'
    t += f'<path d="M{x-3*s},{y-12*s} L{x-2*s},{y-20*s} L{x+6*s},{y-22*s} L{x+3*s},{y-12*s} Z" fill="{INK}"/>'
    t += face(x, y + 2 * s, .55 * s)
    return t


def taiko(x, y, s=1.0):
    return (f'<ellipse cx="{x}" cy="{y+18*s}" rx="{20*s}" ry="{6*s}" fill="{DBROWN}"/>'
            f'<rect x="{x-20*s}" y="{y}" width="{40*s}" height="{18*s}" fill="{BRICK}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{20*s}" ry="{6*s}" fill="#f7e7cf"/>'
            f'<path d="M{x-16*s},{y+6*s} L{x-16*s},{y+20*s} M{x+16*s},{y+6*s} L{x+16*s},{y+20*s}" stroke-width="1.2"/>')


def lantern(x, y):
    return (f'<path d="M{x},{y-14} L{x},{y-6}" stroke-width="1.6"/>'
            f'<ellipse cx="{x}" cy="{y+6}" rx="10" ry="13" fill="{RED}"/>'
            f'<path d="M{x-9},{y+1} Q{x},{y+3} {x+9},{y+1} M{x-9},{y+11} Q{x},{y+13} {x+9},{y+11}" fill="none" stroke-width="1"/>'
            f'<rect x="{x-5}" y="{y-8}" width="10" height="3" fill="{INK}" stroke="none"/>'
            f'<rect x="{x-5}" y="{y+17}" width="10" height="3" fill="{INK}" stroke="none"/>')


# 1. 和風舞台：兩個 Q 版武士＋太鼓＋燈籠
card('stage', '手繪和風舞台，兩個可愛的 Q 版武士拿著扇子和竹刀，前面一個太鼓',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + f'<path d="M3,8 L237,8 L237,22 Q120,34 3,22 Z" fill="#6a4c93"/>'
     + ''.join(f'<path d="M{20+i*40},14 l6,6 l6,-6" fill="none" stroke="{GOLD}" stroke-width="1.6"/>' for i in range(6))
     + f'<path d="M3,134 L237,134 {BOT}" fill="#5a3d2b"/>'
     + ''.join(f'<path d="M{10+i*28},134 L{4+i*28},177" stroke="#7a5640" stroke-width="1.4"/>' for i in range(9))
     + lantern(30, 46) + lantern(210, 46)
     + samurai(84, 76, .95, RED, NAVY, True) + samurai(152, 76, .95, '#4f8fd6', INK, False)
     + taiko(120, 140, .9)
     + star(120, 40, 5) + star(56, 28, 3.4, WHITE) + star(186, 30, 3.4, '#8ff0ff'), bg=NIGHT)

# 2. 白天三場
card('shows', '手繪太陽下三個小時鐘，分別是 10:50、14:00、16:30 三場',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + f'<circle cx="208" cy="30" r="14" fill="{GOLD}"/>'
     + ''.join(f'<path d="M208,30 L{208+22*c},{30+22*s}" stroke="{GOLD}" stroke-width="2.4"/>'
               for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)])
     + f'<circle cx="208" cy="30" r="12" fill="{GOLD}"/>'
     + ''.join(
         f'<circle cx="{x}" cy="88" r="28" fill="{WHITE}" stroke-width="3"/>'
         f'<path d="M{x},88 L{x+hx},{88+hy} M{x},88 L{x+mx},{88+my}" stroke-width="3"/>'
         f'<circle cx="{x}" cy="88" r="3" fill="{INK}"/>'
         f'<text x="{x}" y="142" text-anchor="middle" font-size="16" font-weight="700" fill="{INK}" stroke="none">{lab}</text>'
         for x, hx, hy, mx, my, lab in [(52, -6, -13, -18, -10, '10:50'), (120, 13, -8, 0, -21, '14:00'), (188, 10, 11, 0, 21, '16:30')]), bg=SKY)

# 3. 便當或兩杯飲料
card('bento', '手繪一個便當盒和兩杯飲料，中間寫著「或」，表示每人選一種',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fff1dc"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#f6dcb6"/>'
     + f'<rect x="18" y="56" width="96" height="70" rx="10" fill="{INK}"/>'
     + f'<rect x="24" y="62" width="40" height="58" rx="4" fill="{WHITE}"/>'
     + ''.join(f'<circle cx="{34+(i%2)*14}" cy="{74+(i//2)*16}" r="5" fill="{WHITE}" stroke-width="1"/>' for i in range(6))
     + f'<rect x="68" y="62" width="40" height="27" rx="4" fill="#f7a35c"/>'
     + f'<rect x="68" y="93" width="40" height="27" rx="4" fill="{GREEN}"/>'
     + f'<circle cx="80" cy="76" r="5" fill="{RED}"/><path d="M90,104 q6,-6 12,0" fill="none" stroke-width="2"/>'
     + f'<text x="132" y="98" text-anchor="middle" font-size="18" font-weight="700" fill="{RED}" stroke="none">或</text>'
     + ''.join(f'<path d="M{x-14},60 L{x+14},60 L{x+10},124 L{x-10},124 Z" fill="{c}"/>'
               f'<path d="M{x-13},72 L{x+13},72" stroke-width="1.4"/>'
               f'<path d="M{x+4},60 L{x+10},42" stroke-width="2.4"/>'
               for x, c in [(168, '#ffd86b'), (208, '#ff9fb2')])
     + star(30, 30, 5) + star(130, 34, 4, PINK), bg='#fff1dc')

# 4. 12 月起變便宜
card('cal', '手繪兩張月曆，11 月那張貼著貴一點的標籤，12 月那張的標籤往下降',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef6ff"/>'
     + ''.join(
         f'<rect x="{x}" y="38" width="88" height="92" rx="10" fill="{WHITE}"/>'
         f'<rect x="{x}" y="38" width="88" height="24" rx="10" fill="{col}"/>'
         f'<text x="{x+44}" y="56" text-anchor="middle" font-size="14" font-weight="700" fill="{WHITE}" stroke="none">{m}</text>'
         + ''.join(f'<rect x="{x+8+c*19}" y="{70+r*18}" width="14" height="12" rx="2" fill="#f3ecff" stroke-width="1"/>'
                   for r in range(3) for c in range(4))
         for x, col, m in [(22, BRICK, '11 月'), (130, NAVY, '12 月')])
     + f'<path d="M112,84 L124,84" stroke-width="3"/><path d="M118,78 L126,84 L118,90" fill="none" stroke-width="3"/>'
     + f'<path d="M174,138 L174,160 M164,150 L174,162 L184,150" fill="none" stroke="{GREEN}" stroke-width="4"/>'
     + star(26, 26, 5) + star(214, 26, 5, PINK), bg='#eef6ff')


def rem(name, label, inner):
    F[name] = svg('sr-' + name, 120, 120, label, inner, bg='#fff3c4')


# 帶護照
rem('r-id', '手繪提醒：一本護照，旁邊寫 18+',
    f'<rect x="22" y="20" width="56" height="78" rx="6" fill="{NAVY}"/>'
    f'<circle cx="50" cy="52" r="12" fill="none" stroke="{GOLD}" stroke-width="2"/>'
    f'<path d="M36,80 L64,80" stroke="{GOLD}" stroke-width="2"/>'
    f'<circle cx="88" cy="82" r="20" fill="{RED}"/>'
    f'<text x="88" y="88" text-anchor="middle" font-size="16" font-weight="700" fill="{WHITE}" stroke="none">18+</text>')

# 加點只收現金
rem('r-cash', '手繪提醒：一張日圓鈔票和兩枚硬幣',
    f'<rect x="16" y="36" width="72" height="42" rx="5" fill="#cfe8c4"/>'
    f'<circle cx="52" cy="57" r="11" fill="none" stroke-width="2"/>'
    f'<text x="52" y="62" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}" stroke="none">¥</text>'
    f'<circle cx="88" cy="88" r="13" fill="{GOLD}"/><circle cx="70" cy="96" r="10" fill="#e6e6e6"/>')

# 官網訂了不能退
rem('r-norf', '手繪提醒：一張票被打了叉，旁邊一個日曆',
    f'<path d="M18,40 L82,40 L82,56 Q74,62 82,68 L82,84 L18,84 L18,68 Q26,62 18,56 Z" fill="{GOLD}"/>'
    f'<path d="M34,50 L66,76 M66,50 L34,76" stroke="{RED}" stroke-width="5"/>'
    f'<rect x="72" y="70" width="34" height="32" rx="4" fill="{WHITE}"/>'
    f'<rect x="72" y="70" width="34" height="9" rx="4" fill="{PINK}"/>')

print(save(F, OUT), 'files')
