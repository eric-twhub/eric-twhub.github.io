"""cards.json 的日期檢查，兩件事：

一、比對發卡行官網的逐月登錄時間和 reg_events（要連網）。
二、檢查每張卡的 period 有沒有過期（純本機日期比對，不連網）。

reg_events 的日期是人工填的。填錯不會有任何錯誤訊息，登錄日曆照樣算得出一個
看起來很合理的日期，讀者就會在錯的那天去登錄，而這些活動多半限量。

2026-10-18 踩過一次：富邦的交通卡加碼被填成每月 19 日，但 19 日其實是另一個
活動（亞洲精選）的開放日，兩者的每月名額同樣是 10,000 名所以被混在一起。
日曆因此在開放當天顯示「今天沒有活動開放登錄」。

失敗條件分兩種，因為這支會跑在每輪票價更新裡：
  抓不到、頁面結構變了、對不到活動段落 → 警告，離開碼 0。
    那代表這次驗不了，不代表資料錯。發卡行網站一抖就讓整輪票價停掉太貴。
  抓到了而且日期對不起來 → 錯誤，離開碼 1。那是真的要修的資料錯誤。
"""

import datetime
import json
import re
import sys
import urllib.request

# 期間快到期的提前警告天數。給自己留時間回查，而不是過期當天才炸。
EXPIRY_WARN_DAYS = 14

# period 的寫法不統一，有「2026/7/1 – 2026/12/31」，也有
# 「秋日遊 2026/10/1 – 2026/11/30；其餘方案依國泰世華公告」這種。
# 所以不去解析格式，改成抓出字串裡所有完整日期、取最晚的那個當結束日。
DATE_RE = re.compile(r'(20\d\d)/(\d{1,2})/(\d{1,2})')

UA = 'Mozilla/5.0 (compatible; eric-twhub-checker/1.0)'

# anchor 是那個活動在官網上的標題片段，用來把頁面切成一段一段。
# 同一頁會有好幾組「幾月：日期」清單，只靠名額或日期分不出是哪一個活動，
# 一定要先用標題切段，這正是上次填錯的原因。
SOURCES = [
    {
        'card': '台北富邦 J 卡',
        'url': ('https://www.fubon.com/banking/Personal/credit_card/'
                'all_card/omiyage/omiyage.htm'),
        'sections': [
            {'what': '日本交通卡加碼 7%', 'anchor': '日本三大交通卡最高'},
            {'what': '亞洲精選加碼 5%', 'anchor': 'J卡亞洲精選最高享'},
            {'what': '日韓泰加碼', 'anchor': '日韓泰加碼3%'},
        ],
    },
    {
        'card': '聯邦吉鶴卡',
        'url': 'https://activity.ubot.com.tw/2026JiHoCard/japan.htm',
        'sections': [
            {'what': '交通卡儲值 1.5%', 'anchor': '日本三大交通卡儲值1.5%-注意事項'},
        ],
    },
]

# 查過但沒納入的：
#   中信 LINE Pay 卡  page_travel.html 回 302 轉址，直讀抓不到內容。
#   永豐現金回饋 JCB   頁面上讀不到任何登錄日期文字，應是前端算繪。
# 這兩家要改用瀏覽器才讀得到，不適合放在每輪票價更新裡跑。

# 年份三碼是民國年（聯邦這樣寫），四碼是西元年（富邦這樣寫）。
MONTH_RE = re.compile(
    r'(\d{1,2})月：\s*(\d{3,4})/(\d{1,2})/(\d{1,2})\s*(\d{1,2}):(\d{2})\s*起')


def fetch_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode('utf-8', 'replace')
    t = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = (t.replace('&nbsp;', ' ').replace('&amp;', '&')
          .replace('&lt;', '<').replace('&gt;', '>'))
    return re.sub(r'\s+', ' ', t)


def section_slices(text, sections):
    """把頁面切成 {what: 那一段的文字}。對不到的 anchor 回報出來。"""
    found, missing = [], []
    for s in sections:
        i = text.find(s['anchor'])
        if i < 0:
            missing.append(s)
        else:
            found.append((i, s))
    found.sort()
    out = {}
    for n, (i, s) in enumerate(found):
        end = found[n + 1][0] if n + 1 < len(found) else len(text)
        out[s['what']] = text[i:end]
    return out, missing


def read_schedule(chunk):
    """從一段文字裡讀出逐月的登錄日與時間。

    回傳 (day, time, 月份數)。各月的日期要一致才算得出一個「每月幾號」，
    不一致就回 None，因為本站的資料模型只存得下一個固定的日子。
    """
    hits = MONTH_RE.findall(chunk)
    if not hits:
        return None
    days = {int(d) for _, _, _, d, _, _ in hits}
    times = {f'{int(h):02d}:{mi}' for _, _, _, _, h, mi in hits}
    if len(days) != 1 or len(times) != 1:
        return None
    return days.pop(), times.pop(), len(hits)


def check_periods(cards, today):
    """每張卡的 period 有沒有過期。

    2026-10-20 踩到：中信 LINE Pay 卡的 period 還停在 2026/7/1 到 9/30，
    已經過了三週，而比較表那一欄照樣顯示。登錄日期有人驗，活動期間沒有，
    是做別的事時偶然翻到的。

    這一段不連網，所以官網抓不到也不影響它。
    """
    bad, warn = [], []
    for c in cards['cards']:
        p = c.get('period') or ''
        ds = [datetime.date(int(y), int(m), int(d))
              for y, m, d in DATE_RE.findall(p)]
        if not ds:
            warn.append(f"{c['name']}：period 裡讀不出完整日期（{p or '空的'}），驗不了")
            continue
        end = max(ds)
        left = (end - today).days
        if left < 0:
            bad.append(f"{c['name']}：活動期間寫到 {end}，已經過了 {-left} 天。"
                       f"原文「{p}」")
        elif left <= EXPIRY_WARN_DAYS:
            warn.append(f"{c['name']}：活動期間 {end} 到期，剩 {left} 天，該回查了")
        else:
            print(f'  期間還在　{c["name"]}：到 {end}，剩 {left} 天')
    return bad, warn


def main():
    cards = json.load(open('cards.json', encoding='utf-8'))
    today = datetime.date.today()
    bad_period, warn_period = check_periods(cards, today)
    by_name = {c['name']: c for c in cards['cards']}
    problems, notes = [], []

    for src in SOURCES:
        card = by_name.get(src['card'])
        if card is None:
            notes.append(f"cards.json 裡沒有「{src['card']}」，略過")
            continue
        try:
            text = fetch_text(src['url'])
        except Exception as e:
            notes.append(f"{src['card']}：抓不到官網（{type(e).__name__}），這次驗不了")
            continue

        chunks, missing = section_slices(text, src['sections'])
        for s in missing:
            notes.append(f"{src['card']}：頁面上找不到「{s['anchor']}」，"
                         f"可能改版了，「{s['what']}」這次驗不了")

        events = {e['what']: e for e in (card.get('reg_events') or [])}
        for s in src['sections']:
            chunk = chunks.get(s['what'])
            if chunk is None:
                continue
            got = read_schedule(chunk)
            if got is None:
                notes.append(f"{src['card']}／{s['what']}："
                             f"讀不出一致的逐月登錄時間，這次驗不了")
                continue
            day, time_, months = got
            ev = events.get(s['what'])
            if ev is None:
                notes.append(f"{src['card']}／{s['what']}：官網寫每月 {day} 日 {time_}"
                             f"（{months} 個月份），但 cards.json 沒有這一筆")
                continue
            if ev.get('day') != day or ev.get('time') != time_:
                problems.append(
                    f"{src['card']}／{s['what']}：官網是每月 {day} 日 {time_}"
                    f"（{months} 個月份都一致），cards.json 寫的是"
                    f"每月 {ev.get('day')} 日 {ev.get('time')}")
            else:
                print(f"  對得上　{src['card']}／{s['what']}：每月 {day} 日 {time_}")

    for n in notes:
        print(f'::warning::登錄日期比對：{n}')
    for n in warn_period:
        print(f'::warning::活動期間：{n}')
    for p in problems:
        print(f'::error::登錄日期對不起來：{p}')
    for p in bad_period:
        print(f'::error::活動期間已過期：{p}')

    if problems:
        print('\n修正 cards.json 的 reg_events 之後再推。'
              '同一頁常有好幾個活動的登錄日清單，確認你改的是對的那一個。')
    if bad_period:
        print('\n過期的卡要去發卡行官網查現行期間，把 cards.json 的 period 更新。'
              '順便看回饋率、上限與名額有沒有一起改，換檔期時那幾項常常一起動。')
    return 1 if (problems or bad_period) else 0


if __name__ == '__main__':
    sys.exit(main())
