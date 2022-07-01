from django.urls import path
from .views import (
    ClinetProfile,
    upload_client_doc,
    change_visibility,
    DelDoc,
)

urlpatterns = [
    path('', ClinetProfile.as_view(), name="client-profile"),
    path('upload-client-doc/', upload_client_doc, name="upload-client-doc"),
    path('delete-document/<pk>/', DelDoc.as_view(), name='delete-document'),
    path('change-visibility/', change_visibility, name='change-visibility'),

]