class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError
        self.__balance += amount

    def withdraw(self, amount):
        if self.__balance < amount:
            raise ValueError
        self.__balance -= amount

    def get_balance(self):
        return self.__balance


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, interest_rate=0.05):
        super().__init__(owner, balance)
        self._interest_rate = interest_rate

    def apply_interest(self):
        self.deposit(self.get_balance() * self._interest_rate)

class CheckingAccount(BankAccount):
    def _set_balance(self, new_balance):
        """Updates balance of BankAccount in child class directly."""
        self._BankAccount__balance = new_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError
        self._set_balance(self.get_balance() - amount)


def test_savings_account():
    savings = SavingsAccount("Ivan Ivanov", 0, 0.1)
    savings.deposit(500)
    savings.withdraw(100)
    savings.apply_interest()
    # print(savings.get_balance())
    assert savings.get_balance() > 0

def test_checking_account():
    expected_balance = -900
    check = CheckingAccount("Pavel Perov", 100)
    check.withdraw(1000)
    assert check.get_balance() == expected_balance