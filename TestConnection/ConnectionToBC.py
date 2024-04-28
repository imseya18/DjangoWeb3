from web3 import Web3
from rest_framework.response import Response
from rest_framework import status


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

    def get_tournament_by_id(self, tournament_id):
        try:
            tournament = self.contract.functions.getTournament(tournament_id).call()
            return tournament
        except Exception as e:
            print(e)
            return None

    def get_match_by_player(self, player_id):
        try:
            matchs = self.contract.functions.getPlayerMatchs(player_id).call()
            return matchs
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_transaction_cost(balance_before, balance_after):
        return balance_before - balance_after

    @staticmethod
    def get_usd_transaction_cost(balance_before, balance_after):
        return (balance_before - balance_after) * 3250

    def add_match(self, match_data):
        from .StoreInDB import add_match_to_db, delete_match_from_db
        try:
            match_list = list(match_data.values())
            nonce = self.web3.eth.get_transaction_count(self.eth_address)
            gas_estimate = self.contract.functions.addMatch(*match_list).estimate_gas({'from': self.eth_address})
            transaction = self.contract.functions.addMatch(*match_list).build_transaction({
                'chainId': self.web3.eth.chain_id,
                'gas': gas_estimate,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
            print(txn_receipt['transactionHash'].hex())
            return Response(data=match_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            if "gas" in str(e).lower():
                print(e)
                print("erreur de gas")
                add_match_to_db(**match_data)
                return Response(data=match_data, status=status.HTTP_201_CREATED)
            elif "reverted" in str(e).lower():
                print("transaction revert:")
                print(e)
                delete_match_from_db(match_data['match_id'])
                error_message = "this match already exists"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(e)
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    def add_tournament(self, tournament_data):
        from .StoreInDB import add_tournament_to_db, delete_tournament_from_db
        try:
            tournament_list = list(tournament_data.values())
            nonce = self.web3.eth.get_transaction_count(self.eth_address)
            gas_estimate = self.contract.functions.addTournament(*tournament_list).estimate_gas({'from': self.eth_address})
            transaction = self.contract.functions.addTournament(*tournament_list).build_transaction({
                'chainId': self.web3.eth.chain_id,
                'gas': 0,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
            print(txn_receipt['transactionHash'].hex())
            return Response(data=tournament_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            if "gas" in str(e).lower():
                print(e)
                print("erreur de gas")
                add_tournament_to_db(**tournament_data)
                return Response(data=tournament_data, status=status.HTTP_201_CREATED)
            elif "reverted" in str(e).lower():
                print("transaction revert:")
                print(e)
                delete_tournament_from_db(tournament_data['tournament_id'])
                error_message = "this tournament already exists"
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(e)
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)