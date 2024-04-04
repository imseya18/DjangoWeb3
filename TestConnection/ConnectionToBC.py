from web3 import Web3


class StoreScore:
    def __init__(self, infura_url, contract_address, abi, eth_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)
        self.eth_address = eth_address
        self.private_key = private_key

    def is_connected(self):
        return self.web3.is_connected()

    def get_current_block_number(self):
        return self.web3.eth.block_number

    def get_balance(self):
        balance = self.web3.eth.get_balance(self.eth_address)
        return self.web3.from_wei(balance, "ether")

    def get_match_by_id(self, match_id):
        try:
            match = self.contract.functions.getMatchById(match_id).call()
            return match
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_transaction_cost(balance_before, balance_after):
        return balance_before - balance_after

    @staticmethod
    def get_usd_transaction_cost(balance_before, balance_after):
        return (balance_before - balance_after) * 3500

    def add_match(self, match_id, tournament_id, player1_score, player2_score, player1_name, player2_name, winner):
        from .StoreInDB import add_match_to_db, delete_match_from_db
        try:
            nonce = self.web3.eth.get_transaction_count(self.eth_address)
            gas_estimate = self.contract.functions.addMatch(match_id, tournament_id, player1_score, player2_score, player1_name,
                                                            player2_name, winner).estimate_gas({'from': self.eth_address})
            transaction = self.contract.functions.addMatch(match_id, tournament_id, player1_score, player2_score,
                                                           player1_name, player2_name, winner).build_transaction({
                'chainId': self.web3.eth.chain_id,
                'gas': gas_estimate,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
            return txn_receipt
        except Exception as e:
            if "gas" in str(e).lower():
                print(e)
                print("erreur de gas")
                add_match_to_db(match_id, player1_score, player2_score, player1_name, player2_name, winner)
            elif "reverted" in str(e).lower():
                print("transaction revert:")
                print(e)
                delete_match_from_db(match_id)
            else:
                print(e)


    def add_tournament(self, match_id, tournament_id, player1_score, player2_score, player1_name, player2_name, winner):
        from .StoreInDB import add_match_to_db, delete_match_from_db
        try:
            nonce = self.web3.eth.get_transaction_count(self.eth_address)
            gas_estimate = self.contract.functions.addMatch(match_id, tournament_id, player1_score, player2_score, player1_name,
                                                            player2_name, winner).estimate_gas({'from': self.eth_address})
            transaction = self.contract.functions.addMatch(match_id, tournament_id, player1_score, player2_score,
                                                           player1_name, player2_name, winner).build_transaction({
                'chainId': self.web3.eth.chain_id,
                'gas': gas_estimate,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
            return txn_receipt
        except Exception as e:
            if "gas" in str(e).lower():
                print(e)
                print("erreur de gas")
                add_match_to_db(match_id, player1_score, player2_score, player1_name, player2_name, winner)
            elif "reverted" in str(e).lower():
                print("transaction revert:")
                print(e)
                delete_match_from_db(match_id)
            else:
                print(e)