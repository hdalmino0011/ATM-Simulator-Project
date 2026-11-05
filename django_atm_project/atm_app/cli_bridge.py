#!/usr/bin/env python3
"""
CLI Bridge for executing the real Python OOP ATM Simulator classes (oop_models.py)
and packaging the runnable Django project ZIP archive.
"""

import json
import os
import sys
import zipfile
from pathlib import Path

# Ensure current directory is on sys.path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from atm_app.oop_models import (
    ATMService,
    ATMTransactionError,
    run_documented_test_cases,
)

STATE_FILE = PROJECT_ROOT / ".session_atm_state.json"


def load_service() -> ATMService:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            return ATMService.from_session_data(data)
        except Exception:
            pass
    service = ATMService()
    save_service(service)
    return service


def save_service(service: ATMService) -> None:
    STATE_FILE.write_text(
        json.dumps(service.to_session_data(), indent=2),
        encoding="utf-8",
    )


def build_zip_archive(output_path: Path) -> str:
    """Packages /django_atm_project into a clean, submission-ready ZIP archive."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Exclude cache folders and session temp files per Part VI rules
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "venv", ".venv")]
            for file in files:
                if file.endswith(".pyc") or file.startswith(".session"):
                    continue
                abs_file = Path(root) / file
                rel_path = abs_file.relative_to(PROJECT_ROOT.parent)
                zf.write(abs_file, arcname=str(rel_path))
    return str(output_path)


def build_response(
    service: ATMService,
    feedback=None,
    poly_demo=None,
    inquiry_report=None,
):
    active = service.active_account
    return {
        "python_version": sys.version.split()[0],
        "active_account": active.to_dict(),
        "accounts": [acc.to_dict() for acc in service.accounts],
        "feedback": feedback,
        "poly_demo": poly_demo or ATMService.demonstrate_polymorphism(2000.00),
        "inquiry_report": inquiry_report,
        "test_cases": run_documented_test_cases(),
    }


def main():
    raw_input = sys.stdin.read().strip()
    payload = json.loads(raw_input) if raw_input else {"action": "state"}
    action = payload.get("action", "state")

    service = load_service()
    feedback = None
    poly_demo = None
    inquiry_report = None

    try:
        if action == "deposit":
            tx = service.perform_deposit(payload.get("amount", ""), payload.get("note", ""))
            save_service(service)
            feedback = {
                "status": "success",
                "title": f"Deposit Processed via Account.deposit()",
                "message": (
                    f"Credited PHP {tx.amount:,.2f} to {service.active_account.account_type} "
                    f"({service.active_account.account_number}). "
                    f"New Balance: PHP {tx.balance_after:,.2f}."
                ),
                "error_code": "",
            }

        elif action == "withdraw":
            tx = service.perform_withdrawal(payload.get("amount", ""), payload.get("note", ""))
            save_service(service)
            cls_name = service.active_account.__class__.__name__
            fee_str = f" + PHP {tx.fee:,.2f} checking fee" if tx.fee > 0 else " (PHP 0.00 fee)"
            feedback = {
                "status": "success",
                "title": f"Withdrawal Approved via {cls_name}.withdraw()",
                "message": (
                    f"Dispensed PHP {tx.amount:,.2f}{fee_str} from {service.active_account.account_number}. "
                    f"Remaining Balance: PHP {tx.balance_after:,.2f}."
                ),
                "error_code": "",
            }

        elif action == "inquire":
            inquiry_report = service.active_account.inquire_balance()
            feedback = {
                "status": "info",
                "title": "Balance Inquiry Completed via Account.inquire_balance()",
                "message": (
                    f"Account {inquiry_report['account_number']} ({inquiry_report['account_type']}) "
                    f"current balance is PHP {inquiry_report['current_balance']:,.2f}. "
                    f"Maximum single withdrawal right now is PHP {inquiry_report['withdrawable_balance']:,.2f}."
                ),
                "error_code": "",
            }

        elif action == "switch":
            acc = service.switch_account(payload.get("account_number", ""))
            save_service(service)
            feedback = {
                "status": "info",
                "title": f"Switched to {acc.__class__.__name__} ({acc.account_number})",
                "message": (
                    f"Active account is now {acc.holder_name}'s {acc.account_type} "
                    f"with balance PHP {acc.balance:,.2f}."
                ),
                "error_code": "",
            }

        elif action == "create":
            new_acc = service.create_custom_account(
                payload.get("holder_name", ""),
                payload.get("account_kind", "savings"),
                payload.get("starting_balance", ""),
            )
            save_service(service)
            feedback = {
                "status": "success",
                "title": f"Created New {new_acc.__class__.__name__} Object",
                "message": (
                    f"Instantiated {new_acc.account_type} ({new_acc.account_number}) for "
                    f"{new_acc.holder_name} with starting balance PHP {new_acc.balance:,.2f}."
                ),
                "error_code": "",
            }

        elif action == "polymorphism":
            poly_demo = ATMService.demonstrate_polymorphism(
                payload.get("test_amount", 2000.00),
                payload.get("sample_balance", 10000.00),
            )
            feedback = {
                "status": "info",
                "title": "Polymorphism Verification Executed in Python",
                "message": (
                    f"Ran overridden withdraw(PHP {poly_demo['requested_amount']:,.2f}) on both "
                    f"SavingsAccount and CheckingAccount starting from PHP {poly_demo['sample_starting_balance']:,.2f}."
                ),
                "error_code": "",
            }

        elif action == "reset":
            service = ATMService()
            save_service(service)
            feedback = {
                "status": "info",
                "title": "Session State Reset",
                "message": "Restored all predefined fictional accounts and balances to their initial state.",
                "error_code": "",
            }

        elif action == "build_zip":
            zip_target = Path(payload.get("output_path", "/app/applet/public/CTU_PELEC1_ATM_Simulator_Django.zip"))
            built_path = build_zip_archive(zip_target)
            print(json.dumps({"ok": True, "zip_path": built_path}))
            return

    except ATMTransactionError as exc:
        feedback = {
            "status": "error",
            "title": f"Operation Rejected by {exc.__class__.__name__}",
            "message": exc.message,
            "error_code": exc.error_code,
        }

    print(json.dumps(build_response(service, feedback, poly_demo, inquiry_report)))


if __name__ == "__main__":
    main()
