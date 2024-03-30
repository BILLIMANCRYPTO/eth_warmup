import random

# Рандомное время ожидания между транзакциями (в секундах)
MIN_DELAY = 30  # Минимальное время ожидания
MAX_DELAY = 100  # Максимальное время ожидания

# Рандомная отправляемая сумма депозита(в ETH)
MIN_SEND = 0.00001  # Минимальная сумма
MAX_SEND = 0.0001  # Максимальная сумма

# Рандомная отправляемая сумма для свапов(в ETH)
MIN_SWAP = 0.0000012 # Минимальная сумма
MAX_SWAP = 0.0000014  # Максимальная сумма

# Рандомная сумма для refuel(в ETH)
MIN_BUNGEE = 0.000002 # минимально возможное значение
MAX_BUNGEE = 0.000003

# Стоимость газа (в Gwei)
GAS_PRICE = 22 # Установленное значение стоимости газа

# Функция для генерации случайной суммы в пределах заданного диапазона
def generate_random_amount():
    return random.uniform(MIN_SEND, MAX_SEND)

# Функция для генерации случайной задержки между транзакциями
def generate_random_delay():
    return random.randint(MIN_DELAY, MAX_DELAY)
