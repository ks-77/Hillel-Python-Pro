import asyncio
import aiohttp


async def binance(session):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    async with session.get(url) as response:
        data = await response.json()
        return float(data["price"])


async def coindesk(session):
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    async with session.get(url) as response:
        data = await response.json()
        return float(data["bpi"]["USD"]["rate"].replace(",", ""))


async def coinbase(session):
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    async with session.get(url) as response:
        data = await response.json()
        return float(data["data"]["amount"])


async def kraken(session):
    url = "https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD"
    async with session.get(url) as response:
        data = await response.json()
        return float(data["result"]["XXBTZUSD"]["c"][0])


async def bitfinex(session):
    url = "https://api.bitfinex.com/v1/pubticker/btcusd"
    async with session.get(url) as response:
        data = await response.json()
        return float(data["last_price"])


async def get_all_prices():
    async with aiohttp.ClientSession() as session:
        tasks = [
            coindesk(session),
            coinbase(session),
            binance(session),
            kraken(session),
            bitfinex(session)
        ]
        prices = await asyncio.gather(*tasks)
        return prices


async def all_prices(prices):
    print(f"All rates: {prices}")


async def max_price(prices):
    max_price = max(prices)
    print(f"Highest rate: {max_price}")


async def main():
    prices = await get_all_prices()
    await asyncio.gather(
        all_prices(prices),
        max_price(prices),
    )

asyncio.run(main())
