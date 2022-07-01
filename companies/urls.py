from django.urls import path
from .views import Dashboard

urlpatterns = [
    path('company-dashboard/', Dashboard.as_view(), name="company-dashboard")
]