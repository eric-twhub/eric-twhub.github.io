# -*- coding: utf-8 -*-
"""替既有的轉乘特價頁補上 deal.json。

gen.py 從 2026-09-21 起會在產生特價頁時一併寫出 deal.json，但在那之前
產生的頁面沒有。這支從頁面本身把來源資料解析回來——那些頁把觀測值都
印在自己身上（日圓車資、轉乘起點機票、直飛最低），所以重建得出來。

補不回來的是 fare_rt（機票是來回還是單程）：舊頁沒印，也無法反推，
一律填 null，由之後重產時重新判定。

用法：python3 tools_backfill_deal_data.py [--apply]
"""
import io, re, json, glob, sys, os

RATE = json.load(open('apple.json', encoding='utf-8'))['rate']['jpy_twd']
APPLY = '--apply' in sys.argv
n = lambda s: int(s.replace(',', ''))

made = skipped = 0
for path in sorted(glob.glob('deals/*transfer*/index.html')):
    d = os.path.dirname(path)
    slug = os.path.basename(d)
    if os.path.exists(os.path.join(d, 'deal.json')):
        skipped += 1; continue

    t = io.open(path, encoding='utf-8').read()
    g = lambda p: (re.search(p, t) or [None, None])[1] if re.search(p, t) else None
    own  = g(r'直飛.{1,6}目前最低 <b>NT\$([\d,]+)</b>')
    fl   = g(r'但飛到.{1,6}只要 <b>NT\$([\d,]+)</b>')
    twd  = g(r'約 NT\$([\d,]+) 單程')
    tot  = g(r'加起來約 <b>NT\$([\d,]+)</b>')
    # 熊本那條是「¥5,310（自由席）」，後面還有註記，不能只抓到數字就停
    jpyt = g(r'<td>((?:約 )?¥[^<]*)<br>')
    row  = re.search(r'<td>([^<]+ → [^<]+)<br><small[^>]*>([^<]+)</small></td><td>([^<]+)</td>', t)
    upd  = g(r'發布於 ([\d\- :]+)')
    if not all([own, fl, twd, tot, jpyt, row]):
        print('  ！解析失敗，跳過：', slug); skipped += 1; continue

    # slug 形如 2026-09-10-transfer-tokyo-sendai
    m = re.match(r'^\d{4}-\d{2}-\d{2}-transfer-([a-z-]+?)-([a-z-]+)$', slug)
    via, city = (m.group(1), m.group(2)) if m else (None, None)

    payload = dict(
        schema=1, slug=slug, generated=(upd or '').strip(),
        backfilled_from='index.html',          # 不是產生當下寫的，標記出來
        kind='transfer', city=city, via=via,
        own=n(own), fare={'price': n(fl)},
        fare_rt=None,                          # 舊頁沒印，無法反推
        jpy_text=jpyt, twd_one_way=n(twd), rate=RATE, rate_at='',
        route=row.group(1).strip(), mode=row.group(2).strip(), tm=row.group(3).strip(),
        total=n(tot), save=n(own) - n(tot))

    if APPLY:
        io.open(os.path.join(d, 'deal.json'), 'w', encoding='utf-8').write(
            json.dumps(payload, ensure_ascii=False, indent=1))
    made += 1
    if made <= 2 and not APPLY:
        print(json.dumps(payload, ensure_ascii=False, indent=1)[:420])

print(f"\n{'已寫入' if APPLY else '試算'} {made} 份，跳過 {skipped} 份")
