from django.urls import path
from .views import (
    Dashboard,
    CreateJob,
    ClientList,
)

urlpatterns = [
    path('company-dashboard/', Dashboard.as_view(), name="company-dashboard"),
    path('create-job/', CreateJob.as_view(), name="create-job"),
    path('client-list/', ClientList.as_view(), name='client-list'),
]