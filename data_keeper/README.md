# Data Keeper
## Usage
```shell
python3 main.py --help

usage: main.py [-h] --symbol SYMBOL --stream STREAM --timeout TIMEOUT --output OUTPUT

Binance Stream Listener

optional arguments:
  -h, --help         show this help message and exit
  --symbol SYMBOL    Lowercase symbol
  --stream STREAM    Stream name
  --timeout TIMEOUT  Timeout in seconds
  --output OUTPUT    Output dir (output file name is formated <symbol>@<stream>_from_<start>_to_<end>)

```
## Example: get 20-depth orderbook each 100 ms for 30 min
```shell
python3 main.py --symbol btcusdt --stream depth20@100ms --timeout 1800 --output ../binance_stream_traces/
```

Available streams on [Binance WS API](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#detailed-stream-information)