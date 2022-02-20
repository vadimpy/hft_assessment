import asyncio
import websockets
import json
from tqdm import tqdm

class BinanceStreamListener:
    WS_ENDPOINT = 'wss://stream.binance.com:9443/ws'

    async def __collect(stream_name: str, symbol: str, finish: asyncio.Event) -> list[dict]:
        res = []
        async with websockets.connect(f'{BinanceStreamListener.WS_ENDPOINT}/{symbol}@{stream_name}') as conn:
            while not finish.is_set():
                res.append(json.loads(await conn.recv()))
        return res

    async def __wait_for(timeout: int, finish: asyncio.Event) -> None:
        await asyncio.sleep(timeout)
        finish.set()

    async def __pbar(timeout: int, step: int) -> None:
        for _ in tqdm(range(0, timeout, step)):
            await asyncio.sleep(step)

        print("Listening finished")

    async def collect_with_timeout(stream_name: str, symbol: str, timeout: int) -> list[dict]:
        finish = asyncio.Event()

        print(f"Listening to {symbol}@{stream_name} for {timeout} seconds...")
        collect_task = asyncio.create_task(BinanceStreamListener.__collect(stream_name, symbol, finish))
        wait_task = asyncio.create_task(BinanceStreamListener.__wait_for(timeout, finish))
        pbar_task = asyncio.create_task(BinanceStreamListener.__pbar(timeout, 1))

        await pbar_task
        await wait_task
        res = await collect_task

        return res
