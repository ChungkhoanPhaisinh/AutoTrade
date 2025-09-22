import numpy as np
from collections import deque

def MergeBars(bars: list[tuple]) -> tuple:
    '''
    **bars**: List of (O, H, L, C, V) bars in 1-minute resolution
    '''
    arr = np.array(bars, dtype=np.float32) # Should have shape (m, 5)

    shape = np.shape(arr)
    if len(shape) != 2 or shape[1] != 5:
        raise ValueError("Invalid input, expected shape (m, 5)!")
    elif shape[0] == 1:
        return bars[0]

    result_arr = np.empty(5, dtype=np.float32)
    result_arr[0] = arr[0, 0] # OPEN = first bar's open price
    result_arr[3] = arr[-1, 3] # CLOSE = last bar's close price
    result_arr[1] = np.max(arr[:, 1]).item() # HIGH = highest high price
    result_arr[2] = np.min(arr[:, 2]).item() # LOW = lowest low price
    result_arr[4] = np.sum(arr[:, 4]).item() # VOLUME = total volume

    return tuple(result_arr.tolist())

class BarDataM1:
    def __init__(self, init_data: list[tuple], maxlen: int = 999):
        self.data = deque(init_data, maxlen=maxlen)

    def AddBar(self, bar: tuple) -> bool:
        self.data.append(bar)
        return True

    def IsComplete(self) -> bool:
        return True

    def ToNumpy(self, dtype=np.float32) -> np.ndarray:
        return np.array(self.data, dtype=dtype)

class BarData(BarDataM1):
    def __init__(self, init_data: list[tuple], timeframe: int = 5, maxlen: int = 999):
        '''
        **init_data**: Iterable that hold bars in 1-minute resolution\n
        **timeframe**: resolution in minutes; 5 = 5m, 60 = 1h, ...
        '''
        self.timeframe = timeframe
        self.buffer_data: list[tuple] = []
        self.data = deque(maxlen=maxlen)

        # Initialize data
        grouped_bars = [init_data[i:i+timeframe] for i in range(0, len(init_data), timeframe)]
        if len(grouped_bars[-1]) < timeframe:
            self.buffer_data = grouped_bars.pop()

        for arr in grouped_bars:
            self.data.append(MergeBars(arr))

    def AddBar(self, bar: tuple) -> bool:
        '''
        **bar**: (O, H, L, C, V) in 1-minute resolution

        Returns: If the new bar have just completed
        '''
        self.buffer_data.append(bar)

        if len(self.buffer_data) == self.timeframe:
            self.data.append(MergeBars(self.buffer_data))
            self.buffer_data.clear()
            return True

        return False

    def IsComplete(self) -> bool:
        return len(self.buffer_data) == 0
