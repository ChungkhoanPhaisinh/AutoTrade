import GLOBAL
from agent import Agent
from BarData import BarDataM1, BarData
from agents.ma_cross_agent import ma_cross_agent
from agents.BB_agent import bb_agent
from datetime import datetime

from numpy import set_printoptions
set_printoptions(floatmode='fixed', precision=1, suppress=True) # Optional: only for prettier logs

ACTIVE_BOT: list[Agent] = [
    ma_cross_agent,
    bb_agent
]

ACTIVE_RESOLUTION: dict[str, BarDataM1] = {}

def OnStart(init_data: list[tuple]):
    ACTIVE_RESOLUTION["M1"] = BarDataM1(init_data)
    ACTIVE_RESOLUTION["M2"] = BarData(init_data, 2)
    ACTIVE_RESOLUTION["M3"] = BarData(init_data, 3)

def OnTick(data: tuple):
    # print("Dư mua:", GLOBAL.TOTAL_BID)
    # print("Dư bán:", GLOBAL.TOTAL_OFFER)
    # print("Tổng KLGD mua nước ngoài:", GLOBAL.TOTAL_FOREIGN_BUY)
    # print("Tổng KLGD bán nước ngoài:", GLOBAL.TOTAL_FOREIGN_SELL)
    pass

# Repeatedly exucuted after each 1-minute bar
def OnBarClosed(new_bar: tuple):
    for resolution in ACTIVE_RESOLUTION.values(): # DO NOT REMOVE
        resolution.AddBar(new_bar)

    close_price = new_bar[3]
    # print("Độ sâu mua:", GLOBAL.BID_DEPTH[0]) // Market depth data
    # print("Độ sâu bán:", GLOBAL.OFFER_DEPTH[0])
    print("111111111111111111111111111111")
    print(ACTIVE_RESOLUTION["M1"].ToNumpy()[-6:])

    for agent in ACTIVE_BOT:
        result = agent.Calculate(resolution.ToNumpy())
        if result == True: # MUST CHECK FOR BOOL, SINCE AGENT MAY RETURN NONE TOO!
            GLOBAL.ENTRADE_CLIENT.Order("41I1FA000", "NB", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh LONG tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
        elif result == False:
            GLOBAL.ENTRADE_CLIENT.Order("41I1FA000", "NS", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh SHORT tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")

    if ACTIVE_RESOLUTION["M5"].IsComplete():
        # logic for M5
        # Calculate ACTIVE_RESOLUTION["M5"].ToNumpy()
        print("222222222222222222222222222222")
        print(ACTIVE_RESOLUTION["M2"].ToNumpy()[-3:])

    if ACTIVE_RESOLUTION["M15"].IsComplete():
        # logic for M15
        # Calculate ACTIVE_RESOLUTION["M15"].ToNumpy()
        print("333333333333333333333333333333")
        print(ACTIVE_RESOLUTION["M3"].ToNumpy()[-2:])
