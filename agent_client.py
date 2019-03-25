import requests
AGENT_URL = "https://78qy7hxmjd.execute-api.ap-northeast-1.amazonaws.com/pcsSecurity/eosagent"

def send_agent_refreshkey_order(sym,tid,new_key,sig):

    req = {"AgentEvent":"REFRESH","symbolCode":sym, "signature":sig, "tokenId":tid, "newSubKey":new_key ,"broadcast":"lambda"}

    result = requests.post(AGENT_URL,json=req,headers={ "Content-Type":"application/json"}).json()
    tx = result["signedTransaction"]
    return tx["transaction"],tx["transaction_id"]

def send_agent_transfer_order(sym,tid,new_address,sig):

    req = {"AgentEvent":"TRANSFER","symbolCode":sym, "signature":sig, "tokenId":tid, "newAddress":new_address,"broadcast":"lambda"}
    result = requests.post(AGENT_URL,json=req,headers={ "Content-Type":"application/json"}).json()
    tx = result["signedTransaction"]
    return tx["transaction"],tx["transaction_id"]
