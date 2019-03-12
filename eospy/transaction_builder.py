import datetime

from . import utils


class Action:
    def __init__(self, account, name, actor, permission, data):
        self.account = account
        self.name = name
        self.authorization = [{
            'actor': actor,
            'permission': permission
        }]
        self.data = data


class TransactionBuilder:
    def __init__(self, eos_client):
        self.eos_client = eos_client

    @staticmethod
    def get_action(account, name, actor, permission, data):
        return {
            "account": account,
            "name": name,
            "authorization": [{
                "actor": actor,
                "permission": permission
            }
            ],
            "data": data
        }

    @staticmethod
    def get_transaction(
            expiration, ref_block_num, ref_block_prefix, max_net_usage_words=0, max_cpu_usage_ms=0, delay_sec=0,
            context_free_actions=None, actions=None, transaction_extensions=None, signatures=None,
            context_free_data=None):

        if not context_free_actions:
            context_free_actions = []
        if not actions:
            actions = []
        if not transaction_extensions:
            transaction_extensions = []
        if not signatures:
            signatures = []
        if not context_free_data:
            context_free_data = []

        return {
            "expiration": utils.datetime_to_eos_timestamp(expiration),
            "ref_block_num": ref_block_num,
            "ref_block_prefix": ref_block_prefix,
            "max_net_usage_words": max_net_usage_words,
            "max_cpu_usage_ms": max_cpu_usage_ms,
            "delay_sec": delay_sec,
            "context_free_actions": context_free_actions,
            "actions": actions,
            "transaction_extensions": transaction_extensions,
            "signatures": signatures,
            "context_free_data": context_free_data
        }

    def build_sign_transaction_request(self, actions):
        get_info = self.eos_client.chain_get_info()
        ref_block_num = get_info['last_irreversible_block_num']
        ref_block = self.eos_client.chain_get_block(ref_block_num)
        ref_block_prefix = ref_block['ref_block_prefix']
        timestamp = utils.eos_timestamp_to_datetime(ref_block['timestamp'])
        expiration = timestamp + datetime.timedelta(minutes=10)  # hardcoded ten minutes to expire
        chain_id = get_info['chain_id']

        actions = [e.__dict__ for e in actions]

        return \
            TransactionBuilder.get_transaction(expiration, ref_block_num, ref_block_prefix, actions=actions), chain_id
