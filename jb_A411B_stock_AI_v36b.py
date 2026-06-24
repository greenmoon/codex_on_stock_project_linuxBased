JB_str= 'jb_A411B_stock_AI_v36b.py since 2026.01.10'
print(JB_str)
 
MY_STOCK_LIST = {
    ### TWSE
    2330: 'TSMC_台灣積體電路',
    2454: 'MediaTek_聯發科技',
    2379: 'RealTek_瑞昱半導體',
    6415: 'Silergy-KY_矽力杰',
    2337: '旺宏',
    3008: '大立光',
    2345: 'Accton_智邦科技',
    2382: 'Quanta_廣達電腦',
    2308: 'Delta_台達電',
    2301: 'LiteOn_光寶科技',
    3406: 'Largan_玉晶光',
    3017: 'AVC_奇鋐',
    2317: 'HonHai_鴻海精密',
    #2455: 'All New_全新光電科技',
    4977: 'Group-Dar-KY_眾達科技',
    3450: 'CPO_聯鈞光電',
    2357: 'ASUS_華碩電腦',
    2344: '華邦電', 
    2376: 'Gigabyte_技嘉科技',
    3555: 'Dr_wang',
    3443: '創意',
    6531: '愛普*(SRAM)',
    6695: '芯鼎',
    3037: '欣興（Unimicron)',
    8046: '南電（Nan Ya PCB)',
    3189: '景碩（Kinsus)',
    2408: '南亞科（Nanya Technology)',
    6770: '力積電',
    2912: 'President 7-11',
    #CPO_STOCK_LIST = {
    6515: 'CPI_YingWei_穎崴 (CPO->)',
    2345: 'Accton_智邦',
    #2330: 'TSMC_台積電',
    6442: 'GuangSheng_光聖',
    6789: 'CaiYu_采鈺',
    6451: 'XunXin-KY_訊芯-KY',
    3450: 'LianJun_聯鈞',
    2455: 'AllNew_全新',
    4977: 'GroupDar-KY_眾達-KY',
    #6223: 'WangSi_旺矽',
    #3081: 'LianYa_聯亞',
    #3163: 'BoRuoWei_波若威',
    #3363: 'ShangQuan_上詮',
    #4979: 'HuaXingGuang_華星光',
    #
    # 20 joined dinner 2026
    #2330: '台積電->2026 dinner',
    #2317: '鴻海',
    2382: '廣達',
    2454: '聯發科',
    2357: '華碩',
    4938: '和碩',
    3231: '緯創',
    6669: '緯穎',
    2308: '台達電',
    2449: '京元電',
    2356: '英業達',
    2301: '光寶科',
    3017: '奇鋐',
    2353: '宏碁',
    2376: '技嘉',
    2324: '仁寶',
    2395: '研華',
    2377: '微星',
    3711: '日月光投控',
    3515: '華擎',
    
    # 20 joined dinner 2026
    #2330: '台積電->2026 dinner',
    #2317: '鴻海',
    #2382: '廣達',
    #2454: '聯發科',
    #2357: '華碩',
    4938: '和碩',
    3231: '緯創',
    6669: '緯穎',
    #2308: '台達電',
    2449: '京元電',
    2356: '英業達',
    #2301: '光寶科',
    #3017: '奇鋐',
    2353: '宏碁',
    #2376: '技嘉',
    2324: '仁寶',
    2395: '研華',
    2377: '微星',
    3711: '日月光投控',
    3515: '華擎',
    
    ### TPEX
    3529: '力旺', # TPEX
    5351: '鈺創', # TPEX
    3324: 'TwoHong_雙鴻',
    3081: 'Union Asia',
    4971: 'IET-KY_InP_top',
    3163: 'WaveNoWay',
    4979: '華星光_middle',
    3363: 'Up Complete',
    6488: 'Universal Wefer',
    6735: 'Madar Tester',
    5347: 'World Advance',
    3105: 'Stable'
}

print('\nJB> Wait to Split MY_STOCK_LIST into TWSE / TPEX\n')
print('\nJB> Alert: checking TWSE + TPEX\n')
 
# v25 2026.01.10 1. for TWSE 
# v26 2026.03.06 1. for TPEX 
# v27 2026.03.10 1. for no TPEX 
# v28 2026.03.10 1. use space as up down arrow to browse stock  
# v29 2026.03.11 1. ok and np TPEX
# v30 2026.03.19 1. add more stocks 
# v31 2026.04.01 1. add more 4 stocks 
# v34 2026.05.30 1. SPACE forward only; c/v/b/n/m backward only; no reverse action
# v35 2026.05.30 1. enable TWSE + TPEX; TPEX uses daily all-market JSON endpoint then filters code
# v36 2026.06.01 1. remove right-top summary text block 2. enlarge Price/Bollinger chart area for easier reading
# v36b 2026.06.01 1. make Price/Bollinger larger 2. make Volume/RSI/MACD thinner 3. add more right-side plot area
 
import sys, time, datetime, io, csv, json
import numpy as np
import pandas as pd
import requests
from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Dict, List, Optional, Tuple


def split_name_eng_tc(name: str):
    if not isinstance(name, str):
        return str(name), ""
    if "_" in name:
        a, b = name.split("_", 1)
        return a.strip(), b.strip()
    return name.strip(), ""


# ============================================================
# Market Split (TWSE / TPEX)
# ============================================================

class TWSE_TPEX_Classifier:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.twse_set = set()
        self.tpex_set = set()

    def refresh(self):
        twse_url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
        twse = requests.get(twse_url, timeout=self.timeout).json()
        self.twse_set = {
            str(x.get("公司代號")).strip()
            for x in twse if x.get("公司代號")
        }

        tpex_url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
        tpex = requests.get(tpex_url, timeout=self.timeout).json()
        self.tpex_set = {
            str(x.get("SecuritiesCompanyCode")).strip()
            for x in tpex if x.get("SecuritiesCompanyCode")
        }
        return self

    def split(self, stock_dict):
        twse_dict, tpex_dict, unknown_dict = {}, {}, {}
        for code, name in stock_dict.items():
            code_s = str(code).strip()
            if code_s in self.twse_set:
                twse_dict[code] = name
            elif code_s in self.tpex_set:
                tpex_dict[code] = name
            else:
                unknown_dict[code] = name
        return twse_dict, tpex_dict, unknown_dict


# ============================================================
# Stock List
# ============================================================

AMY_STOCK_LIST = {
    ### TWSE
    2330: 'TSMC_台灣積體電路',
    2454: 'MediaTek_聯發科技',
    2379: 'RealTek_瑞昱半導體',
    2345: 'Accton_智邦科技',
    2382: 'Quanta_廣達電腦',
    2308: 'Delta_台達電',
    2301: 'LiteOn_光寶科技',
    3406: 'Largan_玉晶光',
    3017: 'AVC_奇鋐',
    2317: 'HonHai_鴻海精密',
    6415: 'Silergy-KY_矽力杰',
    2455: 'All New_全新光電科技',
    4977: 'Group-Dar-KY_眾達科技',
    3450: 'CPO_聯鈞光電',
    2357: 'ASUS_華碩電腦',
    2376: 'Gigabyte_技嘉科技',
    3555: 'Dr_wang',
    3443: '創意',
    6531: '愛普*(SRAM)',
    6695: '芯鼎',
    6770: '力積電',
    2408: '南亞科（Nanya Technology)',
    3037: '欣興（Unimicron',
    8046: '南電（Nan Ya PCB)',
    3189: '景碩（Kinsus)',
    
    ### TPEX
    3529: '力旺', # TPEX
    5351: '鈺創', # TPEX
    3324: 'TwoHong_雙鴻',
    3081: 'Union Asia',
    4971: 'IET-KY_InP_top',
    3163: 'WaveNoWay',
    4979: '華星光_middle',
    3363: 'Up Complete',
    6488: 'Universal Wefer',
    6735: 'Madar Tester',
    5347: 'World Advance',
    3105: 'Stable'
}

#print('\nJB> Wait to Split MY_STOCK_LIST into TWSE / TPEX\n')

try:
    _classifier = TWSE_TPEX_Classifier(timeout=10).refresh()
    TWSE_LIST, TPEX_LIST, UNKNOWN_LIST = _classifier.split(MY_STOCK_LIST)

    print("JB> TWSE_LIST :", sorted(TWSE_LIST.keys()))
    print("JB> TPEX_LIST :", sorted(TPEX_LIST.keys()))
    if UNKNOWN_LIST:
        print("JB> UNKNOWN_LIST (ignored):", sorted(UNKNOWN_LIST.keys()))
except Exception as e:
    print("JB> Market split failed; exit. err =", e)
    sys.exit(1)


# ============================================================
# Utilities
# ============================================================

def roc_to_ad(s: str) -> pd.Timestamp:
    s = str(s).strip()
    y, m, d = s.split('/')
    return pd.Timestamp(f"{int(y)+1911}-{int(m):02d}-{int(d):02d}")


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['MA20'] = df['Close'].rolling(20, min_periods=1).mean()
    df['STD20'] = df['Close'].rolling(20, min_periods=1).std()

    df['BBU'] = df['MA20'] + 2.0 * df['STD20']
    df['BBL'] = df['MA20'] - 2.0 * df['STD20']
    df['BBU12'] = df['MA20'] + 1.2 * df['STD20']
    df['BBL12'] = df['MA20'] - 1.2 * df['STD20']

    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14, min_periods=1).mean()
    loss = (-delta.clip(upper=0)).rolling(14, min_periods=1).mean()
    rs = gain / loss.replace(0, np.nan)
    df['RSI'] = (100 - 100 / (1 + rs)).ffill()

    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Hist'] = df['MACD'] - df['Signal']

    df['MACD_Golden'] = (df['MACD'].shift(1) <= df['Signal'].shift(1)) & (df['MACD'] > df['Signal'])
    df['MACD_Death']  = (df['MACD'].shift(1) >= df['Signal'].shift(1)) & (df['MACD'] < df['Signal'])

    return df.ffill()


def _to_float(x):
    s = str(x).strip().replace(',', '')
    if s in ('', '----', '---', '--', 'X', '除權息', 'null', 'None'):
        return np.nan
    try:
        return float(s)
    except:
        return np.nan


def _normalize_tpex_date_text(s: str):
    s = str(s).strip().replace('-', '/')
    parts = s.split('/')
    if len(parts) != 3:
        return None

    try:
        y = int(parts[0])
        m = int(parts[1])
        d = int(parts[2])
    except:
        return None

    if y < 1911:
        y += 1911

    try:
        return pd.Timestamp(f"{y:04d}-{m:02d}-{d:02d}")
    except:
        return None


def _parse_tpex_csv_text(text: str) -> pd.DataFrame:
    if not text or len(text) < 20:
        return pd.DataFrame()

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    raw_lines = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith('='):
            continue
        raw_lines.append(s)

    if not raw_lines:
        return pd.DataFrame()

    parsed = list(csv.reader(io.StringIO("\n".join(raw_lines))))
    if not parsed:
        return pd.DataFrame()

    header_idx = None
    for i, row in enumerate(parsed):
        row_txt = ','.join([str(x) for x in row])
        if ('日期' in row_txt) and (('收盤' in row_txt) or ('均價' in row_txt)) and ('最高' in row_txt) and ('最低' in row_txt):
            header_idx = i
            break

    if header_idx is None:
        return pd.DataFrame()

    header = [str(x).strip() for x in parsed[header_idx]]
    body = parsed[header_idx + 1:]
    if not body:
        return pd.DataFrame()

    maxlen = len(header)
    body2 = []
    for r in body:
        if len(r) < maxlen:
            r = r + [''] * (maxlen - len(r))
        body2.append(r[:maxlen])

    dfm = pd.DataFrame(body2, columns=header)
    if dfm.empty:
        return pd.DataFrame()

    col_date = next((c for c in dfm.columns if '日期' in c), None)
    col_open = next((c for c in dfm.columns if '開盤' in c), None)
    col_high = next((c for c in dfm.columns if '最高' in c), None)
    col_low  = next((c for c in dfm.columns if '最低' in c), None)
    col_close = next((c for c in dfm.columns if ('收盤' in c) or ('均價' in c)), None)
    col_vol = next((c for c in dfm.columns if ('成交股數' in c) or ('成交仟股' in c) or ('成交數量' in c)), None)

    rows = []
    for _, rr in dfm.iterrows():
        dt = _normalize_tpex_date_text(rr[col_date]) if col_date else None
        if dt is None:
            continue

        op = _to_float(rr[col_open]) if col_open else np.nan
        hi = _to_float(rr[col_high]) if col_high else np.nan
        lo = _to_float(rr[col_low]) if col_low else np.nan
        cl = _to_float(rr[col_close]) if col_close else np.nan
        vol = _to_float(rr[col_vol]) if col_vol else np.nan

        if np.isnan(cl) or np.isnan(hi) or np.isnan(lo):
            continue
        if np.isnan(op):
            op = cl
        if np.isnan(vol):
            vol = 0.0

        rows.append({
            "Date": dt,
            "Open": op,
            "High": hi,
            "Low": lo,
            "Close": cl,
            "Volume": vol,
        })

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows, columns=["Date", "Open", "High", "Low", "Close", "Volume"])


def load_tw_stock_safe(code: str, days=30) -> pd.DataFrame:
    rows = []
    today = datetime.date.today()

    for i in range(18):
        y = today.year
        m = today.month - i
        while m <= 0:
            y -= 1
            m += 12

        date_str = f"{y}{m:02d}01"
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
        params = {"response": "json", "date": date_str, "stockNo": code}

        try:
            r = requests.get(url, params=params, timeout=8)
            data = r.json().get("data")
            if not isinstance(data, list) or len(data) == 0:
                continue

            for d in data:
                rows.append({
                    "Date": roc_to_ad(d[0]),
                    "Open": float(d[3].replace(',', '')),
                    "High": float(d[4].replace(',', '')),
                    "Low":  float(d[5].replace(',', '')),
                    "Close": float(d[6].replace(',', '')),
                    "Volume": float(d[1].replace(',', '')),
                })
            time.sleep(0.20)
        except:
            pass

    cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df = pd.DataFrame(rows, columns=cols)

    if df.empty:
        raise ValueError("NO_DATA (TWSE STOCK_DAY returned empty)")

    df = df.drop_duplicates("Date").sort_values("Date").set_index("Date").tail(days)
    df = add_indicators(df)
    return df


# ============================================================
# TPEX loader v35 from jb_A411B_demo_TPEX_v03.py
# ============================================================

def ad_to_roc_date(d: datetime.date) -> str:
    """
    Convert AD date to ROC date text used by many Taiwan market endpoints.
    Example:
        2026-05-30 -> 115/05/30
    """
    return f"{d.year - 1911}/{d.month:02d}/{d.day:02d}"


def normalize_date_text(s) -> Optional[pd.Timestamp]:
    """
    Accept:
      115/05/30
      2026/05/30
      2026-05-30
    Return pandas Timestamp or None.
    """
    if s is None:
        return None

    text = str(s).strip().replace("-", "/")
    if not text:
        return None

    parts = text.split("/")
    if len(parts) != 3:
        return None

    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        if y < 1911:
            y += 1911
        return pd.Timestamp(f"{y:04d}-{m:02d}-{d:02d}")
    except Exception:
        return None


def to_float(x) -> float:
    """
    Taiwan market CSV/JSON fields often contain comma, --, or empty text.
    """
    if x is None:
        return np.nan

    s = str(x).strip().replace(",", "")
    s = s.replace("+", "")
    s = s.replace("X", "").strip()

    if s in ("", "--", "---", "----", "null", "None", "除權息"):
        return np.nan

    try:
        return float(s)
    except Exception:
        return np.nan



# ============================================================
# TPEX daily endpoint fetch
# ============================================================

def _candidate_tpex_daily_calls(day: datetime.date) -> List[Tuple[str, str, Dict[str, str]]]:
    """
    v02 uses daily all-market TPEX endpoint candidates.

    The data.gov.tw page for "上櫃股票收盤行情" links to:
      /web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php

    Some deployments accept o=json; some accept o=data; some need d=ROC_DATE.
    So this function tries several practical variants.
    """
    roc_d = ad_to_roc_date(day)

    base_old = "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php"

    return [
        ("otc_quotes_o_json_with_date", base_old, {"l": "zh-tw", "o": "json", "se": "EW", "d": roc_d}),
        ("otc_quotes_o_data_with_date", base_old, {"l": "zh-tw", "o": "data", "se": "EW", "d": roc_d}),
        ("otc_quotes_o_csv_with_date",  base_old, {"l": "zh-tw", "o": "csv",  "se": "EW", "d": roc_d}),
        # Some environments ignore date and return latest day; keep as fallback.
        ("otc_quotes_o_json_no_date", base_old, {"l": "zh-tw", "o": "json", "se": "EW"}),
        ("otc_quotes_o_data_no_date", base_old, {"l": "zh-tw", "o": "data", "se": "EW"}),
    ]


def _find_key_by_keywords(keys, keyword_list):
    for kw in keyword_list:
        for k in keys:
            if kw in str(k):
                return k
    return None


def parse_tpex_daily_json(obj, fallback_date: datetime.date, debug: bool = False) -> pd.DataFrame:
    """
    Flexible JSON parser for TPEX daily all-market data.

    Expected output columns:
        Date, Code, Name, Open, High, Low, Close, Volume
    """
    if not isinstance(obj, dict):
        return pd.DataFrame()

    fields = None
    data = None

    if isinstance(obj.get("tables"), list) and obj["tables"]:
        t0 = obj["tables"][0]
        fields = t0.get("fields") or t0.get("headers")
        data = t0.get("data") or t0.get("aaData")
    else:
        fields = obj.get("fields") or obj.get("headers")
        data = obj.get("aaData") or obj.get("data")

    if debug:
        print("JB> JSON keys:", list(obj.keys())[:20])
        print("JB> fields:", fields)
        if isinstance(data, list):
            print("JB> data rows:", len(data))
            print("JB> first row:", data[0] if data else None)

    if not isinstance(data, list) or not data:
        return pd.DataFrame()

    rows = []

    # --------------------------------------------------------
    # Case A: row is dict
    # --------------------------------------------------------
    if isinstance(data[0], dict):
        for rr in data:
            keys = list(rr.keys())

            k_date = _find_key_by_keywords(keys, ["資料日期", "日期"])
            k_code = _find_key_by_keywords(keys, ["代號", "股票代號", "證券代號"])
            k_name = _find_key_by_keywords(keys, ["名稱", "股票名稱", "證券名稱"])
            k_close = _find_key_by_keywords(keys, ["收盤"])
            k_open = _find_key_by_keywords(keys, ["開盤"])
            k_high = _find_key_by_keywords(keys, ["最高"])
            k_low = _find_key_by_keywords(keys, ["最低"])
            k_vol = _find_key_by_keywords(keys, ["成交股數", "成交仟股", "成交數量"])

            code = str(rr.get(k_code, "")).strip() if k_code else ""
            name = str(rr.get(k_name, "")).strip() if k_name else ""

            dt = normalize_date_text(rr.get(k_date)) if k_date else pd.Timestamp(fallback_date)

            op = to_float(rr.get(k_open)) if k_open else np.nan
            hi = to_float(rr.get(k_high)) if k_high else np.nan
            lo = to_float(rr.get(k_low)) if k_low else np.nan
            cl = to_float(rr.get(k_close)) if k_close else np.nan
            vol = to_float(rr.get(k_vol)) if k_vol else 0.0

            if not code or dt is None or np.isnan(cl):
                continue
            if np.isnan(op):
                op = cl
            if np.isnan(hi):
                hi = cl
            if np.isnan(lo):
                lo = cl
            if np.isnan(vol):
                vol = 0.0

            rows.append({
                "Date": dt,
                "Code": code,
                "Name": name,
                "Open": op,
                "High": hi,
                "Low": lo,
                "Close": cl,
                "Volume": vol,
            })

    # --------------------------------------------------------
    # Case B: row is list
    # --------------------------------------------------------
    elif isinstance(data[0], list):
        # If fields missing, assume common TPEX daily quote order.
        # Based on data.gov.tw fields:
        # 資料日期、代號、名稱、收盤、漲跌、開盤、最高、最低、成交股數、...
        if not isinstance(fields, list) or not fields:
            fields = ["資料日期", "代號", "名稱", "收盤", "漲跌", "開盤", "最高", "最低", "成交股數"]

        header = [str(x).strip() for x in fields]

        def find_idx(keywords):
            for kw in keywords:
                for idx, h in enumerate(header):
                    if kw in h:
                        return idx
            return None

        i_date = find_idx(["資料日期", "日期"])
        i_code = find_idx(["代號", "股票代號", "證券代號"])
        i_name = find_idx(["名稱", "股票名稱", "證券名稱"])
        i_close = find_idx(["收盤"])
        i_open = find_idx(["開盤"])
        i_high = find_idx(["最高"])
        i_low = find_idx(["最低"])
        i_vol = find_idx(["成交股數", "成交仟股", "成交數量"])

        for rr in data:
            # Fallback if header mapping failed but row has common order.
            if i_code is None and len(rr) >= 9:
                i_date, i_code, i_name, i_close, i_open, i_high, i_low, i_vol = 0, 1, 2, 3, 5, 6, 7, 8

            if i_code is None or i_close is None:
                continue

            def get(i):
                return rr[i] if i is not None and i < len(rr) else None

            code = str(get(i_code)).strip()
            name = str(get(i_name)).strip() if i_name is not None else ""

            dt = normalize_date_text(get(i_date)) if i_date is not None else pd.Timestamp(fallback_date)
            op = to_float(get(i_open))
            hi = to_float(get(i_high))
            lo = to_float(get(i_low))
            cl = to_float(get(i_close))
            vol = to_float(get(i_vol))

            if not code or dt is None or np.isnan(cl):
                continue
            if np.isnan(op):
                op = cl
            if np.isnan(hi):
                hi = cl
            if np.isnan(lo):
                lo = cl
            if np.isnan(vol):
                vol = 0.0

            rows.append({
                "Date": dt,
                "Code": code,
                "Name": name,
                "Open": op,
                "High": hi,
                "Low": lo,
                "Close": cl,
                "Volume": vol,
            })

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


def parse_tpex_daily_csv(text: str, fallback_date: datetime.date, debug: bool = False) -> pd.DataFrame:
    """
    CSV/data parser fallback.
    Some TPEX responses are plain CSV-like text, some are JSON, and some are HTML errors.
    """
    if not text or len(text) < 20:
        return pd.DataFrame()

    if "<html" in text[:500].lower() or "<!doctype" in text[:500].lower():
        return pd.DataFrame()

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Try JSON first if it looks like JSON text.
    if text.lstrip().startswith("{"):
        try:
            return parse_tpex_daily_json(json.loads(text), fallback_date, debug=debug)
        except Exception:
            pass

    raw_lines = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("="):
            continue
        raw_lines.append(s)

    if not raw_lines:
        return pd.DataFrame()

    parsed = list(csv.reader(io.StringIO("\n".join(raw_lines))))
    if not parsed:
        return pd.DataFrame()

    # Find header containing code/close/open/high/low.
    header_idx = None
    for i, row in enumerate(parsed):
        row_txt = ",".join(str(x) for x in row)
        if ("代號" in row_txt or "證券代號" in row_txt) and ("收盤" in row_txt) and ("開盤" in row_txt):
            header_idx = i
            break

    if header_idx is None:
        # Maybe no header: use common order.
        header = ["資料日期", "代號", "名稱", "收盤", "漲跌", "開盤", "最高", "最低", "成交股數"]
        body = parsed
    else:
        header = [str(x).strip() for x in parsed[header_idx]]
        body = parsed[header_idx + 1:]

    rows = []
    for rr in body:
        if len(rr) < 4:
            continue

        def find_idx(keywords):
            for kw in keywords:
                for idx, h in enumerate(header):
                    if kw in h:
                        return idx
            return None

        i_date = find_idx(["資料日期", "日期"])
        i_code = find_idx(["代號", "股票代號", "證券代號"])
        i_name = find_idx(["名稱", "股票名稱", "證券名稱"])
        i_close = find_idx(["收盤"])
        i_open = find_idx(["開盤"])
        i_high = find_idx(["最高"])
        i_low = find_idx(["最低"])
        i_vol = find_idx(["成交股數", "成交仟股", "成交數量"])

        # Common fallback
        if i_code is None and len(rr) >= 9:
            i_date, i_code, i_name, i_close, i_open, i_high, i_low, i_vol = 0, 1, 2, 3, 5, 6, 7, 8

        def get(i):
            return rr[i] if i is not None and i < len(rr) else None

        code = str(get(i_code)).strip() if i_code is not None else ""
        name = str(get(i_name)).strip() if i_name is not None else ""

        dt = normalize_date_text(get(i_date)) if i_date is not None else pd.Timestamp(fallback_date)
        op = to_float(get(i_open))
        hi = to_float(get(i_high))
        lo = to_float(get(i_low))
        cl = to_float(get(i_close))
        vol = to_float(get(i_vol))

        if not code or dt is None or np.isnan(cl):
            continue
        if np.isnan(op):
            op = cl
        if np.isnan(hi):
            hi = cl
        if np.isnan(lo):
            lo = cl
        if np.isnan(vol):
            vol = 0.0

        rows.append({
            "Date": dt,
            "Code": code,
            "Name": name,
            "Open": op,
            "High": hi,
            "Low": lo,
            "Close": cl,
            "Volume": vol,
        })

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


def fetch_tpex_daily_all_market(day: datetime.date, session: requests.Session, debug: bool = False) -> pd.DataFrame:
    """
    Fetch one day all TPEX quotes.
    Return all-market DataFrame. Caller filters by stock code.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tpex.org.tw/",
        "Accept": "application/json,text/csv,text/plain,*/*",
    }

    for tag, url, params in _candidate_tpex_daily_calls(day):
        try:
            r = session.get(url, params=params, headers=headers, timeout=10)

            if debug:
                print("\\n[TPEX v03 TRY]", tag)
                print("url=", r.url)
                print("status=", r.status_code)
                print("content-type=", r.headers.get("Content-Type"))
                print("first200=", r.text[:200].replace("\n", "\\n"))

            if r.status_code != 200:
                continue

            ct = str(r.headers.get("Content-Type", "")).lower()
            df = pd.DataFrame()

            # JSON path
            if ("json" in ct) or r.text.lstrip().startswith("{"):
                try:
                    obj = r.json()
                    df = parse_tpex_daily_json(obj, day, debug=debug)
                except Exception as e:
                    if debug:
                        print("JSON parse failed:", e)

            # CSV/data fallback
            if df.empty:
                df = parse_tpex_daily_csv(r.text, day, debug=debug)

            if not df.empty:
                return df

        except Exception as e:
            if debug:
                print("[TPEX v03 ERROR]", tag, e)

    return pd.DataFrame()


def load_tpex_stock_demo_v03(code: str, calendar_days: int = 180, days: int = 60, debug: bool = False) -> pd.DataFrame:
    """
    Collect recent TPEX all-market daily quotes and filter one code.
    """
    code = str(code).strip()
    today = datetime.date.today()
    session = requests.Session()

    rows = []
    found_dates = set()

    for offset in range(calendar_days):
        day = today - datetime.timedelta(days=offset)

        # skip weekends; Taiwan holidays still handled by empty response.
        if day.weekday() >= 5:
            continue

        df_day = fetch_tpex_daily_all_market(day, session=session, debug=(debug and offset < 3))
        if df_day.empty:
            continue

        df_day["Code"] = df_day["Code"].astype(str).str.strip()
        hit = df_day[df_day["Code"] == code].copy()
        if hit.empty:
            continue

        for _, rr in hit.iterrows():
            dt = pd.Timestamp(rr["Date"])
            if dt in found_dates:
                continue
            found_dates.add(dt)
            rows.append({
                "Date": dt,
                "Open": float(rr["Open"]),
                "High": float(rr["High"]),
                "Low": float(rr["Low"]),
                "Close": float(rr["Close"]),
                "Volume": float(rr["Volume"]),
                "Name": str(rr.get("Name", "")),
            })

        if len(rows) >= days:
            break

        time.sleep(0.05)

    if not rows:
        raise ValueError(f"NO_DATA for TPEX code={code}. Try debug=True to inspect returned endpoint content.")

    df = pd.DataFrame(rows)
    df = df.drop_duplicates("Date").sort_values("Date").set_index("Date").tail(days)

    # Keep Name separately, but indicators require numeric columns.
    name_col = df["Name"] if "Name" in df.columns else None
    df_num = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df_num = add_indicators(df_num)
    if name_col is not None:
        df_num["Name"] = name_col.reindex(df_num.index)

    return df_num



def load_stock_safe(code: str, market: str, days=30) -> pd.DataFrame:
    market = str(market).upper().strip()
    if market == "TWSE":
        return load_tw_stock_safe(code, days)
    elif market == "TPEX":
        return load_tpex_stock_demo_v03(code, calendar_days=220, days=days, debug=False)
    else:
        raise ValueError(f"Unknown market={market}")


def judge_row(row, market="TWSE"):
    market = str(market).upper().strip()

    if market == "TPEX":
        if row['MACD_Golden'] and row['RSI'] < 65:
            return "BUY"
        if row['MACD_Death'] and row['RSI'] > 35:
            return "SELL"
        return "WAIT"

    if row['MACD_Golden'] and row['RSI'] < 70:
        return "BUY"
    if row['MACD_Death'] and row['RSI'] > 30:
        return "SELL"
    return "WAIT"


# ============================================================
# Base Chart
# ============================================================

class BaseChart(QtWidgets.QGraphicsView):
    def __init__(self, df, height=200):
        super().__init__()
        self.df = df.reset_index()
        self.N = len(self.df)

        self.w = 1120
        self.h = height
        self.pad = 30

        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.x_scale = (self.w - 2*self.pad) / max(1, self.N-1)
        self.scene.addRect(0, 0, self.w, self.h, pen=QtGui.QPen(QtCore.Qt.black))

        self.vline = self.scene.addLine(
            0, self.pad, 0, self.h - self.pad,
            QtGui.QPen(QtGui.QColor('red'), 1)
        )
        self.vline.setVisible(False)
        self.vline.setZValue(8)

    def x(self, i):
        return self.pad + i * self.x_scale

    def show_vline(self, i):
        i = max(0, min(self.N - 1, i))
        x = self.x(i)
        self.vline.setLine(x, self.pad, x, self.h - self.pad)
        self.vline.setVisible(True)

    def draw_y_axis(self, ticks, label, fmt="{:.0f}", color="#555555"):
        pen = QtGui.QPen(QtGui.QColor(color))
        font = QtGui.QFont("Menlo", 9)

        title = self.scene.addText(label, font)
        title.setDefaultTextColor(QtGui.QColor(color))
        title.setPos(4, 4)
        title.setZValue(20)

        for val, y in ticks:
            self.scene.addLine(self.pad - 4, y, self.pad, y, pen)
            txt = self.scene.addText(fmt.format(val), font)
            txt.setDefaultTextColor(QtGui.QColor(color))
            txt.setPos(2, y - 8)
            txt.setZValue(20)


# ============================================================
# Price Chart
# ============================================================

class PriceChart(BaseChart):
    def __init__(self, df, code, name, market):
        super().__init__(df, 500)
        self.df_raw = df.reset_index()
        self.stock_code = code
        self.stock_name = name
        self.stock_market = market

        ymin = df[['BBL', 'Close']].min().min()
        ymax = df[['BBU', 'Close']].max().max()
        self.ymin, self.ymax = ymin, ymax

        if self.ymax <= self.ymin:
            self.ymax = self.ymin + 1.0

        self.draw_band(df['BBU'], df['BBL'], fill='#cce6ff', alpha=0.30)
        self.draw_band(df['BBU12'], df['BBL12'], fill='#99ccff', alpha=0.55)
        self.draw_line(df['MA20'], '#ff8800', 2)
        self.draw_line(df['Close'], '#000000', 1.6)

        self.setMouseTracking(True)

        self.cursor_text = self.scene.addText("")
        self.cursor_text.setFont(QtGui.QFont("Menlo", 9))
        self.cursor_text.setDefaultTextColor(QtGui.QColor('red'))
        self.cursor_text.setZValue(9)
        self.cursor_text.setVisible(False)

        self.draw_y_axis(
            ticks=[
                (self.ymax, self.pad),
                ((self.ymax + self.ymin) / 2, self.h / 2),
                (self.ymin, self.h - self.pad),
            ],
            label="Price / Bollinger",
            fmt="{:.0f}"
        )

    def y(self, v):
        den = (self.ymax - self.ymin)
        if den == 0:
            den = 1.0
        return self.pad + (self.ymax - v) / den * (self.h - 2*self.pad)

    def draw_band(self, u, l, fill='#ddeeff', alpha=0.25):
        color = QtGui.QColor(fill)
        color.setAlphaF(alpha)

        path = QtGui.QPainterPath()
        path.moveTo(self.x(0), self.y(u.iloc[0]))

        for i in range(self.N):
            path.lineTo(self.x(i), self.y(u.iloc[i]))
        for i in reversed(range(self.N)):
            path.lineTo(self.x(i), self.y(l.iloc[i]))

        path.closeSubpath()
        self.scene.addPath(path, QtGui.QPen(QtCore.Qt.NoPen), QtGui.QBrush(color))

    def draw_line(self, s, color, w):
        path = QtGui.QPainterPath()
        for i in range(self.N):
            v = s.iloc[i]
            x, y = self.x(i), self.y(v)
            path.moveTo(x, y) if i == 0 else path.lineTo(x, y)
        pen = QtGui.QPen(QtGui.QColor(color))
        pen.setWidthF(w)
        self.scene.addPath(path, pen)

        dot_pen = QtGui.QPen(QtGui.QColor('#222222'))
        dot_brush = QtGui.QBrush(QtGui.QColor('#ffffff'))
        for i in range(self.N):
            v = self.df_raw['Close'].iloc[i]
            x = self.x(i)
            y = self.y(v)
            self.scene.addEllipse(x - 2, y - 2, 4, 4, dot_pen, dot_brush)

    def show_cursor_at_index(self, i):
        i = max(0, min(self.N - 1, i))
        row = self.df_raw.iloc[i]

        close = row['Close']
        ma = row['MA20']
        std = row['STD20']
        sigma = (close - ma) / std if std > 0 else 0.0

        if sigma >= 0.2:
            advice = "SELL near"
            lo = ma + 1.2 * std
            hi = ma + 2.0 * std
            color = QtGui.QColor("red")
        elif sigma <= -0.2:
            advice = "BUY near"
            lo = ma - 2.0 * std
            hi = ma - 1.2 * std
            color = QtGui.QColor("green")
        else:
            advice = "WAIT"
            lo = hi = None
            color = QtGui.QColor("black")

        self.show_vline(i)
        x = self.x(i)

        eng, tc = split_name_eng_tc(self.stock_name)
        line_stock = f"{self.stock_code}  {eng}"
        if tc:
            line_stock += f"  {tc}"

        txt = (
            f"{row['Date']:%Y-%m-%d}\n"
            f"{self.stock_market}\n"
            f"{line_stock}\n"
            f"Close: {close:.2f}\n"
            f"σ: {sigma:+.2f}\n"
            f"Advice: {advice}"
        )

        if lo is not None:
            txt += f"\nRange: {lo:.0f} ~ {hi:.0f}"

        self.cursor_text.setPlainText(txt)
        self.cursor_text.setDefaultTextColor(color)

        font = self.cursor_text.font()
        font.setPointSize(15)
        self.cursor_text.setFont(font)

        margin = 6
        bbox = self.cursor_text.boundingRect()
        text_w = bbox.width()
        text_h = bbox.height()

        tx = x + margin
        ty = self.pad + margin

        if tx + text_w > (self.w - self.pad - margin):
            tx = x - margin - text_w

        if tx < margin:
            tx = margin
        if ty + text_h > (self.h - self.pad):
            ty = self.h - self.pad - text_h

        self.cursor_text.setPos(tx, ty)
        self.cursor_text.setVisible(True)

    def mouseMoveEvent(self, event):
        pos = self.mapToScene(event.pos())

        if pos.x() < self.pad or pos.x() > self.w - self.pad:
            self.vline.setVisible(False)
            self.cursor_text.setVisible(False)
            return

        raw = (pos.x() - self.pad) / self.x_scale
        i = int(raw + 0.5)
        i = max(0, min(self.N - 1, i))

        self.show_cursor_at_index(i)
        super().mouseMoveEvent(event)

        parent = self.parentWidget()
        if parent and hasattr(parent, "show_index"):
            parent.show_index(i)


# ============================================================
# Volume Chart
# ============================================================

class StockVolumeChart(BaseChart):
    def __init__(self, df):
        super().__init__(df, 105)

        vmax = float(df['Volume'].max()) if df['Volume'].max() > 0 else 1.0
        bar_w = self.x_scale * 0.6

        for i in range(self.N):
            vol = float(self.df['Volume'].iloc[i])
            h = vol / vmax * (self.h - 2*self.pad)
            self.scene.addRect(
                self.x(i) - bar_w/2, self.h - self.pad - h,
                bar_w, h,
                QtGui.QPen(QtCore.Qt.NoPen),
                QtGui.QBrush(QtGui.QColor('gray'))
            )

        self.draw_y_axis(
            ticks=[
                (vmax, self.pad),
                (vmax / 2, self.h / 2),
                (0, self.h - self.pad),
            ],
            label="Volume",
            fmt="{:.0f}"
        )


# ============================================================
# RSI Chart
# ============================================================

class StockRSIChart(BaseChart):
    def __init__(self, df):
        super().__init__(df, 90)

        path = QtGui.QPainterPath()
        for i in range(self.N):
            v = float(df['RSI'].iloc[i])
            y = self.pad + (100 - v) / 100 * (self.h - 2*self.pad)
            path.moveTo(self.x(i), y) if i == 0 else path.lineTo(self.x(i), y)
        self.scene.addPath(path, QtGui.QPen(QtGui.QColor('blue'), 1.6))

        for lvl in (30, 70):
            y = self.pad + (100 - lvl) / 100 * (self.h - 2*self.pad)
            self.scene.addLine(
                self.pad, y,
                self.w - self.pad, y,
                QtGui.QPen(QtGui.QColor("#aaaaaa"), 1, QtCore.Qt.DashLine)
            )

        self.draw_y_axis(
            ticks=[(70, self.pad), (50, self.h / 2), (30, self.h - self.pad)],
            label="RSI",
            fmt="{:.0f}"
        )


# ============================================================
# MACD Chart
# ============================================================

class StockMACDChart(BaseChart):
    def __init__(self, df):
        super().__init__(df, 105)

        vmax = np.nanmax(np.abs(df[['MACD', 'Signal', 'Hist']].values))
        vmax = float(vmax) if vmax and vmax > 0 else 1.0

        def y_map(v):
            return self.pad + (vmax - v) / (2 * vmax) * (self.h - 2 * self.pad)

        for i in range(self.N):
            hist = float(self.df['Hist'].iloc[i])
            y0, y1 = y_map(0), y_map(hist)
            color = 'green' if hist >= 0 else 'red'
            self.scene.addRect(
                self.x(i) - 2,
                min(y0, y1),
                4,
                abs(y1 - y0),
                QtGui.QPen(QtCore.Qt.NoPen),
                QtGui.QBrush(QtGui.QColor(color))
            )

        self.scene.addLine(
            self.pad, y_map(0), self.w - self.pad, y_map(0),
            QtGui.QPen(QtGui.QColor('#aaaaaa'), 1, QtCore.Qt.DashLine)
        )

        for col, color in [('MACD', '#0033cc'), ('Signal', '#ff8800')]:
            path = QtGui.QPainterPath()
            for i in range(self.N):
                v = float(df[col].iloc[i])
                path.moveTo(self.x(i), y_map(v)) if i == 0 else path.lineTo(self.x(i), y_map(v))
            self.scene.addPath(path, QtGui.QPen(QtGui.QColor(color), 1.4))

        self.draw_y_axis(
            ticks=[(vmax, self.pad), (0, self.h / 2), (-vmax, self.h - self.pad)],
            label="MACD",
            fmt="{:.2f}"
        )


# ============================================================
# Stock Page
# ============================================================

class StockPage(QtWidgets.QWidget):
    def __init__(self, df, idx, total, code, name, market):
        super().__init__()
        self.market = market
        self.code = code
        self.name = name

        last = df.iloc[-1]
        decision = judge_row(last, market)

        self.summary = (
            f"Stock: {idx} / {total}, {code} {name}\n"
            f"Market: {market}\n"
            f"Date: {last.name:%Y-%m-%d}\n"
            f"Close: {last['Close']:.2f}\n"
            f"RSI: {last['RSI']:.1f}\n"
            f"MACD: {last['MACD']:.2f} / {last['Signal']:.2f}\n"
            f"Decision: {decision}"
        )

        # v36:
        # Remove the right-top summary text block to free more vertical space
        # for the Price / Bollinger chart.
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        self.price = PriceChart(df, code, name, market)
        self.volume = StockVolumeChart(df)
        self.rsi = StockRSIChart(df)
        self.macd = StockMACDChart(df)

        layout.addWidget(self.price)
        layout.addWidget(self.volume)
        layout.addWidget(self.rsi)
        layout.addWidget(self.macd)

    def show_index(self, i):
        self.price.show_cursor_at_index(i)
        self.volume.show_vline(i)
        self.rsi.show_vline(i)
        self.macd.show_vline(i)


# ============================================================
# Main Window V27
# ============================================================

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        global JB_str
        super().__init__()
        self.setWindowTitle("TOOL: View Stock, " + JB_str)
        self.resize(1600, 1000)

        self.stock_items = []   # [(idx, total, code, name, market, page)]
        
        # v34 hotkeys: SPACE forward, c/v/b/n/m backward, no reverse action
        
        # ---------------- central ----------------
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)

        self.main_layout = QtWidgets.QVBoxLayout(cw)
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.main_layout.setSpacing(6)

        # ---------------- title label ----------------
        self.title_label = QtWidgets.QLabel("No stock loaded")
        self.title_label.setFont(QtGui.QFont("Menlo", 16, QtGui.QFont.Bold))
        self.title_label.setStyleSheet("background:#eaeaea; padding:8px;")
        self.main_layout.addWidget(self.title_label)

        # ---------------- search row ----------------
        search_row = QtWidgets.QHBoxLayout()

        lb = QtWidgets.QLabel("Find:")
        lb.setFont(QtGui.QFont("Menlo", 11))
        search_row.addWidget(lb)

        self.edit_find = QtWidgets.QLineEdit()
        self.edit_find.setPlaceholderText("code / name / market")
        self.edit_find.setFont(QtGui.QFont("Menlo", 11))
        search_row.addWidget(self.edit_find, 1)

        self.main_layout.addLayout(search_row)

        # ---------------- splitter ----------------
        self.splitter = QtWidgets.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.main_layout.addWidget(self.splitter, 1)

        # ---------------- left panel ----------------
        left_panel = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setMinimumWidth(320)
        self.list_widget.setFont(QtGui.QFont("Menlo", 11))
        self.list_widget.setAlternatingRowColors(True)
        left_layout.addWidget(self.list_widget)

        self.splitter.addWidget(left_panel)

        # ---------------- right stacked pages ----------------
        self.stack = QtWidgets.QStackedWidget()
        self.splitter.addWidget(self.stack)

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([320, 1340])

        # ---------------- status/progress ----------------
        self.progress = QtWidgets.QProgressBar()
        self.progress.setMaximumHeight(14)
        self.progress.setTextVisible(True)
        self.progress.setFormat("Loading %v / %m")
        self.progress.setVisible(False)
        self.statusBar().addPermanentWidget(self.progress, 1)

        # signals
        self.list_widget.currentRowChanged.connect(self.on_stock_changed)
        self.edit_find.textChanged.connect(self.on_find_text_changed)

        QtCore.QTimer.singleShot(200, self.run_all)
        
        # v34: global shortcuts work even when focus is on list/edit/chart
        # SPACE = forward only, no reverse action
        QtWidgets.QShortcut(QtGui.QKeySequence("Space"), self, activated=self.on_space_forward)

        # c/v/b/n/m = backward only, no reverse action
        for k in ["C", "V", "B", "N", "M"]:
            QtWidgets.QShortcut(QtGui.QKeySequence(k), self, activated=self.on_hotkey_backward)

    # v29 space
    def _next_visible_row(self, start_row, step):
        n = self.list_widget.count()
        r = start_row
        while 0 <= r < n:
            item = self.list_widget.item(r)
            if item and (not item.isHidden()):
                return r
            r += step
        return None

    def on_space_forward(self):
        """v34: SPACE moves forward on the visible stock list; stop at bottom."""
        n = self.list_widget.count()
        if n <= 0:
            return

        row = self.list_widget.currentRow()
        if row < 0:
            row = 0

        nxt = self._next_visible_row(row + 1, +1)
        if nxt is not None:
            self.list_widget.setCurrentRow(nxt)

    def on_hotkey_backward(self):
        """v34: c/v/b/n/m move backward on the visible stock list; stop at top."""
        n = self.list_widget.count()
        if n <= 0:
            return

        row = self.list_widget.currentRow()
        if row < 0:
            row = 0

        prv = self._next_visible_row(row - 1, -1)
        if prv is not None:
            self.list_widget.setCurrentRow(prv)

    # --------------------------------------------------------
    # Data / UI linkage
    # --------------------------------------------------------
    def add_stock_page(self, idx, total, code, name, market, page):
        text = f"{idx:02d} | {code} | {market} | {name}"
        item = QtWidgets.QListWidgetItem(text)
        item.setData(QtCore.Qt.UserRole, len(self.stock_items))
        self.list_widget.addItem(item)

        self.stack.addWidget(page)
        self.stock_items.append((idx, total, code, name, market, page))

    def on_stock_changed(self, row):
        if row < 0 or row >= len(self.stock_items):
            return

        idx, total, code, name, market, page = self.stock_items[row]
        self.stack.setCurrentWidget(page)
        self.title_label.setText(f"{idx} / {total}    {code}.{market}    {name}")

        if hasattr(page, "price") and page.price.N > 0:
            page.show_index(page.price.N - 1)

    def on_find_text_changed(self, text):
        text = str(text).strip().lower()
        first_match_row = None

        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            visible = (text in item.text().lower()) if text else True
            item.setHidden(not visible)
            if visible and first_match_row is None:
                first_match_row = row

        if first_match_row is not None:
            self.list_widget.setCurrentRow(first_match_row)

    # --------------------------------------------------------
    # Keyboard
    # --------------------------------------------------------
    def keyPressEvent(self, event):
        row = self.list_widget.currentRow()
        n = self.list_widget.count()

        if n <= 0:
            return super().keyPressEvent(event)

        def next_visible(start_row, step):
            r = start_row
            while 0 <= r < n:
                item = self.list_widget.item(r)
                if not item.isHidden():
                    return r
                r += step
            return None

        if event.key() == QtCore.Qt.Key_Down:
            r = next_visible(row + 1, +1)
            if r is not None:
                self.list_widget.setCurrentRow(r)
            return

        elif event.key() == QtCore.Qt.Key_Up:
            r = next_visible(row - 1, -1)
            if r is not None:
                self.list_widget.setCurrentRow(r)
            return

        elif event.key() == QtCore.Qt.Key_PageDown:
            r = row
            for _ in range(5):
                rr = next_visible(r + 1, +1)
                if rr is None:
                    break
                r = rr
            self.list_widget.setCurrentRow(r)
            return

        elif event.key() == QtCore.Qt.Key_PageUp:
            r = row
            for _ in range(5):
                rr = next_visible(r - 1, -1)
                if rr is None:
                    break
                r = rr
            self.list_widget.setCurrentRow(r)
            return

        elif event.key() == QtCore.Qt.Key_Home:
            r = next_visible(0, +1)
            if r is not None:
                self.list_widget.setCurrentRow(r)
            return

        elif event.key() == QtCore.Qt.Key_End:
            r = next_visible(n - 1, -1)
            if r is not None:
                self.list_widget.setCurrentRow(r)
            return

        elif event.key() == QtCore.Qt.Key_Slash:
            self.edit_find.setFocus()
            self.edit_find.selectAll()
            return

        super().keyPressEvent(event)

    # --------------------------------------------------------
    # Main loader
    # --------------------------------------------------------
    def run_all(self):
        self.list_widget.clear()

        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()

        self.stock_items = []

        ordered_items = []

        for code, name in TWSE_LIST.items():
            ordered_items.append((code, name, "TWSE"))

        ENABLE_TPEX = True  # v35: enable TPEX using daily all-market JSON loader
        if ENABLE_TPEX:
            for code, name in TPEX_LIST.items():
                ordered_items.append((code, name, "TPEX"))

        total_all = len(ordered_items)

        self.progress.setMaximum(total_all)
        self.progress.setValue(0)
        self.progress.setVisible(True)

        print('\nJB> Checking on TWSE + TPEX len={}\n'.format(total_all))

        ok_count = 0

        for idx, (code, name, market) in enumerate(ordered_items, start=1):
            self.statusBar().showMessage(f"Loading {market} {code} ({idx}/{total_all})")
            jb_str = ' Loading ({}/{}): market={}, code={}, name={}'.format(idx, total_all, market, code, name)
            print('JB>' + jb_str)

            try:
                df = load_stock_safe(str(code), market, 30)
                page = StockPage(df, idx, total_all, code, name, market)
                self.add_stock_page(idx, total_all, code, name, market, page)
                ok_count += 1
            except Exception as e:
                print(code, market, "failed", e)

            self.setWindowTitle("Stock Tool: " + JB_str + jb_str)
            self.progress.setValue(idx)
            QtWidgets.QApplication.processEvents()

        self.progress.setVisible(False)
        self.statusBar().showMessage(f"READY  loaded={ok_count}/{total_all}")

        #if self.list_widget.count() > 0:
        #    self.list_widget.setCurrentRow(0)
        #else:
        #    self.title_label.setText("No stock loaded")

        # v29 space
        # ---- after loading: focus + highlight first visible stock ----
        if self.list_widget.count() > 0:
            self.list_widget.setFocus(QtCore.Qt.OtherFocusReason)  # focus on list
            self.list_widget.setCurrentRow(0)                      # highlight row 0
            self.list_widget.scrollToItem(
                self.list_widget.item(0),
                QtWidgets.QAbstractItemView.PositionAtTop
            )
            # ensure right page + title refresh immediately
            self.on_stock_changed(0)
        else:
            self.title_label.setText("No stock loaded")

# ============================================================
# Entry
# ============================================================

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 
exit()
  
  
