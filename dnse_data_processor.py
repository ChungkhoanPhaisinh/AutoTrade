import GLOBAL
from requests import get
from time import time

def GetOHLCVData(type: str, symbol: str, from_time: int, to_time: int, resolution: str = '15') -> dict[str, list[float]]:
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

def InitializeData():
    global last_T

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

    if len(HISTORY) < 1:
        print("Initialized data failed! Exiting...")
        GLOBAL.Exit()
    else:
        print("Successfully initialized data:\n...")
        print(HISTORY[-5:])
        print("===================================")

    return HISTORY

last_T: int = -1
def UpdateOHLCVData(new_data):
    global last_T

    O = new_data.get("open")
    H = new_data.get("high")
    L = new_data.get("low")
    C = new_data.get("close")
    V = int(new_data.get("volume"))
    current_tick = (O, H, L, C, V)

    T = int(new_data.get("time"))
    if last_T < T: # The candle have just finished, use last data of it as the final result
        last_T = T
        GLOBAL.AddM1Bar(GLOBAL.LAST_TICK)

    GLOBAL.UpdateLastTick(current_tick)

def UpdateStockInfoData(data):
    GLOBAL.TOTAL_FOREIGN_BUY = int(data["buyForeignQuantity"])
    GLOBAL.TOTAL_FOREIGN_SELL = int(data["sellForeignQuantity"])

def UpdateTopPriceData(data):
    GLOBAL.TOTAL_BID = int(data["totalBidQtty"])
    GLOBAL.TOTAL_OFFER = int(data["totalOfferQtty"])

    GLOBAL.BID_DEPTH.clear()
    for dict in data["bid"]:
        GLOBAL.BID_DEPTH.append(tuple(dict.values()))

    GLOBAL.OFFER_DEPTH.clear()
    for dict in data["offer"]:
        GLOBAL.OFFER_DEPTH.append(tuple(dict.values()))

def Start():
    # Initialize first to also get correct "last_T"
    GLOBAL.InitializeHistory(InitializeData()) # type: ignore

    GLOBAL.MQTT_CLIENT.on_ohlc_data.Connect(UpdateOHLCVData)
    GLOBAL.MQTT_CLIENT.on_stock_info_data.Connect(UpdateStockInfoData)
    GLOBAL.MQTT_CLIENT.on_top_price_data.Connect(UpdateTopPriceData)
