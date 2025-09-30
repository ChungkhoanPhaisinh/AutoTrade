import numpy as np

def MA(data: np.ndarray, feature_idx: int = 3) -> float:
    '''
    data: (m, n) np.ndarray
    '''
    _, n = data.shape
    if -n <= feature_idx < n:
        return np.mean(data[:, feature_idx]).item()

    raise ValueError(f"MUST satisfy: -{n} <= feature_idx < {n}")

def STD(data: np.ndarray, feature_idx: int = 3) -> float:
    '''
    data: (m, n) np.ndarray
    '''
    _, n = data.shape
    if -n <= feature_idx < n:
        return np.std(data[:, feature_idx]).item()

    raise ValueError(f"MUST satisfy: -{n} <= feature_idx < {n}")
