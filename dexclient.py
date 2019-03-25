from eospy.eos_client import EosClient
from eospy.endpoints import CONTRACT
from eospy.transaction_builder import TransactionBuilder, Action

class DEXClient(EosClient):

    def addsellobyid(self,symbol,token_id,price,memo):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "addsellobyid",
            "args": {"sym": symbol,"token_id":token_id,"price":price,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'addsellobyid', self.account , self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)
            
    def buyfromorder(self, buyer, symbol, token_id, memo ):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "buyfromorder",
            "args": {"sym": symbol,"token_id":token_id,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'buyfromorder',self.account , self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)
            
    def cancelsobyid(self,symbol, token_id):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "cancelsobyid",
            "args": {"sym": symbol,"token_id":token_id}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'cancelsobyid',self.account , self.permission, binargs),
        ))
        return self.push_transaction(transaction, chain_id)
    
    #quantity is assset type (like "10.0000 EOS") 
    #make sure 4 letters after the decimal point (1.0000)        
    def cancelsello(self,quantity):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "cancelsello",
            "args": {"seller": self.account,"quantity":quantity}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'cancelsello',self.account , self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)
            
    def addbuyorder(self,symbol,price,memo):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "addbuyorder",
            "args": {"buyer":self.account,"sym": symbol,"price":price,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'addbuyorder',self.account , self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)
            
    def selltoorder(self,symbol,token_id, order_id, memo):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "selltoorder",
            "args": {"sym": symbol,"token_id":token_id,"order_id":order_id,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'selltoorder',self.account , self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)
            
    def cancelbobyid(self,symbol, order_id):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "cancelbobyid",
            "args": {"sym": symbol,"order_id":token_id}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'cancelbobyid',self.account , self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)
            
    def cancelbuyo(self, quantity):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "cancelbuyo",
            "args": {"buyer": self.account,"quantity":quantity}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'cancelbuyo',self.account , self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)

    #value is assset type (like "10.0000 EOS") 
    #make sure 4 letters after the decimal point (1.0000)        
    def withdraw(self,value, memo):

        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, 
            "action": "withdraw",
            "args": {"user":self.account,"value":value,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'withdraw',self.account , self.permission, binargs),
        ))

        return self.push_transaction(transaction, chain_id)
            
    
