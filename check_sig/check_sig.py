##python 3.6
import datetime
import requests
import json
from . import keys
from . import utils
from hashlib import sha256

APINAME = "checkSig",
CONTRACT = "toycashio123"
CHAIN_ID = "5fff1dae8dc8e2fc4d5b23b2c7665c97f9e9d8edf2b6485a86ba311c25639191"
API_URL = "https://2u1ebl117d.execute-api.ap-northeast-1.amazonaws.com/pcs_api_beta/ryodansecurity"


def check_sig(symbol,tokenId,privatekey):
    
    a_day = 24 * 60 * 60
    message = str(int(datetime.datetime.now().timestamp()/a_day) *a_day* 1000)
    #sig = False
    #prv = sha256(privatekey.encode()).hexdigest()
    #if message==global_sign.get("message"):
    #    sig = global_sign["sig"].get(prv)
    
    #if not sig:
    sig = sign_message_with_privatekey(privatekey,message)
    #    global_sign["sig"]["prv"] = sig

    auth = call_check_sig_api(symbol,tokenId,sig,message)
    return auth

def sign_message_with_privatekey(privatekey,message,isbyte=False):

    eoskey = keys.EOSKey(privatekey)

    if isbyte:
        digest = utils.sha256(message)
    else:
        digest = utils.sha256(message.encode())
    sign = eoskey.sign(digest)
    return sign

def call_check_sig_api(symbol,tokenId,sig,message):

    payload = {
        "name": APINAME,#"checkSig",
        "contract": CONTRACT,#"toycashio123",
        "symbol": symbol,
        "tokenId": tokenId,
        "sig": sig,
        "message": message
    };
    headers = { 
        "Content-Type": "application/json; charset=utf-8",
        "method": "POST",
        "mode": "cors",
        "cache": "no-cache",
    };

    res = requests.post(API_URL, data=json.dumps(payload), headers=headers)
    return res.json()

