import requests
from eospy.eos_client import EosClient
from check_sig import check_sig ,generate_key
from eospy.endpoints import CONTRACT 
from eospy.transaction_builder import TransactionBuilder, Action

class PCSClient(EosClient):
   
    def check_security(self,symbol,tokenId):
        return check_sig.check_sig(symbol,tokenId,self.subprivatekey)

    def generateKey(self,password):
        return check_sig.generate_key(password)
                       
    def create(self,symbol):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"issuer": self.account, "sym": symbol}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'create',CONTRACT , self.permission, binargs),
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


    def transferid2(self, to , symbol ,token_id , memo ):

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

    def refreshkey2(self,symbol,token_id,new_subkey,sig):
    
        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "refreshkey2",
            "args": {"sym":symbol,"token_id":token_id , "subkey": new_subkey,"sig":sig}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'refreshkey2',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    def issueagent(self,symbol,sig,subkey):
        
        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "issueagent",
            "args": {"sym":symbol,"subkey":subkey,"sig":sig,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'issueagent',self.account, self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)

