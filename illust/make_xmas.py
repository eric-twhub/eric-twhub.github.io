# 東京聖誕市集頁的手繪風插圖（2026-11-13）。
# 景點不能用別人的照片，所以全部自己畫：深咖啡色描邊＋粉彩填色＋可愛臉，
# 再用 feTurbulence/feDisplacementMap 讓線條抖一點，看起來像手畫的。
# 改圖就改這支，跑 `python3 illust/make_xmas.py` 重新輸出 illust/xmas/*.svg，gen.py 會把 SVG 直接內嵌進頁面。
import os

INK = '#5a3d2b'
RED = '#e4625a'
GREEN = '#6bb38a'
DGREEN = '#3f8a63'
GOLD = '#f4c152'
CREAM = '#fff6e6'
BROWN = '#c48a5c'
DBROWN = '#9a6440'
NAVY = '#34416e'
PINK = '#f6a5ad'
SKY = '#dfeefa'
GRAY = '#cfd8e6'
WHITE = '#ffffff'
BRICK = '#d8705e'

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xmas')


def svg(name, w, h, label, body, bg=CREAM, frame=True):
    fid = f'hd-{name}'
    back = (f'<rect x="3" y="3" width="{w-6}" height="{h-6}" rx="22" fill="{bg}" '
            f'stroke="{INK}" stroke-width="2" stroke-dasharray="1 0"/>' if frame else '')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            + (f'role="img" aria-label="{label}">' if label else 'aria-hidden="true">')
            + f'<defs><filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="7"/>'
            '<feDisplacementMap in="SourceGraphic" scale="2.8"/></filter></defs>'
            f'<g filter="url(#{fid})" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            f'{back}{body}</g></svg>')


def face(x, y, s=1.0, blush=True):
    d = 5 * s
    out = (f'<circle cx="{x-d}" cy="{y}" r="{2.1*s}" fill="{INK}" stroke="none"/>'
           f'<circle cx="{x+d}" cy="{y}" r="{2.1*s}" fill="{INK}" stroke="none"/>'
           f'<path d="M{x-2.6*s},{y+3.4*s} q{2.6*s},{2.8*s} {5.2*s},0" fill="none" stroke-width="{1.8*s}"/>')
    if blush:
        out += (f'<ellipse cx="{x-d-4*s}" cy="{y+3*s}" rx="{3*s}" ry="{1.8*s}" fill="{PINK}" stroke="none" opacity=".8"/>'
                f'<ellipse cx="{x+d+4*s}" cy="{y+3*s}" rx="{3*s}" ry="{1.8*s}" fill="{PINK}" stroke="none" opacity=".8"/>')
    return out


def snow(pts, r=2.4, col=WHITE):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="none"/>' for x, y in pts)


def star(x, y, r=7, col=GOLD):
    import math
    p = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        p.append(f'{x + rr*math.cos(a):.1f},{y + rr*math.sin(a):.1f}')
    return f'<polygon points="{" ".join(p)}" fill="{col}" stroke-width="1.6"/>'


def sparkle(x, y, r=5):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r},{y} L{x+r},{y}" stroke="{GOLD}" stroke-width="2"/>')


def tree(x, base, h=70, w=52, smile=True):
    # 三層圓角三角形的聖誕樹，頂上一顆星
    t = ''
    for i, (top, bot, ww) in enumerate([(0, .45, .62), (.25, .72, .82), (.5, 1.0, 1.0)]):
        y1 = base - h + h * top
        y2 = base - h + h * bot
        hw = w / 2 * ww
        t += (f'<path d="M{x},{y1} Q{x+hw*.3},{(y1+y2)/2} {x+hw},{y2} Q{x},{y2+6} {x-hw},{y2} '
              f'Q{x-hw*.3},{(y1+y2)/2} {x},{y1} Z" fill="{GREEN if i % 2 == 0 else DGREEN}"/>')
    t += f'<rect x="{x-6}" y="{base}" width="12" height="10" rx="2" fill="{DBROWN}"/>'
    t += star(x, base - h - 4, 8)
    for ox, oy, c in [(-12, -30, RED), (10, -42, GOLD), (14, -14, RED), (-16, -8, GOLD), (2, -24, WHITE)]:
        t += f'<circle cx="{x+ox}" cy="{base+oy}" r="3.4" fill="{c}" stroke-width="1.4"/>'
    if smile:
        t += face(x, base - 22, .8)
    return t


def hut(x, y, w=70, h=46, roof=RED, label_col=GOLD):
    # 木頭小屋：屋頂有積雪，窗口透出燈光
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{BROWN}"/>'
         + ''.join(f'<path d="M{x+4},{y+10*i} L{x+w-4},{y+10*i}" stroke-width="1.2" opacity=".55"/>' for i in range(1, h // 10))
         + f'<rect x="{x+10}" y="{y+10}" width="{w-20}" height="{h*.42:.0f}" rx="3" fill="{label_col}"/>'
         + f'<rect x="{x+6}" y="{y+h*.62:.0f}" width="{w-12}" height="6" rx="2" fill="{DBROWN}"/>'
         + f'<path d="M{x-8},{y+2} L{x+w/2},{y-30} L{x+w+8},{y+2} Z" fill="{roof}"/>'
         + f'<path d="M{x-6},{y+1} q6,7 12,0 q6,7 12,0 q6,7 12,0 q6,7 12,0 q6,7 12,0 q6,7 12,0 q6,7 12,0" '
           f'fill="{WHITE}" stroke-width="1.6" transform="scale(1)"/>'
         )
    return t


def lights(x1, y1, x2, y2, sag=14, n=7):
    # 一串彎彎的燈泡
    t = f'<path d="M{x1},{y1} Q{(x1+x2)/2},{max(y1,y2)+sag} {x2},{y2}" fill="none" stroke-width="1.6"/>'
    cols = [RED, GOLD, GREEN, PINK, GOLD]
    for i in range(1, n):
        u = i / n
        bx = (1-u)**2*x1 + 2*(1-u)*u*(x1+x2)/2 + u*u*x2
        by = (1-u)**2*y1 + 2*(1-u)*u*(max(y1, y2)+sag) + u*u*y2
        t += f'<ellipse cx="{bx:.1f}" cy="{by+5:.1f}" rx="3.2" ry="4.4" fill="{cols[i % len(cols)]}" stroke-width="1.3"/>'
    return t


def mug(x, y, s=1.0, col=RED):
    return (f'<path d="M{x+30*s},{y+8*s} q14,0 14,12 q0,12 -14,12" fill="none" stroke-width="{3*s}"/>'
            f'<rect x="{x}" y="{y}" width="{32*s}" height="{36*s}" rx="{7*s}" fill="{col}"/>'
            f'<path d="M{x+2*s},{y+6*s} L{x+30*s},{y+6*s}" stroke="{WHITE}" stroke-width="{3*s}"/>'
            + face(x + 16*s, y + 20*s, .8*s)
            + f'<path d="M{x+10*s},{y-6*s} q-5,-6 0,-12 q5,-6 0,-12 M{x+22*s},{y-6*s} q-5,-6 0,-12 q5,-6 0,-12" '
              f'fill="none" stroke-width="{1.8*s}" opacity=".6"/>')


def ground(w, y, col=WHITE):
    return f'<path d="M3,{y} Q{w*.25},{y-12} {w*.5},{y-2} T{w-3},{y-6} L{w-3},{w} L3,{w} Z" fill="{col}"/>'


FILES = {}

# ---- 封面：夜晚的市集，東京鐵塔在後面 ----
W, H = 720, 330
body = (f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="26" fill="{NAVY}"/>'
        + snow([(40, 40), (120, 70), (210, 30), (300, 60), (380, 25), (470, 50), (640, 36), (690, 90), (90, 120), (330, 110), (560, 110)], 2.6)
        + ''.join(sparkle(x, y) for x, y in [(160, 40), (430, 90), (610, 70)])
        # 月亮
        + f'<path d="M96,58 a22,22 0 1,0 26,30 a18,18 0 1,1 -26,-30 Z" fill="{GOLD}"/>'
        # 東京鐵塔（右後方）
        + f'<path d="M585,40 L556,262 L614,262 Z" fill="{RED}"/>'
        + f'<path d="M574,124 L596,124 L599,140 L571,140 Z" fill="{WHITE}"/>'
        + f'<rect x="566" y="166" width="38" height="16" rx="4" fill="{WHITE}"/>'
        + face(585, 173, .75, blush=True)
        + f'<path d="M585,40 L585,22" stroke-width="2.4"/>'
        + f'<path d="M562,262 Q585,226 608,262" fill="{NAVY}"/>'
        # 地面
        + f'<path d="M3,262 Q180,236 360,254 T717,248 L717,304 Q717,327 694,327 L26,327 Q3,327 3,304 Z" fill="{WHITE}"/>'
        # 燈串
        + lights(20, 120, 260, 128, 26, 9) + lights(260, 128, 520, 116, 26, 9)
        # 小屋
        + hut(150, 206, 84, 56, RED) + hut(266, 196, 96, 64, DGREEN) + hut(392, 210, 80, 52, RED)
        + face(308, 222, .9)
        # 大聖誕樹
        + tree(70, 262, 120, 86)
        # 熱紅酒杯
        + mug(486, 238, 1.15, RED)
        # 前景雪點
        + snow([(200, 290), (420, 300), (620, 296), (520, 286)], 3, GRAY)
        )
FILES['hero'] = svg('hero', W, H, '手繪插圖：夜晚的聖誕市集，有小木屋、聖誕樹、熱紅酒和東京鐵塔', body, frame=False)

# ---- 景點小插圖（統一 180×150）----
W, H = 180, 150


def spot(name, label, inner, bg=CREAM):
    FILES[name] = svg(name, W, H, label, inner + snow([(22, 24), (158, 30), (150, 112)], 2.2, GRAY), bg=bg)


# 東京鐵塔
spot('tower', '手繪東京鐵塔',
     f'<path d="M90,20 L62,130 L118,130 Z" fill="{RED}"/>'
     f'<path d="M83,52 L97,52 L99,62 L81,62 Z" fill="{WHITE}"/>'
     f'<rect x="70" y="74" width="40" height="18" rx="5" fill="{WHITE}"/>' + face(90, 81, .8)
     + f'<path d="M90,20 L90,8" /><path d="M68,130 Q90,104 112,130" fill="{CREAM}"/>'
     + f'<path d="M30,132 L150,132" />' + star(40, 50, 6) + sparkle(140, 60))

# 晴空塔
spot('skytree', '手繪東京晴空塔',
     f'<path d="M90,10 L78,132 L102,132 Z" fill="{SKY}"/>'
     f'<rect x="80" y="40" width="20" height="9" rx="3" fill="{GRAY}"/>'
     f'<rect x="73" y="64" width="34" height="16" rx="5" fill="{GRAY}"/>' + face(90, 70, .75)
     + f'<path d="M30,132 L150,132" />' + tree(140, 128, 40, 30, smile=False) + star(42, 48, 6))

# 東京車站（丸之內）
spot('station', '手繪東京車站紅磚站舍',
     f'<rect x="22" y="72" width="136" height="56" rx="3" fill="{BRICK}"/>'
     f'<path d="M22,92 L158,92 M22,110 L158,110" stroke="{WHITE}" stroke-width="2.6"/>'
     f'<path d="M24,72 Q40,40 56,72 Z" fill="#6c7a8c"/><path d="M124,72 Q140,40 156,72 Z" fill="#6c7a8c"/>'
     + ''.join(f'<rect x="{x}" y="78" width="8" height="10" rx="2" fill="{CREAM}" stroke-width="1.4"/>' for x in (66, 82, 98, 114))
     + tree(90, 128, 46, 34) + f'<path d="M14,132 L166,132" />')

# 六本木之丘＋麻布台之丘
spot('hills', '手繪六本木之丘與麻布台之丘的高樓和聖誕樹',
     f'<rect x="36" y="34" width="44" height="96" rx="18" fill="{GRAY}"/>'
     + ''.join(f'<path d="M44,{y} L72,{y}" stroke-width="1.3" opacity=".6"/>' for y in range(52, 128, 12))
     + f'<rect x="104" y="18" width="30" height="112" rx="13" fill="{SKY}"/>'
     + ''.join(f'<path d="M110,{y} L128,{y}" stroke-width="1.3" opacity=".6"/>' for y in range(36, 128, 12))
     + tree(90, 128, 54, 40) + f'<path d="M20,132 L160,132" />' + sparkle(150, 46))

# 上野：戴聖誕帽的熊貓
spot('panda', '手繪戴聖誕帽的熊貓',
     f'<ellipse cx="90" cy="112" rx="34" ry="24" fill="{WHITE}"/>'
     f'<ellipse cx="62" cy="108" rx="9" ry="13" fill="{INK}"/><ellipse cx="118" cy="108" rx="9" ry="13" fill="{INK}"/>'
     f'<circle cx="64" cy="46" r="11" fill="{INK}"/><circle cx="116" cy="46" r="11" fill="{INK}"/>'
     f'<circle cx="90" cy="70" r="30" fill="{WHITE}"/>'
     f'<ellipse cx="78" cy="70" rx="7" ry="9" fill="{INK}" transform="rotate(-25 78 70)"/>'
     f'<ellipse cx="102" cy="70" rx="7" ry="9" fill="{INK}" transform="rotate(25 102 70)"/>'
     f'<circle cx="79" cy="69" r="2" fill="{WHITE}" stroke="none"/><circle cx="101" cy="69" r="2" fill="{WHITE}" stroke="none"/>'
     f'<ellipse cx="90" cy="80" rx="4" ry="3" fill="{INK}"/>'
     f'<ellipse cx="72" cy="84" rx="4" ry="2.4" fill="{PINK}" stroke="none"/><ellipse cx="108" cy="84" rx="4" ry="2.4" fill="{PINK}" stroke="none"/>'
     f'<path d="M64,48 Q84,8 120,30 Q110,40 116,46 Z" fill="{RED}"/>'
     f'<path d="M62,50 Q90,40 118,48" stroke="{WHITE}" stroke-width="7"/>'
     f'<circle cx="122" cy="28" r="7" fill="{WHITE}"/>')

# 惠比壽：小城堡和廣場時鐘
spot('ebisu', '手繪惠比壽花園廣場的城堡建築和時鐘',
     f'<rect x="36" y="70" width="80" height="58" fill="{CREAM}"/>'
     f'<path d="M30,72 L76,44 L122,72 Z" fill="#6c7a8c"/>'
     f'<rect x="28" y="56" width="16" height="72" fill="{CREAM}"/><path d="M24,58 L36,32 L48,58 Z" fill="#6c7a8c"/>'
     f'<rect x="108" y="56" width="16" height="72" fill="{CREAM}"/><path d="M104,58 L116,32 L128,58 Z" fill="#6c7a8c"/>'
     f'<path d="M66,128 L66,106 Q76,94 86,106 L86,128" fill="{DBROWN}"/>'
     f'<rect x="50" y="84" width="10" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/><rect x="92" y="84" width="10" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     f'<path d="M150,128 L150,66" stroke-width="3"/><circle cx="150" cy="56" r="13" fill="{WHITE}"/>'
     f'<path d="M150,56 L150,48 M150,56 L156,59" stroke-width="2"/>'
     f'<path d="M14,130 L166,130" />')

# 日比谷 Creema：手作市集（毛線球＋棒針）
spot('craft', '手繪毛線球和棒針，代表手作市集',
     f'<circle cx="84" cy="88" r="34" fill="{RED}"/>'
     f'<path d="M56,72 Q84,96 112,70 M52,92 Q84,116 116,90 M66,60 Q90,84 104,120" fill="none" stroke-width="1.8"/>'
     f'<path d="M110,30 L64,128 M128,40 L96,132" stroke="{DBROWN}" stroke-width="4"/>'
     f'<circle cx="110" cy="30" r="5" fill="{GOLD}"/><circle cx="128" cy="40" r="5" fill="{GOLD}"/>'
     + face(84, 88, .9) + f'<path d="M118,104 q20,8 30,26" fill="none" stroke="{RED}" stroke-width="2.6"/>' + star(40, 40, 7))

# 東京聖誕市集（新豐洲、芝公園）：德式小屋＋熱紅酒
spot('market', '手繪聖誕市集的木頭小屋和熱紅酒杯',
     hut(30, 76, 82, 50, RED) + face(71, 92, .8) + mug(124, 92, .8, GREEN)
     + lights(14, 34, 166, 34, 16, 8) + f'<path d="M14,132 L166,132" />')

# 目黑：友善環境（葉子＋紙袋）
spot('eco', '手繪紙袋和葉子，代表友善環境的市集',
     f'<path d="M54,62 L126,62 L120,130 L60,130 Z" fill="{BROWN}"/>'
     f'<path d="M72,62 Q72,38 90,38 Q108,38 108,62" fill="none" stroke-width="3"/>'
     + face(90, 96, .9)
     + f'<path d="M126,44 Q160,40 156,78 Q122,82 126,44 Z" fill="{GREEN}"/><path d="M128,46 L152,74" stroke-width="1.6"/>'
     + f'<path d="M30,52 Q50,30 62,54 Q42,66 30,52 Z" fill="{DGREEN}"/>')

# 橫濱紅磚倉庫
spot('brick', '手繪橫濱紅磚倉庫',
     f'<rect x="20" y="66" width="140" height="62" rx="2" fill="{BRICK}"/>'
     f'<path d="M18,66 L162,66" stroke-width="3"/>'
     + ''.join(f'<path d="M{x},116 L{x},100 Q{x+6},92 {x+12},100 L{x+12},116 Z" fill="{CREAM}" stroke-width="1.6"/>' for x in (30, 54, 78, 102, 126))
     + ''.join(f'<rect x="{x}" y="76" width="10" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/>' for x in (32, 56, 80, 104, 128))
     + lights(20, 50, 160, 50, 10, 8) + tree(150, 128, 34, 26, smile=False) + f'<path d="M12,130 L168,130" />')

# 幕張：禮物盒（角色市集不能畫角色本人，只畫禮物）
spot('gift', '手繪聖誕禮物盒',
     f'<rect x="48" y="66" width="84" height="62" rx="6" fill="{GREEN}"/>'
     f'<rect x="42" y="54" width="96" height="18" rx="5" fill="{GREEN}"/>'
     f'<path d="M90,54 L90,128" stroke="{RED}" stroke-width="9"/>'
     f'<path d="M90,54 Q66,26 70,46 Q72,56 90,54 Q114,26 110,46 Q108,56 90,54 Z" fill="{RED}"/>'
     + face(90, 98, 1.0) + star(38, 40, 7) + sparkle(146, 44))

# ---- 裝飾：分隔線的燈串（橫長）----
FILES['garland'] = svg('garland', 720, 60, '', lights(10, 14, 360, 14, 26, 12) + lights(360, 14, 710, 14, 26, 12)
                       + ''.join(f'<path d="M{x},10 l0,-6" stroke-width="1.4"/>' for x in (10, 360, 710)), frame=False)

os.makedirs(OUT, exist_ok=True)
for k, v in FILES.items():
    open(os.path.join(OUT, k + '.svg'), 'w', encoding='utf-8').write(v)
print(len(FILES), 'files')
