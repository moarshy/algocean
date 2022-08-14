# Create Ocean instance
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
import streamlit as st
import os
os.environ['OCEAN_NETWORK_URL'] = 'http://ganache:8545'
config = ExampleConfig.get_config()
st.write(config)
ocean = Ocean(config)


# Create Alice's wallet
import os
from ocean_lib.web3_internal.wallet import Wallet




alice_private_key = os.getenv('TEST_PRIVATE_KEY1')

alice_wallet = Wallet(ocean.web3, alice_private_key, config.block_confirmations, config.transaction_timeout)

# Publish an NFT token
data_nft = ocean.create_data_nft('NFTToken2', 'NFT2', alice_wallet)
print(f"Created data NFT. Its address is {data_nft.address}")


# Create datatoken related to the above NFT.

datatoken = data_nft.create_datatoken("Datatoken 1", "DT1", from_wallet=alice_wallet)
st.write(f"Created datatoken. Its address is {datatoken.address}")


# config
st.write(f"config.network_url = '{config.network_url}'")
st.write(f"config.block_confirmations = {config.block_confirmations.value}")
st.write(f"config.metadata_cache_uri = '{config.metadata_cache_uri}'")
st.write(f"config.provider_url = '{config.provider_url}'")

# wallet
st.write(f"alice_wallet.address = '{alice_wallet.address}'")

# data NFT
st.write(f"data NFT token name: {data_nft.token_name()}")
st.write(f"data NFT symbol: {data_nft.symbol()}")

# datatoken
st.write(f"datatoken name: {datatoken.token_name()}")
st.write(f"datatoken symbol: {datatoken.symbol()}")