from dnse_client import DNSEClient
from entrade_client import EntradeClient
from json import load

def ReadConfig():
    with open("config.json", 'r') as f:
        return load(f)

NOT_TERMINATED = True

# Initialized at start, shouldn't be modified in runtime
DNSE_CLIENT = DNSEClient()
ENTRADE_CLIENT = EntradeClient()

#==================================================
# Global data collected during runtime:

# List of 10 highest bid/lowest offer and their quantity
BID_DEPTH: list[tuple[float, int]] = []
OFFER_DEPTH: list[tuple[float, int]] = []

# Dư mua/Dư bán
TOTAL_BID: int = -1
TOTAL_OFFER: int = -1

# Tổng KLGD mua/bán của NĐT nước ngoài trong ngày
TOTAL_FOREIGN_BUY: int = -1
TOTAL_FOREIGN_SELL: int = -1
