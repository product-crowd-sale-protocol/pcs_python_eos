#DEX

class DEXManager(EosClient):
    def addsellobyid(self,sym,token_id,price,memo):
        binargs = self.chain_abi_json_to_bin({
            "code": CONTRACT, "action": "create",
            "args": {"sym": symbol,"token_id":token_id,"price":price,"memo":memo}
        })['binargs']

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action(CONTRACT, 'addsellobyid',self.account , self.permission, transfer_binargs),
        ))
        return self.push_transaction(transaction, chain_id)
            
    def call_buyfromorder():
    def call_cancelsobyid():
    def call_cancelsello():
    def call_addbuyorder():
    def call_selltoorder():
    def call_cancelbobyid():
    def call_cancelbuyo():
    def call_withdraw():
    
