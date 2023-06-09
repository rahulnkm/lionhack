from web3 import Web3
from dotenv import dotenv_values

config = dotenv_values("../.env")


class TX:

    def __init__(self, frm, to, value, chain):
        self.value = value
        if chain == "ETH":
            self.w3 = Web3(Web3.HTTPProvider(config["ALCHEMY_API_URL"]))
            self.chain_id = 5  # Goerli Testnet
        elif chain == "AGOR":
            self.w3 = Web3(Web3.HTTPProvider(config["ARBITRUM_URL"]))
            self.chain_id = 421613  # Arbitrum Goerli Testnet
        elif chain == "AVAX":
            self.w3 = Web3(Web3.HTTPProvider(config["AVA_URL"]))
            self.chain_id = 43113  # Fuji Testnet (Avalanche C-Chain)
        else:
            raise ValueError("Invalid chain specified")

        self.frm = self.w3.to_checksum_address(frm)
        self.to = self.w3.to_checksum_address(to)

    def to_dict(self):
        val = {
            "from": self.frm,
            'to': self.to,
            'value': self.w3.to_wei(self.value, "ether"),
            "nonce": self.w3.eth.get_transaction_count(self.frm),
            "gas": 21_000,
            "gasPrice": self.w3.eth.gas_price,
            "chainId": self.chain_id
        }
        return val

def send_tx(tx: TX):

    private_key = config["SAMPLE_PRIVATE_KEY"]

    signed_tx = tx.w3.eth.account.sign_transaction(tx.to_dict(), private_key)

    tx_hash = tx.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(tx.w3.to_hex(tx_hash))
