import ccxt
from time import sleep
from termcolor import colored

print("Please input Symbol name(default is 'BTC/USDT')")
SYMBOL = input()
if SYMBOL == "":
    SYMBOL = 'BTC/USDT'  # シンボルを定数として定義
print(f"Symol is {SYMBOL}")


def fetch_btc_price(exchange_id, symbol):
    """ 指定された取引所から特定のシンボルの価格を取得する """
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class()
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

def main():
    exchanges = [
        'bybit', 'mexc', 'bitget', 'kucoin',
        'okx', 'binance', 
    ]
    prices = {}

    for exchange_id in exchanges:
        try:
            price = fetch_btc_price(exchange_id, SYMBOL)
            prices[exchange_id] = price
            print(f"{exchange_id.ljust(8)}: {SYMBOL} = {price:,.2f}")
        except Exception as e:
            print(f"{exchange_id.ljust(8)}: {SYMBOL} = ERROR")


    # 最も安い価格を赤字で表示
    if not prices:
        lowest_price_exchange = max(prices, key=prices.get)
        if lowest_price_exchange in ['bybit', 'mexc', 'kucoin']:
            lowest_price = prices[lowest_price_exchange]
            print(colored(f"Max price: {lowest_price_exchange} = {lowest_price:,.2f}", 'red'))

def run():
    while True:
        main()
        print(f"{'-' * 80}")
        sleep(1)

if __name__ == "__main__":
    run()
