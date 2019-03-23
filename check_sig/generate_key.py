import ecdsa
import requests
from hashlib import sha256
from . import keys
import json
import base58

SALT_ENDPOINT = "https://85z0ywf1ol.execute-api.ap-northeast-1.amazonaws.com/secretHashing0/"

def gen_private_key(password,symbol,nftId):

    salt = _get_salt(password,symbol,nftId)
    key = _genkey(password+salt)
    return key

def _get_salt(seed,symbol,nftId):

    print("=====salt of {0}, tokenid : {1}".format(symbol,nftId))
    seedHash = sha256(seed.encode()).hexdigest()
    payload = {
        "hash": seedHash,
        "symbol": symbol,
        "tokenId": nftId
    };
    res = requests.post(SALT_ENDPOINT,data=json.dumps(payload),headers={ "Content-Type": "application/json"})
    
    body = res.json()["body"]
    if len(body)!=64:
        raise
    return body

def _genkey(seed):
    hex_string = sha256(seed.encode()).hexdigest()
    integ = int(hex_string,16)
    priv_key = ecdsa.SigningKey.from_secret_exponent(curve=ecdsa.SECP256k1,secexp=integ)
    eoskey = keys.EOSKey()
    eoskey._sk = priv_key
    eoskey._vk = eoskey._sk.get_verifying_key()

    return eoskey.to_public(),eoskey.to_wif()
