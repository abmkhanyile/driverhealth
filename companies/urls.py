from django.urls import path
from .views import (
    Dashboard,
    CreateJob,
    ClientList,
    PostedJobs,
    JobApplicants,
    CompanyClientProfile,
    RequestsList,
)

urlpatterns = [
    path('company-dashboard/', Dashboard.as_view(), name="company-dashboard"),
    path('create-job/', CreateJob.as_view(), name="create-job"),
    path('client-list/', ClientList.as_view(), name='client-list'),
    path('clientprofile/<pk>/', CompanyClientProfile.as_view(), name='clientprofile'),
    path('posted-jobs/', PostedJobs.as_view(), name='posted-jobs'),
    path('job-applicants/<pk>/', JobApplicants.as_view(), name='job-applicants'),
    path('requests-list', RequestsList.as_view(), name='requests-list'),
]