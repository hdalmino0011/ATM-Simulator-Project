"""
Django Views for the CTU Express ATM Simulator (P ELEC 1 Final Project).
All business calculations, validations, polymorphism, and exception handling
are delegated to the Python OOP classes in atm_app/oop_models.py.
"""

from django.shortcuts import render, redirect
from .oop_models import (
    ATMService,
    ATMTransactionError,
    run_documented_test_cases,
)

SESSION_KEY = "ctu_atm_simulator_state"
FLASH_KEY = "ctu_atm_flash_feedback"
POLY_KEY = "ctu_atm_poly_demo"
INQUIRY_KEY = "ctu_atm_inquiry_report"


def _load_service(request) -> ATMService:
    """Reconstructs the ATMService object graph from the Django session."""
    raw_state = request.session.get(SESSION_KEY)
    return ATMService.from_session_data(raw_state)


def _save_service(request, service: ATMService) -> None:
    """Persists the ATMService object graph back into the Django session."""
    request.session[SESSION_KEY] = service.to_session_data()
    request.session.modified = True


def _set_feedback(request, status: str, title: str, message: str, error_code: str = "") -> None:
    """Stores a one-time status banner message in the session for the next template render."""
    request.session[FLASH_KEY] = {
        "status": status,  # "success" | "error" | "info"
        "title": title,
        "message": message,
        "error_code": error_code,
    }


def atm_dashboard(request):
    """
    Main ATM Simulator view.
    Renders the active Account (SavingsAccount or CheckingAccount),
    balance, withdrawal rules, session transaction history, and OOP test report.
    """
    service = _load_service(request)
    _save_service(request, service)

    active_account = service.active_account
    feedback = request.session.pop(FLASH_KEY, None)
    poly_demo = request.session.get(POLY_KEY) or ATMService.demonstrate_polymorphism(2000.00)
    inquiry_report = request.session.pop(INQUIRY_KEY, None)
    active_tab = request.GET.get("tab", "atm")

    context = {
        "active_account": active_account.to_dict(),
        "accounts": [acc.to_dict() for acc in service.accounts],
        "feedback": feedback,
        "poly_demo": poly_demo,
        "inquiry_report": inquiry_report,
        "test_cases": run_documented_test_cases(),
        "active_tab": active_tab,
    }
    return render(request, "atm/index.html", context)


def deposit_view(request):
    """Processes an HTML form POST deposit using Account.deposit()."""
    if request.method == "POST":
        service = _load_service(request)
        raw_amount = request.POST.get("amount", "")
        note = request.POST.get("note", "").strip()
        try:
            tx = service.perform_deposit(raw_amount, note=note)
            _save_service(request, service)
            _set_feedback(
                request,
                status="success",
                title="Deposit Processed Successfully",
                message=(
                    f"Deposited PHP {tx.amount:,.2f} into {service.active_account.account_type} "
                    f"({service.active_account.account_number}). "
                    f"Updated Balance: PHP {tx.balance_after:,.2f}."
                ),
            )
        except ATMTransactionError as exc:
            _set_feedback(
                request,
                status="error",
                title=f"Deposit Rejected ({exc.__class__.__name__})",
                message=exc.message,
                error_code=exc.error_code,
            )
    return redirect("atm_dashboard")


def withdraw_view(request):
    """
    Processes an HTML form POST withdrawal using the polymorphic Account.withdraw() method.
    Calls SavingsAccount.withdraw() or CheckingAccount.withdraw() based on active account type.
    """
    if request.method == "POST":
        service = _load_service(request)
        raw_amount = request.POST.get("amount", "")
        note = request.POST.get("note", "").strip()
        try:
            tx = service.perform_withdrawal(raw_amount, note=note)
            _save_service(request, service)
            fee_text = f" (plus PHP {tx.fee:,.2f} checking fee)" if tx.fee > 0 else " (PHP 0.00 fee)"
            _set_feedback(
                request,
                status="success",
                title=f"Withdrawal Approved via {service.active_account.__class__.__name__}.withdraw()",
                message=(
                    f"Dispensed PHP {tx.amount:,.2f}{fee_text} from {service.active_account.account_number}. "
                    f"Remaining Balance: PHP {tx.balance_after:,.2f}."
                ),
            )
        except ATMTransactionError as exc:
            _set_feedback(
                request,
                status="error",
                title=f"Withdrawal Rejected ({exc.__class__.__name__})",
                message=exc.message,
                error_code=exc.error_code,
            )
    return redirect("atm_dashboard")


def balance_inquiry_view(request):
    """Executes an explicit Balance Inquiry using Account.inquire_balance()."""
    if request.method == "POST":
        service = _load_service(request)
        report = service.active_account.inquire_balance()
        request.session[INQUIRY_KEY] = report
        _set_feedback(
            request,
            status="info",
            title="Balance Inquiry Statement Generated",
            message=(
                f"Account {report['account_number']} ({report['account_type']}) has an available balance "
                f"of PHP {report['current_balance']:,.2f} and max single withdrawal of "
                f"PHP {report['withdrawable_balance']:,.2f}."
            ),
        )
    return redirect("atm_dashboard")


def switch_account_view(request):
    """Switches between predefined or custom fictional accounts in the active session."""
    if request.method == "POST":
        service = _load_service(request)
        account_number = request.POST.get("account_number", "")
        try:
            acc = service.switch_account(account_number)
            _save_service(request, service)
            _set_feedback(
                request,
                status="info",
                title="Active Account Switched",
                message=(
                    f"Now operating on {acc.holder_name}'s {acc.account_type} ({acc.account_number}) "
                    f"using Python class {acc.__class__.__name__}."
                ),
            )
        except ATMTransactionError as exc:
            _set_feedback(
                request,
                status="error",
                title="Account Switch Error",
                message=exc.message,
                error_code=exc.error_code,
            )
    return redirect("atm_dashboard")


def create_account_view(request):
    """Creates a new fictional SavingsAccount or CheckingAccount during the session."""
    if request.method == "POST":
        service = _load_service(request)
        holder_name = request.POST.get("holder_name", "")
        account_kind = request.POST.get("account_kind", "savings")
        starting_balance = request.POST.get("starting_balance", "")
        try:
            new_acc = service.create_custom_account(holder_name, account_kind, starting_balance)
            _save_service(request, service)
            _set_feedback(
                request,
                status="success",
                title=f"New {new_acc.__class__.__name__} Instantiated",
                message=(
                    f"Created {new_acc.account_type} ({new_acc.account_number}) for {new_acc.holder_name} "
                    f"with starting balance PHP {new_acc.balance:,.2f}."
                ),
            )
        except ATMTransactionError as exc:
            _set_feedback(
                request,
                status="error",
                title=f"Account Creation Failed ({exc.__class__.__name__})",
                message=exc.message,
                error_code=exc.error_code,
            )
    return redirect("atm_dashboard")


def polymorphism_demo_view(request):
    """Runs the side-by-side polymorphic withdraw() comparison on SavingsAccount vs CheckingAccount."""
    if request.method == "POST":
        raw_amount = request.POST.get("test_amount", "2000")
        try:
            demo_result = ATMService.demonstrate_polymorphism(raw_amount)
            request.session[POLY_KEY] = demo_result
            _set_feedback(
                request,
                status="info",
                title="Polymorphism Comparison Executed",
                message=(
                    f"Tested overridden withdraw(PHP {demo_result['requested_amount']:,.2f}) on both "
                    f"SavingsAccount and CheckingAccount starting from PHP 10,000.00."
                ),
            )
        except ATMTransactionError as exc:
            _set_feedback(
                request,
                status="error",
                title=f"Polymorphism Test Invalid Input ({exc.__class__.__name__})",
                message=exc.message,
                error_code=exc.error_code,
            )
    return redirect("atm_dashboard")


def reset_session_view(request):
    """Resets the session back to the initial predefined accounts and balances."""
    if request.method == "POST":
        fresh_service = ATMService()
        _save_service(request, fresh_service)
        request.session.pop(POLY_KEY, None)
        request.session.pop(INQUIRY_KEY, None)
        _set_feedback(
            request,
            status="info",
            title="Session Reset Complete",
            message="All fictional accounts and session transactions have been restored to initial defaults.",
        )
    return redirect("atm_dashboard")
