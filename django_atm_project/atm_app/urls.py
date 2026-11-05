"""
URL routes for the CTU Express ATM Simulator Django App (atm_app).
Connects browser form submissions to the OOP-backed Django views.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.atm_dashboard, name="atm_dashboard"),
    path("deposit/", views.deposit_view, name="deposit"),
    path("withdraw/", views.withdraw_view, name="withdraw"),
    path("inquire/", views.balance_inquiry_view, name="balance_inquiry"),
    path("switch-account/", views.switch_account_view, name="switch_account"),
    path("create-account/", views.create_account_view, name="create_account"),
    path("polymorphism-demo/", views.polymorphism_demo_view, name="polymorphism_demo"),
    path("reset-session/", views.reset_session_view, name="reset_session"),
]
