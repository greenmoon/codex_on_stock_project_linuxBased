from __future__ import annotations

import csv
import datetime as dt
import io
import json
import ssl
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "data" / "stocks"
SSL_CONTEXT = ssl._create_unverified_context()

TPEX_CODES = [
    "3555",
    "3529",
    "5351",
    "3324",
    "3081",
    "4971",
    "3163",
    "4979",
    "3363",
    "6488",
    "6735",
    "5347",
    "3105",
]


def parse_number(value):
    text = str(value or "").replace(",", "").replace("+", "").replace("X", "").strip()
    if text in {"", "--", "---", "----", "null", "None", "除權息"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def roc_to_date(value, fallback):
    text = str(value or "").replace("-", "/").strip()
    parts = text.split("/")
    if len(parts) != 3:
        return fallback.isoformat()
    try:
        year, month, day = [int(x) for x in parts]
    except ValueError:
        return fallback.isoformat()
    if year < 1911:
        year += 1911
    return f"{year:04d}-{month:02d}-{day:02d}"


def ad_to_roc(day):
    return f"{day.year - 1911}/{day.month:02d}/{day.day:02d}"


def candidate_tpex_daily_calls(day):
    base = "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php"
    roc_day = ad_to_roc(day)
    return [
        (base, {"l": "zh-tw", "o": "json", "se": "EW", "d": roc_day}),
        (base, {"l": "zh-tw", "o": "data", "se": "EW", "d": roc_day}),
        (base, {"l": "zh-tw", "o": "csv", "se": "EW", "d": roc_day}),
        (base, {"l": "zh-tw", "o": "json", "se": "EW"}),
        (base, {"l": "zh-tw", "o": "data", "se": "EW"}),
    ]


def find_key(keys, words):
    return next((key for key in keys if any(word in str(key) for word in words)), None)


def parse_tpex_object(obj, fallback):
    if not isinstance(obj, dict):
        return []

    table = (obj.get("tables") or [{}])[0] if isinstance(obj.get("tables"), list) else {}
    fields = table.get("fields") or table.get("headers") or obj.get("fields") or obj.get("headers") or []
    data = table.get("data") or table.get("aaData") or obj.get("aaData") or obj.get("data") or []
    if not isinstance(data, list) or not data:
        return []

    rows = []
    if isinstance(data[0], dict):
        for item in data:
            keys = list(item.keys())
            k_date = find_key(keys, ["資料日期", "日期"])
            k_code = find_key(keys, ["代號", "股票代號", "證券代號"])
            k_name = find_key(keys, ["名稱", "股票名稱", "證券名稱"])
            k_close = find_key(keys, ["收盤"])
            k_open = find_key(keys, ["開盤"])
            k_high = find_key(keys, ["最高"])
            k_low = find_key(keys, ["最低"])
            k_vol = find_key(keys, ["成交股數", "成交仟股", "成交數量"])
            rows.append(make_row(
                fallback,
                item.get(k_date),
                item.get(k_code),
                item.get(k_name),
                item.get(k_open),
                item.get(k_high),
                item.get(k_low),
                item.get(k_close),
                item.get(k_vol),
            ))
        return [row for row in rows if row]

    header = [str(x).strip() for x in fields] if fields else []
    if not header:
        header = ["資料日期", "代號", "名稱", "收盤", "漲跌", "開盤", "最高", "最低", "成交股數"]

    def idx(words):
        return next((i for i, h in enumerate(header) if any(word in h for word in words)), None)

    indexes = {
        "date": idx(["資料日期", "日期"]),
        "code": idx(["代號", "股票代號", "證券代號"]),
        "name": idx(["名稱", "股票名稱", "證券名稱"]),
        "close": idx(["收盤"]),
        "open": idx(["開盤"]),
        "high": idx(["最高"]),
        "low": idx(["最低"]),
        "volume": idx(["成交股數", "成交仟股", "成交數量"]),
    }

    for item in data:
        if not isinstance(item, list):
            continue
        if indexes["code"] is None and len(item) >= 9:
            indexes = {"date": 0, "code": 1, "name": 2, "close": 3, "open": 5, "high": 6, "low": 7, "volume": 8}
        rows.append(make_row_from_list(fallback, item, indexes))
    return [row for row in rows if row]


def parse_tpex_text(text, fallback):
    text = (text or "").strip()
    if len(text) < 20:
        return []
    head = text[:500].lower()
    if "<html" in head or "<!doctype" in head:
        return []
    if text.startswith("{"):
        try:
            return parse_tpex_object(json.loads(text), fallback)
        except json.JSONDecodeError:
            return []

    raw_lines = [
        line.strip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if line.strip() and not line.strip().startswith("=")
    ]
    parsed = list(csv.reader(io.StringIO("\n".join(raw_lines))))
    parsed = [row for row in parsed if len(row) >= 4]
    if not parsed:
        return []

    header_idx = None
    for i, row in enumerate(parsed):
        joined = ",".join(row)
        if ("代號" in joined or "證券代號" in joined) and "收盤" in joined and "開盤" in joined:
            header_idx = i
            break

    if header_idx is None:
        obj = {"fields": ["資料日期", "代號", "名稱", "收盤", "漲跌", "開盤", "最高", "最低", "成交股數"], "data": parsed}
    else:
        obj = {"fields": parsed[header_idx], "data": parsed[header_idx + 1:]}
    return parse_tpex_object(obj, fallback)


def make_row_from_list(fallback, item, indexes):
    def get(name):
        i = indexes[name]
        return item[i] if i is not None and i < len(item) else None

    return make_row(
        fallback,
        get("date"),
        get("code"),
        get("name"),
        get("open"),
        get("high"),
        get("low"),
        get("close"),
        get("volume"),
    )


def make_row(fallback, raw_date, raw_code, raw_name, raw_open, raw_high, raw_low, raw_close, raw_volume):
    code = str(raw_code or "").strip()
    close = parse_number(raw_close)
    if not code or close is None:
        return None
    open_ = parse_number(raw_open)
    high = parse_number(raw_high)
    low = parse_number(raw_low)
    volume = parse_number(raw_volume)
    return {
        "date": roc_to_date(raw_date, fallback),
        "code": code,
        "name": str(raw_name or "").strip(),
        "open": open_ if open_ is not None else close,
        "high": high if high is not None else close,
        "low": low if low is not None else close,
        "close": close,
        "volume": volume if volume is not None else 0,
    }


def fetch_url_text(url, params, headers):
    full_url = f"{url}?{urlencode(params)}"
    request = Request(full_url, headers=headers)
    with urlopen(request, timeout=10, context=SSL_CONTEXT) as response:
      if response.status != 200:
          return ""
      charset = response.headers.get_content_charset() or "utf-8"
      return response.read().decode(charset, errors="replace")


def fetch_tpex_day(day):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tpex.org.tw/",
        "Accept": "application/json,text/csv,text/plain,*/*",
    }
    for url, params in candidate_tpex_daily_calls(day):
        text = fetch_url_text(url, params, headers)
        rows = parse_tpex_text(text, day)
        if rows:
            return rows
    return []


def normalize_rows(rows):
    by_date = {}
    for row in rows:
        if not row.get("date") or row.get("close") is None:
            continue
        by_date[row["date"]] = row
    return [by_date[key] for key in sorted(by_date)]


def fetch_tpex_stock(code, calendar_days=220, days=60):
    today = dt.date.today()
    rows = []
    for offset in range(calendar_days):
        day = today - dt.timedelta(days=offset)
        if day.weekday() >= 5:
            continue
        day_rows = [row for row in fetch_tpex_day(day) if row["code"] == code]
        rows.extend(day_rows)
        if len(normalize_rows(rows)) >= days:
            break
        time.sleep(0.05)
    return normalize_rows(rows)[-days:]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target_codes = set(TPEX_CODES)
    rows_by_code = {code: [] for code in TPEX_CODES}
    today = dt.date.today()

    for offset in range(220):
        if all(len(normalize_rows(rows)) >= 60 for rows in rows_by_code.values()):
            break
        day = today - dt.timedelta(days=offset)
        if day.weekday() >= 5:
            continue
        day_rows = fetch_tpex_day(day)
        if not day_rows:
            continue
        for row in day_rows:
            code = row["code"]
            if code in target_codes:
                rows_by_code[code].append(row)
        got = sum(1 for rows in rows_by_code.values() if rows)
        print(f"{day}: found data for {got}/{len(TPEX_CODES)} target codes")
        time.sleep(0.05)

    for code in TPEX_CODES:
        rows = normalize_rows(rows_by_code[code])[-60:]
        path = OUT_DIR / f"{code}.json"
        path.write_text(
            json.dumps({"code": code, "market": "TPEX", "rows": rows}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"{code}: {len(rows)} rows -> {path}")


if __name__ == "__main__":
    main()
