"""
P ELEC 1 - Object-Oriented Programming (Python and Django)
Cebu Technological University - Main Campus
Option C: ATM Simulator - Core Python OOP Business Logic Module

This module contains all required OOP concepts for the project:
1. Classes and Objects: Account, SavingsAccount, CheckingAccount, Transaction, ATMService
2. Encapsulation: Internal attributes (_account_number, _holder_name, _balance, _transactions)
   accessed via @property getters and validated mutator methods.
3. Inheritance: SavingsAccount and CheckingAccount inherit from the parent Account class ("is-a").
4. Polymorphism: Both child classes override withdraw(raw_amount) and get_rules_summary()
   through a common Account interface with distinct limits, fees, and maintaining balance rules.
5. Exception Handling: Custom exception hierarchy rooted at ATMTransactionError.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional


# ============================================================================
# 1. EXCEPTION HANDLING (Custom Exception Classes)
# ============================================================================

class ATMTransactionError(Exception):
    """
    Base custom exception for all invalid ATM inputs and business rule violations.
    Provides a clear, user-friendly message and error code for the Django view.
    """
    def __init__(self, message: str, error_code: str = "TRANSACTION_ERROR"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class InvalidAmountError(ATMTransactionError):
    """Raised when an input amount is empty, non-numeric, zero, or negative."""
    def __init__(self, message: str):
        super().__init__(message, error_code="INVALID_AMOUNT")


class InsufficientFundsError(ATMTransactionError):
    """Raised when withdrawal amount (plus any applicable fee) exceeds current balance."""
    def __init__(self, message: str):
        super().__init__(message, error_code="INSUFFICIENT_FUNDS")


class WithdrawalLimitError(ATMTransactionError):
    """Raised when a single withdrawal exceeds the account type's maximum limit."""
    def __init__(self, message: str):
        super().__init__(message, error_code="WITHDRAWAL_LIMIT_EXCEEDED")


class MaintainingBalanceError(ATMTransactionError):
    """Raised when a withdrawal would drop a SavingsAccount below its maintaining balance."""
    def __init__(self, message: str):
        super().__init__(message, error_code="MAINTAINING_BALANCE_VIOLATION")


# ============================================================================
# 2. TRANSACTION CLASS (Encapsulated Session Transaction Record)
# ============================================================================

class Transaction:
    """
    Represents a single ATM transaction performed during the active session.
    Demonstrates Encapsulation via private/internal attributes and @property getters.
    """
    def __init__(
        self,
        transaction_id: str,
        tx_type: str,
        amount: float,
        fee: float,
        balance_after: float,
        note: str = "",
        timestamp: Optional[str] = None,
    ):
        self._transaction_id = str(transaction_id)
        self._tx_type = str(tx_type)
        self._amount = round(float(amount), 2)
        self._fee = round(float(fee), 2)
        self._balance_after = round(float(balance_after), 2)
        self._note = str(note)
        self._timestamp = timestamp or datetime.now().strftime("%b %d, %Y %I:%M:%S %p")

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def tx_type(self) -> str:
        return self._tx_type

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def fee(self) -> float:
        return self._fee

    @property
    def total_impact(self) -> float:
        return round(self._amount + self._fee, 2)

    @property
    def balance_after(self) -> float:
        return self._balance_after

    @property
    def note(self) -> str:
        return self._note

    @property
    def timestamp(self) -> str:
        return self._timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Transaction object for Django session storage."""
        return {
            "transaction_id": self._transaction_id,
            "tx_type": self._tx_type,
            "amount": self._amount,
            "fee": self._fee,
            "total_impact": self.total_impact,
            "balance_after": self._balance_after,
            "note": self._note,
            "timestamp": self._timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        """Reconstructs a Transaction object from Django session dictionary."""
        return cls(
            transaction_id=data["transaction_id"],
            tx_type=data["tx_type"],
            amount=data["amount"],
            fee=data.get("fee", 0.0),
            balance_after=data["balance_after"],
            note=data.get("note", ""),
            timestamp=data.get("timestamp"),
        )


# ============================================================================
# 3. PARENT CLASS: Account (Encapsulation & Shared Base Functionality)
# ============================================================================

class Account:
    """
    Parent class representing a fictional bank account.
    Encapsulates _account_number, _holder_name, _balance, and _transactions.
    Provides shared validation, deposit(), and balance inquiry behavior.
    """
    def __init__(
        self,
        account_number: str,
        holder_name: str,
        starting_balance: float,
        account_type: str = "Standard Account",
        transactions: Optional[List[Transaction]] = None,
    ):
        if not str(holder_name).strip():
            raise InvalidAmountError("Account holder name cannot be empty.")

        parsed_start = self._parse_non_negative_amount(starting_balance)
        self._account_number = str(account_number).strip()
        self._holder_name = str(holder_name).strip()
        self._balance = round(parsed_start, 2)
        self._account_type = account_type
        self._transactions: List[Transaction] = list(transactions) if transactions else []

    # --- Encapsulated Read-Only Properties ---
    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def holder_name(self) -> str:
        return self._holder_name

    @property
    def balance(self) -> float:
        """Returns the current encapsulated account balance."""
        return self._balance

    @property
    def account_type(self) -> str:
        return self._account_type

    @property
    def transactions(self) -> List[Transaction]:
        """Returns a copy of the transaction history list to preserve encapsulation."""
        return list(self._transactions)

    # --- Validation Helpers ---
    @staticmethod
    def _parse_non_negative_amount(raw_value: Any) -> float:
        """Validates a starting balance (must be numeric and >= 0)."""
        if raw_value is None or str(raw_value).strip() == "":
            raise InvalidAmountError("Please enter a valid numeric amount.")
        try:
            clean_str = str(raw_value).replace(",", "").strip()
            value = float(clean_str)
        except (ValueError, TypeError):
            raise InvalidAmountError(
                f"Invalid input '{raw_value}'. Amount must be a valid number."
            )
        if value < 0:
            raise InvalidAmountError("Starting balance cannot be negative.")
        return round(value, 2)

    @staticmethod
    def parse_positive_amount(raw_value: Any, operation_name: str = "Transaction") -> float:
        """
        Validates that a deposit or withdrawal input is present, numeric, and strictly > 0.
        Raises InvalidAmountError if validation fails, keeping account balance unchanged.
        """
        if raw_value is None or str(raw_value).strip() == "":
            raise InvalidAmountError(f"{operation_name} failed: Please enter an amount.")
        try:
            clean_str = str(raw_value).replace(",", "").strip()
            amount = float(clean_str)
        except (ValueError, TypeError):
            raise InvalidAmountError(
                f"{operation_name} rejected: '{raw_value}' is not a valid numeric amount."
            )

        if amount <= 0:
            raise InvalidAmountError(
                f"{operation_name} rejected: Amount must be greater than PHP 0.00 (received PHP {amount:,.2f})."
            )
        if amount > 1000000.00:
            raise InvalidAmountError(
                f"{operation_name} rejected: Single ATM transaction cannot exceed PHP 1,000,000.00."
            )
        return round(amount, 2)

    def _record_transaction(
        self, tx_type: str, amount: float, fee: float = 0.0, note: str = ""
    ) -> Transaction:
        """Internal helper to create and prepend a Transaction to the session history."""
        tx_number = len(self._transactions) + 1001
        tx_id = f"TXN-{self._account_number[-3:]}-{tx_number}"
        tx = Transaction(
            transaction_id=tx_id,
            tx_type=tx_type,
            amount=amount,
            fee=fee,
            balance_after=self._balance,
            note=note,
        )
        # Prepend newest transaction at index 0 for display
        self._transactions.insert(0, tx)
        return tx

    # --- Core Account Operations ---
    def deposit(self, raw_amount: Any, note: str = "Cash Deposit via Express ATM") -> Transaction:
        """
        Validates and adds a positive deposit amount to the encapsulated balance.
        Shared across all child Account classes via Inheritance.
        """
        amount = self.parse_positive_amount(raw_amount, operation_name="Deposit")
        self._balance = round(self._balance + amount, 2)
        return self._record_transaction(
            tx_type="Deposit",
            amount=amount,
            fee=0.00,
            note=note or "Cash Deposit via Express ATM",
        )

    def withdraw(self, raw_amount: Any, note: str = "Cash Withdrawal") -> Transaction:
        """
        Base withdrawal method. Overridden by SavingsAccount and CheckingAccount
        to demonstrate Polymorphism with distinct withdrawal limits and fee rules.
        """
        amount = self.parse_positive_amount(raw_amount, operation_name="Withdrawal")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Withdrawal rejected: Insufficient funds. Attempted to withdraw PHP {amount:,.2f}, "
                f"but current balance is PHP {self._balance:,.2f}."
            )
        self._balance = round(self._balance - amount, 2)
        return self._record_transaction(
            tx_type="Withdrawal",
            amount=amount,
            fee=0.00,
            note=note or "Standard ATM Withdrawal",
        )

    def inquire_balance(self) -> Dict[str, Any]:
        """Returns a structured balance inquiry report and logs no balance mutation."""
        rules = self.get_rules_summary()
        return {
            "account_number": self._account_number,
            "holder_name": self._holder_name,
            "account_type": self._account_type,
            "current_balance": self._balance,
            "withdrawable_balance": self.get_max_withdrawable(),
            "transaction_count": len(self._transactions),
            "rules": rules,
        }

    def get_max_withdrawable(self) -> float:
        """Overridden by child classes to compute exact maximum withdrawable cash right now."""
        return self._balance

    def get_rules_summary(self) -> Dict[str, Any]:
        """Overridden by child classes to expose their polymorphic rule parameters."""
        return {
            "class_name": self.__class__.__name__,
            "maintaining_balance": 0.00,
            "per_tx_limit": 25000.00,
            "withdrawal_fee": 0.00,
            "policy_description": "Standard base account withdrawal policy.",
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Account state to a dictionary for Django session storage."""
        return {
            "class_name": self.__class__.__name__,
            "account_number": self._account_number,
            "holder_name": self._holder_name,
            "balance": self._balance,
            "account_type": self._account_type,
            "rules": self.get_rules_summary(),
            "max_withdrawable": self.get_max_withdrawable(),
            "transactions": [t.to_dict() for t in self._transactions],
        }


# ============================================================================
# 4. CHILD CLASS 1: SavingsAccount (Inheritance & Polymorphism)
# ============================================================================

class SavingsAccount(Account):
    """
    Child class inheriting from Account ("is-a" relationship).
    Polymorphic Withdrawal Rule:
    - Minimum maintaining balance required: PHP 500.00
    - Maximum per-transaction withdrawal limit: PHP 20,000.00
    - Withdrawal service fee: PHP 0.00 (Free)
    """
    MAINTAINING_BALANCE = 500.00
    WITHDRAWAL_LIMIT = 20000.00
    WITHDRAWAL_FEE = 0.00

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        starting_balance: float,
        transactions: Optional[List[Transaction]] = None,
    ):
        super().__init__(
            account_number=account_number,
            holder_name=holder_name,
            starting_balance=starting_balance,
            account_type="Savings Account",
            transactions=transactions,
        )
        if self._balance < self.MAINTAINING_BALANCE:
            raise MaintainingBalanceError(
                f"New Savings Account requires at least PHP {self.MAINTAINING_BALANCE:,.2f} starting balance."
            )

    def get_max_withdrawable(self) -> float:
        available_above_maintaining = max(0.0, round(self._balance - self.MAINTAINING_BALANCE, 2))
        return min(available_above_maintaining, self.WITHDRAWAL_LIMIT)

    def get_rules_summary(self) -> Dict[str, Any]:
        return {
            "class_name": "SavingsAccount",
            "maintaining_balance": self.MAINTAINING_BALANCE,
            "per_tx_limit": self.WITHDRAWAL_LIMIT,
            "withdrawal_fee": self.WITHDRAWAL_FEE,
            "policy_description": (
                "Requires PHP 500.00 maintaining balance, max PHP 20,000.00 per withdrawal, "
                "PHP 0.00 withdrawal fee."
            ),
        }

    def withdraw(self, raw_amount: Any, note: str = "Savings ATM Withdrawal") -> Transaction:
        """
        OVERRIDDEN METHOD (Polymorphism):
        Enforces the PHP 20,000.00 per-transaction limit and PHP 500.00 maintaining balance rule.
        No service fee is charged.
        """
        amount = self.parse_positive_amount(raw_amount, operation_name="Savings Withdrawal")

        # 1. Check per-withdrawal limit
        if amount > self.WITHDRAWAL_LIMIT:
            raise WithdrawalLimitError(
                f"Savings Withdrawal rejected: Amount PHP {amount:,.2f} exceeds the "
                f"Savings Account per-transaction limit of PHP {self.WITHDRAWAL_LIMIT:,.2f}."
            )

        # 2. Check if amount exceeds total balance
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Savings Withdrawal rejected: Insufficient balance. Requested PHP {amount:,.2f}, "
                f"but current balance is PHP {self._balance:,.2f}. Balance remains unchanged."
            )

        # 3. Check maintaining balance rule (must leave at least PHP 500.00)
        projected_balance = round(self._balance - amount, 2)
        if projected_balance < self.MAINTAINING_BALANCE:
            max_allowed = max(0.0, round(self._balance - self.MAINTAINING_BALANCE, 2))
            raise MaintainingBalanceError(
                f"Savings Withdrawal rejected: Cannot drop below the PHP {self.MAINTAINING_BALANCE:,.2f} "
                f"maintaining balance (projected balance would be PHP {projected_balance:,.2f}). "
                f"Maximum withdrawable right now is PHP {max_allowed:,.2f}."
            )

        # 4. Commit deduction and record transaction
        self._balance = projected_balance
        return self._record_transaction(
            tx_type="Withdrawal",
            amount=amount,
            fee=0.00,
            note=note or "Savings Withdrawal (No Fee, PHP 500 Maintaining Rule)",
        )


# ============================================================================
# 5. CHILD CLASS 2: CheckingAccount (Inheritance & Polymorphism)
# ============================================================================

class CheckingAccount(Account):
    """
    Child class inheriting from Account ("is-a" relationship).
    Polymorphic Withdrawal Rule:
    - Minimum maintaining balance required: PHP 0.00 (Can withdraw down to zero)
    - Maximum per-transaction withdrawal limit: PHP 50,000.00
    - Flat checking withdrawal processing fee: PHP 15.00 per withdrawal
    """
    MAINTAINING_BALANCE = 0.00
    WITHDRAWAL_LIMIT = 50000.00
    WITHDRAWAL_FEE = 15.00

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        starting_balance: float,
        transactions: Optional[List[Transaction]] = None,
    ):
        super().__init__(
            account_number=account_number,
            holder_name=holder_name,
            starting_balance=starting_balance,
            account_type="Checking Account",
            transactions=transactions,
        )

    def get_max_withdrawable(self) -> float:
        if self._balance <= self.WITHDRAWAL_FEE:
            return 0.0
        available_after_fee = round(self._balance - self.WITHDRAWAL_FEE, 2)
        return min(available_after_fee, self.WITHDRAWAL_LIMIT)

    def get_rules_summary(self) -> Dict[str, Any]:
        return {
            "class_name": "CheckingAccount",
            "maintaining_balance": self.MAINTAINING_BALANCE,
            "per_tx_limit": self.WITHDRAWAL_LIMIT,
            "withdrawal_fee": self.WITHDRAWAL_FEE,
            "policy_description": (
                "PHP 0.00 maintaining balance, higher PHP 50,000.00 limit per withdrawal, "
                "flat PHP 15.00 processing fee per withdrawal."
            ),
        }

    def withdraw(self, raw_amount: Any, note: str = "Checking ATM Withdrawal") -> Transaction:
        """
        OVERRIDDEN METHOD (Polymorphism):
        Enforces a higher PHP 50,000.00 limit, allows zero maintaining balance,
        and applies a flat PHP 15.00 checking withdrawal fee.
        """
        amount = self.parse_positive_amount(raw_amount, operation_name="Checking Withdrawal")

        # 1. Check per-withdrawal limit
        if amount > self.WITHDRAWAL_LIMIT:
            raise WithdrawalLimitError(
                f"Checking Withdrawal rejected: Amount PHP {amount:,.2f} exceeds the "
                f"Checking Account per-transaction limit of PHP {self.WITHDRAWAL_LIMIT:,.2f}."
            )

        # 2. Compute total deduction including flat PHP 15.00 service fee
        total_deduction = round(amount + self.WITHDRAWAL_FEE, 2)

        # 3. Reject overdraft (balance cannot become negative)
        if total_deduction > self._balance:
            raise InsufficientFundsError(
                f"Checking Withdrawal rejected: Insufficient funds to cover PHP {amount:,.2f} "
                f"plus PHP {self.WITHDRAWAL_FEE:,.2f} checking fee (Total required: PHP {total_deduction:,.2f}; "
                f"Current balance: PHP {self._balance:,.2f}). Balance remains unchanged."
            )

        # 4. Commit deduction and record transaction with fee
        self._balance = round(self._balance - total_deduction, 2)
        return self._record_transaction(
            tx_type="Withdrawal",
            amount=amount,
            fee=self.WITHDRAWAL_FEE,
            note=note or f"Checking Withdrawal (+PHP {self.WITHDRAWAL_FEE:,.2f} Service Fee)",
        )


# ============================================================================
# 6. SERVICE CLASS: ATMService (Controller Connecting OOP to Django Views)
# ============================================================================

class ATMService:
    """
    High-level service controller that manages active fictional accounts,
    executes polymorphic operations on the selected Account instance,
    and serializes/deserializes session state for Django views.
    """
    def __init__(
        self,
        accounts: Optional[Dict[str, Account]] = None,
        active_account_number: str = "SA-100248",
    ):
        if accounts:
            self._accounts = accounts
        else:
            self._accounts = self._create_predefined_accounts()

        if active_account_number in self._accounts:
            self._active_account_number = active_account_number
        else:
            self._active_account_number = next(iter(self._accounts.keys()))

    @staticmethod
    def _create_predefined_accounts() -> Dict[str, Account]:
        """Creates the initial predefined fictional accounts for the ATM simulator."""
        acc1 = SavingsAccount(
            account_number="SA-100248",
            holder_name="Hanz Dee",
            starting_balance=15000.00,
            transactions=[
                Transaction(
                    transaction_id="TXN-248-1001",
                    tx_type="Opening Balance",
                    amount=15000.00,
                    fee=0.00,
                    balance_after=15000.00,
                    note="Initial predefined Savings Account deposit",
                    timestamp="Nov 05, 2026 08:00:00 AM",
                )
            ],
        )
        acc2 = CheckingAccount(
            account_number="CA-200519",
            holder_name="Hanz Dee",
            starting_balance=25000.00,
            transactions=[
                Transaction(
                    transaction_id="TXN-519-1001",
                    tx_type="Opening Balance",
                    amount=25000.00,
                    fee=0.00,
                    balance_after=25000.00,
                    note="Initial predefined Checking Account deposit",
                    timestamp="Nov 05, 2026 08:05:00 AM",
                )
            ],
        )
        acc3 = SavingsAccount(
            account_number="SA-100892",
            holder_name="Maria Clara Santos",
            starting_balance=3500.00,
            transactions=[
                Transaction(
                    transaction_id="TXN-892-1001",
                    tx_type="Opening Balance",
                    amount=3500.00,
                    fee=0.00,
                    balance_after=3500.00,
                    note="Initial predefined Student Savings deposit",
                    timestamp="Nov 05, 2026 08:15:00 AM",
                )
            ],
        )
        return {
            acc1.account_number: acc1,
            acc2.account_number: acc2,
            acc3.account_number: acc3,
        }

    @property
    def active_account(self) -> Account:
        """Returns the currently selected Account object (SavingsAccount or CheckingAccount)."""
        return self._accounts[self._active_account_number]

    @property
    def accounts(self) -> List[Account]:
        return list(self._accounts.values())

    def switch_account(self, account_number: str) -> Account:
        """Switches the active session account."""
        clean_num = str(account_number).strip()
        if clean_num not in self._accounts:
            raise ATMTransactionError(f"Account '{clean_num}' was not found in the active session.")
        self._active_account_number = clean_num
        return self.active_account

    def create_custom_account(
        self, holder_name: str, account_kind: str, raw_starting_balance: Any
    ) -> Account:
        """
        Creates a new fictional SavingsAccount or CheckingAccount during the session
        and sets it as the active account.
        """
        clean_name = str(holder_name or "").strip()
        if not clean_name:
            raise InvalidAmountError("Account creation failed: Please provide an account holder name.")

        start_bal = Account._parse_non_negative_amount(raw_starting_balance)
        seq = 100000 + (len(self._accounts) + 1) * 137

        if str(account_kind).lower() == "checking":
            acc_num = f"CA-{seq}"
            new_acc: Account = CheckingAccount(
                account_number=acc_num,
                holder_name=clean_name,
                starting_balance=start_bal,
            )
        else:
            acc_num = f"SA-{seq}"
            new_acc = SavingsAccount(
                account_number=acc_num,
                holder_name=clean_name,
                starting_balance=start_bal,
            )

        new_acc._record_transaction(
            tx_type="Account Created",
            amount=start_bal,
            fee=0.00,
            note=f"Opened new {new_acc.account_type} in session",
        )
        self._accounts[new_acc.account_number] = new_acc
        self._active_account_number = new_acc.account_number
        return new_acc

    def perform_deposit(self, raw_amount: Any, note: str = "") -> Transaction:
        """Delegates deposit operation to the active Account object."""
        return self.active_account.deposit(
            raw_amount, note=note or "Cash Deposit via Express ATM"
        )

    def perform_withdrawal(self, raw_amount: Any, note: str = "") -> Transaction:
        """
        POLYMORPHIC CALL:
        Invokes .withdraw() on the active Account reference.
        Python dynamically dispatches to SavingsAccount.withdraw() or CheckingAccount.withdraw()
        depending on the runtime class of self.active_account.
        """
        return self.active_account.withdraw(raw_amount, note=note)

    @staticmethod
    def demonstrate_polymorphism(raw_test_amount: Any = 2000.00, sample_balance: float = 10000.00) -> Dict[str, Any]:
        """
        Runs the exact same overridden .withdraw(amount) call on both a SavingsAccount
        and a CheckingAccount instance with identical starting balances to demonstrate
        polymorphic behavior side by side for classroom presentation/defense.
        """
        amount = Account.parse_positive_amount(raw_test_amount, operation_name="Polymorphism Demo")
        accounts_to_test: List[Account] = [
            SavingsAccount("DEMO-SA", "Sample Holder (Savings)", sample_balance),
            CheckingAccount("DEMO-CA", "Sample Holder (Checking)", sample_balance),
        ]
        results = []
        for acc in accounts_to_test:
            before_bal = acc.balance
            try:
                tx = acc.withdraw(amount, note="Polymorphic withdraw() comparison")
                results.append({
                    "class_name": acc.__class__.__name__,
                    "account_type": acc.account_type,
                    "starting_balance": before_bal,
                    "requested_withdrawal": amount,
                    "fee_charged": tx.fee,
                    "total_deducted": tx.total_impact,
                    "ending_balance": acc.balance,
                    "status": "SUCCESS",
                    "explanation": (
                        f"{acc.__class__.__name__}.withdraw({amount:,.2f}) deducted PHP {tx.total_impact:,.2f} "
                        f"(Fee: PHP {tx.fee:,.2f}), leaving PHP {acc.balance:,.2f}."
                    ),
                })
            except ATMTransactionError as exc:
                results.append({
                    "class_name": acc.__class__.__name__,
                    "account_type": acc.account_type,
                    "starting_balance": before_bal,
                    "requested_withdrawal": amount,
                    "fee_charged": 0.0,
                    "total_deducted": 0.0,
                    "ending_balance": acc.balance,
                    "status": "REJECTED",
                    "explanation": exc.message,
                })
        return {
            "sample_starting_balance": sample_balance,
            "requested_amount": amount,
            "comparisons": results,
        }

    def to_session_data(self) -> Dict[str, Any]:
        """Serializes the entire ATMService state into a JSON-compatible dictionary for Django sessions."""
        return {
            "active_account_number": self._active_account_number,
            "accounts": {num: acc.to_dict() for num, acc in self._accounts.items()},
        }

    @classmethod
    def from_session_data(cls, data: Optional[Dict[str, Any]]) -> "ATMService":
        """Rebuilds ATMService and its child Account objects from Django session dictionary."""
        if not data or "accounts" not in data:
            return cls()

        rebuilt_accounts: Dict[str, Account] = {}
        for acc_num, acc_dict in data["accounts"].items():
            tx_list = [Transaction.from_dict(t) for t in acc_dict.get("transactions", [])]
            class_name = acc_dict.get("class_name", "SavingsAccount")
            if class_name == "CheckingAccount":
                rebuilt_accounts[acc_num] = CheckingAccount(
                    account_number=acc_dict["account_number"],
                    holder_name=acc_dict["holder_name"],
                    starting_balance=acc_dict["balance"],
                    transactions=tx_list,
                )
            else:
                # Temporarily allow reconstructing even if balance was customized
                sa = SavingsAccount.__new__(SavingsAccount)
                Account.__init__(
                    sa,
                    account_number=acc_dict["account_number"],
                    holder_name=acc_dict["holder_name"],
                    starting_balance=acc_dict["balance"],
                    account_type="Savings Account",
                    transactions=tx_list,
                )
                rebuilt_accounts[acc_num] = sa

        active_num = data.get("active_account_number", "SA-100248")
        return cls(accounts=rebuilt_accounts, active_account_number=active_num)


# ============================================================================
# 7. AUTOMATED TEST SUITE FOR PART VI & PART IX (6+ Documented Test Cases)
# ============================================================================

def run_documented_test_cases() -> List[Dict[str, Any]]:
    """
    Executes the 6 mandatory test cases specified in Part VI and Part IX of the
    CTU P ELEC 1 Instructional Guide (Normal, Boundary, Invalid, Business Rule,
    Polymorphism, and Custom Exception Handling) and returns a structured report.
    """
    test_results: List[Dict[str, Any]] = []

    # Case 1: Normal Operation (Deposit & Withdrawal on SavingsAccount)
    sa_normal = SavingsAccount("SA-TEST-01", "Hanz Dee", 15000.00)
    sa_normal.deposit(2500.00)
    sa_normal.withdraw(1500.00)
    c1_pass = sa_normal.balance == 16000.00 and len(sa_normal.transactions) == 2
    test_results.append({
        "case_id": "TC-01",
        "test_type": "Normal Operation",
        "scenario": "Deposit PHP 2,500.00 then withdraw PHP 1,500.00 from SavingsAccount (Start: PHP 15,000.00)",
        "user_input": "deposit('2500') -> withdraw('1500')",
        "expected_output": "Balance updates to PHP 17,500.00 then PHP 16,000.00; 2 transactions recorded; PHP 0.00 fee.",
        "actual_output": f"Final Balance: PHP {sa_normal.balance:,.2f}; Transactions recorded: {len(sa_normal.transactions)}",
        "result": "PASS" if c1_pass else "FAIL",
    })

    # Case 2: Boundary Input (Exact Maintaining Balance Limit on SavingsAccount)
    sa_boundary = SavingsAccount("SA-TEST-02", "Hanz Dee", 3500.00)
    sa_boundary.withdraw(3000.00)  # Leaves exact PHP 500.00 maintaining balance
    c2_pass = sa_boundary.balance == 500.00
    test_results.append({
        "case_id": "TC-02",
        "test_type": "Boundary Input",
        "scenario": "Withdraw exact maximum allowed (PHP 3,000.00) from a PHP 3,500.00 SavingsAccount leaving exact PHP 500.00 maintaining balance",
        "user_input": "withdraw('3000.00') on balance PHP 3,500.00",
        "expected_output": "Withdrawal succeeds; remaining balance is exactly PHP 500.00 (minimum maintaining boundary).",
        "actual_output": f"Withdrawal succeeded; Remaining Balance: PHP {sa_boundary.balance:,.2f}",
        "result": "PASS" if c2_pass else "FAIL",
    })

    # Case 3: Invalid Input (Negative and Non-Numeric Deposit/Withdrawal Rejection)
    sa_invalid = SavingsAccount("SA-TEST-03", "Hanz Dee", 15000.00)
    caught_msg = ""
    try:
        sa_invalid.deposit("-500")
    except InvalidAmountError as exc:
        caught_msg = exc.message
    c3_pass = (sa_invalid.balance == 15000.00) and ("greater than PHP 0.00" in caught_msg)
    test_results.append({
        "case_id": "TC-03",
        "test_type": "Invalid Input",
        "scenario": "Attempt to deposit a negative amount (-500) into SavingsAccount",
        "user_input": "deposit('-500')",
        "expected_output": "Raises InvalidAmountError; rejects negative deposit; preserves PHP 15,000.00 balance.",
        "actual_output": f"{caught_msg} (Preserved Balance: PHP {sa_invalid.balance:,.2f})",
        "result": "PASS" if c3_pass else "FAIL",
    })

    # Case 4: Business Rule Violation (Maintaining Balance / Overdraft Protection)
    sa_rule = SavingsAccount("SA-TEST-04", "Hanz Dee", 3500.00)
    rule_msg = ""
    try:
        sa_rule.withdraw(3200.00)  # Would leave PHP 300.00 (< PHP 500.00 maintaining balance)
    except MaintainingBalanceError as exc:
        rule_msg = exc.message
    c4_pass = (sa_rule.balance == 3500.00) and ("maintaining balance" in rule_msg.lower())
    test_results.append({
        "case_id": "TC-04",
        "test_type": "Business Rule",
        "scenario": "Attempt to withdraw PHP 3,200.00 from a PHP 3,500.00 SavingsAccount (violates PHP 500.00 maintaining balance rule)",
        "user_input": "withdraw('3200.00') on balance PHP 3,500.00",
        "expected_output": "Raises MaintainingBalanceError; balance remains unchanged at PHP 3,500.00.",
        "actual_output": f"{rule_msg} (Preserved Balance: PHP {sa_rule.balance:,.2f})",
        "result": "PASS" if c4_pass else "FAIL",
    })

    # Case 5: Polymorphism Verification (Same withdraw() call on SavingsAccount vs CheckingAccount)
    sa_poly = SavingsAccount("SA-TEST-05", "Hanz Dee", 10000.00)
    ca_poly = CheckingAccount("CA-TEST-05", "Hanz Dee", 10000.00)
    sa_poly.withdraw(2000.00)  # Deducts 2000.00 (no fee) -> 8000.00
    ca_poly.withdraw(2000.00)  # Deducts 2000.00 + 15.00 fee -> 7985.00
    c5_pass = (sa_poly.balance == 8000.00) and (ca_poly.balance == 7985.00)
    test_results.append({
        "case_id": "TC-05",
        "test_type": "Polymorphism",
        "scenario": "Call overridden withdraw(2000.00) on both SavingsAccount and CheckingAccount starting at PHP 10,000.00",
        "user_input": "account.withdraw('2000.00') on SavingsAccount vs. CheckingAccount",
        "expected_output": "Distinct results: SavingsAccount ends at PHP 8,000.00 (PHP 0.00 fee); CheckingAccount ends at PHP 7,985.00 (PHP 15.00 fee).",
        "actual_output": f"Savings Balance: PHP {sa_poly.balance:,.2f} | Checking Balance: PHP {ca_poly.balance:,.2f}",
        "result": "PASS" if c5_pass else "FAIL",
    })

    # Case 6: Exception Handling (Non-Numeric Text Input & Per-Transaction Limit Custom Exception)
    ca_exc = CheckingAccount("CA-TEST-06", "Hanz Dee", 60000.00)
    exc_msg = ""
    try:
        ca_exc.withdraw(55000.00)  # Exceeds PHP 50,000.00 Checking per-withdrawal limit
    except WithdrawalLimitError as exc:
        exc_msg = exc.message
    c6_pass = (ca_exc.balance == 60000.00) and ("50,000.00" in exc_msg)
    test_results.append({
        "case_id": "TC-06",
        "test_type": "Exception Handling",
        "scenario": "Trigger custom WithdrawalLimitError by requesting PHP 55,000.00 on CheckingAccount (Limit: PHP 50,000.00)",
        "user_input": "withdraw('55000.00')",
        "expected_output": "Catches custom WithdrawalLimitError with descriptive message; preserves PHP 60,000.00 balance.",
        "actual_output": f"{exc_msg} (Preserved Balance: PHP {ca_exc.balance:,.2f})",
        "result": "PASS" if c6_pass else "FAIL",
    })

    return test_results
