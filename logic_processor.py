from agent import Agent
import GLOBAL
from agents.ma_cross_agent import ma_cross_agent
from agents.BB_agent import bb_agent
from datetime import datetime

ACTIVE_BOT: list[Agent] = [
    ma_cross_agent,
    bb_agent
]

def OnTick(data: tuple):
    print("Dư mua:", GLOBAL.TOTAL_BID)
    print("Dư bán:", GLOBAL.TOTAL_OFFER)
    print("Tổng KLGD mua nước ngoài:", GLOBAL.TOTAL_FOREIGN_BUY)
    print("Tổng KLGD bán nước ngoài:", GLOBAL.TOTAL_FOREIGN_SELL)

def OnBarClosed(data: list[tuple]):
    close_price = data[-1][3]
    # print("Độ sâu mua:", GLOBAL.BID_DEPTH[0]) // Market depth data
    # print("Độ sâu bán:", GLOBAL.OFFER_DEPTH[0])

    for agent in ACTIVE_BOT:
        result = agent.Calculate(data)
        if result == True: # MUST CHECK FOR BOOL, SINCE AGENT MAY RETURN NONE TOO!
            GLOBAL.ENTRADE_CLIENT.Order("VN30F2509", "NB", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh LONG tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
        elif result == False:
            GLOBAL.ENTRADE_CLIENT.Order("VN30F2509", "NS", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh SHORT tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
