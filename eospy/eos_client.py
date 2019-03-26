import json
import logging
import time
import urllib.request
import urllib.parse
import urllib.error
from io import BytesIO

from .wallet_context_manager import WalletContextManager
from . import endpoints
from .transaction_builder import TransactionBuilder, Action


class EosClient:
    def __init__(self, account=None, permission=None, subkey=None, subprivatekey=None, api_endpoint=None, wallet_endpoint=None):

        if not api_endpoint:
            api_endpoint = endpoints.DEFAULT_EOS_API_ENDPOINT
        if not wallet_endpoint:
            wallet_endpoint = endpoints.DEFAULT_WALLET_ENDPOINT
            
        self.api_endpoint = api_endpoint
        self.wallet_endpoint = wallet_endpoint
        self.account = account
        self.permission = permission
        self.subkey = subkey
        self.subprivatekey = subprivatekey

    def request(self, endpoint, uri, body=None):
        """
        this is kinda qeird

        :param endpoint:
        :param uri:
        :param body:
        :return:
        """
        if body:
            body = json.dumps(body).encode()
        url = urllib.parse.urljoin(endpoint, uri)
        request = urllib.request.Request(url, data=body)
        try:
            response = urllib.request.urlopen(request)
            return json.load(response)
        except urllib.error.HTTPError as http_error:
            logger = logging.getLogger(__name__)
            http_error_response = http_error.read()
            logger.exception(http_error_response.decode())
            fp = BytesIO(http_error_response)
            raise urllib.error.HTTPError(http_error.url, http_error.code, http_error.msg, http_error.hdrs, fp)

    def api_request(self, uri, body=None):
        return self.request(self.api_endpoint, uri, body)

    def wallet_request(self, uri, body=None):
        if not self.wallet_endpoint:
            raise ValueError('No wallet endpoint set, cannot make wallet request!')
        return self.request(self.wallet_endpoint, uri, body)

    # ===== v1/wallet/ =====
    def wallet_create(self, wallet='default'):
        return self.wallet_request(endpoints.WALLET_CREATE, wallet)

    def wallet_unlock(self, password, wallet='default'):
        return self.wallet_request(endpoints.WALLET_UNLOCK, [wallet, password])

    def wallet_lock(self, wallet='default'):
        return self.wallet_request(endpoints.WALLET_LOCK, wallet)

    def wallet_open(self, wallet='default'):
        return self.wallet_request(endpoints.WALLET_OPEN, wallet)

    def wallet_import_key(self, private_key, wallet='default'):
        return self.wallet_request(endpoints.WALLET_IMPORT_KEY, [wallet, private_key])

    def wallet_get_public_keys(self):
        return self.wallet_request(endpoints.WALLET_GET_PUBLIC_KEYS)

    def wallet_sign_transaction(self, transaction, public_keys, chain_id):
        return self.wallet_request(
            endpoints.WALLET_SIGN_TRANSACTION, [transaction, public_keys, chain_id])

    # ===== v1/chain/ =====
    def chain_get_info(self):
        return self.api_request(endpoints.CHAIN_GET_INFO)

    def chain_get_block(self, num_or_id):
        return self.api_request(endpoints.CHAIN_GET_BLOCK, {'block_num_or_id': num_or_id})

    def chain_abi_json_to_bin(self, abi_args):
        return self.api_request(endpoints.CHAIN_ABI_JSON_TO_BIN, abi_args)

    def chain_get_required_keys(self, transaction, available_keys):
        return self.api_request(endpoints.CHAIN_GET_REQUIRED_KEYS, {
            'transaction': transaction,
            'available_keys': available_keys
        })

    def chain_push_transaction(self, transaction):
        return self.api_request(endpoints.CHAIN_PUSH_TRANSACTION, {
            'transaction': transaction,
            'compression': 'none',
            'signatures': transaction['signatures']
        })

    # ===== v1/history/ =====
    def history_get_actions(self, account_name, pos=-1, offset=-20):
        return self.api_request(endpoints.HISTORY_GET_ACTIONS, {
            'account_name': account_name,
            'pos': pos,
            'offset': offset,
        })

    def history_get_transaction(self, transaction_id):
        return self.api_request(endpoints.HISTORY_GET_TRANSACTION, {
            'id': transaction_id
        })

    # ===== EOSIO STANDARD TRANSACTIONS =====
    def get_transfer_binargs(self, from_, to, quantity, memo):
        return self.chain_abi_json_to_bin({
            "code": "eosio.token", "action": "transfer",
            "args": {"from": from_, "to": to, "quantity": quantity, "memo": memo}
        })['binargs']

    def transfer(self, from_, to, amount, memo, permission='active'):
        transfer_binargs = self.get_transfer_binargs(from_, to, amount, memo)
        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action('eosio.token', 'transfer', from_, permission, transfer_binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    # ===== EOSIO SYSTEM CONTRACT =====

    def get_system_newaccount_binargs(self, creator, name, owner_key, active_key):
        return self.chain_abi_json_to_bin({
            "code": "eosio", "action": "newaccount",
            "args": {
                "creator": creator, "name": name,
                "owner": {
                    "threshold": 1,
                    "keys": [{
                        "key": owner_key,
                        "weight": 1
                    }],
                    "accounts": [],
                    "waits": []
                },
                "active": {
                    "threshold": 1,
                    "keys": [{
                        "key": active_key,
                        "weight": 1
                    }],
                    "accounts": [],
                    "waits": []
                }
            }
        })['binargs']

    def get_system_buyram_binargs(self, payer, receiver, quant):
        return self.chain_abi_json_to_bin({
            "code": "eosio", "action": "buyram",
            "args": {"payer": payer, "receiver": receiver, "quant": quant}
        })['binargs']

    def get_system_buyrambytes_binargs(self, payer, receiver, bytes_):
        return self.chain_abi_json_to_bin({
            "code": "eosio", "action": "buyrambytes",
            "args": {"payer": payer, "receiver": receiver, "bytes": bytes_}})['binargs']

    def get_system_delegatebw_binargs(self, from_, receiver, stake_net_quantity, stake_cpu_quantity, transfer):
        return self.chain_abi_json_to_bin({
            "code": "eosio", "action": "delegatebw",
            "args": {
                "from": from_,
                "receiver": receiver,
                "stake_net_quantity": stake_net_quantity,
                "stake_cpu_quantity": stake_cpu_quantity,
                "transfer": transfer
            }})['binargs']

    def system_newaccount(self, creator_account, created_account, owner_key, active_key,
                          stake_net_quantity, stake_cpu_quantity, transfer, buy_ram_kbytes, permission='active'):
        newaccount_binargs = self.get_system_newaccount_binargs(
            creator_account, created_account, owner_key, active_key)
        buyrambytes_binargs = self.get_system_buyrambytes_binargs(
            creator_account, created_account, buy_ram_kbytes * 1024)
        delegatebw_binargs = self.get_system_delegatebw_binargs(
            creator_account, created_account, stake_net_quantity, stake_cpu_quantity, transfer)

        transaction, chain_id = TransactionBuilder(self).build_sign_transaction_request((
            Action('eosio', 'newaccount', creator_account, permission, newaccount_binargs),
            Action('eosio', 'buyrambytes', creator_account, permission, buyrambytes_binargs),
            Action('eosio', 'delegatebw', creator_account, permission, delegatebw_binargs),
        ))
        return self.push_transaction(transaction, chain_id)

    # ===== HIGHER-LEVEL METHODS =====
    def push_transaction(self, transaction, chain_id):
        available_public_keys = self.wallet_get_public_keys()
        required_public_keys = self.chain_get_required_keys(transaction, available_public_keys)['required_keys']
        signed_transaction = self.wallet_sign_transaction(transaction, required_public_keys, chain_id)
        return self.chain_push_transaction(signed_transaction)

    def get_last_action_seq_on_account(self, account):
        return self.history_get_actions(account, pos=-1, offset=-1)['actions'][0]['account_action_seq']

    def stream_actions_from_account(self, account_name, start_from=-1, filter_by_action_name=None):
        if start_from == -1:
            start_from = self.get_last_action_seq_on_account(account_name)
        while True:
            actions = self.history_get_actions(account_name, start_from, 100)['actions']
            for action in actions:
                if not filter_by_action_name:
                    yield action
                else:
                    if action['action_trace']['act']['name'] == filter_by_action_name:
                        yield action
            if not actions:
                time.sleep(0.5)
                continue
            start_from = actions[-1]['account_action_seq'] + 1

    def wallet_operations(self, wallet_password, wallet_name='default'):
        return WalletContextManager(self, wallet_password, wallet_name)

if __name__ == "__main__":
    #test
    ec = EosClient()
    print(ec.chain_get_info())
