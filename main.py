import GLOBAL
from dotenv import load_dotenv
from os import getenv
from dnse_data_processor import Start as DDP_START
from logic_processor import Start as LP_START

load_dotenv()
gmailEntrade = getenv("usernameEntrade") # Email/SĐT tài khoản Entrade
passwordEntrade = getenv("passwordEntrade") # Mật khẩu tài khoản Entrade

gmailDNSE = getenv("gmailDNSE") # Email/SĐT tài khoản DNSE
passwordDNSE = getenv("passwordDNSE") # Mật khẩu tài khoản DNSE

if __name__ == "__main__":
    try:
        # Connect to Entrade (Only needed if used to auto trade)
        GLOBAL.ENTRADE_CLIENT.Authenticate(gmailEntrade, passwordEntrade)
        GLOBAL.ENTRADE_CLIENT.GetAccountInfo() # Set investor_id
        GLOBAL.ENTRADE_CLIENT.GetAccountBalance() # Set investor_account_id

        # Connect to DNSE
        GLOBAL.DNSE_CLIENT.Authenticate(gmailDNSE, passwordDNSE)

        if GLOBAL.DNSE_CLIENT.token is None:
            raise SystemError("Login to DNSE failed!")

        investor_id = GLOBAL.DNSE_CLIENT.GetAccountInfo().get("investorId")
        token = GLOBAL.DNSE_CLIENT.token

        # Start other modules (safe since it only initialize data and connect Signal)
        DDP_START()
        LP_START()

        # Connect to MQTT server
        GLOBAL.MQTT_CLIENT.Connect(investor_id, token)
        GLOBAL.MQTT_CLIENT.Start()
        GLOBAL.Wait()
    except KeyboardInterrupt:
        pass
    finally:
        print("Disconnecting...")
        GLOBAL.MQTT_CLIENT.client.disconnect()
        GLOBAL.MQTT_CLIENT.client.loop_stop()
