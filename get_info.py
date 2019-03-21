import requests
from eospy import eos_client
ec = eos_client.EosClient()
print(ec.chain_get_info())

