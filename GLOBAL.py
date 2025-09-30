from dnse_client import DNSEClient
from entrade_client import EntradeClient
from dnse_mqtt_client import DNSE_MQTT_Client
from bar_data import BarData
from json import load
from signal import pause, SIGINT
from os import kill, getpid
from SIGNAL import Signal

from typing import TypeAlias # OPTIONAL: Stricter type-check
OHLCVData: TypeAlias = tuple[float, float, float, float, int]

def Wait():
    pause()

def Exit():
    kill(getpid(), SIGINT) # Same as Ctrl+C

def ReadConfig():
    with open("config.json", 'r') as f:
        return load(f)

ON_OHLCV_TICK = Signal()
ON_M1_BAR_CLOSED = Signal()

# Initialized at start, shouldn't be modified in runtime
DNSE_CLIENT = DNSEClient()
ENTRADE_CLIENT = EntradeClient()
MQTT_CLIENT = DNSE_MQTT_Client(get_top_price=False, get_stock_info=False)

# LIST OF ADDITIONAL TIMEFRAMES TO USES (M5, M15, ...)
BAR_DATA: dict[str, BarData] = {
    "m5": BarData([]),
    # "m12": BarData([], 12)
}

#==================================================
# Global data collected during runtime:

# List of previous m1 bars
HISTORY: list[OHLCVData] = []
def InitializeHistory(history: list[OHLCVData]):
    HISTORY.clear()
    HISTORY.extend(history)

    for bar_data in BAR_DATA.values():
        bar_data.InitData(history)

def AddM1Bar(bar: OHLCVData):
    HISTORY.append(bar)
    ON_M1_BAR_CLOSED.Emit(bar)

# Last received OHLCV data tick
LAST_TICK: OHLCVData
def UpdateLastTick(data: OHLCVData):
    global LAST_TICK

    LAST_TICK = data
    ON_OHLCV_TICK.Emit(data)

# List of 10 highest bid/lowest offer and their quantity
BID_DEPTH: list[tuple[float, int]] = []
OFFER_DEPTH: list[tuple[float, int]] = []

# Dư mua/Dư bán
TOTAL_BID: int = -1
TOTAL_OFFER: int = -1

# Tổng KLGD mua/bán của NĐT nước ngoài trong ngày
TOTAL_FOREIGN_BUY: int = -1
TOTAL_FOREIGN_SELL: int = -1
