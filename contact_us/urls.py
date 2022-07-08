from django.urls import path
from .views import ContactUs

urlpatterns = [
    path('', ContactUs.as_view(), name="contact-us"),
]