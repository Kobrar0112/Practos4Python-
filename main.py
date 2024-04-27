from web3 import Web3
from web3.middleware import geth_poa_middleware
from contact_info import abi, contract_address
import re

# Инициализация подключения к Ethereum ноде
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)

print(w3.eth.get_balance("0xd431A61361A275f6eE8814BFaae34CC0B34B9EE7"))
print(w3.eth.get_balance("0x86777B25e99D7d59Deb94860Ac57Dd1129AFC7d6"))
print(w3.eth.get_balance("0xDa005b7B842e72FCc608c9D21E287E6CD4AfDAF5"))
print(w3.eth.get_balance("0xD61CA8A3F68e5f2ACcDdf6427b40247EF39cB646"))
print(w3.eth.get_balance("0x42Ebe42605a037450675F38f554D7dd470053E32"))


def is_strong_password(password):
    if len(password) < 12:
        return False
    if re.search(r"password123|qwerty123", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%]", password):
        return False
    return True

def auth():
    public_key = input("Введите публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(public_key, password)
        print("Вы авторизованы")
        return public_key
    except Exception as e:
        print("Ошибка авторизации:", e)
        return None

def registration():
    password = input("Введите сложный пароль: ")
    if not is_strong_password(password):
        print("Пароль не соответствует требованиям. Попробуйте еще раз.")
        return None
    try:
        address = w3.geth.personal.new_account(password)
        print(f"Адрес нового аккаунта: {address}")
        return address
    except Exception as e:
        print("Ошибка при создании аккаунта:", e)
        return None

def create_estate(public_key):
    size = int(input("Введите размер недвижимости (кв. м): "))
    photo = input("Введите URL или хэш изображения недвижимости: ")
    rooms = int(input("Введите количество комнат: "))
    estate_type = input("Введите тип недвижимости (Дом, Квартира, Мансарда): ")
    estate_type = {"Дом": 0, "Квартира": 1, "Мансарда": 2}.get(estate_type, 0)
    
    try:
        tx_hash = contract.functions.createEstate(size, photo, rooms, estate_type).transact({'from': public_key})
        print("Недвижимость создана успешно. Хеш транзакции:", tx_hash.hex())
    except Exception as e:
        print("Ошибка при создании недвижимости:", e)

def create_advertisement(public_key):
    estate_id = int(input("Введите ID недвижимости: "))
    price = int(input("Введите цену недвижимости (в wei): "))
    
    try:
        tx_hash = contract.functions.createAd(estate_id, price).transact({'from': public_key})
        print("Объявление создано успешно. Хеш транзакции:", tx_hash.hex())
    except Exception as e:
        print("Ошибка при создании объявления:", e)

def change_estate_status(public_key):
    estate_id = int(input("Введите ID недвижимости: "))
    new_status = int(input("Введите новый статус (0 - неактивный, 1 - активный): "))
    
    try:
        tx_hash = contract.functions.changeEstateStatus(estate_id, new_status).transact({'from': public_key})
        print("Статус недвижимости изменен. Хеш транзакции:", tx_hash.hex())
    except Exception as e:
        print("Ошибка при изменении статуса недвижимости:", e)

def change_ad_status(public_key):
    ad_id = int(input("Введите ID объявления: "))
    new_status = int(input("Введите новый статус (0 - закрыто, 1 - открыто): "))
    
    try:
        tx_hash = contract.functions.changeAdStatus(ad_id, new_status).transact({'from': public_key})
        print("Статус объявления изменен. Хеш транзакции:", tx_hash.hex())
    except Exception as e:
        print("Ошибка при изменении статуса объявления:", e)

def buy_estate(public_key):
    ad_id = int(input("Введите ID объявления, по которому вы хотите купить недвижимость: "))
    price = int(input("Введите цену покупки (в wei): "))
    
    try:
        tx_hash = contract.functions.buyEstate(ad_id).transact({'from': public_key, 'value': price})
        print("Недвижимость успешно куплена. Хеш транзакции:", tx_hash.hex())
    except Exception as e:
        print("Ошибка при покупке недвижимости:", e)

def withdraw_funds(public_key):
    amount = int(input("Введите сумму для вывода (в wei): "))
    
    try:
        tx_hash = contract.functions.withdrawFunds(amount).transact({'from': public_key})
        print("Средства успешно выведены. Хеш транзакции:", tx_hash.hex())
    except Exception as e:
        print("Ошибка при выводе средств:", e)

def get_estates():
    try:
        estates = contract.functions.getEstates().call()
        print("Доступные недвижимости:")
        for estate in estates:
            print(estate)
    except Exception as e:
        print("Ошибка при получении информации о недвижимости:", e)

def get_ads():
    try:
        ads = contract.functions.getAds().call()
        print("Доступные объявления:")
        for ad in ads:
            print(ad)
    except Exception as e:
        print("Ошибка при получении информации о объявлениях:", e)

def get_balance(public_key):
    try:
        balance = contract.functions.getBalance().call({'from': public_key})
        print(f"Ваш баланс на смарт-контракте: {balance}")
    except Exception as e:
        print("Ошибка при получении баланса:", e)

def main():
    account = None
    is_auth = False
    
    while True:
        if not is_auth:
            choice = input("Выберите:\n1. Авторизация\n2. Регистрация\n")
            if choice == "1":
                account = auth()
                if account:
                    is_auth = True
            elif choice == "2":
                account = registration()
                if account:
                    is_auth = True
        else:
            choice = input(
                "Выберите:\n1. Создать недвижимость\n2. Создать объявление\n3. Изменить статус недвижимости\n4. Изменить статус объявления\n5. Купить недвижимость\n6. Вывести средства\n7. Получить информацию о недвижимости\n8. Получить информацию о объявлениях\n9. Получить баланс\n10. Выйти\n"
            )
            if choice == "1":
                create_estate(account)
            elif choice == "2":
                create_advertisement(account)
            elif choice == "3":
                change_estate_status(account)
            elif choice == "4":
                change_ad_status(account)
            elif choice == "5":
                buy_estate(account)
            elif choice == "6":
                withdraw_funds(account)
            elif choice == "7":
                get_estates()
            elif choice == "8":
                get_ads()
            elif choice == "9":
                get_balance(account)
            elif choice == "10":
                is_auth = False
                print("Вы вышли из учетной записи.")
            else:
                print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()