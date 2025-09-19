import numpy as np

def MA(data: np.ndarray, feature_idx: int = 3) -> float | None:
    '''
    data: (m, n) np.ndarray
    '''
    _, n = data.shape
    if -n <= feature_idx < n:
        return np.mean(data[:, feature_idx]).item()

    return None

def STD(data: np.ndarray, feature_idx: int = 3) -> float | None:
    '''
    data: (m, n) np.ndarray
    '''
    _, n = data.shape
    if -n <= feature_idx < n:
        return np.std(data[:, feature_idx]).item()

    return None
