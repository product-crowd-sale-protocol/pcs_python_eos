import time

def basic_usage(contract_function_name):

    if contract_function_name=="create":
        print("=====Explain "+contract_function_name+"()=======")
        print('pcsc.create("TST")')

    elif contract_function_name=="issue":
        print("=====Explain "+contract_function_name+"()=======")
        print("make 2 new tokens [TST *] to the accounts onigiri21423")
        print('pcsc.issue("onigiri21423","2 TST","test")')

    elif contract_function_name=="issuetoagent":
        print("=====Explain "+contract_function_name+"()=======")
        print('AFTER SET PASS LIKE : pcsc.set_keys_by_password("yarnstart","TST")')
        print('EXECUTE : pcsc.issuetoagent("TST",pcsc.subkey,"memo")')
        print('PLEASE MAKE SURE OF REMEMBERING TOKEN NUMBER')

    elif contract_function_name=="transferbyid":
        print("=====Explain "+contract_function_name+"()=======")
        print("send the token [TST 2] to the account [onigiri21423]")
        print('pcsc.transferbyid("onigiri21423","TST",2,"memo")')

    elif contract_function_name=="transferid2":
        print("=====Explain "+contract_function_name+"()=======")
        print("send the token [TST 2] to the account [onigiri21423]")
        print('pcsc.transferid2("onigiri21423","TST",2)')

    elif contract_function_name=="refreshkey":
        print("=====Explain "+contract_function_name+"()=======")
        print("set a new subkey for the token [TST 1]")
        print('pcsc.refreshkey("TST",1,"EOS61ei7zBcVTJFP5PwgzPaFydVasnDgDGft6ckFRxnrpq4QNYtQB")')

    elif contract_function_name=="refreshkey2":
        print("=====Explain "+contract_function_name+"()=======")
        print("set a new subkey for the token [TST 1]")
        print('pcsc.refreshkey2("TST",1,"EOS61ei7zBcVTJFP5PwgzPaFydVasnDgDGft6ckFRxnrpq4QNYtQB")')

    elif contract_function_name=="addsellobyid":
        print("=====Explain "+contract_function_name+"()=======")
        print('selling the token [TST 1] at the price 1.0000 EOS')
        print('pcsc.addsellobyid("TST",1,"1.0000 EOS","memo")')

    elif contract_function_name=="cancelobyid":
        print("=====Explain "+contract_function_name+"()=======")
        print('selling token [TST 1] at the price 1.0000 EOS')
        print('pcsc.cancelsobyid("BUG",1,)')
        print("ORDER ID YOU MADE CAN BE FOUND HERE : scope will be symbol")

    elif contract_function_name=="agent_refresh_key":
        print("=====Explain "+contract_function_name+"()=======")
        print("set a new subkey for the token [TST 1]")
        print('pcsc.agent_refresh_key("TST",1,"EOS61ei7zBcVTJFP5PwgzPaFydVasnDgDGft6ckFRxnrpq4QNYtQB")')
        print("[IMPORTANT]: this function does not need wallet(cleos) running.")

    elif contract_function_name=="agent_transfer":
        print("=====Explain "+contract_function_name+"()=======")
        print("send the token [TST 2] to the account [onigiri21423]")
        print('pcsc.transferid2("onigiri21423","TST",2)')
        print("[IMPORTANT]: this function does not need wallet(cleos) running.")

    elif contract_function_name=="check_security":
        print("=====Explain "+contract_function_name+"()=======")
        print("AFTER SUBKEY SET: pcsc.check_security(symbol,tokenId)")
        print("[IMPORTANT]: this function does not need wallet(cleos) running.")

    else:
        print("Could not find that function: "+contract_function_name)

def check_mode(x,y,sentence):

    print(sentence) 
    mode = input().strip()

    while mode!=x and mode !=y:
        print(x+" or "+y)
        mode = input().strip()
    return mode


def main():
    mode = check_mode("G","T","Guide(G) or Trouble(T)? just type (G / T)")

    if mode == "G":
        print("PCS is a security and liquidity protocol.")        
        print("Only knowing the set of (password,token_ID) is required to login to Secure Apps.")
        time.sleep(10)
        print("When you make the wallet afterawards, you are able to have that token more safely, and you are able to sell that token at DEX")
        print(" ")
        print(" ")
        time.sleep(5)
        desire = check_mode("X","T","Do you want the eXperience or going on a TALK (X/T)")
        if desire=="X":
            print("you can take a TEST token (symbol=TST number=5~20 password=yarnstart)")
            print("Please visit this website")
            print("https://link-airdrop.s3.amazonaws.com/index.html")
            return True

        print("With this middle ware protocol, devs can build secure apps easily")
        print("There are many many functions on this protocol.")
        print("The most important function for BUILDERs is check_security()")
        print("Because, with only using this function, anyone can build secure apps on website ")
        print("This function only passes particular token holders")
        print("So we can make apps for a specific community.")
        print(" ")
        print(" ")
        print("This was built simply because as well...")
        print("Such simple and open security systems can bind people.")
        time.sleep(30)
        print("transfer and refreshkey are also important for users.")
        print("There are three types of them ,for admins, for wallet users, and for no-wallet no-account users.")
        print("This partision makes your apps on blockchain far more easy to use for everybody.")        
        time.sleep(20)
        print(" ")
        print(" ")
        print("Well, in README.md or client.py, you can find many functions.")
        flag = "Y"
        while flag=="Y":
            flag = check_mode("Y","N","Any function do you want to check?")
            if flag=="Y":
                func = input("what is the name of the function? ").strip()            
                basic_usage(func)
        print("I see...")
        print("The permission pcseveryone2@test is yours. The key is 5KhcoSuV9vCyDY5efv7giGdpEmbyuscWfT9R3tY2dmGy9E7ZotM")
        print(" It's stuck permission, so there's no conflict. Don't mind.")
        print("Feel free.")

    if mode == "T":
        known = check_mode("Y","N","Do you know the name of function causing trouble? (Y/N)")
        if known=="Y":
            function_name = input("What's that function name?").strip()
            basic_usage(function_name)
        else:
            serious = check_mode("Y","N","Serious Security Bug? (Y/N)")
            if serious =="Y":
                print("Please DM or reply to @leo_hio on Twitter")
                return True            

            print("IF IT'S A PROBLEM OF NETWORK....")
            print("Please check eospy/endpoints and..")
            print("Change to alternative ENDPOINTS")
            print(" ")
            print(" ")
            time.sleep(4)
            print("IF IT'S A PROBLEM OF CONTRACT OR BLOCKCHAIN..")
            print("Please check out the name of the function you're calling and..")
            print("Be careful of EOS or RAM shortage..")
            print("you can get fausets at ")
            print(" http://faucet.cryptokylin.io/get_token?your_account_name")
            print(" ")
            print(" ")
            time.sleep(4)
            print("IF IT'S A PROBLEM OF AGENT..")
            print("Please make sure that you have a correct set of (symbol,id,password)")
            print("if you fail with PCS_EOS.check_sig(symbol,id) ...")
            print("It's a wrong set")


if __name__ == "__main__":
    main()
