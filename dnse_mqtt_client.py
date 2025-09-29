import paho.mqtt.client as mqtt
from paho.mqtt import enums
from ssl import CERT_NONE
from json import JSONDecoder
from random import randint
from SIGNAL import Signal

# Configuration
OHLC_DATA_TOPIC = "plaintext/quotes/krx/mdds/v2/ohlc/derivative/1/VN30F1M"
MARKET_DATA_TOPIC = "plaintext/quotes/krx/mdds/topprice/v1/roundlot/symbol/41I1FA000"
FOREIGN_DATA_TOPIC = "plaintext/quotes/krx/mdds/stockinfo/v1/roundlot/symbol/41I1FA000"

BROKER_HOST = "datafeed-lts-krx.dnse.com.vn"
BROKER_PORT = 443
CLIENT_ID_PREFIX = "dnse-price-json-mqtt-ws-sub-"
# Generate random client ID
client_id = f"{CLIENT_ID_PREFIX}{randint(1000, 2000)}"

class DNSE_MQTT_Client:
    def __init__(self, investor_id: str, token: str, get_market_data: bool = True, get_foreign_data: bool = True):
        client = mqtt.Client(
            enums.CallbackAPIVersion.VERSION2,
            client_id,
            protocol=mqtt.MQTTv5,
            transport="websockets"
        )
        client.username_pw_set(investor_id, token)
        # SSL/TLS configuration (since it's wss://)
        client.ws_set_options(path="/wss")
        client.tls_set(cert_reqs=CERT_NONE) # Bỏ qua kiểm tra SSL
        client.tls_insecure_set(True) # Cho phép kết nối với chứng chỉ self-signed
        client.enable_logger()

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        self.client = client
        self.subscribed_topics = []

        self.on_ohlc_tick = Signal()
        self.on_market_tick = Signal()
        self.on_foreign_tick = Signal()

        self.get_market_data = get_market_data
        self.get_foreign_data = get_foreign_data

        # self.client.on_connect = on_connect
        # self.client.on_message = on_message # or lambda c, u, m: dp.UpdateData(json.JSONDecoder().decode(m.payload.decode())) [LACK logic!]

    def Connect(self):
        self.client.connect(BROKER_HOST, BROKER_PORT, keepalive=1200)

    def Subscribe(self, topic: str):
        if self.client.is_connected():
            self.client.subscribe(topic, qos=1)

            print(f"Subscribed to {topic} successfully!")
            self.subscribed_topics.append(topic)
            return True
        else:
            print(f"DNSE_MQTT_Client.Subscribe(): MQTT client is not connected!")
            return False

    def Unsubscribe(self, topic: str):
        if self.client.is_connected():
            if topic in self.subscribed_topics:
                self.client.unsubscribe(topic)
                self.subscribed_topics.remove(topic)
                print(f"Unsubscribed from {topic} successfully!")
                return True
            else:
                print(f"Topic {topic} is not subscribed!")
                return False
        else:
            print(f"DNSE_MQTT_Client.Unsubscribe(): MQTT client is not connected!")
            return False

    def Start(self):
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        payload = JSONDecoder().decode(msg.payload.decode())

        if msg.topic == OHLC_DATA_TOPIC:
            self.on_ohlc_tick.emit(payload)
        elif msg.topic == MARKET_DATA_TOPIC:
            self.on_market_tick.emit(payload)
        elif msg.topic == FOREIGN_DATA_TOPIC:
            self.on_foreign_tick.emit(payload)

    def on_connect(self, client, userdata, flags, rc, properties):
        '''MQTTv5 connection callback'''
        if rc == 0 and client.is_connected():
            print("Connected to MQTT Broker!")
            # Modify topics as needed
            self.Subscribe(OHLC_DATA_TOPIC)
            if self.get_market_data:
                self.Subscribe(MARKET_DATA_TOPIC)
            if self.get_foreign_data:
                self.Subscribe(FOREIGN_DATA_TOPIC)
        else:
            print(f"DNSE_MQTT_Client.on_connect(): Failed to connect, return code {rc}")
