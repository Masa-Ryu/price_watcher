import asyncio
import ccxt.async_support as ccxt
from termcolor import colored

print("Please input Symbol name(default is 'BTC/USDT')")
SYMBOL = input()
if SYMBOL == "":
    SYMBOL = 'BTC/USDT'  # シンボルを定数として定義
print(f"Symol is {SYMBOL}")


async def fetch_btc_price(exchange_id, symbol):
    """ 指定された取引所から特定のシンボルの価格を非同期で取得する """
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class()
        ticker = await exchange.fetch_ticker(symbol)
        price = ticker['last']
    except Exception as e:
        price = None
        print(f"{exchange_id.ljust(8)}: {symbol} = ERROR")
    finally:
        await exchange.close()
    return price

async def main():
    exchanges = [
        'bybit', 'mexc', 'bitget', 'kucoin',
        'okx', 'binance', 'gateio', 'bitfinex'
    ]
    prices = {}

    tasks = [fetch_btc_price(exchange, SYMBOL) for exchange in exchanges]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for exchange_id, price in zip(exchanges, results):
        if price is not None:
            prices[exchange_id] = price
            print(f"{exchange_id.ljust(8)}: {SYMBOL} = {price:,.2f}")

    # 最も安い価格を赤字で表示
    if prices:
        lowest_price_exchange = min(prices, key=prices.get)
        if lowest_price_exchange in ['bybit', 'mexc', 'kucoin', 'okx']:
            lowest_price = prices[lowest_price_exchange]
            print(colored(f"最安値: {lowest_price_exchange} = {lowest_price:,.2f}", 'red'))

async def run():
    while True:
        await main()
        print(f"{'-' * 80}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run())

