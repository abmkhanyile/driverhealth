from django.urls import path
from .views import (
    ClinetProfile,
    upload_client_doc,
    change_visibility,
    DelDoc,
    UplaodProfileImg,
    EditClient,
    EditWorkExp,
    JobApplications,
)

urlpatterns = [
    path('', ClinetProfile.as_view(), name="client-profile"),
    path('upload-client-doc/', upload_client_doc, name="upload-client-doc"),
    path('delete-document/<pk>/', DelDoc.as_view(), name='delete-document'),
    path('change-visibility/', change_visibility, name='change-visibility'),
    path('upload-image/', UplaodProfileImg.as_view(), name='upload-image'),
    path('edit-client/', EditClient.as_view(), name='edit-client'),
    path('edit-workexp/<pk>/', EditWorkExp.as_view(), name='edit-workexp'),
    path('job-applications/', JobApplications.as_view(), name='job-applications'),

]