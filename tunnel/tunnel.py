# ultra-short friendly server + cloudflared URL sniffing
from bottle import Bottle, HTTPResponse, request, run
import subprocess, re, time, sys
from threading import Thread
from zalo import SendMessage

from import_helper import *
from entrade_client import EntradeClient
from utils import ReadJSONFile

def InitializeEntradeClient():
    entrade_client_data = ReadJSONFile("./tunnel/entrade_client_data.json")
    ENTRADE_CLIENT = EntradeClient()
    ENTRADE_CLIENT.investor_id = entrade_client_data["investor_id"]
    ENTRADE_CLIENT.investor_account_id = entrade_client_data["investor_account_id"]
    ENTRADE_CLIENT.token = entrade_client_data["token"]
    return ENTRADE_CLIENT

app = Bottle()

@app.get("/order") # type: ignore
def get_order():
    print("✅ Received request from", request.remote_addr)

    start = request.query.get("start", 0) # type: ignore
    end = request.query.get("end", 100) # type: ignore
    is_demo = True if request.query.get("demo") else False # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.GetOrders(start, end, is_demo)
    if response:
        return response

    raise HTTPResponse("Get Order failed (Entrade)...", 500)

@app.post("/order") # type: ignore
def order():
    print("✅ Received request from", request.remote_addr)

    symbol = request.query.get("symbol", None) # type: ignore
    if symbol is None:
        raise HTTPResponse('The query should contains "symbol"', 400)

    order_type = request.query.get("type", "LO") # type: ignore
    price = request.query.get("price", None) # type: ignore
    if order_type == "LO" and price is None:
        raise HTTPResponse('The query should contains "price" for LO order', 400)

    side = request.query.get("side", "NB") # type: ignore
    loan = request.query.get("loan", None) # type: ignore
    volume = request.query.get("volume", 1) # type: ignore
    is_demo = True if request.query.get("demo") else False # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.Order(symbol, side, price, loan, volume, order_type, is_demo) # ENTRADE_CLIENT.Order(symbol, side, price, loan, volume, order_type, is_demo)
    if response:
        return response

    raise HTTPResponse("Order failed (Entrade)...", 500)

@app.route("/cancel_order", method=["GET", "POST"]) # type: ignore
def cancel_order():
    print("✅ Received request from", request.remote_addr)

    order_id = request.query.get("id", None) # type: ignore
    if order_id is None:
        raise HTTPResponse('The query should contains "id"', 400)

    is_demo = True if request.query.get("demo") else False # type: ignore
    all = True if request.query.get("all") else False # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.CancelAllOrders(is_demo) if all else ENTRADE_CLIENT.CancelOrder(order_id, is_demo)
    if response:
        return response

    raise HTTPResponse("Cancel Order failed (Entrade)...", 500)

@app.route("/conditional_order", method=["GET", "POST"]) # type: ignore
def conditional_order():
    print("✅ Received request from", request.remote_addr)

    symbol = request.query.get("symbol", None) # type: ignore
    price = request.query.get("price", None) # type: ignore
    target_price = request.query.get("target_price", None) # type: ignore
    if symbol is None or price is None or target_price is None:
        raise HTTPResponse('The query should contains "symbol, "price" and "target_price"', 400)

    side = request.query.get("side", "NB") # type: ignore
    loan = request.query.get("loan", None) # type: ignore
    volume = request.query.get("volume", 1) # type: ignore
    is_demo = True if request.query.get("demo") else False # type: ignore
    condition = f"{'price >=' if request.query.get("condition", "<") == ">" else 'price <='} {target_price}" # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.ConditionalOrder(symbol, side, float(price), loan, volume, condition, is_demo)
    if response:
        return response

    raise HTTPResponse("Conditional Order failed (Entrade)...", 500)

@app.route("/cancel_conditional_order", method=["GET", "POST"]) # type: ignore
def cancel_conditional_order():
    print("✅ Received request from", request.remote_addr)

    order_id = request.query.get("id", None) # type: ignore
    if order_id is None:
        raise HTTPResponse('The query should contains "id"', 400)

    is_demo = True if request.query.get("demo") else False # type: ignore
    all = True if request.query.get("all") else False # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.CancelAllConditionalOrders(is_demo) if all else ENTRADE_CLIENT.CancelConditionalOrder(order_id, is_demo)
    if response:
        return response

    raise HTTPResponse("Cancel Conditional Order failed (Entrade)...", 500)

@app.get("/deals") # type: ignore
def get_deal():
    print("✅ Received request from", request.remote_addr)

    start = request.query.get("start", 0) # type: ignore
    end = request.query.get("end", 100) # type: ignore
    is_demo = True if request.query.get("demo") else False # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.GetDeals(start, end, is_demo)
    if response:
        return response

    raise HTTPResponse("Get Deal failed (Entrade)...", 500)

@app.route("/cancel_deal", method=["GET", "POST"]) # type: ignore
def cancel_deal():
    print("✅ Received request from", request.remote_addr)

    deal_id = request.query.get("id", None) # type: ignore
    if deal_id is None:
        raise HTTPResponse('The query should contains "id"', 400)

    is_demo = True if request.query.get("demo") else False # type: ignore
    all = True if request.query.get("all") else False # type: ignore

    ENTRADE_CLIENT = InitializeEntradeClient()
    response = ENTRADE_CLIENT.CloseAllDeals(is_demo) if all else ENTRADE_CLIENT.CloseDeal(deal_id, is_demo)
    if response:
        return response

    raise HTTPResponse("Cancel Deal failed (Entrade)...", 500)

@app.route("/send_message", method=["GET", "POST"]) # type: ignore
def send_message():
    msg = request.query.get("msg", None) # type: ignore
    thread_id = request.query.get("id", None) # type: ignore

    if SendMessage(msg, thread_id):
        return "Send message successfully!"
    else:
        raise HTTPResponse("Send message failed, it may because your Zalo login detail is not correct or server error.", 500)

@app.get("/") # type: ignore
def home():
    return "Server running — try /order"

def OpenTunnel(PORT: int = 7777):
    CF_CMD = ["cloudflared", "tunnel", "--url", f"http://0.0.0.0:{PORT}"]

    # start cloudflared
    print("Starting cloudflared tunnel...")
    proc = subprocess.Popen(CF_CMD, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # look for trycloudflare url in output with a tolerant regex
    pattern = re.compile(r"https?://[\w\-.]+\.trycloudflare\.com")
    url = None
    start = time.time()
    buf = []
    while True:
        # read line if available
        line = proc.stdout.readline() # type: ignore
        if not line:
            # if no output yet, check timeout
            if time.time() - start > 5:
                break
            time.sleep(0.1)
            continue
        line = line.strip()
        buf.append(line)
        m = pattern.search(line)
        if m:
            url = m.group(0)
            break
        # some versions print 'url=' style
        m2 = re.search(r"url=(https?://[\w\-.]+\.trycloudflare\.com)", line)
        if m2:
            url = m2.group(1)
            break
        # small safety timeout
        if time.time() - start > 5:
            break

    if url:
        print(f"\n🌐 Public URL: {url}\n")
    else:
        print("\n⚠️ Couldn't auto-detect trycloudflare URL. Here are recent cloudflared logs:")
        print("\n".join(buf[-20:]) or "(no output yet)")
        print("\nYou can also run `cloudflared tunnel --url http://0.0.0.0:7777` yourself and paste the URL it prints.\n")

    print(f"Listening locally on http://0.0.0.0:{PORT} ...")
    try:
        run(app, host='0.0.0.0', port=PORT)
    except KeyboardInterrupt:
        print("\nStopping...")
        proc.terminate()
        sys.exit(0)

def run_cloudflared_tunnel(TUNNEL_ID):
    try:
        # Lệnh PowerShell để chạy cloudflared tunnel
        command = ['powershell', '-Command', f'cloudflared tunnel run {TUNNEL_ID}']

        # Thực thi lệnh và ghi log đầu ra
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Cloudflared tunnel {TUNNEL_ID} is running.\nOutput: {result.stdout}")
        print(f"Error: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the tunnel: {e}\n{e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Chạy hàm run_cloudflared_tunnel trong một tiến trình riêng biệt
def OpenCustomTunnel():
    try:
        TUNNEL_ID = int(ReadJSONFile("config.json")) # type: ignore
        tunnel_thread = Thread(target=run_cloudflared_tunnel, args=(TUNNEL_ID,))
        tunnel_thread.start()
        print("Cloudflared tunnel thread started.")

        run(app, host='0.0.0.0', port=TUNNEL_ID) # Hình như đã set config cloudflared chỉ map về port 5000 rùi
    except KeyboardInterrupt:
        print("\nStopping...")
        sys.exit(0)


OpenTunnel()
# OpenCustomTunnel()