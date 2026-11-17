from datetime import datetime
import random


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
    if len(s) <= 4:
        return s
    return ("*" * (len(s) - 4)) + s[-4:]


def generate_terminal_id():
    return f"EB-ATM-{random.randint(1040, 9899)}"


def generate_auth_code():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.choice(chars) for _ in range(6))


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
        if input_pin is None:
            return False
        entered = str(input_pin)
        return entered.isdigit() and entered == self._pin

    @staticmethod
    def parse_positive_amount(raw_value, operation_name="Transaction"):
        if raw_value is None or str(raw_value).strip() == "":
            raise InvalidAmountError(f"{operation_name} rejected: Please enter an amount.")
        try:
            clean_str = str(raw_value).replace(",", "").strip()
            amount = float(clean_str)
        except (ValueError, TypeError):
            raise InvalidAmountError(f"{operation_name} rejected: '{raw_value}' is not a valid numeric amount.")
        if amount != amount or amount == float("inf") or amount == float("-inf") or amount <= 0:
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

    def withdraw(self, raw_amount, extra_fee=0.0):
        amount = self.parse_positive_amount(raw_amount, "Withdrawal")
        total_fee = round(float(extra_fee), 2)
        total_deduction = round(amount + total_fee, 2)
        if total_deduction > self._balance:
            raise InsufficientFundsError("Withdrawal rejected: Insufficient funds.")
        self._balance = round(self._balance - total_deduction, 2)
        return self._record_transaction("Withdrawal", amount, total_fee)

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

    def __init__(self, account_number, holder_name, pin="", starting_balance=15000.00, transactions=None):
        super().__init__(account_number, holder_name, pin, starting_balance, "Savings Account", transactions)

    def get_max_withdrawable(self):
        avail = max(0.0, round(self._balance - self.MAINTAINING_BALANCE, 2))
        return min(avail, self.WITHDRAWAL_LIMIT)

    def withdraw(self, raw_amount, extra_fee=0.0):
        amount = self.parse_positive_amount(raw_amount, "Withdrawal")
        if amount > self.WITHDRAWAL_LIMIT:
            raise WithdrawalLimitError(
                f"Withdrawal rejected: Exceeds Savings limit of PHP {self.WITHDRAWAL_LIMIT:,.2f}."
            )
        total_fee = round(float(extra_fee), 2)
        total_deduction = round(amount + total_fee, 2)
        if total_deduction > self._balance:
            raise InsufficientFundsError(
                f"Withdrawal rejected: Insufficient funds to cover PHP {amount:,.2f} plus PHP {total_fee:,.2f} fee."
            )
        projected = round(self._balance - total_deduction, 2)
        if projected < self.MAINTAINING_BALANCE:
            raise MaintainingBalanceError(
                f"Withdrawal rejected: PHP {self.MAINTAINING_BALANCE:,.2f} maintaining balance required."
            )
        self._balance = projected
        return self._record_transaction("Withdrawal", amount, total_fee)


class CheckingAccount(Account):
    MAINTAINING_BALANCE = 0.00
    WITHDRAWAL_LIMIT = 50000.00
    WITHDRAWAL_FEE = 15.00

    def __init__(self, account_number, holder_name, pin="", starting_balance=25000.00, transactions=None):
        super().__init__(account_number, holder_name, pin, starting_balance, "Checking Account", transactions)

    def get_max_withdrawable(self):
        if self._balance <= self.WITHDRAWAL_FEE:
            return 0.0
        return min(round(self._balance - self.WITHDRAWAL_FEE, 2), self.WITHDRAWAL_LIMIT)

    def withdraw(self, raw_amount, extra_fee=0.0):
        amount = self.parse_positive_amount(raw_amount, "Withdrawal")
        if amount > self.WITHDRAWAL_LIMIT:
            raise WithdrawalLimitError(
                f"Withdrawal rejected: Exceeds Checking limit of PHP {self.WITHDRAWAL_LIMIT:,.2f}."
            )
        total_fee = round(self.WITHDRAWAL_FEE + float(extra_fee), 2)
        total_deduction = round(amount + total_fee, 2)
        if total_deduction > self._balance:
            raise InsufficientFundsError(
                f"Withdrawal rejected: Insufficient funds to cover withdrawal plus PHP {total_fee:,.2f} total fee."
            )
        self._balance = round(self._balance - total_deduction, 2)
        return self._record_transaction("Withdrawal", amount, total_fee)


class ATMService:
    USD_EXCHANGE_RATE = 58.00
    INTL_USD_FEE = 3.50
    INTL_PCT_FEE = 0.0175
    INTL_FX_FEE = 0.03

    CARD_CATALOG = {
        "local_debit": {
            "id": "local_debit",
            "title": "ExpressBank Everyday Debit",
            "type": "local",
            "bin": "421900",
            "full_pan": "4219 0010 0000 0248",
            "masked_pan": "**** **** **** 0248",
            "network": "Visa",
            "account_number": "100000248",
            "holder_name": "Hanz Dalmino",
            "local_bank_fee": 0.00,
        },
        "local_gold": {
            "id": "local_gold",
            "title": "MetroGold Premier Credit",
            "type": "local",
            "bin": "542810",
            "full_pan": "5428 1020 0000 0519",
            "masked_pan": "**** **** **** 0519",
            "network": "Mastercard",
            "account_number": "200000519",
            "holder_name": "Kristof Badayos",
            "local_bank_fee": 18.00,
        },
        "intl_platinum": {
            "id": "intl_platinum",
            "title": "GlobalPass Platinum Travel",
            "type": "international",
            "bin": "453288",
            "full_pan": "4532 8830 0000 1234",
            "masked_pan": "**** **** **** 1234",
            "network": "Mastercard",
            "account_number": "300000814",
            "holder_name": "April Dianne Calvo",
            "local_bank_fee": 0.00,
        },
        "intl_silver": {
            "id": "intl_silver",
            "title": "CitiReach Classic ATM",
            "type": "international",
            "bin": "529104",
            "full_pan": "5291 0440 0000 5678",
            "masked_pan": "**** **** **** 5678",
            "network": "Visa",
            "account_number": "400000932",
            "holder_name": "Diana Sismar",
            "local_bank_fee": 0.00,
        },
    }

    def __init__(self, accounts=None, active_type="savings", logged_in_card="100000248", selected_card_id="local_debit"):
        if accounts:
            self.accounts = accounts
        else:
            self.accounts = self._create_predefined_accounts()
        self.active_type = active_type if active_type in ("savings", "checking") else "savings"
        self.logged_in_card = logged_in_card if logged_in_card in self.accounts else "100000248"
        self.selected_card_id = selected_card_id if selected_card_id in self.CARD_CATALOG else "local_debit"
        self.current_account = self.accounts[self.logged_in_card][self.active_type]

    @staticmethod
    def _create_predefined_accounts():
        sa1 = SavingsAccount("100000248", "Hanz Dalmino", "248159", 15000.00)
        sa1._record_transaction("Opening Balance", 15000.00, 0.0)
        ca1 = CheckingAccount("100000248", "Hanz Dalmino", "248159", 25000.00)
        ca1._record_transaction("Opening Balance", 25000.00, 0.0)

        sa2 = SavingsAccount("200000519", "Kristof Badayos", "5194", 20000.00)
        sa2._record_transaction("Opening Balance", 20000.00, 0.0)
        ca2 = CheckingAccount("200000519", "Kristof Badayos", "5194", 35000.00)
        ca2._record_transaction("Opening Balance", 35000.00, 0.0)

        sa3 = SavingsAccount("300000814", "April Dianne Calvo", "814620", 45000.00)
        sa3._record_transaction("Opening Balance", 45000.00, 0.0)
        ca3 = CheckingAccount("300000814", "April Dianne Calvo", "814620", 60000.00)
        ca3._record_transaction("Opening Balance", 60000.00, 0.0)

        sa4 = SavingsAccount("400000932", "Diana Sismar", "9327", 30000.00)
        sa4._record_transaction("Opening Balance", 30000.00, 0.0)
        ca4 = CheckingAccount("400000932", "Diana Sismar", "9327", 40000.00)
        ca4._record_transaction("Opening Balance", 40000.00, 0.0)

        return {
            "100000248": {"savings": sa1, "checking": ca1},
            "200000519": {"savings": sa2, "checking": ca2},
            "300000814": {"savings": sa3, "checking": ca3},
            "400000932": {"savings": sa4, "checking": ca4},
        }

    def get_active_card_profile(self):
        return self.CARD_CATALOG.get(self.selected_card_id, self.CARD_CATALOG["local_debit"])

    def compute_network_fees(self, amount, card_id=None):
        cid = card_id or self.selected_card_id
        card = self.CARD_CATALOG.get(cid, self.CARD_CATALOG["local_debit"])
        amt = round(float(amount), 2) if amount else 0.0
        if card["type"] == "international":
            usd_min_php = round(self.INTL_USD_FEE * self.USD_EXCHANGE_RATE, 2)
            pct_php = round(amt * self.INTL_PCT_FEE, 2)
            intl_withdrawal_fee = max(usd_min_php, pct_php) if amt > 0 else usd_min_php
            fx_fee = round(amt * self.INTL_FX_FEE, 2)
            return {
                "card_type": "international",
                "local_bank_fee": 0.00,
                "intl_withdrawal_fee": intl_withdrawal_fee,
                "fx_conversion_fee": fx_fee,
                "total_network_fee": round(intl_withdrawal_fee + fx_fee, 2),
            }
        local_fee = round(card.get("local_bank_fee", 0.0), 2)
        return {
            "card_type": "local",
            "local_bank_fee": local_fee,
            "intl_withdrawal_fee": 0.00,
            "fx_conversion_fee": 0.00,
            "total_network_fee": local_fee,
        }

    def login(self, raw_acc, raw_pin, card_id=None):
        acc_in = str(raw_acc or "").strip()
        pin_in = "" if raw_pin is None else str(raw_pin)
        if not acc_in or not pin_in:
            raise ATMTransactionError("Please enter both your Account Number and PIN Code.")

        normalized = acc_in.replace(" ", "").replace("-", "")
        if not normalized.isdigit() or len(normalized) < 9:
            raise ATMTransactionError("Account Number must be at least 9 digits.")

        if not pin_in.isdigit() or len(pin_in) not in (4, 6):
            raise ATMTransactionError("Invalid PIN Code. Enter your exact assigned 4-digit or 6-digit PIN.")

        if normalized not in self.accounts:
            raise ATMTransactionError("Invalid Account Number or PIN Code.")

        user_accounts = self.accounts[normalized]
        sa = user_accounts["savings"]
        ca = user_accounts["checking"]
        if not (sa.verify_pin(pin_in) and ca.verify_pin(pin_in)):
            raise ATMTransactionError("Incorrect PIN Code. Access denied.")

        self.logged_in_card = normalized
        if card_id and card_id in self.CARD_CATALOG:
            self.selected_card_id = card_id
        else:
            for cid, cinfo in self.CARD_CATALOG.items():
                if cinfo["account_number"] == normalized:
                    self.selected_card_id = cid
                    break
        self.active_type = "savings"
        self.current_account = user_accounts["savings"]
        return self.current_account

    def select_account_type(self, kind):
        if kind == "checking":
            self.active_type = "checking"
        else:
            self.active_type = "savings"
        self.current_account = self.accounts[self.logged_in_card][self.active_type]
        return self.current_account

    def perform_deposit(self, raw_amount):
        return self.current_account.deposit(raw_amount)

    def perform_withdrawal(self, raw_amount):
        amount = Account.parse_positive_amount(raw_amount, "Withdrawal")
        fee_info = self.compute_network_fees(amount)
        return self.current_account.withdraw(amount, extra_fee=fee_info["total_network_fee"])

    def to_session_data(self):
        serialized = {}
        for card_num, pair in self.accounts.items():
            serialized[card_num] = {
                "savings": pair["savings"].to_dict(),
                "checking": pair["checking"].to_dict(),
            }
        return {
            "active_type": self.active_type,
            "logged_in_card": self.logged_in_card,
            "selected_card_id": self.selected_card_id,
            "accounts": serialized,
        }

    @classmethod
    def from_session_data(cls, data):
        if not data or "accounts" not in data:
            return cls()
        rebuilt = {}
        for card_num, pair in data["accounts"].items():
            if "savings" not in pair or "checking" not in pair:
                return cls()
            s_data = pair["savings"]
            c_data = pair["checking"]
            s_txs = [Transaction.from_dict(t) for t in s_data.get("transactions", [])]
            c_txs = [Transaction.from_dict(t) for t in c_data.get("transactions", [])]
            if "pin" not in s_data or "pin" not in c_data:
                return cls()
            rebuilt[card_num] = {
                "savings": SavingsAccount(s_data["account_number"], s_data["holder_name"], s_data["pin"], s_data["balance"], s_txs),
                "checking": CheckingAccount(c_data["account_number"], c_data["holder_name"], c_data["pin"], c_data["balance"], c_txs),
            }
        return cls(
            accounts=rebuilt,
            active_type=data.get("active_type", "savings"),
            logged_in_card=data.get("logged_in_card", "100000248"),
            selected_card_id=data.get("selected_card_id", "local_debit"),
        )
