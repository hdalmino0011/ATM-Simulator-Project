from django.urls import path, include

urlpatterns = [
    path("", include("atm_app.urls")),
]
