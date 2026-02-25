import time
import requests

SIMMER_API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.simmer.markets"

ENTRY_MIN = 0.48
ENTRY_MAX = 0.51

TP1 = 0.66
TP2 = 0.75

MAX_POSITION = 3.0

def get_binance_momentum():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    r = requests.get(url, timeout=5)
    price_now = float(r.json()["price"])
    return price_now

def discover_market():
    url = "https://gamma-api.polymarket.com/markets?limit=100&closed=false"
    r = requests.get(url, timeout=5)
    markets = r.json()

    print("Markets returned:", len(markets))

    for m in markets[:5]:
        print(m.get("question"))

    for m in markets:
        question = m.get("question", "").lower()

    if (
        ("bitcoin up or down" in question or "btc" in question)
        and ("5 minute" in question or "5 minutes" in question)
    ):
        prices = m.get("outcomePrices")

        if prices and len(prices) >= 2:
            yes_price = float(prices[0])
            return m["slug"], yes_price

return None, None

def place_trade(slug, side, amount):
    headers = {"Authorization": f"Bearer {SIMMER_API_KEY}"}

    data = {
        "market_slug": slug,
        "side": side,
        "amount": amount
    }

    r = requests.post(f"{BASE_URL}/api/sdk/trade", json=data, headers=headers)
    return r.json()

def place_sell_orders(slug, shares):
    print(f"Placing TP sells for {shares} shares")

while True:
    try:
        slug, yes_price = discover_market()

        if not slug:
            print("No market found")
            time.sleep(10)
            continue

        print(f"YES price: {yes_price}")

        if ENTRY_MIN <= yes_price <= ENTRY_MAX:
            print("Entry zone detected")

            momentum = get_binance_momentum()

            print("Momentum OK → BUY YES")

            result = place_trade(slug, "yes", MAX_POSITION)

            print(result)

            place_sell_orders(slug, MAX_POSITION)

        else:
            print("Price outside entry zone")

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
