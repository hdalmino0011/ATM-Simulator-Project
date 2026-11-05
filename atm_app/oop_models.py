from datetime import datetime


class ATMTransactionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidAmountError(ATMTransactionError):
    pass


class InsufficientFundsError(ATMTransactionError):
    pass


class WithdrawalLimitError(ATMTransactionError):
    pass


class MaintainingBalanceError(ATMTransactionError):
    pass


def mask_account_number(acc_num):
    s = str(acc_num or "").strip()
    if len(s) <= 3:
        return s
    return ("*" * (len(s) - 3)) + s[-3:]


class Transaction:
    def __init__(self, transaction_id, tx_type, amount, fee, balance_after, timestamp=None):
        self._transaction_id = str(transaction_id)
        self._tx_type = str(tx_type)
        self._amount = round(float(amount), 2)
        self._fee = round(float(fee), 2)
        self._balance_after = round(float(balance_after), 2)
        self._timestamp = timestamp or datetime.now().strftime("%b %d, %Y %I:%M %p")

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def tx_type(self):
        return self._tx_type

    @property
    def amount(self):
        return self._amount

    @property
    def fee(self):
        return self._fee

    @property
    def balance_after(self):
        return self._balance_after

    @property
    def timestamp(self):
        return self._timestamp

    def to_dict(self):
        return {
            "transaction_id": self._transaction_id,
            "tx_type": self._tx_type,
            "amount": self._amount,
            "fee": self._fee,
            "balance_after": self._balance_after,
            "timestamp": self._timestamp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            transaction_id=data["transaction_id"],
            tx_type=data["tx_type"],
            amount=data["amount"],
            fee=data.get("fee", 0.0),
            balance_after=data["balance_after"],
            timestamp=data.get("timestamp"),
        )


class Account:
    MAINTAINING_BALANCE = 0.00
    WITHDRAWAL_LIMIT = 25000.00
    WITHDRAWAL_FEE = 0.00

    def __init__(self, account_number, holder_name, pin, starting_balance, account_type="Standard Account", transactions=None):
        self._account_number = str(account_number).strip()
        self._holder_name = str(holder_name).strip()
        self._pin = str(pin).strip()
        self._balance = round(float(starting_balance), 2)
        self._account_type = account_type
        self._transactions = list(transactions) if transactions else []

    @property
    def account_number(self):
        return self._account_number

    @property
    def masked_account_number(self):
        return mask_account_number(self._account_number)

    @property
    def holder_name(self):
        return self._holder_name

    @property
    def balance(self):
        return self._balance

    @property
    def account_type(self):
        return self._account_type

    @property
    def transactions(self):
        return list(self._transactions)

    def verify_pin(self, input_pin):
        clean_in = str(input_pin).strip()
        return clean_in.isdigit() and 4 <= len(clean_in) <= 6

    @staticmethod
    def parse_positive_amount(raw_value, operation_name="Transaction"):
        if raw_value is None or str(raw_value).strip() == "":
            raise InvalidAmountError(f"{operation_name} rejected: Please enter an amount.")
        try:
            clean_str = str(raw_value).replace(",", "").strip()
            amount = float(clean_str)
        except (ValueError, TypeError):
            raise InvalidAmountError(f"{operation_name} rejected: '{raw_value}' is not a valid numeric amount.")
        if amount <= 0:
            raise InvalidAmountError(f"{operation_name} rejected: Amount must be greater than PHP 0.00.")
        return round(amount, 2)

    def _record_transaction(self, tx_type, amount, fee=0.0):
        tx_num = len(self._transactions) + 1001
        tx_id = f"TXN-{self._account_number[-3:]}-{tx_num}"
        tx = Transaction(tx_id, tx_type, amount, fee, self._balance)
        self._transactions.insert(0, tx)
        return tx

    def deposit(self, raw_amount):
        amount = self.parse_positive_amount(raw_amount, "Deposit")
        self._balance = round(self._balance + amount, 2)
        return self._record_transaction("Deposit", amount, 0.0)

    def withdraw(self, raw_amount):
        amount = self.parse_positive_amount(raw_amount, "Withdrawal")
        if amount > self._balance:
            raise InsufficientFundsError("Withdrawal rejected: Insufficient funds.")
        self._balance = round(self._balance - amount, 2)
        return self._record_transaction("Withdrawal", amount, 0.0)

    def get_max_withdrawable(self):
        return self._balance

    def inquire_balance(self):
        return {
            "account_number": self.masked_account_number,
            "account_type": self._account_type,
            "balance": self._balance,
            "max_withdrawable": self.get_max_withdrawable(),
            "maintaining_balance": self.MAINTAINING_BALANCE,
            "withdrawal_fee": self.WITHDRAWAL_FEE,
        }

    def to_dict(self):
        return {
            "class_name": self.__class__.__name__,
            "account_number": self._account_number,
            "masked_account_number": self.masked_account_number,
            "holder_name": self._holder_name,
            "pin": self._pin,
            "balance": self._balance,
            "account_type": self._account_type,
            "transactions": [t.to_dict() for t in self._transactions],
        }


class SavingsAccount(Account):
    MAINTAINING_BALANCE = 500.00
    WITHDRAWAL_LIMIT = 20000.00
    WITHDRAWAL_FEE = 0.00

    def __init__(self, account_number, holder_name, pin="123456", starting_balance=15000.00, transactions=None):
        super().__init__(account_number, holder_name, pin, starting_balance, "Savings Account", transactions)

    def get_max_withdrawable(self):
        avail = max(0.0, round(self._balance - self.MAINTAINING_BALANCE, 2))
        return min(avail, self.WITHDRAWAL_LIMIT)

    def withdraw(self, raw_amount):
        amount = self.parse_positive_amount(raw_amount, "Withdrawal")
        if amount > self.WITHDRAWAL_LIMIT:
            raise WithdrawalLimitError(
                f"Withdrawal rejected: Exceeds Savings limit of PHP {self.WITHDRAWAL_LIMIT:,.2f}."
            )
        if amount > self._balance:
            raise InsufficientFundsError("Withdrawal rejected: Insufficient funds.")
        projected = round(self._balance - amount, 2)
        if projected < self.MAINTAINING_BALANCE:
            raise MaintainingBalanceError(
                f"Withdrawal rejected: PHP {self.MAINTAINING_BALANCE:,.2f} maintaining balance required."
            )
        self._balance = projected
        return self._record_transaction("Withdrawal", amount, 0.0)


class CheckingAccount(Account):
    MAINTAINING_BALANCE = 0.00
    WITHDRAWAL_LIMIT = 50000.00
    WITHDRAWAL_FEE = 15.00

    def __init__(self, account_number, holder_name, pin="123456", starting_balance=25000.00, transactions=None):
        super().__init__(account_number, holder_name, pin, starting_balance, "Checking Account", transactions)

    def get_max_withdrawable(self):
        if self._balance <= self.WITHDRAWAL_FEE:
            return 0.0
        return min(round(self._balance - self.WITHDRAWAL_FEE, 2), self.WITHDRAWAL_LIMIT)

    def withdraw(self, raw_amount):
        amount = self.parse_positive_amount(raw_amount, "Withdrawal")
        if amount > self.WITHDRAWAL_LIMIT:
            raise WithdrawalLimitError(
                f"Withdrawal rejected: Exceeds Checking limit of PHP {self.WITHDRAWAL_LIMIT:,.2f}."
            )
        total_deduction = round(amount + self.WITHDRAWAL_FEE, 2)
        if total_deduction > self._balance:
            raise InsufficientFundsError(
                f"Withdrawal rejected: Insufficient funds to cover withdrawal plus PHP {self.WITHDRAWAL_FEE:,.2f} fee."
            )
        self._balance = round(self._balance - total_deduction, 2)
        return self._record_transaction("Withdrawal", amount, self.WITHDRAWAL_FEE)


class ATMService:
    def __init__(self, accounts=None, active_type="savings", logged_in_card="100000248"):
        if accounts:
            self.accounts = accounts
        else:
            self.accounts = self._create_predefined_accounts()
        self.active_type = active_type if active_type in self.accounts else "savings"
        self.logged_in_card = logged_in_card
        self.current_account = self.accounts[self.active_type]

    @staticmethod
    def _create_predefined_accounts():
        sa = SavingsAccount("100000248", "Hanz Dee", "123456", 15000.00)
        sa._record_transaction("Opening Balance", 15000.00, 0.0)

        ca = CheckingAccount("200000519", "Hanz Dee", "123456", 25000.00)
        ca._record_transaction("Opening Balance", 25000.00, 0.0)

        return {
            "savings": sa,
            "checking": ca,
        }

    def login(self, raw_acc, raw_pin):
        acc_in = str(raw_acc or "").strip()
        pin_in = str(raw_pin or "").strip()
        if not acc_in or not pin_in:
            raise ATMTransactionError("Please enter both your Account Number and PIN Code.")

        normalized = acc_in.replace(" ", "").replace("-", "")
        if not normalized.isdigit() or len(normalized) < 9:
            raise ATMTransactionError("Account Number must be at least 9 digits.")

        sa = self.accounts["savings"]
        if not sa.verify_pin(pin_in):
            raise ATMTransactionError("Invalid PIN Code. Please enter a 4 to 6 digit PIN.")

        self.logged_in_card = normalized
        self.accounts["savings"]._account_number = normalized
        self.accounts["checking"]._account_number = normalized
        self.current_account = self.accounts["savings"]
        return self.current_account

    def select_account_type(self, kind):
        if kind == "checking":
            self.active_type = "checking"
        else:
            self.active_type = "savings"
        self.current_account = self.accounts[self.active_type]
        return self.current_account

    def perform_deposit(self, raw_amount):
        return self.current_account.deposit(raw_amount)

    def perform_withdrawal(self, raw_amount):
        return self.current_account.withdraw(raw_amount)

    def to_session_data(self):
        return {
            "active_type": self.active_type,
            "logged_in_card": self.logged_in_card,
            "accounts": {k: acc.to_dict() for k, acc in self.accounts.items()},
        }

    @classmethod
    def from_session_data(cls, data):
        if not data or "accounts" not in data:
            return cls()
        rebuilt = {}
        for k, v in data["accounts"].items():
            txs = [Transaction.from_dict(t) for t in v.get("transactions", [])]
            if v.get("class_name") == "CheckingAccount":
                rebuilt[k] = CheckingAccount(v["account_number"], v["holder_name"], v.get("pin", "123456"), v["balance"], txs)
            else:
                rebuilt[k] = SavingsAccount(v["account_number"], v["holder_name"], v.get("pin", "123456"), v["balance"], txs)
        return cls(
            accounts=rebuilt,
            active_type=data.get("active_type", "savings"),
            logged_in_card=data.get("logged_in_card", "100000248"),
        )
