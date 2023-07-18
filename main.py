import os
import time
import asyncio
import aioredis
import aiohttp
from contextlib import closing
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = os.getenv('TIMEOUT', 3600)
SYMBOL = os.getenv('SYMBOL', 'ETHUSDT')
REQUEST_FREQ = os.getenv('REQUEST_FREQ', 5)


async def main():
    redis = aioredis.from_url(
        "redis://redis_t", encoding="utf-8", decode_responses=True
    )
    while True:
        start_pointer = time.time()

        async with aiohttp.ClientSession() as session:
            url = f'https://fapi.binance.com/fapi/v1/premiumIndex?symbol={SYMBOL}'
            async with session.get(url) as resp:
                result = await resp.json()
                now_pointer = result['time']
                price = float(result['markPrice'])

        await redis.zadd('market', {price: now_pointer})
        await redis.expire(str(now_pointer), int(TIMEOUT))
        old_prices = await redis.zrange('market', 0, -1)
        for key in reversed(old_prices):
	    diff_price = abs((float(key)/price)*100/price)
            if diff_price >= 1:
                print(f'Сообщение об изменении цены, {diff_price}: {key} -> {price}')

        diff_time = time.time() - start_pointer
        if diff_time <= REQUEST_FREQ:
            time.sleep(REQUEST_FREQ-int(diff_time))


if __name__ == "__main__":
    with closing(asyncio.get_event_loop()) as event_loop:
        event_loop.run_until_complete(main())
