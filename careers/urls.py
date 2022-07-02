from django.urls import path
from .views import (
    JobView,
    JobList,
)

urlpatterns = [
    path('job/<pk>/', JobView.as_view(), name="job"),
    path('jobs-list/', JobList.as_view(), name="jobs-list"),
]