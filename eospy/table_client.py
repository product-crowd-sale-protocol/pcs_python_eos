import requests
from . import endpoints
import json

def get_token_table(scope,limit):

    url = "https://api-kylin.eosasia.one:443/v1/chain/get_table_rows"
    req = {"json": True,"code":endpoints.CONTRACT,"reverse":True,"scope":scope,"table":"token","limit":limit}

    result = requests.post(url,json=req,headers={ "Content-Type":"application/json"}).json()
    return result["rows"]

def get_token_lastid(symbol):
    res = get_token_table(symbol,1)
    if len(res):
        return res[0]["id"]
    else:
        return -1
