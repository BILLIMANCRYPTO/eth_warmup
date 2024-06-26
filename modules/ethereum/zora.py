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
    
zora_contract_abi = abi_data['zora']
zora_contract_address = "0x1a0ad011913A150f69f6A19DF447A0CfD9551054"

# Генерация кошельков из приватных ключей
wallets = [Account.from_key(private_key).address for private_key in private_keys]

# Blur Deposit
def zora_donate(wallet_address, private_key, web3, i, GAS_PRICE):
    zora_contract = web3.eth.contract(address=web3.to_checksum_address(zora_contract_address), abi=zora_contract_abi)
    nonce = web3.eth.get_transaction_count(wallet_address)
    balance = web3.eth.get_balance(wallet_address)
    if balance <= 0:
        logging.error(f"Insufficient balance in wallet {wallet_address}")
        return None

    current_gas_price = web3.eth.gas_price
    gas_price = int(current_gas_price * 1.05)
    payable_amount = web3.to_wei(random.uniform(MIN_SEND, MAX_SEND), 'ether') # меняй сумму
    gas_limit = web3.eth.estimate_gas({
        'from': wallet_address,
        'to': zora_contract_address,
        'value': payable_amount,
        'data': zora_contract.encodeABI(fn_name='donateETH'),
    })

    print(f'Start with wallet [{i}/{len(wallets)}]: {wallet_address}')
    print(Fore.CYAN + f'Zora donate {web3.from_wei(payable_amount, "ether")} eth')
    try:
        tx_params = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_limit,
            'to': zora_contract_address,
            'value': payable_amount,
            'data': zora_contract.encodeABI(fn_name='donateETH'),
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