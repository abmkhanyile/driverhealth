from django.urls import path
from .views import BookTraining

urlpatterns = [
    path('<pk>/<int:month>/<int:year>/', BookTraining.as_view(), name="book-training")
]