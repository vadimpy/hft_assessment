import asyncio
import argparse
import json
import datetime
from binance_stream_listener import BinanceStreamListener

async def main():
    parser = argparse.ArgumentParser(description='Binance Stream Listener')
    parser.add_argument('--symbol', required=True, dest='symbol', type=str, help='Lowercase symbol')
    parser.add_argument('--stream', required=True, dest='stream', type=str, help='Stream name')
    parser.add_argument('--timeout', required=True, dest='timeout', type=int, help='Timeout in seconds')
    parser.add_argument('--output', required=True, dest='output', type=str, help='Output dir (output file name is formated <symbol>@<stream>_from_<start>_to_<end>)')

    args = parser.parse_args()

    start_time = datetime.datetime.now()
    res = await BinanceStreamListener.collect_with_timeout(args.stream, args.symbol, args.timeout)
    end_time = start_time + datetime.timedelta(seconds=args.timeout)
    print(f'{len(res)} messeges recieved')

    time_fmt = '%Y-%m-%d_%H:%M:%S'
    start_time = start_time.strftime(time_fmt)
    end_time = end_time.strftime(time_fmt)
    filename = f'{args.symbol}@{args.stream}_from_{start_time}_to_{end_time}.json'
    path = f'{args.output}/{filename}'

    with open(path, 'w') as f:
        json.dump(res, fp=f, indent=4)

    print('Output path:', path)

asyncio.run(main())
