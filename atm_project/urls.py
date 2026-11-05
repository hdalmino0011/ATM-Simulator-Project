"""Root URL configuration for atm_project."""
from django.urls import path, include

urlpatterns = [
    path("", include("atm_app.urls")),
]
