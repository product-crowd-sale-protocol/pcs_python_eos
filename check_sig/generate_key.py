import ecdsa
import requests
from hashlib import sha256
from . import keys

def get_salt(password):

def genkey(seed):
    hex_string = sha256(seed.encode()).hexdigest()
    integ = int(hex_string,16)
    y = ecdsa.SigningKey.from_secret_exponent(curve=ecdsa.SECP256k1,secexp=integ)
    a = keys.EOSKey()
    a._sk = y
    a._vk = a._sk.get_verifying_key()
    return a.to_public()
