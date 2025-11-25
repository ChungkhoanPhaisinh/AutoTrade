import GLOBAL
from dnse_data_processor import Start as DDP_START
from logic_processor import Start as LP_START
from utils import ReadJSONFile, WriteJSONFile

JSON_DATA = ReadJSONFile("config.json")
gmailEntrade = JSON_DATA["username_entrade"] # Email/SĐT tài khoản Entrade
passwordEntrade = JSON_DATA["password_entrade"] # Mật khẩu tài khoản Entrade

gmailDNSE = JSON_DATA["username_dnse"] # Email/SĐT tài khoản DNSE
passwordDNSE = JSON_DATA["password_dnse"] # Mật khẩu tài khoản DNSE

if __name__ == "__main__":
    try:
        # Connect to Entrade (Only needed if used to auto trade)
        GLOBAL.ENTRADE_CLIENT.Authenticate(gmailEntrade, passwordEntrade)
        GLOBAL.ENTRADE_CLIENT.GetAccountInfo() # Set investor_id
        GLOBAL.ENTRADE_CLIENT.GetAccountBalance() # Set investor_account_id

        entrade_client_data = {
            "investor_id": GLOBAL.ENTRADE_CLIENT.investor_id,
            "investor_account_id": GLOBAL.ENTRADE_CLIENT.investor_account_id,
            "token": GLOBAL.ENTRADE_CLIENT.token
        }
        WriteJSONFile("./tunnel/entrade_client_data.json", entrade_client_data)

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
    except Exception as e:
        print(e)
    except KeyboardInterrupt: # OPTIONAL: Allow shutdown by Control+C in Mac
        pass
    finally:
        print("Disconnecting...")
        GLOBAL.MQTT_CLIENT.client.disconnect()
        GLOBAL.MQTT_CLIENT.client.loop_stop()
