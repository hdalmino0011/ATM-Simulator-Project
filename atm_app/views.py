from django.shortcuts import render, redirect
from .oop_models import ATMService, ATMTransactionError

SESSION_KEY = "expressbank_atm_session"


def _load_service(request):
    raw_state = request.session.get(SESSION_KEY)
    return ATMService.from_session_data(raw_state)


def _save_service(request, service):
    request.session[SESSION_KEY] = service.to_session_data()
    request.session.modified = True


def atm_dashboard(request):
    service = _load_service(request)
    _save_service(request, service)
    context = {
        "active_account": service.current_account.to_dict(),
        "inquiry": service.current_account.inquire_balance(),
    }
    return render(request, "atm/index.html", context)


def login_view(request):
    if request.method == "POST":
        service = _load_service(request)
        acc_num = request.POST.get("account_number", "")
        pin_code = request.POST.get("pin_code", "")
        try:
            service.login(acc_num, pin_code)
            _save_service(request, service)
        except ATMTransactionError as exc:
            request.session["login_error"] = exc.message
    return redirect("atm_dashboard")


def select_account_view(request):
    if request.method == "POST":
        service = _load_service(request)
        account_kind = request.POST.get("account_type", "savings")
        service.select_account_type(account_kind)
        _save_service(request, service)
    return redirect("atm_dashboard")


def deposit_view(request):
    if request.method == "POST":
        service = _load_service(request)
        raw_amount = request.POST.get("amount", "")
        try:
            service.perform_deposit(raw_amount)
            _save_service(request, service)
        except ATMTransactionError as exc:
            request.session["transaction_error"] = exc.message
    return redirect("atm_dashboard")


def withdraw_view(request):
    if request.method == "POST":
        service = _load_service(request)
        raw_amount = request.POST.get("amount", "")
        try:
            service.perform_withdrawal(raw_amount)
            _save_service(request, service)
        except ATMTransactionError as exc:
            request.session["transaction_error"] = exc.message
    return redirect("atm_dashboard")


def balance_inquiry_view(request):
    service = _load_service(request)
    request.session["inquiry"] = service.current_account.inquire_balance()
    return redirect("atm_dashboard")
