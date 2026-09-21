# -*- coding: utf-8 -*-
"""把既有轉乘特價頁的日圓換算改成實際匯率。

特價頁寫出去就不會再重產，所以 gen.py 修好之後追不到舊頁。這支只動
「由匯率換算出來的數字」——車資 TWD、估算總計、省下多少——以及頁面上
標示的匯率本身。日圓車資、機票價、直飛價都是當天的觀測值，一律不動。

用法：python3 /tmp/fix_rate.py [--apply]
"""
import io, re, json, glob, sys

RATE = json.load(open('apple.json', encoding='utf-8'))['rate']['jpy_twd']
APPLY = '--apply' in sys.argv
n = lambda s: int(s.replace(',', ''))
f = lambda v: f'{v:,}'

done = skipped = 0
for path in sorted(glob.glob('deals/*transfer*/index.html')):
    t = io.open(path, encoding='utf-8').read()
    if '0.213 台幣' not in t:
        skipped += 1; continue
    m_j = re.search(r'¥([\d,]+)', t)
    m_f = re.search(r'但飛到.{1,6}只要 <b>NT\$([\d,]+)</b>', t)
    m_o = re.search(r'直飛.{1,6}目前最低 <b>NT\$([\d,]+)</b>', t)
    m_t = re.search(r'約 NT\$([\d,]+) 單程', t)
    if not all([m_j, m_f, m_o, m_t]):
        print('  ！解析失敗，跳過：', path); skipped += 1; continue

    jpy, fl, own, o_twd = n(m_j.group(1)), n(m_f.group(1)), n(m_o.group(1)), n(m_t.group(1))
    o_total, o_save = fl + o_twd * 2, own - (fl + o_twd * 2)
    twd = int(jpy * RATE)
    total, save = fl + twd * 2, own - (fl + twd * 2)

    # 只換「NT$舊值」這個完整樣式，避免誤傷其他同數字的地方
    sub = [(f'NT${f(o_twd)}', f'NT${f(twd)}'),
           (f'NT${f(o_total)}', f'NT${f(total)}'),
           (f'NT${f(o_save)}', f'NT${f(save)}')]
    new = t
    for a, b in sub:
        new = new.replace(a, b)
    new = new.replace('1 日圓 ≈ 0.213 台幣概估',
                      f'1 日圓 ≈ {RATE} 台幣換算')
    if new == t:
        print('  ！沒有任何替換：', path); skipped += 1; continue
    if APPLY:
        io.open(path, 'w', encoding='utf-8').write(new)
    done += 1
    if done <= 3 or not APPLY:
        print(f"{path.split('/')[1]}　車資 {f(o_twd)}→{f(twd)}　"
              f"總計 {f(o_total)}→{f(total)}　省 {f(o_save)}→{f(save)}")

print(f"\n{'已套用' if APPLY else '試算'} {done} 頁，跳過 {skipped} 頁（匯率 {RATE}）")
