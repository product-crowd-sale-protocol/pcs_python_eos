from eospy.eos_client import EosClient
from check_sig import *

class PSCAccount(EosClient):
   
    def checkSecurity(self,symbol,tokenId):
        return check_sig(symbol,tokenId,self.subprivatekey)
                       
    def create(self,symbol,AGENT=False):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"issuer": self.account, "sym": symbol}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'create',self.account , self.permission, transfer_binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def issue(self,quantity,memo,AGENT=False):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"issuer": self.account, "quantity": quantity,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'issue',self.account, self.permission, transfer_binargs),
        ))

        return self.push_transaction(transaction, chain_id)
    
    def transferbyid(self, to , symbol , token_id , memo ,AGENT=False):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "transferbyid",
            "args": {"from": self.account, 
                     "to": to,
                     "symbol": symbol,
                     "token_id":token_id,
                     "memo":memo}
            })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'transferbyid',self.account, self.permission, transfer_binargs),
        ))
        return self.push_transaction(transaction, chain_id)


    def refreshkey(self,symbol,token_id,new_subkey,AGENT=False):
    
        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"symbol":symbol,"token_id":token_id , "subkey": new_subkey}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'refreshkey',self.account, self.permission, transfer_binargs),
        ))
        return self.push_transaction(transaction, chain_id)
