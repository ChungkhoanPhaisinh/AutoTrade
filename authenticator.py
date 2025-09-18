from global_var import DNSE_CLIENT, ENTRADE_CLIENT
from dotenv import load_dotenv
from os import getenv
from mqtt_client import MQTTClient

load_dotenv()
gmailEntrade = getenv("usernameEntrade") # Email/SĐT tài khoản Entrade
passwordEntrade = getenv("passwordEntrade") # Mật khẩu tài khoản Entrade

gmailDNSE = getenv("gmailDNSE") # Email đăng kí DNSE
passwordDNSE = getenv("passwordDNSE") # Mật khẩu tài khoản DNSE
appPasswordDNSE = getenv("appPasswordDNSE") # App Password cho email đăng kí DNSE

if __name__ == "__main__":
    # Connect to Entrade (Only needed if used to auto trade)
    ENTRADE_CLIENT.Authenticate(gmailEntrade, passwordEntrade)
    ENTRADE_CLIENT.GetAccountInfo()
    ENTRADE_CLIENT.GetAccountBalance()

    # Connect to MQTT server
    DNSE_CLIENT.Authenticate(gmailDNSE, passwordDNSE)

    if DNSE_CLIENT.token is None:
        raise SystemError("Login to DNSE failed!")

    investor_id = DNSE_CLIENT.GetAccountInfo().get("investorId")
    token = DNSE_CLIENT.token

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
