from agent import Agent
import numpy as np
import technical_analysis as ta

class BBAgent(Agent):
    def __init__(self, low_thres: float = -1, high_thres: float = 1, window: int = 20, name: str = "Bot Bollinger Bands"):
        super().__init__(name)
        self.low_thres = low_thres
        self.high_thres = high_thres
        self.window = window

    def Calculate(self, data) -> bool | None:
        np_data = np.array(data, dtype=np.float32)

        std = ta.STD(np_data[-self.window:])
        ma = ta.MA(np_data[-self.window:])
        close_price = np_data[-1, 3].item()

        bb = (close_price - ma) / std

        if bb < self.low_thres and self.deal_pos < 1:
            self.deal_pos = 1
            return True
        elif bb > self.high_thres and self.deal_pos > -1:
            self.deal_pos = -1
            return False
        else:
            return None

bb_agent = BBAgent()