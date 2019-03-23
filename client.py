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

    def set_keys_by_password(self,password,symbol,tokenId=False):

        #False is flag of automation. get next id automatically 
        if tokenId==False :
            tokenId = table_client.get_token_lastid(symbol)
            print("Given ID of {0} is {1}".format(symbol,tokenId+1))
             
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
            "args": {"sym":symbol,"token_id":token_id , "subkey": new_subkey}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'refreshkey',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def transferid2(self, to , symbol ,token_id ,sig, memo ):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "transferbyid",
            "args": {"to": to,
                     "sig":sig,
                     "sym": symbol,
                     "token_id":token_id,
                     "memo":memo}
            })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'transferid2',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    def refreshkey2(self,symbol,token_id,new_subkey):

        a_day = 24 * 60 * 60
        message = str(int(datetime.datetime.now().timestamp()/a_day) *a_day* 1000)        
        sig = check_sig.sign_message_with_privatekey(self.subprivatekey,message)

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "refreshkey2",
            "args": {"sym":symbol,"token_id":token_id , "subkey": new_subkey,"sig":sig}
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

def subkey_signature_in_contract(action, sym, token_id=False,new_subkey=False):

    from check_sig.format import Name,SymbolCode,Uint64,public_key_to_bytes34 

    action_name = Name(action)
    sym = SymbolCode(sym)
    timestamp = Uint64(int(datetime.datetime.now().timestamp()) // 15 * 15 * 1000 * 1000)
    print("timestamp: {}".format(int(timestamp)))

    if action=="refreshkey2":
        token_id = Uint64(token_id)
        message = bytes(action_name) + bytes(sym) + bytes(token_id) + public_key_to_bytes34(new_subkey) + bytes(timestamp)
        print(len(message))
    elif action=="issuetoagent":
        message = bytes(action_name) + bytes(sym) + bytes(timestamp)
        print(len(message)) 
    return message
    
