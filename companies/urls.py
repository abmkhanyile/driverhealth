from django.urls import path
from .views import (
    Dashboard,
    CreateJob,
    ClientList,
    PostedJobs,
    JobApplicants,
)

urlpatterns = [
    path('company-dashboard/', Dashboard.as_view(), name="company-dashboard"),
    path('create-job/', CreateJob.as_view(), name="create-job"),
    path('client-list/', ClientList.as_view(), name='client-list'),
    path('posted-jobs/', PostedJobs.as_view(), name='posted-jobs'),
    path('job-applicants/<pk>/', JobApplicants.as_view(), name='job-applicants'),
]