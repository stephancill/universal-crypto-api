#!/usr/bin/env python

import exchanges
from sanic import Sanic
from sanic.response import json
import sys

app = Sanic()
exchanges = {
    "bittrex": exchanges.summary_bittrex,
    "luno": exchanges.summary_luno,
    "coinbase": exchanges.summary_coinbase
}

def extract_pairs(raw):
    """Return a list of tuple pairs from a string of comma-separated pairs"""
    try:
        pairs = list(set([(p.split("-")[0].strip().upper(), p.split("-")[1].strip().upper()) for p in raw.split(",")]))
    except IndexError as e:
        raise IndexError("Invalid pair")

    for x, y in pairs:
        if not (len(x) > 1 and len(y) > 1):
            raise Exception(f'Invalid pair: {x}-{y}')
        
    if len(pairs) is 0:
        raise Exception("No valid pairs")

    return pairs

@app.route("/v0/summary")
async def summary(request):
    """Sample request: https://127.0.0.1:8000/summary?bittrex=BTC-DOGE,BTC-ADA,BTC-ETH&luno=BTC-ZAR """
    
    result = {} # Key: exchange, Value: list of pairs 
    
    # Extract pairs
    try:
        for exchange in request.raw_args.keys():
            result[exchange.lower()] = extract_pairs(request.raw_args[exchange])

    except Exception as e:
        return json({"success": False, "result": f'An error occurred in parsing your request. ({e})'}, status=400)

    try:
        for exchange in result.keys():
            if exchange in exchanges:
                result[exchange] = exchanges[exchange](result[exchange])
            else:
                raise Exception(f'Exchange ({exchange}) not listed')
    except Exception as e:
        return json({"success": False, "result": f'An error occurred in processing your request. ({e})'}, status=400)

    return json({"success": True, "result": result})

if __name__ == "__main__":
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except Exception:
        host = "0.0.0.0"
        port = 8080

    app.run(host=host, port=port)