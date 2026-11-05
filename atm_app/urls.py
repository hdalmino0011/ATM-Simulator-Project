from django.urls import path
from . import views

urlpatterns = [
    path("", views.atm_dashboard, name="atm_dashboard"),
    path("login/", views.login_view, name="login"),
    path("select-account/", views.select_account_view, name="select_account"),
    path("deposit/", views.deposit_view, name="deposit"),
    path("withdraw/", views.withdraw_view, name="withdraw"),
    path("inquire/", views.balance_inquiry_view, name="balance_inquiry"),
]
