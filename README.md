# ExpressBank ATM Simulator — Python & Django OOP Final Project

**Course:** P ELEC 1 - Object-Oriented Programming (Python and Django)  
**Institution:** Cebu Technological University — Main Campus (CCICT)  
**Approved Project Option:** Option C — ATM Simulator  
**Languages & Technologies Used:** Strictly **Python, HTML, and CSS** (Django backend + Brython browser OOP runtime, zero code comments, pure inline SVG vector icons)

---

## 1. Group Members & Contribution Record (5 Members)

| Member Name | Assigned Role | Completed OOP, Django & UI Responsibilities |
| :--- | :--- | :--- |
| **April Dianne Calvo** | Project Lead & Documentation Specialist | Led project planning, system workflow alignment with Part III & Part IV rules, UML class diagramming, and documentation of test cases. |
| **Hanz Dee Dalmino** | Lead Python OOP Architect | Designed the `Account` parent class, encapsulation `@property` getters (`masked_account_number`, `balance`, `transactions`), strict `verify_pin()` enforcement, and custom exception hierarchy (`ATMTransactionError`). |
| **Diana Sismar** | Inheritance & Polymorphism Developer | Implemented the `SavingsAccount` and `CheckingAccount` child classes and overridden `withdraw()` and `get_max_withdrawable()` methods enforcing maintaining balances, limits, and fees. |
| **Kristof Glendale Badayos** | Django Views, Routing & Session Engineer | Built `ATMService`, `Transaction` class, local vs. international fee computation, `atm_app/views.py`, `atm_app/urls.py`, multi-account strict credential verification, and session/local state serialization. |
| **Steve Niño Larino** | Frontend UI/UX (HTML & CSS) & QA Tester | Designed the Realistic Metallic Black ATM kiosk casing paired with the White & Light-Blue display UI (`style.css` and `index.html`), single-viewport scaling, welcome carousel, physical card/receipt hardware deck, and SVG vector icons. |

---

## 2. About the System & Summary of System Updates

The **ExpressBank ATM Simulator** is a realistic, single-viewport kiosk Automated Teller Machine simulation built strictly with **Python, HTML, and CSS** following **Option C (ATM Simulator)** of the P ELEC 1 Final Project Instructional Guide.

### Key System Features & Updates

1. **Kiosk Visual Design & Single-Viewport Layout**
   - **Realistic Metallic Black ATM Machine:** Deep dark metallic gradient casing (`linear-gradient(145deg, #1a1a1a, #0d0d0d, #262626)`), recessed screen bezel, and physical bottom hardware modules.
   - **White & Light-Blue Inner Screen UI:** Crisp white (`#ffffff`) and sky-blue (`#f0f9ff`, `#e0f2fe`, `#0284c7`) inner ATM interface and card selector drawer for clear legibility.
   - **No-Scroll Viewport Fit:** Responsive `clamp()` heights and compact hardware spacing keep the top terminal fascia, ATM monitor, and bottom hardware controls (`CLAIM RECEIPT`, `Select Card`, `ENTER CARD HERE`) visible at once without vertical scrolling.

2. **Dynamic Welcome Screen & Hardware Deck Controls**
   - **Welcome Carousel:** Displays *"Welcome to ExpressBank ATM"* over a 5-second automatic sliding banner (*"Fast, Secure, and Reliable Transactions"*, *"24/7 Access to Your Funds"*, *"International Card Accepted Here"*, *"Your Security is Our Priority"*).
   - **Bottom-Right (`ENTER CARD HERE`):** Triggers card insertion / chip reading and transitions to the **Card Detected** PIN screen.
   - **Bottom-Center (`Select Card`):** Opens a 4-card visual drawer showing distinct debit, premium credit, international travel, and classic ATM cards.
   - **Bottom-Left (`CLAIM RECEIPT`):** Remains disabled (`"No Transaction"`) until a user chooses **Yes** at the receipt prompt. Once clicked, it displays the formatted transaction slip **once** and immediately resets back to disabled (`"No Transaction"`).

3. **Card Information Visibility & Last-4-Digit Privacy Masking**
   - **Before Login (`Select Card` Drawer):** Full card numbers and account numbers are visible so users can inspect and choose a card.
   - **Card Detected & Logged-In Dashboard:** Card PANs and account numbers are covered/masked to show **only the last 4 digits** (`**** **** **** 0248`, `*****0248`) along with masked cardholder initials before PIN entry, and remain masked throughout the logged-in header, Balance Inquiry, hardware slot status, receipts, and any post-login card view.

4. **Strict Assigned PIN Authentication (4-Digit & 6-Digit Accounts)**
   - PIN fields use a clean **`Enter PIN here`** placeholder with **no example PINs** displayed anywhere in the UI.
   - Each cardholder account has a **unique assigned PIN** (some 6-digit, some 4-digit).
   - `Account.verify_pin()` and `ATMService.login()` strictly require an exact digit-for-digit match on the account's assigned PIN — any wrong, shorter, longer, whitespace-padded, or non-numeric PIN is strictly rejected.
   - Manual submission only via **Enter** key or clicking **Enter ATM**.

5. **Predefined Cardholder Accounts & Assigned PINs**

   | Card / Network | Cardholder | Type & BIN | Account Number | Assigned PIN | Savings Start | Checking Start | Local / Intl Withdrawal Fee Rule |
   | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
   | **ExpressBank Everyday Debit** | Hanz Dalmino | Local · BancNet (`421900`) | `100000248` (`*****0248`) | `248159` *(6 digits)* | `₱ 15,000.00` | `₱ 25,000.00` | `₱ 0.00` Local Bank Fee |
   | **MetroGold Premier Credit** | Kristof Badayos | Local · Mastercard (`542810`) | `200000519` (`*****0519`) | `5194` *(4 digits)* | `₱ 20,000.00` | `₱ 35,000.00` | `₱ 18.00` Local Interbank Fee |
   | **GlobalPass Platinum Travel** | April Dianne Calvo | International · Visa (`453288`) | `300000814` (`*****0814`) | `814620` *(6 digits)* | `₱ 45,000.00` | `₱ 60,000.00` | `max($3.50, 1.75%)` + `3.00%` FX Fee |
   | **CitiReach Classic Global ATM** | Diana Sismar | International · Plus/Cirrus (`529104`) | `400000932` (`*****0932`) | `9327` *(4 digits)* | `₱ 30,000.00` | `₱ 40,000.00` | `max($3.50, 1.75%)` + `3.00%` FX Fee |

6. **Account Types, Fee Breakdown & Receipt Prompt Flow**
   - Every operation prompts for **Account Type**:
     - **Savings Account:** `₱ 500.00` maintaining balance · `₱ 20,000.00` max withdrawal limit · `₱ 0.00` account fee.
     - **Checking Account:** `₱ 0.00` maintaining balance · `₱ 50,000.00` max withdrawal limit · `₱ 15.00` account fee.
   - Cash withdrawals display a live fee preview (account fee + local bank fee or international withdrawal + 3% FX conversion fee) and ask **"Do you want a receipt?"** (`Yes` / `No`) before finalizing.
   - Strictly rejects empty, non-numeric (`abc`, `nan`, `inf`), zero/negative amounts, limit violations, maintaining balance violations, and overdrafts while preserving the exact balance.

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
- Hosting the `main` branch on **GitHub Pages** (`https://hdalmino0011.github.io/ATM-Simulator-Project/`) executes the exact same Python OOP classes (`Account`, `SavingsAccount`, `CheckingAccount`, `Transaction`, `ATMService`, and `ATMTransactionError`) directly in the browser via Brython using `index.html` and `style.css`.

---

## 4. Mandatory Python OOP Requirements Mapping (Part III)

| Mandatory OOP Concept | Python File | Class(es) Involved | Implementation Details |
| :--- | :--- | :--- | :--- |
| **1. Classes and Objects** | `atm_app/oop_models.py` | `Account`, `SavingsAccount`, `CheckingAccount`, `Transaction`, `ATMService` | Five meaningful classes with attributes and methods instantiated and used in authentication, deposit, withdrawal, fee calculation, balance inquiry, and transaction history workflows. |
| **2. Encapsulation** | `atm_app/oop_models.py` | `Account`, `Transaction` | Internal attributes (`_account_number`, `_holder_name`, `_pin`, `_balance`, `_account_type`, `_transactions`) are protected and accessed via `@property` getters (`account_number`, `masked_account_number`, `holder_name`, `balance`, `account_type`, `transactions`) and validated mutators (`deposit()`, `withdraw()`, `verify_pin()`). |
| **3. Inheritance** | `atm_app/oop_models.py` | Parent: `Account`<br>Children: `SavingsAccount`, `CheckingAccount` | `SavingsAccount` and `CheckingAccount` inherit from `Account` (`"is-a"` relationship) via `super().__init__()` and share `deposit()`, `inquire_balance()`, `verify_pin()`, `parse_positive_amount()`, and `_record_transaction()`. |
| **4. Polymorphism** | `atm_app/oop_models.py` | `SavingsAccount`, `CheckingAccount` | Both child classes override `withdraw(raw_amount, extra_fee=0.0)` and `get_max_withdrawable()` through a common `Account` interface invoked by `ATMService.perform_withdrawal()`, producing distinct rules and balances based on account tier. |
| **5. Exception Handling** | `atm_app/oop_models.py` & `atm_app/views.py` | `ATMTransactionError`, `InvalidAmountError`, `InsufficientFundsError`, `WithdrawalLimitError`, `MaintainingBalanceError` | Custom exception hierarchy catches invalid PINs, empty/non-numeric/zero/negative amounts, per-transaction limit violations, maintaining balance violations, and overdrafts while preserving the exact account balance after errors. |

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
| + withdraw(raw_amount, extra_fee=0.0): Transaction            |
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
| + withdraw(raw_amount, fee)   |   | + withdraw(raw_amount, fee)   |
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
| + selected_card_id: str                                       |
| + current_account: Account                                    |
+---------------------------------------------------------------+
| + login(raw_acc, raw_pin, card_id=None): Account              |
| + select_account_type(kind): Account                          |
| + compute_network_fees(amount, card_id=None): dict            |
| + perform_deposit(raw_amount): Transaction                    |
| + perform_withdrawal(raw_amount): Transaction                 |
+---------------------------------------------------------------+
```

---

## 6. Six (6) Documented Test Cases Report (Part VI)

| Case ID | Test Type | Scenario | User Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Normal Operation & One-Time Receipt | Login to `100000248` (`248159`), select `Savings Account`, deposit `₱ 2,500.00`, withdraw `₱ 1,500.00` with Receipt = `Yes`, then click `CLAIM RECEIPT` | Deposit: `2500`<br>Withdraw: `1500`<br>Receipt: `Yes` | Balance updates to `₱ 16,000.00` (`₱ 0.00` fee); `CLAIM RECEIPT` opens receipt once and immediately resets to disabled `"No Transaction"`. | Balance is `₱ 16,000.00`; receipt dispenses once and button disables. | **PASS** |
| **TC-02** | Strict PIN Length & Value | Attempt login to 6-digit PIN account `100000248` (`248159`) with 4 digits (`2481`) or 7 digits (`2481590`), and 4-digit PIN account `200000519` (`5194`) with `519` or `519400` | Shorter, longer, or cross-account PINs | `verify_pin()` & `login()` strictly reject login with error message; only exact assigned PIN succeeds. | All shorter, longer, and mismatched PINs rejected; exact assigned PINs logged in. | **PASS** |
| **TC-03** | Invalid Amount & Non-Numeric Input | Enter `-500`, `0`, `abc`, `nan`, or `inf` in Deposit/Withdraw | Amount: `-500`, `abc`, `nan` | Raises `InvalidAmountError`; balance remains unchanged. | Error banner displayed; balance preserved. | **PASS** |
| **TC-04** | Business Rule (Maintaining Balance) | Attempt to withdraw `₱ 14,800.00` from `Savings Account` (`₱ 15,000.00` balance), dropping below `₱ 500.00` | Withdraw: `14800` | Raises `MaintainingBalanceError`; preserves `₱ 15,000.00` balance. | Rejected with maintaining balance error; balance stays `₱ 15,000.00`. | **PASS** |
| **TC-05** | Polymorphism & Local vs. Intl Fees | Withdraw `₱ 2,000.00` on `SavingsAccount` vs. `CheckingAccount` (Local `100000248` vs. International `300000814`) | Withdraw: `2000` | Local Savings deducts `₱ 2,000.00`; Local Checking deducts `₱ 2,015.00`; Intl Savings adds `₱ 203.00` (`$3.50`) + `₱ 60.00` (`3%` FX) = `₱ 2,263.00`. | Fee calculations and deductions match exact account & card tier rules. | **PASS** |
| **TC-06** | Exception Handling (Limit & Overdraft) | Attempt to withdraw `₱ 25,000.00` from `SavingsAccount` (exceeds `₱ 20,000.00` limit) | Withdraw: `25000` | Raises `WithdrawalLimitError`; balance remains unchanged. | Rejected with limit error message; balance remains unchanged. | **PASS** |

---

## 7. Known Persistence & Data Reset Limitations (Part IV)

- Per **Part IV (Django Integration and Development Rules)**, a relational database is **not required**.
- Account balances and session transactions are persisted in **Django signed cookie sessions** (`request.session`) and browser **JSON Local Storage** (`expressbank_kiosk_atm_v8`).
- Clearing browser site data/cookies resets all four predefined accounts (`100000248`, `200000519`, `300000814`, and `400000932`) back to their initial starting balances and PINs.
