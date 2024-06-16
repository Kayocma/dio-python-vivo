import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class User:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class Client(User):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf

class Account:
    def __init__(self, number, user):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._user = user
        self._history = History()

    @classmethod
    def new_account(cls, number, user):
        return cls(number, user)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def number(self):
        return self._number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def user(self):
        return self._user
    
    @property
    def history(self):
        return self._history
    
    def withdraw(self, value):
        balance = self.balance
        exceeded_balance = value > balance

        if exceeded_balance:
            print("\n@@@ Operation failed! You do not have enough balance. @@@")
            
        elif value > 0:
            self._balance -= value
            self._history.add_transaction("Withdraw", value)
            print("\n=== Withdraw successfully! ===")

        else:
            print("\n@@@ Operation failed! The informed value is invalid. @@@")

    def deposit(self, value):
        if value > 0:
            self._balance += value
            self._history.add_transaction("Deposit", value)
            print("\n=== Deposit successfully! ===")
        else:
            print("\n@@@ Operation failed! The informed value is invalid. @@@")

class CurrentAccount(Account):
    def __init__(self, number, user, limit=500, limit_withdraws=3):
        super().__init__(number, user)
        self.limit = limit
        self.limit_withdraws = limit_withdraws
        self.withdraws = 0

    def withdraw(self, value):
        number_withdraws = len([transaction for transaction in self.history.transactions if transaction["type"] == "Withdraw"])

        exceeded_limit = value > self.limit
        exceeded_withdraws = number_withdraws >= self.limit_withdraws

        if exceeded_limit:
            print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")

        elif exceeded_withdraws:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

        else:
            super().withdraw(value)
            self.withdraws += 1

    def __str__(self):
        return f"""\
            Agency:\t{self.agency}
            C/C:\t{self.number}
            Holder:\t{self.user.name}
        """
    
class History:
    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction_type, transaction_value):
        self._transactions.append(
            {
                "type": transaction_type,
                "value": transaction_value, 
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transaction(ABC):
    @property
    @abstractproperty
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass

class Withdraw(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        sucess_transaction = account.withdraw(self.value)

        if sucess_transaction:
            account.history.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        sucess_transaction = account.deposit(self.value)

        if sucess_transaction:
            account.history.add_transaction(self)

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdraw
    [3]\tExtract
    [4]\tNew user
    [5]\tNew account
    [6]\tList account
    [0]\tExit
    => """
    return input(textwrap.dedent(menu))


def deposit(users):
    cpf = input("\nInform the CPF: ")
    user = user_filter(cpf, users)

    if not user:
        print("\n@@@ User not found! @@@")
        return
    
    value = float(input("\nInform the deposit amount: "))
    transaction = Deposit(value)

    account = recover_account(user)
    if not account:
        return
    
    user.transaction(account, transaction)

def withdraw(users):
    cpf = input("\nInform the CPF: ")
    user = user_filter(cpf, users)

    if not user:
        print("\n@@@ User not found! @@@")
        return
    
    value = float(input("\nInform the withdrawal amount: "))
    transaction = Withdraw(value)

    account = recover_account(user)
    if not account:
        return
    
    user.transaction(account, transaction)

def extract(users):
    cpf = input("\nInform the CPF: ")
    user = user_filter(cpf, users)

    if not user:
        print("\n@@@ User not found! @@@")
        return
    
    account = recover_account(user)
    if not account:
        return
    
    print("\n=========== Extract ===========")
    transactions = account.history.transactions

    extract = ""
    if not transactions:
        extract = "No transactions found."
    else:
        for transaction in transactions:
            extract += f"\n{transaction['type']}:\n\tR${transaction['value']:.2f} in {transaction['date']}"

    print(extract)
    print(f"\nBalance:\n\tR$ {account.balance:.2f}")
    print("===============================")

def create_user(users):
    cpf = input("\nInform the CPF: ")
    user = user_filter(cpf, users)

    if user:
        print("\n@@@ User already registered! @@@")
        return
    
    name = input("\nInform the name: ")
    birth_date = input("\nInform the birth date (dd-mm-aaaa): ")
    address = input("\nInform the address: ")

    user = Client(name=name, birth_date=birth_date, cpf=cpf, address=address)

    users.append(user)

    print("\n=== User created successfully! ===")


def create_account(account_number, users, accounts):
    cpf = input("\nInform the CPF: ")
    user = user_filter(cpf, users)

    if not user:
        print("\n@@@ User not found! @@@")
        return
    
    account = CurrentAccount.new_account(user=user, number=account_number)
    accounts.append(account)
    user.accounts.append(account)

    print("\n=== Account created successfully! ===")

def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def user_filter(cpf, users):
    filtered_users = [user for user in users if user.cpf == cpf]
    return filtered_users[0] if filtered_users else None

def recover_account(user):
    if not user.accounts:
        print("\n@@@ User has no accounts! @@@")
        return 
    
    return user.accounts[0]

def main():
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "1":
            deposit(users)

        elif option == "2":
            withdraw(users)

        elif option == "3":
            extract(users)

        elif option == "4":
            create_user(users)

        elif option == "5":
            account_number = len(accounts) + 1
            create_account(account_number, users, accounts)

        elif option == "6":
            list_accounts(accounts)

        elif option == "0":
            break

        else:
            print("\n@@@ Invalid option! @@@")

main()