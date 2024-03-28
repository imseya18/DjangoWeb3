import json
from django.conf import settings
from web3 import Web3
from web3.contract import Contract

infural_url = f"https://sepolia.infura.io/v3/{settings.INFURA_API_KEY}"
web3 = Web3(Web3.HTTPProvider(infural_url))
address = '0xb58383e5Ba1213B982e946d1555a96238E670f99'
abi = json.loads('[{"inputs": [{"internalType": "address","name": "owner","type": "address"}],"name": "OwnableInvalidOwner","type": "error"},{"inputs": [{"internalType": "address","name": "account","type": "address"}],"name": "OwnableUnauthorizedAccount","type": "error"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "previousOwner","type": "address"},{"indexed": true,"internalType": "address","name": "newOwner","type": "address"}],"name": "OwnershipTransferred","type": "event"},{"inputs": [{"internalType": "uint256","name": "_r_matchId","type": "uint256"},{"internalType": "uint256","name": "_tournamentId","type": "uint256"},{"internalType": "uint8","name": "_player1Score","type": "uint8"},{"internalType": "uint8","name": "_player2Score","type": "uint8"},{"internalType": "string","name": "_player1Id","type": "string"},{"internalType": "string","name": "_player2Id","type": "string"},{"internalType": "string","name": "_winner","type": "string"}],"name": "addMatch","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256[]","name": "_r_matchId","type": "uint256[]"},{"internalType": "uint256","name": "_tournamentId","type": "uint256"},{"internalType": "uint8[]","name": "_player1Score","type": "uint8[]"},{"internalType": "uint8[]","name": "_player2Score","type": "uint8[]"},{"internalType": "string[]","name": "_player1Id","type": "string[]"},{"internalType": "string[]","name": "_player2Id","type": "string[]"},{"internalType": "string[]","name": "_winner","type": "string[]"}],"name": "addTournament","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "renounceOwnership","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "newOwner","type": "address"}],"name": "transferOwnership","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "_r_matchId","type": "uint256"}],"name": "getMatchById","outputs": [{"components": [{"internalType": "uint256","name": "matchId","type": "uint256"},{"internalType": "uint8","name": "player1Score","type": "uint8"},{"internalType": "uint8","name": "player2Score","type": "uint8"},{"internalType": "string","name": "player1Id","type": "string"},{"internalType": "string","name": "player2Id","type": "string"},{"internalType": "string","name": "winner","type": "string"}],"internalType": "struct storeScore.Match","name": "","type": "tuple"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_playerName","type": "string"}],"name": "getPlayerMatchs","outputs": [{"components": [{"internalType": "uint256","name": "matchId","type": "uint256"},{"internalType": "uint8","name": "player1Score","type": "uint8"},{"internalType": "uint8","name": "player2Score","type": "uint8"},{"internalType": "string","name": "player1Id","type": "string"},{"internalType": "string","name": "player2Id","type": "string"},{"internalType": "string","name": "winner","type": "string"}],"internalType": "struct storeScore.Match[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "_tournamentId","type": "uint256"}],"name": "getTournament","outputs": [{"components": [{"internalType": "uint256","name": "matchId","type": "uint256"},{"internalType": "uint8","name": "player1Score","type": "uint8"},{"internalType": "uint8","name": "player2Score","type": "uint8"},{"internalType": "string","name": "player1Id","type": "string"},{"internalType": "string","name": "player2Id","type": "string"},{"internalType": "string","name": "winner","type": "string"}],"internalType": "struct storeScore.Match[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "owner","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"}]')

contract = web3.eth.contract(address=address, abi=abi)
def connnecttobc():
    print(web3.is_connected())
    print(web3.eth.block_number)
    balance = web3.eth.get_balance(settings.ETH_ADDRESS)
    print(web3.from_wei(balance, "ether"))
    try:
        match = contract.functions.getMatchById(2).call()
        print(match)
    except Exception as e:
        print(e)
    balance = web3.eth.get_balance(settings.ETH_ADDRESS)
    print(web3.from_wei(balance, "ether"))