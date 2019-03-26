from client import PCSClient
from dexclient import DEXClient
from eospy.endpoints import *

"""
one instance of this class is 
basically binded to one PCS-NFT token
"""

class PCS_EOS(PCSClient,DEXClient):

    pass
    """
    init is in eospy/eos_client
    def __init__(self, api_endpoint,wallet_endpoint,account,permission,subkey,subprivatekey)
    """

def recover_accountless_token(symbol,tokenId,password):

    pcsc = PCS_EOS()
    pcsc.set_subkeys_by_password(password,symbol,tokenId)
    return pcsc


def test_check_sig(symbol,tokenId,password):
    pcsc = recover_accountless_token(symbol,tokenId,password)
    result = pcsc.check_security(symbol,tokenId)
    if result["verify"]:
        print("verified")
    else:
        print("rejected")
    return result["verify"]


def create(new_symbol,account=None,permission="active"):

    print("making new token symbol: " +new_symbol)
    if not account:
        pcsc = PCS_EOS("pcseveryone2","test")
    else:
        pcsc = PCS_EOS(account,permission)
    pcsc.create(new_symbol)
    

