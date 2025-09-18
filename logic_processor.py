from global_var import ENTRADE_CLIENT #, LAST_BID_DEPTH, LAST_OFFER_DEPTH
from datetime import datetime
from agents.ma_cross_agent import ma_cross_agent
from agents.BB_agent import bb_agent
from agent import Agent

ACTIVE_BOT: list[Agent] = [
    ma_cross_agent,
    bb_agent
]

def CalculateStrategy(processed_data):
    close_price = processed_data[-1][3]
    # print(LAST_BID_DEPTH) // Market depth data
    # print(LAST_OFFER_DEPTH)

    for agent in ACTIVE_BOT:
        result = agent.Calculate(processed_data)
        if result == True: # MUST CHECK FOR BOOL, SINCE AGENT MAY RETURN NONE TOO!
            ENTRADE_CLIENT.Order("VN30F2509", "NB", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh LONG tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
        elif result == False:
            ENTRADE_CLIENT.Order("VN30F2509", "NS", None, None, 1, "MTL", True)
            print(f"{agent.name} đã đặt lệnh SHORT tại giá {close_price:.1f} ({datetime.now().strftime("%H:%M %d/%m")})")
