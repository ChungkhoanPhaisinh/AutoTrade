import GLOBAL
from agent import Agent
from agents.ma_cross_agent import ma_cross_agent
from agents.BB_agent import bb_agent
from datetime import datetime

from numpy import set_printoptions
set_printoptions(floatmode='fixed', precision=1, suppress=True) # OPTIONAL: Prettier logs

ACTIVE_BOT: list[Agent] = [
    ma_cross_agent,
    bb_agent
]

def OnTick(data: GLOBAL.OHLCVData):
    # print("Dư mua:", GLOBAL.TOTAL_BID)
    # print("Dư bán:", GLOBAL.TOTAL_OFFER)
    # print("Tổng KLGD mua nước ngoài:", GLOBAL.TOTAL_FOREIGN_BUY)
    # print("Tổng KLGD bán nước ngoài:", GLOBAL.TOTAL_FOREIGN_SELL)
    print("LogicProcessor.OnTick() called :3")

# CORE FUNCTIONS, DON'T REMOVE
def OnM1BarClosed(bar: GLOBAL.OHLCVData):
    close_price = bar[3]

    for agent in ACTIVE_BOT:
        result = agent.Calculate(GLOBAL.HISTORY)
        if result == True: # MUST CHECK FOR BOOL, SINCE AGENT MAY RETURN NONE TOO!
            GLOBAL.ENTRADE_CLIENT.Order("41I1FA000", "NB", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh LONG tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
        elif result == False:
            GLOBAL.ENTRADE_CLIENT.Order("41I1FA000", "NS", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh SHORT tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")

def Start():
    GLOBAL.ON_OHLCV_TICK.Connect(OnTick)
    GLOBAL.ON_M1_BAR_CLOSED.Connect(OnM1BarClosed)

    # Add more to BAR_DATA and connect if needed
    GLOBAL.BAR_DATA["m5"].on_bar_closed.Connect(OnM5BarClosed)
    # GLOBAL.BAR_DATA["m12"].on_bar_closed.Connect(OnM12BarClosed)

# CUSTOM FUNCTIONS BELOW
def OnM5BarClosed(M5_bar: GLOBAL.OHLCVData):
    print("==========M5 BAR===========")
    print(M5_bar)

# def OnM12BarClosed(M12_bar: GLOBAL.OHLCVData):
#     close_price = M12_bar[3] # Logic is the same :3

#     for agent in ACTIVE_BOT:
#         result = agent.Calculate(GLOBAL.HISTORY)
#         if result == True: # MUST CHECK FOR BOOL, SINCE AGENT MAY RETURN NONE TOO!
#             GLOBAL.ENTRADE_CLIENT.Order("41I1FA000", "NB", None, None, 1, "MTL", True)
#             print(f"{agent.name} đã đặt lệnh LONG tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
#         elif result == False:
#             GLOBAL.ENTRADE_CLIENT.Order("41I1FA000", "NS", None, None, 1, "MTL", True)
#             print(f"{agent.name} đã đặt lệnh SHORT tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
