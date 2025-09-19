import GLOBAL
from mqtt_client import MQTTClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()
gmailEntrade = getenv("usernameEntrade") # Email/SĐT tài khoản Entrade
passwordEntrade = getenv("passwordEntrade") # Mật khẩu tài khoản Entrade

gmailDNSE = getenv("gmailDNSE") # Email đăng kí DNSE
passwordDNSE = getenv("passwordDNSE") # Mật khẩu tài khoản DNSE
appPasswordDNSE = getenv("appPasswordDNSE") # App Password cho email đăng kí DNSE

if __name__ == "__main__":
    # Connect to Entrade (Only needed if used to auto trade)
    GLOBAL.ENTRADE_CLIENT.Authenticate(gmailEntrade, passwordEntrade)
    GLOBAL.ENTRADE_CLIENT.GetAccountInfo() # Get investor_id
    GLOBAL.ENTRADE_CLIENT.GetAccountBalance() # Get investor_account_id

    # Connect to DNSE
    GLOBAL.DNSE_CLIENT.Authenticate(gmailDNSE, passwordDNSE)

    if GLOBAL.DNSE_CLIENT.token is None:
        raise SystemError("Login to DNSE failed!")

    investor_id = GLOBAL.DNSE_CLIENT.GetAccountInfo().get("investorId")
    token = GLOBAL.DNSE_CLIENT.token

    # Connect to MQTT server
    MQTT_CLIENT = MQTTClient(investor_id, token)
    MQTT_CLIENT.Connect()
    MQTT_CLIENT.Start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Disconnecting...")
        MQTT_CLIENT.client.disconnect()
        MQTT_CLIENT.client.loop_stop()
