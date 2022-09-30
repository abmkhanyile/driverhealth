from django.urls import path
from .views import BookTraining, BookingSuccess, GetTimes, Booking, ElearningCourses, ElearningEnquiry

urlpatterns = [
    path('<pk>/<int:month>/<int:year>/', BookTraining.as_view(), name="book-training"),
    path('booking-success/<pk>/', BookingSuccess.as_view(), name="booking-success"),
    path('get-times/', GetTimes.as_view(), name="get-times"),
    path('booking/<pk>/<str:date>/', Booking.as_view(), name="booking"),
    path('elearning-courses', ElearningCourses.as_view(), name="elearning-courses"),
    path('elearning-enquiry/<int:course_id>/', ElearningEnquiry.as_view(), name="elearning-enquiry"),
]