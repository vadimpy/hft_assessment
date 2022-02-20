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
## Get best bid / ask quotes for 5 seconds
```shell
python3 main.py --symbol btcusdt --stream bookTiker --timeout 5 --output ../binance_stream_traces/
```

Available streams on [Binance WS API](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#detailed-stream-information)