from requests import get, post
from time import localtime

class DNSEClient:
    def __init__(self):
        self.token = None
        self.trading_token = None
        self.base_url = "https://api.dnse.com.vn/"

    def Authenticate(self, username, password):
        _headers = {
            "Content-Type": "application/json"
        }
        _json = {
            "username": username,
            "password": password
        }

        url = f"{self.base_url}auth-service/login"
        response = post(url, json=_json, headers=_headers)
        response.raise_for_status()
        self.token = response.json().get("token")
        print("Đăng nhập thành công! (DNSE)")

    def GetAccountInfo(self):
        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        url = f"{self.base_url}user-service/api/me"
        response = get(url, headers=_headers)
        response.raise_for_status()
        return response.json()

    def GetOTP(self):
        _headers = {
            "Authorization": f"Bearer {self.token}"
        }

        url = f"{self.base_url}auth-service/api/email-otp"
        response = get(url, headers=_headers)
        response.raise_for_status()
        print("Gửi OTP thành công! (DNSE)")

    def GetTradingToken(self, otp):
        url = f"{self.base_url}/order-service/trading-token"
        _headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "otp": otp
        }
        response = post(url, headers=_headers)
        response.raise_for_status()
        self.trading_token = response.json().get("tradingToken")
        print("Lấy Trading Token thành công! (DNSE)")

    def Order(self, symbol, account, side, price, loan, volume, order_type):
        url = f"{self.base_url}order-service/v2/orders" # Default to normal stock :3
        loan_package_id = 1372

        if len(symbol) > 3:
            url = f"{self.base_url}order-service/derivative/orders"
            loan_package_id = 2278

        _headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
            "trading-token": self.trading_token
        }
        _json = {
            "accountNo": account,
            "loanPackageId": loan or loan_package_id,
            "orderType": order_type,
            "price": price,
            "quantity": volume,
            "side": side,
            "symbol": symbol
        }
        response = post(url, headers=_headers, json=_json)
        response.raise_for_status()
        print("Gửi yêu cầu đặt lệnh thành công! (DNSE)")
        return response.json()

    def ConditionalOrder(self, symbol, account : int, side, price : float, loan, volume, order_type, condition):
        url = f"{self.base_url}conditional-order-api/v1/orders"

        # Default to derivative
        loan_package_id = 2278
        market_id = "DERIVATIVES"

        if len(symbol) < 4: # It's normal stock :3
            loan_package_id = 1372
            market_id = "UNDERLYING"

        _headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
            "trading-token": self.trading_token
        }

        current_time = localtime()
        _json = {
            "condition": condition,
            "targetOrder": {"quantity": volume, "side": side, "price": price, "loanPackageId": loan or loan_package_id, "orderType": order_type},
            "symbol": symbol,
            "props": {"stopPrice": int(condition[9:]), "marketId": market_id},
            "accountNo": account,
            "category": "STOP",
            "timeInForce": {"expireTime": f"{current_time.tm_year}-{current_time.tm_mon:02d}-{current_time.tm_mday:02d}T07:30:00.000Z", "kind": "GTD"}
        }
        response = post(url, headers=_headers, json=_json)
        response.raise_for_status()
        print("Gửi yêu cầu đặt lệnh điều kiện thành công! (DNSE)")
        return response.json()
