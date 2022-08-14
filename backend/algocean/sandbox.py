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
data_nft = ocean.create_data_nft('NFTToken1', 'NFT1', alice_wallet)
print(f"Created data NFT. Its address is {data_nft.address}")