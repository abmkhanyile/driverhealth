from unicodedata import name
from django.urls import path, re_path
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView,
                                       PasswordResetDoneView)
from .views import (
    CompanyRegistration,
    login,
    auth_view,
    logout_view,
    logout_success_view,
    password_change_view,
    UserType,
    Register,
    registration_success_view,
)

urlpatterns = [
    path('login/', login, name="login"),
    path('auth/', auth_view, name='auth'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'), 

    re_path(r'^auth/$', auth_view, name='auth'),
    re_path(r'^login/$', login, name='login'),
    re_path(r'^logout/$', logout_view, name='logout'),
    re_path(r'^logout_success/$', logout_success_view, name='logout_success'),
    re_path(r'^password_change/$', password_change_view, name='password_change'),
    re_path(r'^password_reset/$', PasswordResetView.as_view(template_name='authentication/password_reset_form.html'), name='password_reset'),

    path('pre-registration/', UserType.as_view(), name="pre-registration"),
    path('register/', Register.as_view(), name="register"),
    path('registration-success/', registration_success_view, name="registration-success"),
    path('company-registration/', CompanyRegistration.as_view(), name="company-registration"),
]