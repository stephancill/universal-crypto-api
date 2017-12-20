# universal-crypto-api
Endpoints of the most popular crypto exchanges aggregated into a central endpoint.

# Requirements
* Python 3.6
* Pipenv

# Installation
1. `git clone https://github.com/stephancill/universal-crypto-api.git`
2. `cd universal-crypto-api`
3. `pipenv install`

# Usage
To start the server, do `pipenv run python src/main.py`

URL query structure: 

`http://ENDPOINT/v<API_VERSION>/summary?<EXCHANGE_1>=<PAIR_1>,<PAIR_2>&<EXCHANGE_2>=<PAIR_1>,<PAIR_2>`

e.g.

`http://localhost:8080/v0/summary?bittrex=BTC-DOGE,BTC-ETH&coinbase=USD-BTC`

The API currently supports the following exchanges:
* Bittrex
* Luno
* Coinbase

The response has the following structure:
```
{
    "success": bool,
    "result": {
        "<EXCHANGE_1>": {
            "<PAIR_1>": {
                "endpoint": URL used to communicate with external API,
                "bid": float,
                "ask": float,
                "last": float,
                "volume": float (base),
                "yesterday": float, *
                "change": float (%) *
            },
            "<PAIR_2>": {...}
        },
        "EXCHANGE_2": {...}
    }
}

* Subject to availability
```

The result of the example query will be:

```
{
    "success": true,
    "result": {
        "bittrex": {
            "BTC-ETH": {
                "endpoint": "https://bittrex.com/api/v1.1/public/getmarketsummary?market=BTC-ETH",
                "bid": 0.04660601,
                "ask": 0.04679093,
                "last": 0.04678,
                "volume": 7982.8513052,
                "yesterday": 0.04696,
                "change": -0.38
            },
            "BTC-DOGE": {
                "endpoint": "https://bittrex.com/api/v1.1/public/getmarketsummary?market=BTC-DOGE",
                "bid": 3.2e-7,
                "ask": 3.3e-7,
                "last": 3.3e-7,
                "volume": 522.71876288,
                "yesterday": 3.3e-7,
                "change": 0
            }
        },
        "coinbase": {
            "USD-BTC": {
                "endpoint": "https://api.gdax.com/products/BTC-USD/ticker",
                "bid": 17396.48,
                "ask": 17397.32,
                "last": 17397.32,
                "volume": 49085.7326418
            }
        }
    }
}
```

# Contributing
If you feel like contributing or adding an additional exchange, create a function in `exchanges.py` that accepts an array of symbol pairs (tuples) in the form [(base, other)] similar to the ones that are currently implemented and submit a pull request.