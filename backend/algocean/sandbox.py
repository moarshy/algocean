# Create Ocean instance
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
import streamlit as st
import os

# Create Alice's wallet
import os
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.web3_internal.constants import ZERO_ADDRESS


class OceanModule:
    default_wallet_key = 'default'
    wallets = {}
    pkhash2wallet = {}



    def __init__(config=None):
        if config == None:
            self.config = ExampleConfig.get_config()
        self.ocean = Ocean(config)
        self.web3 = self.ocean.web3

    @classmethod
    def get_config(cls):
        return ExampleConfig.get_config()
    

    def add_wallet(self, wallet_key:str='default', private_key:str='TEST_PRIVATE_KEY1'):
        '''
        wallet_key: what is the key you want to store the wallet in
        private_key: the key itself or an env variable name pointing to that key
        '''
        config = self.config
        # fetch the name or the key
        pk = os.getenv(pk, pk)

        # get the hash of the private key
        pk_hash = str(hash(pk))

        # check if wallet is registed
        pkhash_wallet_key = self.pkhash2wallet.get(pk_hash)

        if pkhash_wallet_key != None:
            # if the key is registered, then we will swtich the old key with the new key
            self.wallets[wallet_key] =  self.wallets.pop(pkhash_wallet_key)
            self.pkhash2wallet[pk_hash] = wallet_key
            self.wallet2pkhash[wallet_key] = self.wallet2pkhash.pop(pkhash_wallet_key)
        else:
            # if the k ey is not registered, we create the wallet with the private key and config
            self.wallets[wallet_key] = Wallet(self.web3, pk, config.block_confirmations, config.transaction_timeout)
            
            # store the pk hash associating with the wallet_key
            self.pkhash2wallet[pk_hash] = wallet_key
            self.wallet2pkhash[wallet_key] = pk_hash
        
        self.ensure_default_wallet()
        return self.wallets[wallet_key]

    def rm_wallet(self, key):
        '''
        remove wallet and all data relating to it
        '''
        del self.wallets[key]
        del self.pkhash2wallet[self.wallet2pkhash[key]]
        del self.wallet2pkhash[key]
        self.ensure_default_wallet()

    def list_wallets(self, keys_only=True):
        '''
        list wallets
        '''
        if keys_only:
            return self.wallets.keys()
        else:
            return  [(k,v) for k,v in self.wallets.items()]

    def get_wallet(self, wallet_key:str, handle_key_error=False):
        if handle_key_error:
            return self.wallets.get(wallet_key, None)
        else:
            return self.wallets[wallet_key]

    @property
    def wallet(self):
        # gets the default wallet
        return self.wallets[self.default_wallet_key]

    def set_default_wallet(self, key):

        self.default_wallet_key = key
        return self.default_wallet_key

    def ensure_default_wallet(self):
        if self.default_wallet_key not in self.wallets:
            if len(self.wallets) > 0:
                self.default_wallet_key = list(self.wallets.keys())[0]
            else:
                # if there are no more wallets, default  it to the original
                self.default_wallet_key = 'default'


    def ensure_wallet(self, wallet):
        if wallet == None:
            wallet = self.wallet
        return wallet

    def create_data_nft(name:str , symbol:str, wallet=None):
        wallet = self.ensure_wallet(wallet=wallet)
        data_nft = self.ocean.create_data_nft(name=name, symbol=symbol, from_wallet=wallet)
        
        self.data_nfts[symbol] = data_nft
        return data_nft

    def create_datatoken(self, name:str, symbol:str, data_nft=None, wallet=None):
        
        
    
module = OceanModule()
module.add_wallet(key='alice', pk='TEST_PRIVATE_KEY1')



with st.form('Publish Data'):

    alice_private_key = os.getenv('TEST_PRIVATE_KEY1')

    alice_wallet = Wallet(ocean.web3, alice_private_key, config.block_confirmations, config.transaction_timeout)

    # Publish an NFT token

    print(f"Created data NFT. Its address is {data_nft.address}")

    # Create datatoken related to the above NFT.

    datatoken = data_nft.create_datatoken("Datatoken 1", "DT1", from_wallet=alice_wallet)
    st.write(f"Created datatoken. Its address is {datatoken.address}")


    # # config
    # st.write(f"config.network_url = '{config.network_url}'")
    # st.write(f"config.block_confirmations = {config.block_confirmations.value}")
    # st.write(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
    # st.write(f"config.provider_url = '{config.provider_url}'")

    # # wallet
    # st.write(f"alice_wallet.address = '{alice_wallet.address}'")

    # # data NFT
    # st.write(f"data NFT token name: {data_nft.token_name()}")
    # st.write(f"data NFT symbol: {data_nft.symbol()}")

    # # datatoken
    # st.write(f"datatoken name: {datatoken.token_name()}")
    # st.write(f"datatoken symbol: {datatoken.symbol()}")




# # Specify metadata and services, using the Branin test dataset
# date_created = "2021-12-28T10:55:11Z"

# metadata = {
#     "created": date_created,
#     "updated": date_created,
#     "description": "Branin dataset",
#     "name": "Branin dataset",
#     "type": "dataset",
#     "author": "Trent",
#     "license": "CC0: PublicDomain",
# }

# # ocean.py offers multiple file types, but a simple url file should be enough for this example
# from ocean_lib.structures.file_objects import UrlFile
# url_file = UrlFile(
#     url="https://raw.githubusercontent.com/trentmc/branin/main/branin.arff"
# )

# # Publish asset with services on-chain.
# # The download (access service) is automatically created, but you can explore other options as well
# asset = ocean.assets.create(
#     metadata,
#     alice_wallet,
#     [url_file],
#     datatoken_templates=[1],
#     datatoken_names=["Datatoken 1"],
#     datatoken_symbols=["DT1"],
#     datatoken_minters=[alice_wallet.address],
#     datatoken_fee_managers=[alice_wallet.address],
#     datatoken_publish_market_order_fee_addresses=[ZERO_ADDRESS],
#     datatoken_publish_market_order_fee_tokens=[ocean.OCEAN_address],
#     datatoken_publish_market_order_fee_amounts=[0],
#     datatoken_bytess=[[b""]],
# )

# did = asset.did  # did contains the datatoken address
# print(f"did = '{did}'")