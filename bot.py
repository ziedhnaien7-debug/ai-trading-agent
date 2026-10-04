import json
import urllib.request
from datetime import datetime

STARTING_EUROS = 20.0
SYMBOL = "BTCUSDT"
INTERVAL = "5m"
LIMIT = 50

def get_prices():
    url = (
    f"https://api.binance.us/api/v3/klines"
    f"?symbol={SYMBOL}&interval={INTERVAL}&limit={LIMIT}"
)

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())

    return [float(candle[4]) for candle in data]


def load_state():
    try:
        with open("state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "euros": STARTING_EUROS,
            "btc": 0.0,
            "last_action": "NONE"
        }


def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)


def main():
    prices = get_prices()
    state = load_state()

    short_average = sum(prices[-10:]) / 10
    long_average = sum(prices[-30:]) / 30
    current_price = prices[-1]

    print("=== AI Trading Agent - PAPER TRADING ===")
    print(f"Time: {datetime.now()}")
    print(f"BTC price: ${current_price:.2f}")
    print(f"Short average: ${short_average:.2f}")
    print(f"Long average: ${long_average:.2f}")
    print(f"Virtual euros: €{state['euros']:.2f}")
    print(f"Virtual BTC: {state['btc']:.8f}")

    # BUY signal
    if short_average > long_average and state["euros"] > 0:
        state["btc"] = state["euros"] / current_price
        state["euros"] = 0.0
        state["last_action"] = "BUY"
        print("SIGNAL: BUY (paper only)")

    # SELL signal
    elif short_average < long_average and state["btc"] > 0:
        state["euros"] = state["btc"] * current_price
        state["btc"] = 0.0
        state["last_action"] = "SELL"
        print("SIGNAL: SELL (paper only)")

    else:
        print("SIGNAL: HOLD")

    save_state(state)

    total = state["euros"] + state["btc"] * current_price
    print(f"Virtual portfolio value: €{total:.2f}")
    print(f"Last action: {state['last_action']}")


if __name__ == "__main__":
    main()
