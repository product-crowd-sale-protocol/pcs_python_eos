import requests
from eospy.eos_client import EosClient
from check_sig import check_sig
from eospy.endpoints import CONTRACT 
from eospy.transaction_builder import TransactionBuilder, Action

class PCSClient(EosClient):
   
    def check_security(self,symbol,tokenId):
        return check_sig.check_sig(symbol,tokenId,self.subprivatekey)

    def generateKey(self,password):
                       
    def create(self,symbol,AGENT=False):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"issuer": self.account, "sym": symbol}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'create',CONTRACT , self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def issue(self,given_user,quantity,memo,AGENT=False):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "issue",
            "args": {"user": given_user, "quantity": quantity,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'issue', self.account, self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)
    
    def transferbyid(self, to , symbol , token_id , memo ,AGENT=False):

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


    def refreshkey(self,symbol,token_id,new_subkey,AGENT=False):
    
        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "refreshkey",
            "args": {"sym":symbol,"token_id":token_id , "subkey": new_subkey}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'refreshkey',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)
