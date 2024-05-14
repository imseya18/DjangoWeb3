from web3 import Web3
from rest_framework.response import Response
from rest_framework import status
from .loger_config import setup_logger
from web3.exceptions import TimeExhausted
import requests

logger = setup_logger(__name__)


class StoreScore:
    def __init__(self, infura_url, contract_address, abi, eth_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)
        self.eth_address = eth_address
        self.private_key = private_key
        self.maxPriorityFeePerGas = 1
        self.maxFeePerGas = 0
        self.last_tx = None
        self.nb_passage = 1
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
            logger.info(e)
            return None

    def get_tournament_by_id(self, tournament_id):
        try:
            tournament = self.contract.functions.getTournament(tournament_id).call()
            return tournament
        except Exception as e:
            logger.info(e)
            return None

    def get_match_by_player(self, player_id):
        try:
            matchs = self.contract.functions.getPlayerMatchs(player_id).call()
            return matchs
        except Exception as e:
            logger.info(e)
            return None

    @staticmethod
    def get_transaction_cost(balance_before, balance_after):
        return balance_before - balance_after

    @staticmethod
    def get_usd_transaction_cost(balance_before, balance_after):
        return (balance_before - balance_after) * 3250

    #def get_gas_price_by_api(self):
    #    try:
    #        gas_api_response = requests.get("https://sepolia.beaconcha.in/api/v1/execution/gasnow")
    #        gas_api_data = gas_api_response.json()
    #        max_priority_fee_per_gas = gas_api_data["data"]["rapid"]
    #        return max_priority_fee_per_gas
    #    except Exception as e:
    #        logger.info(e)

    def create_match_transaction(self, match_list):
        nonce = self.web3.eth.get_transaction_count(self.eth_address)
        gas_estimate = self.contract.functions.addMatch(*match_list).estimate_gas({'from': self.eth_address})
        logger.info(f"gas_estimate = {gas_estimate}")
        logger.info(f"maxPriorityFeePerGas = {self.maxPriorityFeePerGas}")
        if self.maxFeePerGas == 0:
            latest_block = self.web3.eth.get_block('latest')
            self.maxFeePerGas = latest_block['baseFeePerGas'] * 2
        else:
            self.maxFeePerGas = round(self.maxFeePerGas * 1.2)
        logger.info(f"maxFeePerGas = {self.maxFeePerGas}")
        return self.contract.functions.addMatch(*match_list).build_transaction({
            'chainId': self.web3.eth.chain_id,
            'gas': gas_estimate,
            'maxFeePerGas': self.maxFeePerGas,
            'maxPriorityFeePerGas': Web3.to_wei(self.maxPriorityFeePerGas * 2, 'gwei'),
            'nonce': nonce,
        })

    def create_tournament_transaction(self, match_list):
        nonce = self.web3.eth.get_transaction_count(self.eth_address)
        logger.info(f"nonce = {nonce}")
        gas_estimate = self.contract.functions.addTournament(*match_list).estimate_gas({'from': self.eth_address})
        logger.info(f"gas_estimate = {gas_estimate}")
        return self.contract.functions.addTournament(*match_list).build_transaction({
            'chainId': self.web3.eth.chain_id,
            'gas': gas_estimate,
            'maxPriorityFeePerGas': Web3.to_wei(self.maxPriorityFeePerGas, 'gwei'),
            'nonce': nonce,
        })

    def sign_and_send_transaction(self, transaction):
        from .utils import TransactionToLongError, FailedTransactionError
        try:
            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            self.last_tx = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(self.last_tx, 3)
            if txn_receipt.status == 0:
                raise FailedTransactionError
            self.maxPriorityFeePerGas = 1
            self.maxFeePerGas = 0
            return self.last_tx
        except TimeExhausted:
            raise TransactionToLongError(self.last_tx)

    def gas_error(self, e, add_to_db_func, data):
        logger.debug(e)
        logger.info("gas error")
        add_to_db_func(data)
        error_message = "Problem with blockchain, your data is safely stored in the database and will be stored in the blockchain ASAP."
        return Response({"error": error_message}, status=status.HTTP_200_OK)

    def reverted_error(self, e, delete_from_db_func, identifier):
        logger.info(f"transaction revert: {e}")
        delete_from_db_func(identifier)
        error_message = f"{identifier} already exists"
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def handle_transaction_error(self, e, add_to_db_func, delete_from_db_func, data, identifier):
        from .utils import TransactionToLongError, FailedTransactionError
        from .StoreInDB import add_tx_to_db
        if isinstance(e, TransactionToLongError):
            self.maxPriorityFeePerGas += 1
            return self.add_match(data, 0)
            #logger.error(f"The transaction is pending and will soon be displayed on the blockchain tx_hash:{e.txn_hash.hex()}")
            #add_tx_to_db(data['match_id'], data['tournament_id'], e.txn_hash.hex())
            #return Response({"error": "transaction pending will be soon display on blockchain"}, status=status.HTTP_200_OK)
        elif "gas" in str(e).lower() or isinstance(e, FailedTransactionError):
            return self.gas_error(e, add_to_db_func, data)
        elif "reverted" in str(e).lower():
            return self.reverted_error(e, delete_from_db_func, identifier)
        else:
            logger.info(e)
            add_to_db_func(data)
            return Response({"error": str(e).lower()}, status=status.HTTP_400_BAD_REQUEST)

    def add_match(self, match_data, from_db):
        from .StoreInDB import add_match_to_db, delete_match_from_db, add_tx_to_db
        try:
            logger.info(f"nb_passage = {self.nb_passage}")
            self.nb_passage += 1
            match_list = list(match_data.values())
            if self.last_tx:
                try:
                    tx_receipt = self.web3.eth.get_transaction_receipt(self.last_tx.hex())
                    if tx_receipt is not None and tx_receipt.status == 1:
                        add_tx_to_db(match_data['match_id'], match_data['tournament_id'], self.last_tx.hex())
                        self.last_tx = None
                        return Response(data=match_data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    pass
            transaction = self.create_match_transaction(match_list)
            txn_hash = self.sign_and_send_transaction(transaction)
            logger.info(f' txn_hash = {txn_hash.hex()}')
            add_tx_to_db(match_data['match_id'], match_data['tournament_id'], txn_hash.hex())
            self.last_tx = None
            self.nb_passage = 1
            if from_db:
                return True
            return Response(data=match_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return self.handle_transaction_error(e, add_match_to_db, delete_match_from_db, match_data, match_data['match_id'])

    def add_tournament(self, tournament_data, from_db):
        from .StoreInDB import add_tournament_to_db, delete_tournament_from_db, add_tx_to_db
        try:
            tournament_list = list(tournament_data.values())
            transaction = self.create_tournament_transaction(tournament_list)
            txn_hash = self.sign_and_send_transaction(transaction)
            logger.info(f' txn_hash = {txn_hash.hex()}')
            add_tx_to_db(0, tournament_data['tournament_id'], txn_hash.hex())
            if from_db:
                return True
            return Response(data=tournament_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return self.handle_transaction_error(e, add_tournament_to_db, delete_tournament_from_db, tournament_data,
                                                 tournament_data['tournament_id'])
