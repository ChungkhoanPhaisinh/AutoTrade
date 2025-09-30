from collections import deque
from SIGNAL import Signal

from typing import TypeAlias # OPTIONAL: Stricter type-check
OHLCVData: TypeAlias = tuple[float, float, float, float, int]

def MergeBars(bars: list[OHLCVData]) -> OHLCVData:
    '''
    **bars**: List of (O, H, L, C, V) bars in 1-minute resolution
    '''
    O = bars[0][0]
    H = bars[0][1]
    L = bars[0][2]
    C = bars[-1][3]
    V = 0
    for i in range(1, len(bars)):
        _, h, l, _, v = bars[i]
        H = max(h, H)
        L = min(l, L)
        V += v

    return (O, H, L, C, V)

class BarData:
    def __init__(self, init_data: list[OHLCVData], timeframe: int = 5, maxlen: int = 999):
        '''
        **init_data**: Iterable that hold bars in 1-minute resolution\n
        **timeframe**: resolution in minutes; 5 = 5m, 60 = 1h, ...
        '''
        self.on_bar_closed = Signal()
        self.timeframe = timeframe
        self.buffer_data: list[OHLCVData] = []
        self.data = deque[OHLCVData](maxlen=maxlen)

        if init_data:
            self.InitData(init_data)

    def AddBar(self, bar: OHLCVData):
        '''
        **bar**: (O, H, L, C, V) in 1-minute resolution

        Returns: If the new bar have just completed
        '''
        self.buffer_data.append(bar)

        if len(self.buffer_data) == self.timeframe:
            new_bar = MergeBars(self.buffer_data)
            self.data.append(new_bar)
            self.on_bar_closed.Emit(new_bar)
            self.buffer_data.clear()

    def InitData(self, data: list[OHLCVData]):
        grouped_bars = [data[i:i+self.timeframe] for i in range(0, len(data), self.timeframe)]
        if len(grouped_bars[-1]) < self.timeframe:
            self.buffer_data = grouped_bars.pop()

        for arr in grouped_bars:
            self.data.append(MergeBars(arr))
