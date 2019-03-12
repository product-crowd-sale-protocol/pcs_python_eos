URL = "https://api-kylin.eosasia.one"

class EOSAccount(keys.EOSKey):

    def __init__(self,account_name,private_key):
                
        self.account = account_name
        self.private_key= private_key

        if private_str :
            private_key, format, key_type = self._parse_key(private_str)
            self._sk = ecdsa.SigningKey.from_string(unhexlify(private_key), curve=ecdsa.SECP256k1)
        else :
            prng = self._create_entropy()
            self._sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=prng)
        self._vk = self._sk.get_verifying_key()
                   
    def call_create(self,symbol):
        self.command_args = ["--url",URL,"--key-file",self.private_key_file]
        self.command_args += [""]
        
    def call_issue():
    def call_transferbyid():
    def call_transfer():
    def call_burnbyid():
    def call_refreshkey():
    
    #DEX
    def call_addsellobyid():
    def call_buyfromorder():
    def call_cancelsobyid():
    def call_cancelsello():
    def call_addbuyorder():
    def call_selltoorder():
    def call_cancelbobyid():
    def call_cancelbuyo():
    def call_withdraw():
