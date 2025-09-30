import paho.mqtt.client as mqtt
from paho.mqtt import enums
from ssl import CERT_NONE
from json import JSONDecoder
from random import randint
from SIGNAL import Signal

# Configuration
OHLC_DATA_TOPIC = "plaintext/quotes/krx/mdds/v2/ohlc/derivative/1/VN30F1M"
TOP_PRICE_TOPIC = "plaintext/quotes/krx/mdds/topprice/v1/roundlot/symbol/41I1FA000"
STOCK_INFO_TOPIC = "plaintext/quotes/krx/mdds/stockinfo/v1/roundlot/symbol/41I1FA000"

BROKER_HOST = "datafeed-lts-krx.dnse.com.vn"
BROKER_PORT = 443
CLIENT_ID_PREFIX = "dnse-price-json-mqtt-ws-sub-"

class DNSE_MQTT_Client:
    def __init__(self, get_top_price: bool = True, get_stock_info: bool = True):
        client = mqtt.Client(
            enums.CallbackAPIVersion.VERSION2,
            f"{CLIENT_ID_PREFIX}{randint(1000, 2000)}", # Generate random client ID
            protocol=mqtt.MQTTv5,
            transport="websockets"
        )
        # SSL/TLS configuration (since it's wss://)
        client.ws_set_options(path="/wss")
        client.tls_set(cert_reqs=CERT_NONE) # Ignore SSL check
        client.tls_insecure_set(True) # Accept connection for self-signed certificate
        client.enable_logger()

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        self.client = client
        self.subscribed_topics = []

        self.on_ohlc_data = Signal()
        self.on_stock_info_data = Signal()
        self.on_top_price_data = Signal()

        self.get_stock_info = get_stock_info
        self.get_top_price = get_top_price

    def Start(self):
        self.client.loop_start()

    def Connect(self, investor_id: str, token: str):
        self.client.username_pw_set(investor_id, token)
        self.client.connect(BROKER_HOST, BROKER_PORT, keepalive=1200)

    def Subscribe(self, topic: str):
        if self.client.is_connected():
            self.client.subscribe(topic, qos=1)
            self.subscribed_topics.append(topic)

            print(f"Subscribed to {topic} successfully!")
            return True

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

        print(f"DNSE_MQTT_Client.Unsubscribe(): MQTT client is not connected!")
        return False

    def on_message(self, client, userdata, msg):
        payload = JSONDecoder().decode(msg.payload.decode())

        if msg.topic == OHLC_DATA_TOPIC:
            self.on_ohlc_data.Emit(payload)
        elif msg.topic == TOP_PRICE_TOPIC:
            self.on_top_price_data.Emit(payload)
        elif msg.topic == STOCK_INFO_TOPIC:
            self.on_stock_info_data.Emit(payload)

    def on_connect(self, client, userdata, flags, rc, properties):
        '''MQTTv5 connection callback'''
        if rc == 0 and client.is_connected():
            print("Connected to MQTT Broker!")
            # Modify topics as needed
            self.Subscribe(OHLC_DATA_TOPIC)
            if self.get_top_price:
                self.Subscribe(TOP_PRICE_TOPIC)
            if self.get_stock_info:
                self.Subscribe(STOCK_INFO_TOPIC)
        else:
            print(f"DNSE_MQTT_Client.on_connect(): Failed to connect, return code {rc}")
