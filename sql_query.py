import sqlite3


class SQL_atm:

    @staticmethod
    def create_table():

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);''')
            print('Создание таблицы Users_data')

    """Создание нового пользователя"""

    @staticmethod
    def insert_users(data_users):

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute('''INSERT INTO Users_data (Number_card, Pin_code, Balance) VALUES (?, ?, ?)''', data_users)
            print('Создание нового пользователя')

    """Ввод и проверка карты"""

    @staticmethod
    def input_card(number_card):

        try:
            with sqlite3.connect('atm.db') as db:
                cur = db.cursor()
                cur.execute(f'''SELECT Number_card FROM Users_data WHERE Number_card = {number_card}''')
                result_card = cur.fetchone()
                if result_card == None:
                    print('Введен неизвестный номер карты')
                    return False
                else:
                    print(f'Введен номер карты: {number_card}')
                    return True
        except:
            print('Введен неизвестный номер карты')

    """Ввод и проверка пин-код"""

    @staticmethod
    def input_cod(number_card):

        pin_code = input('Введите пожалуйста пин-код карты: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Pin_code FROM Users_data WHERE Number_card = {number_card}''')
            pin_result = cur.fetchone()
            input_pin = pin_result[0]
            try:
                if input_pin == int(pin_code):
                    print('Введен верный пин-код')
                    return True
                else:
                    print('Введен некорректный пин-код')
                    return False
            except:
                print('Введен некорректный пин-код')
                return False

    """Вывод на экран баланса карты"""

    @staticmethod
    def info_balance(number_card):

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Balance FROM Users_data WHERE Number_card = {number_card}''')
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            print(f'Баланс вашей карты {balance_card}')

    """Снятие денежных средств с баланса карты"""

    @staticmethod
    def withdraw_money(number_card):

        amount = input('Введите пожалуйста сумму которую желаете снять: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f'''SELECT Balance FROM Users_data WHERE Number_card = {number_card}''')
            balance_info_result = cur.fetchone()
            balance_card = balance_info_result[0]
            try:
                if int(amount) > balance_card:
                    print('На вашей карте недостаточно денежных средств')
                    return False
                else:
                    cur.execute(
                        f'''UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card}''')
                    db.commit()
                    SQL_atm.info_balance(number_card)
                    return True
            except:
                print('Попытка выполнить некорректное действие')
                return False

    """Внесение денежных средств с баланса карты"""

    @staticmethod
    def depositing_money(number_card):

        amount = input('Введите пожалуйста сумму которую желаете внести: ')
        with sqlite3.connect('atm.db') as db:
            try:
                cur = db.cursor()
                cur.execute(f'''UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card}''')
                db.commit()
                SQL_atm.info_balance(number_card)
                return True
            except:
                print('Попытка выполнить некорректное действие')
                return False

    """Перевод денежных средств между пользователями"""

    @staticmethod
    def transfer_money():
        amount = input('Введите пожалуйста сумму которую желаете перевести: ')
        while not amount.isdigit():
            amount = input('Введите пожалуйста сумму которую желаете перевести: ')
        number_card = input('Введите номер карты на которую необходимо выполнить перевод: ')
        while not number_card.isdigit():
            number_card = input('Введите пожалуйста сумму которую желаете перевести: ')
        with sqlite3.connect('atm.db') as db:
            try:
                cur = db.cursor()
                cur.execute(f'''UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card}''')
                db.commit()
                SQL_atm.info_balance(number_card)
                return True
            except:
                print('Попытка выполнить некорректное действие')
                return False

    """Выбор операции"""

    @staticmethod
    def input_operation(number_card):

        while True:
            operation = input('Введите пожалуйста операцию которую хотите совершить\n'
                              '1. Узнать баланс\n'
                              '2. Снять денежные средства\n'
                              '3. Внести денежные средства\n'
                              '4. Завершить работу\n'
                              '5. Перевести денежные средства\n')

            if operation == '1':
                SQL_atm.info_balance(number_card)
            elif operation == '2':
                SQL_atm.withdraw_money(number_card)
            elif operation == '3':
                SQL_atm.depositing_money(number_card)
            elif operation == '5':
                SQL_atm.transfer_money()
            elif operation == '4':
                print('Спасибо за ваш визит, всего доброго!')                
                return False
            else:
                print('Данная операция недоступна, приносим свои извинения')
