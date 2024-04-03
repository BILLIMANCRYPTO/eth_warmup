import json
import random
import time
import logging
from web3 import Web3
from colorama import init, Fore
from settings import MIN_DELAY, MAX_DELAY, MIN_SEND, MAX_SEND, GAS_PRICE
from eth_account import Account
from modules.keys import private_keys

# Чтение ABI контрактов из файла abi.json
with open('abi.json', 'r') as f:
    abi_data = json.load(f)
    
ens1_contract_abi = abi_data['ens_renewal']
ens1_contract_address = "0x253553366Da8546fC250F225fe3d25d0C782303b"

# Генерация кошельков из приватных ключей
wallets = [Account.from_key(private_key).address for private_key in private_keys]

# ENS WITHDRAW
def ens_withdraw(wallet_address, private_key, web3, i, GAS_PRICE):
    ens1_contract = web3.eth.contract(address=web3.to_checksum_address(ens1_contract_address), abi=ens1_contract_abi)
    nonce = web3.eth.get_transaction_count(wallet_address)
    balance = web3.eth.get_balance(wallet_address)
    if balance <= 0:
        logging.error(f"Insufficient balance in wallet {wallet_address}")
        return None

    current_gas_price = web3.eth.gas_price
    gas_price = int(current_gas_price * 1.05)
    payable_amount = web3.to_wei(random.uniform(0, 0), 'ether') # меняй сумму
    gas_limit = web3.eth.estimate_gas({
        'from': wallet_address,
        'to': ens1_contract_address,
        'value': payable_amount,
        'data': ens1_contract.encodeABI(fn_name='withdraw'),
    })

    print(f'Start with wallet [{i}/{len(wallets)}]: {wallet_address}')
    print(Fore.CYAN + f'Cheap TX')
    try:
        tx_params = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_limit,
            'to': ens1_contract_address,
            'value': payable_amount,
            'data': ens1_contract.encodeABI(fn_name='withdraw'),
            'chainId': 1,  # ID сети ETH
        }

        signed_tx = web3.eth.account.sign_transaction(tx_params, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        print(f'Transaction sent: {tx_hash.hex()}')

        # Ожидание подтверждения транзакции
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            print(Fore.GREEN + f'Transaction {tx_hash.hex()} successfully confirmed')
        else:
            print(Fore.RED + f'Transaction {tx_hash.hex()} failed')
        
        return tx_hash.hex()
    
    except Exception as e:
        logging.error(f'Error occurred for wallet {wallet_address}: {e}')
        logging.exception("Exception occurred", exc_info=True)
        return None