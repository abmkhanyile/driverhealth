from django.urls import path
from .views import RequestDriver

urlpatterns = [
    path('<pk>/', RequestDriver.as_view(), name="request-driver"),
]