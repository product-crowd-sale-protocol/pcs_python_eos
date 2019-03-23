import requests
import datetime
from eospy.eos_client import EosClient
from eospy import table_client
from check_sig import check_sig ,generate_key
from eospy.endpoints import CONTRACT
from eospy.transaction_builder import TransactionBuilder, Action

class PCSClient(EosClient):

    def check_security(self,symbol,tokenId):
        return check_sig.check_sig(symbol,tokenId,self.subprivatekey)

    @staticmethod
    def generateKey(password,symbol,tokenId):
        return generate_key.gen_private_key(password,symbol,tokenId)

    def set_keys_by_password(self,password,symbol,tokenId=None):

        #None is flag of automation. get next id automatically
        if tokenId==None :
            tokenId = table_client.get_token_lastid(symbol)
            print("Given ID of {0} is {1}".format(symbol,tokenId+1))
            tokenId = tokenId +1
        if tokenId<-1:
            raise

        pubkey,prvkey = PCSClient.generateKey(password,symbol,tokenId)
        print(pubkey)
        print(prvkey)
        self.subkey=pubkey
        self.subprivatekey= prvkey

    def create(self,symbol):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"issuer": self.account, "sym": symbol}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'create',self.account , self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def issue(self,given_user,quantity,memo):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "issue",
            "args": {"user": given_user, "quantity": quantity,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'issue', self.account, self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)

    def transferbyid(self, to , symbol ,token_id , memo ):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "transferbyid",
            "args": {"from": self.account,
                     "to": to,
                     "sym": symbol,
                     "token_id":token_id,
                     "memo":memo}
            })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'transferbyid',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def refreshkey(self,symbol,token_id,new_subkey):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "refreshkey",
            "args": {"sym":symbol,"token_id":token_id , "new_subkey": new_subkey}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'refreshkey',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def transferid2(self, to , symbol ,token_id):

        message = subkey_signature_in_contract("transferid2",symbol,token_id=token_id,to=to)
        sig = check_sig.sign_message_with_privatekey(self.subprivatekey,message,True)

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "transferid2",
            "args": {"to": to,
                     "sig":sig,
                     "sym": symbol,
                     "token_id":token_id,
                     "memo":""}
            })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'transferid2',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    def refreshkey2(self,symbol,token_id,new_subkey):

        message = subkey_signature_in_contract("refreshkey2",symbol,token_id=token_id,new_subkey=new_subkey)
        sig = check_sig.sign_message_with_privatekey(self.subprivatekey,message,True)

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "refreshkey2",
            "args": {"sym":symbol,"token_id":token_id , "new_subkey": new_subkey,"sig":sig}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'refreshkey2',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    def issuetoagent(self,symbol,subkey,memo):

        #get_last_id
        last_id = table_client.get_token_lastid(symbol)
        tokenId = last_id +1

        #making sig
        a_day = 24 * 60 * 60
        message = subkey_signature_in_contract("issuetoagent",symbol)
        sig = check_sig.sign_message_with_privatekey(self.subprivatekey,message,isbyte=True)

        binargs = self.chain_abi_json_to_bin({

            "code": CONTRACT, "action": "issuetoagent",
            "args": {"sym":symbol,"token_id":tokenId,"subkey":subkey,"sig":sig,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'issuetoagent',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    def lock(self,symbol,token_id):
        message = subkey_signature_in_contract("lock",symbol,token_id=token_id)
        sig = check_sig.sign_message_with_privatekey(self.subprivatekey,message,True)

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "lock",
            "args": {"sym":symbol,"token_id":token_id ,"sig":sig}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'lock',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

def subkey_signature_in_contract(action, sym, token_id=None, new_subkey=None, to=None):
    print((action,sym,token_id,new_subkey,to))
    from check_sig.format import Name,SymbolCode,Uint64,public_key_to_bytes34

    act_bin = bytes(Name(action))
    sym_bin = bytes(SymbolCode(sym))
    timestamp = int(datetime.datetime.now().timestamp()) // 15 * 15 * 1000 * 1000
    print("timestamp: {}".format(timestamp))
    ts_bin = bytes(Uint64(timestamp))

    if action == "refreshkey2":
        id_bin = bytes(Uint64(token_id))
        sk_bin = public_key_to_bytes34(new_subkey)
        message = act_bin + sym_bin + id_bin + sk_bin + ts_bin
    elif action == "issuetoagent":
        message = act_bin + sym_bin + ts_bin
    elif action == "lock":
        id_bin = bytes(Uint64(token_id))
        message = act_bin + sym_bin + id_bin + ts_bin
    elif action == "transferid2":
        to_bin =  bytes(Name(to))
        id_bin = bytes(Uint64(token_id))
        message = act_bin + to_bin + sym_bin + id_bin + ts_bin
        print(list(message))
        print(len(list(message)))
    else:
        raise
    return message
