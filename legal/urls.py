from django.urls import path
from .views import (
    TermsAndConditions,
    TermsOfService,
    PrivacyPolicy,
    CookiePolicy,
)


urlpatterns = [
    path('ts-and-cs/', TermsAndConditions.as_view(), name="ts-and-cs"),
    path('terms-of-service/', TermsOfService.as_view(), name="terms-of-service"),
    path('privacy-policy/', PrivacyPolicy.as_view(), name="privacy-policy"),
    path('cookie-policy/', CookiePolicy.as_view(), name="cookie-policy"),
]