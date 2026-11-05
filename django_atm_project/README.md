# CTU Express ATM Simulator — Python & Django OOP Final Project

**Course:** P ELEC 1 - Object-Oriented Programming (Python and Django)  
**Institution:** Cebu Technological University — Main Campus (CCICT)  
**Approved Project Option:** Option C — ATM Simulator  
**Python Version:** Python 3.10+  
**Framework:** Django 4.2+ / 5.x (Pure Python, HTML, and CSS — Zero Database Required)

---

## 1. Group Information & Member Contribution Record

| Member Name | Assigned Role | Completed OOP & Django Responsibilities |
| :--- | :--- | :--- |
| **Member 1 (Hanz Dee)** | Lead OOP Architect | Designed `Account` parent class, encapsulation properties, and custom exception hierarchy (`ATMTransactionError`) in `atm_app/oop_models.py`. |
| **Member 2** | Inheritance & Polymorphism Developer | Implemented `SavingsAccount` and `CheckingAccount` child classes and overridden `withdraw()` & `get_rules_summary()` methods in `atm_app/oop_models.py`. |
| **Member 3** | Django Integration & Session Engineer | Implemented `ATMService`, `Transaction` class, `atm_app/views.py`, `atm_app/urls.py`, and session serialization (`request.session`). |
| **Member 4** | Frontend UI (HTML/CSS) & QA Tester | Built `templates/atm/index.html` and Light Blue & White Glassmorphic `static/atm/style.css`; authored and verified the 6 documented test cases. |

---

## 2. Setup and Run Instructions

1. **Extract the Project Archive:**
   Unzip `CTU_PELEC1_ATM_Simulator_Django.zip` and open a terminal inside `django_atm_project/`.

2. **Create and Activate a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. **Install Django:**
   ```bash
   pip install django
   ```

4. **Start the Django Development Server (No Database Migrations Needed):**
   ```bash
   python manage.py runserver
   ```

5. **Open in Browser:**
   Visit `http://127.0.0.1:8000/` in your web browser.

---

## 3. Main Application Workflow

1. **Select or Create a Fictional Account:**
   - Choose from three predefined fictional accounts (`SA-100248` Hanz Dee Savings, `CA-200519` Hanz Dee Checking, or `SA-100892` Maria Clara Santos Savings) or instantiate a new `SavingsAccount` / `CheckingAccount` object during the active session.
2. **Balance Inquiry:**
   - Displays current balance, maximum withdrawable amount right now, and active account rules (`Maintaining Balance`, `Per-Withdrawal Limit`, and `Withdrawal Processing Fee`).
3. **Deposit Funds (`Account.deposit()`):**
   - Validates that input is numeric and strictly positive (`> 0`). Updates `_balance` and prepends a `Transaction` object to the active session history.
4. **Withdraw Cash (`SavingsAccount.withdraw()` vs. `CheckingAccount.withdraw()`):**
   - Demonstrates **Polymorphism**:
     - `SavingsAccount.withdraw()` enforces a `PHP 20,000.00` per-transaction limit, `PHP 500.00` minimum maintaining balance, and `PHP 0.00` fee.
     - `CheckingAccount.withdraw()` enforces a `PHP 50,000.00` per-transaction limit, `PHP 0.00` maintaining balance, and a flat `PHP 15.00` checking service fee per withdrawal.
5. **Session Transaction History:**
   - Displays all transactions recorded during the active session in reverse chronological order.

---

## 4. Known Persistence & Data Reset Limitations

- In accordance with **Part IV (Django Integration and Development Rules)** of the instructional guide, a relational database is **not required**.
- Account states and transaction histories are stored in **Django signed cookie sessions** (`SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`).
- Clicking **"Reset Session"** (or clearing browser cookies) restores all predefined accounts and balances to their initial starting state.

---

## 5. OOP Implementation Summary Mapping

| Mandatory OOP Concept | Python File | Class(es) Involved | Method(s) / Properties Demonstrating Concept |
| :--- | :--- | :--- | :--- |
| **Classes and Objects** | `atm_app/oop_models.py` | `Account`, `SavingsAccount`, `CheckingAccount`, `Transaction`, `ATMService` | Instantiated in `ATMService._create_predefined_accounts()`, `create_custom_account()`, and `_record_transaction()`. |
| **Encapsulation** | `atm_app/oop_models.py` | `Account`, `Transaction` | Protected internal attributes `_account_number`, `_holder_name`, `_balance`, `_transactions` accessed via `@property` getters and validated mutator methods (`deposit()`, `withdraw()`). |
| **Inheritance** | `atm_app/oop_models.py` | Parent: `Account`<br>Children: `SavingsAccount`, `CheckingAccount` | Both child classes inherit `deposit()`, `inquire_balance()`, `_record_transaction()`, and properties from `Account` via `super().__init__()`. |
| **Polymorphism** | `atm_app/oop_models.py` | `SavingsAccount`, `CheckingAccount` | Overridden `withdraw(raw_amount)` and `get_rules_summary()` called through `ATMService.perform_withdrawal()` and `demonstrate_polymorphism()`. |
| **Exception Handling** | `atm_app/oop_models.py` & `atm_app/views.py` | `ATMTransactionError`, `InvalidAmountError`, `InsufficientFundsError`, `WithdrawalLimitError`, `MaintainingBalanceError` | Raised in `parse_positive_amount()` and `withdraw()`; caught in `views.py` (`try...except ATMTransactionError`) to preserve balance and render readable browser alerts. |

---

## 6. UML Class Diagram

```text
+-------------------------------------------------------+
|                 ATMTransactionError                   |
|                     (Exception)                       |
+-------------------------------------------------------+
| + message: str                                        |
| + error_code: str                                     |
+-------------------------------------------------------+
     ^                  ^                   ^
     |                  |                   |
InvalidAmountError  InsufficientFundsError  MaintainingBalanceError / WithdrawalLimitError


+-------------------------------------------------------+
|                      Account                          |
|                   (Parent Class)                      |
+-------------------------------------------------------+
| - _account_number: str                                |
| - _holder_name: str                                   |
| - _balance: float                                     |
| - _account_type: str                                  |
| - _transactions: List[Transaction]                    |
+-------------------------------------------------------+
| + balance: float (@property)                          |
| + transactions: List[Transaction] (@property)         |
| + parse_positive_amount(raw_value): float             |
| + deposit(raw_amount, note): Transaction              |
| + withdraw(raw_amount, note): Transaction             |
| + inquire_balance(): dict                             |
| + get_max_withdrawable(): float                       |
| + get_rules_summary(): dict                           |
+-------------------------------------------------------+
              ^                           ^
              | (is-a)                    | (is-a)
+---------------------------+   +---------------------------+
|      SavingsAccount       |   |      CheckingAccount      |
|       (Child Class)       |   |       (Child Class)       |
+---------------------------+   +---------------------------+
| + MAINTAINING_BALANCE=500 |   | + MAINTAINING_BALANCE=0   |
| + WITHDRAWAL_LIMIT=20000  |   | + WITHDRAWAL_LIMIT=50000  |
| + WITHDRAWAL_FEE=0.00     |   | + WITHDRAWAL_FEE=15.00    |
+---------------------------+   +---------------------------+
| + withdraw(raw_amount)    |   | + withdraw(raw_amount)    |
| + get_max_withdrawable()  |   | + get_max_withdrawable()  |
| + get_rules_summary()     |   | + get_rules_summary()     |
+---------------------------+   +---------------------------+


+-------------------------------------------------------+
|                    Transaction                        |
+-------------------------------------------------------+
| - _transaction_id: str                                |
| - _tx_type: str                                       |
| - _amount: float                                      |
| - _fee: float                                         |
| - _balance_after: float                               |
| - _timestamp: str                                     |
+-------------------------------------------------------+
| + to_dict(): dict                                     |
| + from_dict(data): Transaction                        |
+-------------------------------------------------------+
```

---

## 7. Six (6) Documented Test Cases Report

| Case ID | Test Type | Scenario | Exact User Input | Expected Result | Actual Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Normal Operation | Deposit PHP 2,500.00 then withdraw PHP 1,500.00 on `SavingsAccount` (`SA-100248`, Start: PHP 15,000.00) | Deposit: `2500`<br>Withdraw: `1500` | Balance becomes PHP 17,500.00 then PHP 16,000.00; 2 transactions logged. | Final Balance: PHP 16,000.00; 2 transactions recorded. | **PASS** |
| **TC-02** | Boundary Input | Withdraw exact max allowed (PHP 3,000.00) from PHP 3,500.00 `SavingsAccount` leaving exact PHP 500.00 maintaining balance | Withdraw: `3000.00` | Withdrawal succeeds; remaining balance is exactly PHP 500.00. | Remaining Balance: PHP 500.00; no error raised. | **PASS** |
| **TC-03** | Invalid Input | Enter negative deposit amount (`-500`) on `SavingsAccount` (Balance: PHP 15,000.00) | Deposit: `-500` | Rejects negative deposit via `InvalidAmountError`; balance stays PHP 15,000.00. | `InvalidAmountError` displayed; Balance preserved at PHP 15,000.00. | **PASS** |
| **TC-04** | Business Rule | Attempt to withdraw PHP 3,200.00 from PHP 3,500.00 `SavingsAccount` (would leave PHP 300.00 < PHP 500.00 maintaining balance) | Withdraw: `3200.00` | Rejects via `MaintainingBalanceError`; balance stays PHP 3,500.00. | `MaintainingBalanceError` displayed; Balance preserved at PHP 3,500.00. | **PASS** |
| **TC-05** | Polymorphism | Execute `account.withdraw(2000.00)` on both `SavingsAccount` and `CheckingAccount` starting at PHP 10,000.00 | Withdraw: `2000.00` | `SavingsAccount` ends at PHP 8,000.00 (PHP 0 fee); `CheckingAccount` ends at PHP 7,985.00 (PHP 15 fee). | Savings: PHP 8,000.00; Checking: PHP 7,985.00. | **PASS** |
| **TC-06** | Exception Handling | Request PHP 55,000.00 withdrawal on `CheckingAccount` (exceeds PHP 50,000.00 single withdrawal limit) | Withdraw: `55000.00` | Raises custom `WithdrawalLimitError` with readable message; balance unchanged. | `WithdrawalLimitError` displayed in browser; Balance unchanged. | **PASS** |
