from client import PCSClient
from dexclient import DEXClient

PCS_ACCOUNT_FOR_EVERYONE = "pcseveryone1"
PCS_PRIVETEKEY_FOR_EVERYONE = "5KiFgPfSP1fK2uUaoxDDXjNSVNksq7gkMoZKfGmQtg1vcUHkuXc"

class PCS_EOS(PCSClient,DEXClient):
    pass

if __name__ == "__main__":

#    import requests
#    url = "http://127.0.0.1:8888/v1/wallet/open"
#    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
#    response = requests.request("POST", url, headers=headers)
#    print(response.text)

    pcsc = PCS_EOS(None,"http://127.0.0.1:8888",PCS_ACCOUNT_FOR_EVERYONE,"active",None,None)
    print(pcsc.chain_get_info())
    pcsc.set_keys_by_password("yarnstart","TST")
    print(pcsc.issuetoagent("TST",pcsc.subkey,""))

    #print("======================")
    #print(pcsc.create("TST"))
    #print(pcsc.issue("leohioleohio","2 BUG","test"))

    #print(pcsc.transferbyid("mokemokecore","BUG","2,"gift"))
    #print(pcsc.refreshkey("BUG",1,"EOS61ei7zBcVTJFP5PwgzPaFydVasnDgDGft6ckFRxnrpq4QNYtQB"))
    #print(pcsc.addsellobyid("BUG",1,"1.0000 EOS","pls buy"))
    #print(pcsc.cancelsobyid("BUG",1,))


    #print(pcsc.wallet_endpoint)
    #print(pcsc.wallet_open())
    #unlock = pcsc.wallet_unlock("PW5...")
    #print(unlock)
