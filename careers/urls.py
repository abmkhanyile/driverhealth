from django.urls import path
from .views import (
    JobView,
    JobList,
    JobApplicationView,
)

urlpatterns = [
    path('job/<pk>/', JobView.as_view(), name="job"),
    path('jobs-list/', JobList.as_view(), name="jobs-list"),
    path('job-application/<pk>/', JobApplicationView.as_view(), name="job-application"),
]