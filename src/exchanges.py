
import requests

def summary_bittrex(pairs):
    """Returns a list of summaries of requested pairs

    Arguments:
    pairs -- a list of tuple trading pairs e.g. [("BTC", "LTC"), ("ETH", "ADA")]

    Return:
    result -- a dictionary with keys "exception" (Exception) and "rates" (dict)
    
    """

    rates = {}

    for base, other in pairs:
        pair = f'{base}-{other}'
        url = f'https://bittrex.com/api/v1.1/public/getmarketsummary?market={pair}'
        response = requests.request("GET", url)
        resp = response.json()
        if not resp["success"]:
            raise Exception(f'Bittrex: {resp["message"]} (Pair: {pair})')

        summary = {
            "endpoint"  :   url,
            "bid"       :   float(resp["result"][0]["Bid"]),
            "ask"       :   float(resp["result"][0]["Ask"]),
            "last"      :   float(resp["result"][0]["Last"]),
            "volume"    :   float(resp["result"][0]["BaseVolume"]),
            "yesterday" :   float(resp["result"][0]["PrevDay"])
        }
        summary["change"] = round((summary["last"] - summary["yesterday"])/((summary["last"] + summary["yesterday"])/2) * 10**4)/10**2

        rates[pair] = summary
    
    return rates

def summary_luno(pairs):
    """Returns a list of summaries of requested pairs

    Arguments:
    pairs -- a list of tuple trading pairs e.g. [("BTC", "ZAR"), ("BTC", "ETH")]

    Return:
    result -- a dictionary with keys "exception" (Exception) and "rates" (dict)
    
    """

    rates = {}

    for base, other in pairs:
        pair = f'{other}{base}'.replace("BTC", "XBT")
        url = f'https://api.mybitx.com/api/1/ticker?pair={pair}'
        response = requests.request("GET", url)
        resp = response.json()
        if "error" in resp:
            raise Exception(f'Luno: {resp["error"]} (Pair: {pair})')

        summary = {
            "endpoint"  :   url,
            "bid"       :   float(resp["bid"]),
            "ask"       :   float(resp["ask"]),
            "last"      :   float(resp["last_trade"]),
            "volume"    :   float(resp["rolling_24_hour_volume"]),
        }

        

        rates[f'{base}-{other}'] = summary
    
    return rates

def summary_coinbase(pairs):
    """Returns a list of summaries of requested pairs

    Arguments:
    pairs -- a list of tuple trading pairs e.g. [("BTC", "ZAR"), ("BTC", "ETH")]

    Return:
    result -- a dictionary with keys "exception" (Exception) and "rates" (dict)
    
    """

    rates = {}

    for base, other in pairs:
        pair = f'{other}-{base}'
        url = f'https://api.gdax.com/products/{pair}/ticker'
        response = requests.request("GET", url)
        resp = response.json()
        
        if "message" in resp:
            # if resp["message"] == "NotFound":
            raise Exception(f'Coinbase: {resp["message"]} (Pair: {pair})')

        summary = {
            "endpoint"  :   url,
            "bid"       :   float(resp["bid"]),
            "ask"       :   float(resp["ask"]),
            "last"      :   float(resp["price"]),
            "volume"    :   float(resp["volume"]),
        }

        rates[f'{base}-{other}'] = summary
    
    return rates


