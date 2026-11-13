# 手繪風插圖的共用工具（2026-11-13）。
# 全站的插圖都用這套：深咖啡色描邊＋粉彩填色＋可愛臉，
# 再用 feTurbulence/feDisplacementMap 讓線條抖一點，看起來像手畫的。
# 景點不能用別人的照片，所以全部自己畫；角色 IP（吉伊卡哇、寶可夢、哆啦A夢、吉卜力等）不畫角色本人。
import os, math

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




def sticker(name, label, inner, bg=CREAM, W=180, H=150, dots=True):
    """景點／主題貼紙：180×150、米色圓角框、角落幾點雪花。"""
    return svg(name, W, H, label, inner + (snow([(22, 24), (158, 30), (150, 112)], 2.2, GRAY) if dots else ''), bg=bg)


def save(files, out):
    os.makedirs(out, exist_ok=True)
    for k, v in files.items():
        open(os.path.join(out, k + '.svg'), 'w', encoding='utf-8').write(v)
    return len(files)
