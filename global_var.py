from dnse_client import DNSEClient
from entrade_client import EntradeClient
from json import load

DNSE_CLIENT = DNSEClient()
ENTRADE_CLIENT = EntradeClient()

LAST_BID_DEPTH: list[tuple[float, int]] = []
LAST_OFFER_DEPTH: list[tuple[float, int]] = []

def ReadConfig():
    with open("config.json", 'r') as f:
        return load(f)
