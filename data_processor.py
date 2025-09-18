import logic_processor as lp
from global_var import LAST_BID_DEPTH, LAST_OFFER_DEPTH
from requests import get
from time import time

def GetOHLCVData(type : str, symbol : str, from_time : int, to_time : int, resolution : str = '15') -> dict[str, list[float]]:
    '''
    **type**: "derivative", "stock" hoặc "index"\n
    **symbol**: mã cổ phiếu/phái sinh/thị trường tương ứng với 'type'\n
    **from_time/to_time**: thời điểm bắt đầu/kết thúc lấy dữ liệu (Unix epoch time)\n
    **resolution**: 1, 3, 5, 15, 30, 1H, 1D, 1W (nến 1/3/5/... phút)
    '''

    url = f"https://api.dnse.com.vn/chart-api/v2/ohlcs/{type}?from={from_time}&to={to_time}&symbol={symbol}&resolution={resolution}"

    response = get(url)
    response.raise_for_status()
    return response.json()

HISTORY = []
last_T = None

def InitializeData():
    global HISTORY, last_T

    last_T = int(time())
    past = last_T - 72_000 # 20 hours prior to now, ensure that we definitely get at least 89 candles (1 minute resolution!) :3

    json_data = GetOHLCVData("derivative", "VN30F1M", past, last_T, '1')
    HISTORY = list(zip(
        json_data['o'],
        json_data['h'],
        json_data['l'],
        json_data['c'],
        json_data['v']
    ))

    print("Successfully initialized data:\n...")
    print(HISTORY[-10:])
    print("==================================================")

def UpdateData(new_data):
    global HISTORY, last_T

    T = int(new_data.get("time"))
    if last_T < T: # The candle have just finished, use last data of it as the final result
        last_T = T

        O = new_data.get("open")
        H = new_data.get("high")
        L = new_data.get("low")
        C = new_data.get("close")
        V = int(new_data.get("volume"))
        HISTORY.append([O, H, L, C, V])
        lp.CalculateStrategy(HISTORY)

def UpdateMarketDepthData(new_market_depth_data):
    LAST_BID_DEPTH.clear()
    LAST_OFFER_DEPTH.clear()

    for dict in new_market_depth_data["bid"]:
        LAST_BID_DEPTH.append(tuple(dict.values()))

    for dict in new_market_depth_data["offer"]:
        LAST_OFFER_DEPTH.append(tuple(dict.values()))
