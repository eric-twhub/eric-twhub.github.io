"""抓 ShopBack 台灣與 LINE 旅遊的回饋率，寫進 cashback.json 與 cashback-log.json。

給 /japan-cashback/ 用。兩邊都是公開的商家頁（robots.txt 允許），每個商家一頁、
每輪十幾個請求，中間停一秒。

- ShopBack：頁面內嵌的 currentOffer（表格看得到的層級比內嵌資料少，所以讀資料）。
  offerType=BASELINE 是平時，其他（UPSIZE、FLASH…）是加碼，endAt 是結束時間。
  頁面不給平時值，所以每次抓到 BASELINE 就記進 base_sb，加碼時拿它當「平時」。
- LINE 旅遊：buy.line.me/u/partner/<id> 的 APOLLO_STATE。merchantReward 有
  加碼前後的點數與起訖時間（毫秒）。

抓失敗的商家保留上一次的資料（各自帶 at 時間），整支程式一律 exit 0，
不要因為某一家改版就擋住整輪建置。gen.py 看 at 判斷資料夠不夠新。
"""
import json, os, re, sys, time, datetime, urllib.request

TZ = datetime.timezone(datetime.timedelta(hours=8))
NOW = datetime.datetime.now(TZ)
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0 Safari/537.36')
SRC = json.load(open('cashback-src.json', encoding='utf-8'))
OUT, LOG = 'cashback.json', 'cashback-log.json'


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'zh-TW,zh;q=0.9'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', 'replace')


def sb_offer(h):
    h = h.replace('\\"', '"')
    i = h.find('"currentOffer":')
    if i < 0:
        return None
    j = h.find('{', i)
    dep = 0
    for k in range(j, len(h)):
        c = h[k]
        if c == '{':
            dep += 1
        elif c == '}':
            dep -= 1
            if dep == 0:
                break
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), h[j:k + 1])
    o = json.loads(s)
    tiers = [[re.sub(r'\s+', ' ', t['label']).strip(), t['value']]
             for t in o.get('cashbackTiers') or [] if t.get('type') == 'PERCENT']
    end = o.get('endAt')
    if end:
        end = datetime.datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(TZ).isoformat(timespec='minutes')
    return {'type': o.get('offerType'), 'end': end, 'tiers': tiers}


def line_partner(h):
    m = re.search(r'data-hid="APOLLO_STATE">(.*?)</script>', h, re.S)
    s = m.group(1).strip()
    d = json.loads(s[s.find('{'):].rstrip(';'))

    def ts(x):
        return datetime.datetime.fromtimestamp(x / 1000, TZ).isoformat(timespec='minutes') if x else None
    for k, v in d['ROOT_QUERY'].items():
        if not k.startswith('merchant('):
            continue
        r = v.get('merchantReward') or {}
        p = v.get('point') or {}
        now = v.get('displayPoints') or []
        now = max(now) if now else None
        lim = p.get('limit')
        return {'name': v.get('name'), 'now': now,
                'prev': r.get('previousPoint'), 'start': ts(r.get('rewardStartTime')),
                'end': ts(r.get('rewardEndTime')), 'cap': lim if lim and lim > 0 else None,
                'disabled': bool(v.get('disabled'))}
    return None


def main():
    old = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    log = json.load(open(LOG, encoding='utf-8')) if os.path.exists(LOG) else []
    sb, line = old.get('sb', {}), old.get('line', {})
    base_sb = {k: v for k, v in SRC['base_seed'].items() if not k.startswith('_')}
    base_sb.update(old.get('base_sb') or {})
    at = NOW.isoformat(timespec='minutes')
    ok = bad = 0
    for mc in SRC['merchants']:
        if mc.get('sb'):
            try:
                o = sb_offer(get(f'https://www.shopback.com.tw/{mc["sb"]}'))
                if not o or not o['tiers']:
                    raise ValueError('沒有 currentOffer')
                o['at'] = at
                sb[mc['sb']] = o
                if o['type'] == 'BASELINE':
                    base_sb[mc['sb']] = {'at': NOW.date().isoformat(), 'src': 'scan', 'tiers': o['tiers']}
                ok += 1
            except Exception as e:
                print(f'::warning::ShopBack {mc["sb"]} 抓取失敗：{e}', file=sys.stderr)
                bad += 1
            time.sleep(1)
        for cat, pid in (mc.get('line') or {}).items():
            try:
                o = line_partner(get(f'https://buy.line.me/u/partner/{pid}'))
                if not o or o['now'] is None:
                    raise ValueError('沒有 merchant 資料')
                o['at'] = at
                line[pid] = o
                ok += 1
            except Exception as e:
                print(f'::warning::LINE {pid} 抓取失敗：{e}', file=sys.stderr)
                bad += 1
            time.sleep(1)

    # 加碼紀錄：同一檔（來源、商家、層級、比例、結束時間）只記一筆，更新 last_seen。
    # ShopBack 不給開始時間，用第一次看到的時間代替。
    idx = {(e['src'], e['id'], e['label'], e['value'], e['end']): e for e in log}

    def note(src, id_, label, value, base, start, end):
        key = (src, id_, label, value, end)
        e = idx.get(key)
        if e:
            e['last_seen'] = at
        else:
            e = {'src': src, 'id': id_, 'label': label, 'value': value, 'base': base,
                 'start': start, 'end': end, 'first_seen': at, 'last_seen': at}
            log.append(e)
            idx[key] = e
    for slug, o in sb.items():
        if o.get('at') != at or o['type'] == 'BASELINE' or not o.get('end'):
            continue   # 沒有結束時間的加碼（樂天旅遊長期掛著）不算一檔
        base = dict((l, v) for l, v in (base_sb.get(slug) or {}).get('tiers', []))
        cat = next((m.get('sb_cat') or {} for m in SRC['merchants'] if m.get('sb') == slug), {})
        for l, v in o['tiers']:
            # 平時值已知：比平時高才算加碼；還不知道平時值：只記有對到本頁類別的層級
            if (l in base and v > base[l]) or (l not in base and l in cat):
                note('sb', slug, l, v, base.get(l), None, o['end'])
    for pid, o in line.items():
        if o.get('at') != at or not o.get('prev') or o['now'] <= o['prev']:
            continue
        note('line', pid, o['name'], o['now'], o['prev'], o['start'], o['end'])
    # 只留 120 天
    cut = (NOW - datetime.timedelta(days=120)).isoformat()
    log = [e for e in log if e['last_seen'] >= cut]

    # 頁面與瀏覽器端共用的「商家 × 類別」列。正規化只在這裡做一次，
    # gen.py 與頁面上的 JS 都只是照著排版，兩邊才不會算出不一樣的東西。
    rows = []
    for mc in SRC['merchants']:
        o = sb.get(mc.get('sb') or '')
        _bs = base_sb.get(mc.get('sb') or '') or {}
        base = dict((l, v) for l, v in _bs.get('tiers', []))
        bmax = _bs.get('max')
        for cat in SRC['cats']:
            r = {'m': mc['key'], 'name': mc['name'], 'cat': cat}
            if not mc.get('sb'):
                r['sb'] = {'st': 'none'}            # ShopBack 沒有這家
            elif not o:
                r['sb'] = {'st': 'err'}             # 沒抓到
            else:
                labs = [l for l, c in (mc.get('sb_cat') or {}).items() if c == cat]
                hit = [(l, v) for l, v in o['tiers'] if l in labs]
                if not hit:
                    r['sb'] = {'st': 'nocat'}       # 這家在 ShopBack 沒有這類
                else:
                    l, v = max(hit, key=lambda x: x[1])
                    b = base.get(l)
                    # 加碼但沒有結束時間（樂天旅遊長期掛 UPSIZE）就當平時。
                    # 平時值不知道時：有「平時最高」就比它，否則標加碼、平時值留空。
                    if o['type'] == 'BASELINE' or not o.get('end'):
                        boost, b = False, v
                    elif b is not None:
                        boost = v > b
                    elif bmax is not None:
                        boost = v > bmax
                    else:
                        boost = True
                    r['sb'] = {'st': 'ok', 'now': v, 'base': b, 'bmax': bmax if b is None else None,
                               'boost': boost, 'end': o['end'] if boost else None,
                               'label': l, 'at': o['at'], 'url': f'https://www.shopback.com.tw/{mc["sb"]}'}
            pid = (mc.get('line') or {}).get(cat)
            lo = line.get(pid) if pid else None
            if not (mc.get('line') or {}):
                r['line'] = {'st': 'none'}
            elif not pid:
                r['line'] = {'st': 'nocat'}
            elif not lo:
                r['line'] = {'st': 'err'}
            else:
                boost = bool(lo.get('prev')) and lo['now'] > lo['prev']
                r['line'] = {'st': 'ok', 'now': lo['now'], 'base': lo['prev'] if boost else lo['now'],
                             'boost': boost, 'start': lo['start'] if boost else None,
                             'end': lo['end'] if boost else None, 'cap': lo.get('cap'),
                             'at': lo['at'], 'url': f'https://buy.line.me/u/partner/{pid}'}
            if r['sb']['st'] in ('none', 'nocat') and r['line']['st'] in ('none', 'nocat'):
                continue
            rows.append(r)

    json.dump({'checked': at if ok else old.get('checked'), 'rows': rows,
               'sb': sb, 'line': line, 'base_sb': base_sb},
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(log, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'回饋率：成功 {ok}、失敗 {bad}')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:      # 不擋建置
        print(f'::warning::scan_cashback 整支失敗：{e}', file=sys.stderr)
