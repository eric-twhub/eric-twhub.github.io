# -*- coding: utf-8 -*-
"""直接向台灣虎航官網取價，寫成 tigerair-fares.json。

為什麼要這支：票價資料庫收的是各家 OTA 的報價，虎航這種廉航主要自己賣，
OTA 拿到的是加價後的票。2026-10-13 抽六筆不同航線比對，六筆官網都比較便宜，
差 13% 到 37%。手動用 fare-overrides.json 補跟不上，因為最低價那幾個位子
賣掉就跳價：同一天同一班，上午查 2,799，下午再查就變 3,299。

資料來源是虎航訂位系統自己的每日票價 API（GraphQL，appDailyPrices），
就是訂位頁上日期列那排價格的來源，不需要登入也不需要建立訂位 session。
一次可以要一整年，所以全部航線加起來只有二十幾次請求。

航線不寫死：先問官網「這個出發地有哪些航點」，再逐條抓。寫死的清單會過期，
而過期的清單會讓人誤判某條航線不存在。

注意：抓到的是最低票價（tigerlight），不含託運行李。

用法：python3 scan_tigerair.py [--months 12] [--out tigerair-fares.json]
"""
import json, sys, datetime, urllib.request, urllib.error, time

try:                                   # 一律以台北時間為準（CI 執行環境是 UTC）
    from zoneinfo import ZoneInfo
    TPE = ZoneInfo('Asia/Taipei')
except Exception:
    TPE = datetime.timezone(datetime.timedelta(hours=8))

API = 'https://api-book.tigerairtw.com/graphql'
DESTS = ('https://api-book.tigerairtw.com/api/general/'
         'available-destinations?locale=zh-TW&origin=%s')
TW = ('TPE', 'RMQ', 'KHH', 'TNN')          # 虎航有飛的台灣出發地
UA = 'Mozilla/5.0 (compatible; twhub-fare-check/1.0)'

Q_DAILY = ('query appDailyPrices($input: QueryDailyPricesInput!) '
           '{ appDailyPrices(input: $input) { origin destination date amount } }')


def _post(payload, tries=3):
    body = json.dumps(payload).encode('utf-8')
    for k in range(tries):
        try:
            req = urllib.request.Request(
                API, data=body,
                headers={'Content-Type': 'application/json', 'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(2 * (k + 1))


def _get(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(2 * (k + 1))


def jp_routes():
    """每個台灣出發地飛日本的航點。MAC 碼（XX6 這種多機場代碼）不算航點。"""
    out = {}
    for o in TW:
        try:
            d = _get(DESTS % o)
        except Exception as e:
            print(f'   ⚠ {o} 的航點查不到：{e}')
            continue
        codes = []
        for grp in (d.get('data') or {}).get('appAvailableDestinations') or []:
            if ((grp.get('country') or {}).get('code2')) != 'JP':
                continue
            for m in grp.get('stationMenus') or []:
                st = m.get('station') or {}
                if st.get('stationCode'):
                    codes.append(st['stationCode'])
        if codes:
            out[o] = sorted(set(codes))
    return out


def daily(o, d, since, until):
    """某條航線在一段期間內，每天的最低票價。沒有班機的日子不會出現。"""
    r = _post({'query': Q_DAILY, 'variables': {'input': {
        'origin': o, 'destination': d, 'source': 'resultPageCal',
        'userCurrency': 'TWD', 'since': since, 'until': until}}})
    if r.get('errors'):
        raise RuntimeError(r['errors'][0].get('message', '')[:120])
    return {x['date']: x['amount']
            for x in (r.get('data') or {}).get('appDailyPrices') or []
            if x.get('amount')}


def main():
    months = 12
    out_path = 'tigerair-fares.json'
    for i, a in enumerate(sys.argv):
        if a == '--months' and i + 1 < len(sys.argv):
            months = int(sys.argv[i + 1])
        if a == '--out' and i + 1 < len(sys.argv):
            out_path = sys.argv[i + 1]

    # 用台北的今天，不是 runner 的今天。CI 跑在 UTC，台北入夜後兩者差一天，
    # 會害今天出發的班機整天抓不到。
    now = datetime.datetime.now(TPE)
    today = now.date()
    since = today.isoformat()
    until = (today + datetime.timedelta(days=int(months * 30.5))).isoformat()

    rt = jp_routes()
    if not rt:
        sys.exit('一條航線都查不到，不覆寫既有檔案')
    pairs = []
    for o, ds in rt.items():
        for d in ds:
            pairs.append((o, d))
            pairs.append((d, o))        # 回程方向也要，來回票要兩段相加

    fares, fail = {}, []
    for o, d in pairs:
        try:
            got = daily(o, d, since, until)
        except Exception as e:
            fail.append(f'{o}-{d}: {e}')
            continue
        if got:
            fares[f'{o}-{d}'] = dict(sorted(got.items()))
        time.sleep(0.4)                 # 不要連打

    if not fares:
        sys.exit('一條航線都沒抓到價格，不覆寫既有檔案')

    doc = {
        '_說明': '台灣虎航官網的每日最低票價，單位 TWD，單程、含稅。',
        '_來源': '虎航訂位系統 appDailyPrices（GraphQL），'
                '就是訂位頁日期列那排價格的來源。',
        '_來源網址': 'https://booking.tigerairtw.com/',
        '_為什麼要': '票價資料庫收的是 OTA 報價，虎航主要自己賣，'
                 'OTA 拿到的是加價後的票，查下來官網便宜 13% 到 37%。',
        '_不含什麼': '抓到的是最低票價（tigerlight），不含託運行李。',
        '_會變動': '最低價那幾個位子賣掉就跳價，同一天上午與下午可能不同，'
               '所以這份每天重抓，不要拿舊的用。',
        '_來回不等於兩段相加': '虎航來回一起訂常比兩段單程相加便宜，'
                     '所以用這份算出來的來回價是上限，不是最優惠價。',
        'generated': now.strftime('%Y-%m-%d %H:%M'),
        '_時區': '台北時間。站上其他時間戳也都是台北時間，不要混到 UTC。',
        'since': since, 'until': until,
        'routes': rt,
        'fares': dict(sorted(fares.items())),
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)

    n_days = sum(len(v) for v in fares.values())
    print(f'✅ 虎航官網票價：{len(fares)} 條航線方向、{n_days} 個有班機的日期'
          f'（{since} 到 {until}）→ {out_path}')
    for o in sorted(rt):
        print(f'   {o} 飛日本 {len(rt[o])} 個點：{"、".join(rt[o])}')
    for x in fail:
        print(f'   ⚠ 抓不到 {x}')


if __name__ == '__main__':
    main()
