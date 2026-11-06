# ExpressBank ATM Simulator — Python & Django OOP Final Project

**Course:** P ELEC 1 - Object-Oriented Programming (Python and Django)  
**Institution:** Cebu Technological University — Main Campus (CCICT)  
**Approved Project Option:** Option C — ATM Simulator  
**Languages & Technologies Used:** Strictly **Python, HTML, and CSS** (Django 4.2+ / 5.x, Pure CSS Glassmorphism, Poppins Bold Typography, SVG Vector Icons)

---

## 1. Group Members & Contribution Record (5 Members)

| Member Name | Assigned Role | Completed OOP, Django & UI Responsibilities |
| :--- | :--- | :--- |
| **April Dianne Calvo** | Project Lead & Documentation Specialist | Led project planning, system workflow alignment with Part III & Part IV rules, UML class diagramming, and documentation of test cases. |
| **Hanz Dee Dalmino** | Lead Python OOP Architect | Designed the `Account` parent class, encapsulation `@property` getters (`masked_account_number`, `balance`, `transactions`), and custom exception hierarchy (`ATMTransactionError`) in `atm_app/oop_models.py`. |
| **Steve Niño Larino** | Inheritance & Polymorphism Developer | Implemented the `SavingsAccount` and `CheckingAccount` child classes and overridden `withdraw()` and `get_max_withdrawable()` methods enforcing maintaining balances, limits, and fees. |
| **Kristof Glendale Badayos** | Django Views, Routing & Session Engineer | Built `ATMService`, `Transaction` class, `atm_app/views.py`, `atm_app/urls.py`, multi-account credential verification, and session/local state serialization. |
| **Diana Sismar** | Frontend UI/UX (HTML & CSS) & QA Tester | Designed the Light Blue & White Glassmorphic interface (`style.css` and `index.html`) using **Poppins Bold** typography, SVG vector icons, loading state transitions, and expanded transaction history modal. |

---

## 2. About the System & Summary of System Updates

The **ExpressBank ATM Simulator** is a web-based Automated Teller Machine simulation built strictly with **Python, HTML, and CSS** following **Option C (ATM Simulator)** of the P ELEC 1 Final Project Instructional Guide.

### Key System Features & Recent Updates

1. **ATM Card Login Screen (9+ Digit Account Number & 6-Digit PIN)**
   - Users log in using only their **Account Number** (validated to be **at least 9 digits**) and **PIN Code** (up to **6 digits**, with support for 4-digit PINs and an on-screen note: *"If your PIN is below 6 digits, type and hit Enter"*).
   - **Manual Enter Submission Only:** Auto-enter/auto-submit on typing is disabled. The user must manually press the **Enter** key or click the **Enter ATM** button to submit credentials.
   - **Loading Spinner Verification:** Displays a smooth circular loading indicator (*"Verifying Credentials..."*) before entering the ATM menu or showing an error banner.

2. **Masked Account Number Privacy (`******248` / `******519`)**
   - Encapsulated via the `Account.masked_account_number` property and `mask_account_number()` helper.
   - Hides all leading digits with asterisks (`*`) and reveals only the **last 3 digits** (e.g., `Card Account #******248` and `******519`) in the ATM header and Balance Inquiry view.

3. **Predefined Cardholder Accounts**
   - Each predefined account number authenticates its specific cardholder and maintains its own separate **Savings Account** and **Checking Account** balances and transaction histories:
     - **Account 1:** Account Number `100000248` (`******248`) · Holder: **Hanz Dalmino** · PIN: `123456` (or `1234`) · Savings Starting Balance: `₱ 15,000.00` · Checking Starting Balance: `₱ 25,000.00`
     - **Account 2:** Account Number `200000519` (`******519`) · Holder: **Kristof Badayos** · PIN: `123456` (or `1234`) · Savings Starting Balance: `₱ 15,000.00` · Checking Starting Balance: `₱ 25,000.00`

4. **Account Type Selection Before Every Operation**
   - Selecting **Withdraw**, **Deposit**, **Balance Inquiry**, or **Transactions** from the main ATM menu first prompts the user to select an **Account Type**:
     - **Savings Account:** `₱ 500.00` maintaining balance · `₱ 20,000.00` per-withdrawal limit · `₱ 0.00` withdrawal fee.
     - **Checking Account:** `₱ 0.00` maintaining balance · `₱ 50,000.00` per-withdrawal limit · `₱ 15.00` flat withdrawal fee.

5. **Authentic ATM Transaction Flow & Completion Prompt**
   - Account balances are hidden on the main menu so **Balance Inquiry** serves its real-world ATM purpose.
   - Every transaction and screen transition displays a realistic processing spinner (*"Processing Transaction..."*).
   - **"Transaction Completed!" Screen:** Appears **only** after a successful **Withdraw** or **Deposit** (not on Balance Inquiry or Transactions history).
   - **Another Transaction Prompt:** After completing a transaction or viewing Balance Inquiry / Transactions, the ATM asks *"Would you like to perform another transaction?"*:
     - Clicking **Yes** shows a loading spinner and returns to the main ATM options menu.
     - Clicking **No** (or **Exit ATM**) displays *"Thank you for using ExpressBank ATM! Please take your card. Returning to login screen..."* and returns to the login page.

6. **Visual Design, Typography & Expanded Modal**
   - **Light Blue & White Glassmorphism:** Translucent frosted-glass cards (`backdrop-filter: blur(22px)`), soft sky-blue radial gradients, and crisp borders.
   - **Poppins Bold Font Across the Entire System:** Uses `Poppins` (`font-weight: 700`) globally across all headings, labels, inputs, keypad buttons, and tables.
   - **Expanded Transactions Modal:** Dynamically widens the ATM modal (`max-width: 960px`) when viewing **Transactions** so all 6 table columns (`Reference`, `Type`, `Date & Time`, `Amount`, `Fee`, `Balance`) fit comfortably without wrapping.
   - **Pure SVG Vector Icons:** Uses inline `<svg>` vector graphics throughout the interface with zero emojis.

---

## 3. Setup and Run Instructions

### Option A: Run with Django Development Server
1. **Create and Activate a Virtual Environment (Optional):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```
2. **Install Django:**
   ```bash
   pip install django
   ```
3. **Run the Server (No Database Migrations Required):**
   ```bash
   python manage.py runserver
   ```
4. **Open in Browser:**
   Visit `http://127.0.0.1:8000/` in your browser.

### Option B: Static / GitHub Pages Browser Execution
- Opening `index.html` directly or hosting the repository on **GitHub Pages** executes the exact same Python OOP classes (`Account`, `SavingsAccount`, `CheckingAccount`, `Transaction`, `ATMService`, and `ATMTransactionError`) directly in the browser via Brython alongside `style.css`.

---

## 4. Mandatory Python OOP Requirements Mapping (Part III)

| Mandatory OOP Concept | Python File | Class(es) Involved | Implementation Details |
| :--- | :--- | :--- | :--- |
| **1. Classes and Objects** | `atm_app/oop_models.py` | `Account`, `SavingsAccount`, `CheckingAccount`, `Transaction`, `ATMService` | Five meaningful classes with attributes and methods instantiated and used in login, deposit, withdrawal, balance inquiry, and transaction history workflows. |
| **2. Encapsulation** | `atm_app/oop_models.py` | `Account`, `Transaction` | Internal attributes (`_account_number`, `_holder_name`, `_pin`, `_balance`, `_account_type`, `_transactions`) are protected and accessed via `@property` getters (`account_number`, `masked_account_number`, `holder_name`, `balance`, `account_type`, `transactions`) and validated mutator methods (`deposit()`, `withdraw()`). |
| **3. Inheritance** | `atm_app/oop_models.py` | Parent: `Account`<br>Children: `SavingsAccount`, `CheckingAccount` | `SavingsAccount` and `CheckingAccount` inherit from `Account` (`"is-a"` relationship) via `super().__init__()` and share `deposit()`, `inquire_balance()`, `verify_pin()`, `parse_positive_amount()`, and `_record_transaction()`. |
| **4. Polymorphism** | `atm_app/oop_models.py` | `SavingsAccount`, `CheckingAccount` | Both child classes override `withdraw(raw_amount)` and `get_max_withdrawable()` through a common `Account` interface called by `ATMService.perform_withdrawal()`, producing distinct results based on account type. |
| **5. Exception Handling** | `atm_app/oop_models.py` & `atm_app/views.py` | `ATMTransactionError`, `InvalidAmountError`, `InsufficientFundsError`, `WithdrawalLimitError`, `MaintainingBalanceError` | Custom exception hierarchy catches empty, non-numeric, zero/negative amounts, per-transaction limit violations, maintaining balance violations, and overdrafts while preserving the exact account balance after errors. |

---

## 5. UML Class Diagram

```text
+---------------------------------------------------------------+
|                     ATMTransactionError                       |
|                         (Exception)                           |
+---------------------------------------------------------------+
| + message: str                                                |
+---------------------------------------------------------------+
       ^                 ^                  ^                 ^
       |                 |                  |                 |
InvalidAmountError  InsufficientFundsError  WithdrawalLimitError  MaintainingBalanceError


+---------------------------------------------------------------+
|                           Account                             |
|                        (Parent Class)                         |
+---------------------------------------------------------------+
| - _account_number: str                                        |
| - _holder_name: str                                           |
| - _pin: str                                                   |
| - _balance: float                                             |
| - _account_type: str                                          |
| - _transactions: list[Transaction]                            |
+---------------------------------------------------------------+
| + account_number: str (@property)                             |
| + masked_account_number: str (@property)                      |
| + holder_name: str (@property)                                |
| + balance: float (@property)                                  |
| + account_type: str (@property)                               |
| + transactions: list[Transaction] (@property)                 |
| + verify_pin(input_pin): bool                                 |
| + parse_positive_amount(raw_value, operation_name): float     |
| + deposit(raw_amount): Transaction                            |
| + withdraw(raw_amount): Transaction                           |
| + get_max_withdrawable(): float                               |
| + inquire_balance(): dict                                     |
+---------------------------------------------------------------+
                 ^                             ^
                 | (is-a)                      | (is-a)
+-------------------------------+   +-------------------------------+
|        SavingsAccount         |   |        CheckingAccount        |
|         (Child Class)         |   |         (Child Class)         |
+-------------------------------+   +-------------------------------+
| + MAINTAINING_BALANCE = 500.0 |   | + MAINTAINING_BALANCE = 0.0   |
| + WITHDRAWAL_LIMIT = 20000.0  |   | + WITHDRAWAL_LIMIT = 50000.0  |
| + WITHDRAWAL_FEE = 0.0        |   | + WITHDRAWAL_FEE = 15.0       |
+-------------------------------+   +-------------------------------+
| + withdraw(raw_amount)        |   | + withdraw(raw_amount)        |
| + get_max_withdrawable()      |   | + get_max_withdrawable()      |
+-------------------------------+   +-------------------------------+


+---------------------------------------------------------------+
|                         Transaction                           |
+---------------------------------------------------------------+
| - _transaction_id: str                                        |
| - _tx_type: str                                               |
| - _amount: float                                              |
| - _fee: float                                                 |
| - _balance_after: float                                       |
| - _timestamp: str                                             |
+---------------------------------------------------------------+
| + to_dict(): dict                                             |
| + from_dict(data): Transaction                                |
+---------------------------------------------------------------+


+---------------------------------------------------------------+
|                         ATMService                            |
+---------------------------------------------------------------+
| + accounts: dict                                              |
| + logged_in_card: str                                         |
| + current_account: Account                                    |
+---------------------------------------------------------------+
| + login(raw_acc, raw_pin): Account                            |
| + select_account_type(kind): Account                          |
| + perform_deposit(raw_amount): Transaction                    |
| + perform_withdrawal(raw_amount): Transaction                 |
+---------------------------------------------------------------+
```

---

## 6. Six (6) Documented Test Cases Report (Part VI)

| Case ID | Test Type | Scenario | User Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Normal Operation | Login to `100000248` (Hanz Dalmino), select `Savings Account`, deposit `₱ 2,500.00`, then withdraw `₱ 1,500.00` (Start: `₱ 15,000.00`) | Deposit: `2500`<br>Withdraw: `1500` | Balance updates to `₱ 17,500.00` then `₱ 16,000.00` (`₱ 0.00` fee); displays *"Transaction Completed!"*. | Balance is `₱ 16,000.00`; both transactions logged in history. | **PASS** |
| **TC-02** | Boundary Input | Withdraw exact maximum withdrawable amount (`₱ 14,500.00`) from `Savings Account` (`₱ 15,000.00` balance), leaving exact `₱ 500.00` maintaining balance | Withdraw: `14500` | Withdrawal succeeds; remaining balance is exactly `₱ 500.00`. | Remaining balance is `₱ 500.00`; *"Transaction Completed!"* shown. | **PASS** |
| **TC-03** | Invalid Input | Enter negative or non-numeric amount (`-500` or `abc`) in Deposit/Withdraw or `< 9` digit Account Number (`100248`) on Login | Amount: `-500`<br>Account: `100248` | Raises `InvalidAmountError` / `ATMTransactionError`; balance remains unchanged. | Error banner displayed; balance preserved at `₱ 15,000.00`. | **PASS** |
| **TC-04** | Business Rule | Attempt to withdraw `₱ 14,800.00` from `Savings Account` (`₱ 15,000.00` balance), which would drop balance to `₱ 200.00` (`< ₱ 500.00` maintaining balance) | Withdraw: `14800` | Raises `MaintainingBalanceError`; preserves `₱ 15,000.00` balance. | Rejected with maintaining balance error; balance stays `₱ 15,000.00`. | **PASS** |
| **TC-05** | Polymorphism | Withdraw `₱ 2,000.00` from `SavingsAccount` vs. `₱ 2,000.00` from `CheckingAccount` | Withdraw: `2000` on both account types | `SavingsAccount` deducts `₱ 2,000.00` (`₱ 0.00` fee); `CheckingAccount` deducts `₱ 2,015.00` (`₱ 15.00` fee). | Savings deducts `₱ 2,000.00`; Checking deducts `₱ 2,015.00`. | **PASS** |
| **TC-06** | Exception Handling | Attempt to withdraw `₱ 25,000.00` from `SavingsAccount` (exceeds `₱ 20,000.00` Savings per-withdrawal limit) | Withdraw: `25000` | Raises `WithdrawalLimitError` with descriptive message; balance unchanged. | Rejected with limit error message; balance remains unchanged. | **PASS** |

---

## 7. Known Persistence & Data Reset Limitations (Part IV)

- Per **Part IV (Django Integration and Development Rules)**, a relational database is **not required**.
- Account balances and session transactions are persisted in **Django signed cookie sessions** (`request.session`) and browser **JSON Local Storage** (`expressbank_atm_json_v6`).
- Clearing browser site data/cookies resets all predefined accounts (`100000248` Hanz Dalmino and `200000519` Kristof Badayos) back to their initial starting balances.
