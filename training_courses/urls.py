from django.urls import path
from .views import BookTraining, BookingSuccess, GetTimes

urlpatterns = [
    path('<pk>/<int:month>/<int:year>/', BookTraining.as_view(), name="book-training"),
    path('booking-success/<pk>/', BookingSuccess.as_view(), name="booking-success"),
    path('get-times/', GetTimes.as_view(), name="get-times"),
]