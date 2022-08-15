# Create Ocean instance
import streamlit as st
import os, sys
sys.path.append(os.getenv('PWD'))

from algocean.utils import RecursiveNamespace, dict_put, dict_has
from algocean.client import ClientModule
from algocean.config.loader import ConfigLoader

from ocean_lib.example_config import ExampleConfig
from ocean_lib.web3_internal.contract_base import ContractBase
from ocean_lib.models.datatoken import Datatoken
from ocean_lib.ocean.ocean import Ocean
from typing import *
# Create Alice's wallet

from ocean_lib.models.data_nft import DataNFT
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
import fsspec



class OceanModule:
    default_cfg_path = 'ocean.module'
    default_wallet_key = 'default'
    wallets = {}


    def __init__(self, config=None):
        self.data_nfts = {}
        self.data_tokens = {}
        
        self.client = self.get_clients()
        self.config = self.get_config(config=config)

        self.ocean = Ocean(self.config['ocean'])
        self.web3 = self.ocean.web3

        

    def get_clients(self):
        return ClientModule()
    
    def get_config(self, config=None):
        self.config_loader = ConfigLoader()
        if config == None:
            config = self.config_loader.load(path=self.default_cfg_path)
            config['ocean'] = ExampleConfig.get_config()
        return config


    def get_existing_wallet_key(self, private_key:str=None, address:str=None):
        for w_k, w in self.wallets.items():
            if private_key==w.private_key or address == w.address:
                return w_k

        return None

    def add_wallet(self, wallet_key:str='default', private_key:str='TEST_PRIVATE_KEY1'):
        '''
        wallet_key: what is the key you want to store the wallet in
        private_key: the key itself or an env variable name pointing to that key
        '''
        # fetch the name or the key
        private_key = os.getenv(private_key, private_key)

        existing_wallet_key = self.get_existing_wallet_key(private_key=private_key)
        # if the key is registered, then we will swtich the old key with the new key
        if existing_wallet_key == None:
            self.wallets[wallet_key] = Wallet(web3=self.web3, private_key=private_key, block_confirmations=self.config['ocean'].block_confirmations, transaction_timeout=self.config['ocean'].transaction_timeout)  
        else:
            self.wallets[wallet_key] =  self.wallets.pop(existing_wallet_key)

        self.ensure_default_wallet()
        return self.wallets[wallet_key]

    def rm_wallet(self, key):
        '''
        remove wallet and all data relating to it
        '''
        del self.wallets[key]
        self.ensure_default_wallet()

    def list_wallets(self, keys_only=True):
        '''
        list wallets
        '''
        if keys_only:
            return list(self.wallets.keys())
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
        elif isinstance(wallet, str):
            wallet = self.wallets[wallet]
        elif isinstance(wallet,Wallet):
            wallet = wallet
        else:
            raise Exception(f'Bro, the wallet {wallet} does not exist or is not supported')

        return wallet

    def create_data_nft(self, name:str , symbol:str, wallet:Union[str, Wallet]=None):
        wallet = self.ensure_wallet(wallet=wallet)

        nft_key =  symbol
        data_nft = self.data_nfts.get(nft_key)
        if data_nft == None:
            data_nft = self.ocean.create_data_nft(name=name, symbol=symbol, from_wallet=wallet)
            self.data_nfts[nft_key] = data_nft

        return data_nft

    def ensure_data_nft(self, data_nft:Union[str, DataNFT]): 
        if isinstance(data_nft, str):
            return self.data_nfts[data_nft]
        elif isinstance(data_nft, DataNFT):
            return data_nft
        else:
            raise Exception(f'The Data nft {data_nft} is not supported fam')

    def list_data_nfts(self):
        return list(self.data_nfts.keys())

    def create_datatoken(self, name:str, symbol:str, data_nft:Union[str, DataNFT]=None, wallet:Union[str, Wallet]=None):
        wallet = self.ensure_wallet(wallet)
        data_nft = self.ensure_data_nft(data_nft)

        nft_symbol = data_nft.symbol()
        key = '.'.join([nft_symbol, symbol])

        data_token = self.data_tokens.get(key)

        if data_token == None:
            datatoken = data_nft.create_datatoken(name=name, symbol=symbol, from_wallet=wallet)
            
            self.data_tokens[key] = datatoken
        
        return self.data_tokens[key]


    def get_contract(self, address:str, contract_class=ContractBase):
        return contract_class(web3=self.web3, address=address)
    
    def get_address(self, contract):
        return contract.address

    def load(self):
        self.load_state()
        # some loading post processing
        for k,v in self.data_nfts.items():
            self.data_nfts[k] = self.get_contract(address=v, contract_class=DataNFT)
        for k,v in self.data_tokens.items():
            self.data_tokens[k] = self.get_contract(address=v, contract_class=Datatoken)


    def load_state(self):
        for k, v in self.config['load'].items():
            load_fn = getattr(getattr(self.client, v['module']), v['fn'])
            data = load_fn(**v['params'])
            if data == None:
                data = v.get('default', data)
            self.__dict__[k] = data



    def save(self):
        # some loading post processing
        for k,v in self.data_nfts.items():
            self.data_nfts[k] = self.get_address(contract=v)
        for k,v in self.data_tokens.items():
            self.data_tokens[k] = self.get_address(contract=v)

        self.save_state()

    def save_state(self):
        for k, v in self.config['save'].items():

            data = self.__dict__[k]
            save_fn = getattr(getattr(self.client, v['module']), v['fn'])
            save_fn(**v['params'], data=data)


    
module = OceanModule()

module.load()

# module.add_wallet(wallet_key='alice', private_key='TEST_PRIVATE_KEY1')
# module.create_data_nft(name='DataNFT1', symbol='NFT1')
# module.create_data_nft(name='DataNFT1', symbol='NFT2')
# module.create_data_nft(name='DataNFT1', symbol='NFT3')
# module.create_datatoken(name='DataToken1', symbol='DT1', data_nft='NFT1')
# module.create_datatoken(name='DataToken1', symbol='DT2', data_nft='NFT1')

st.write(module.data_tokens, module.data_nfts)
module.save()
# st.write(module.data_nfts)


