from django.urls import path
from .views import (
    BookTraining, 
    BookingSuccess, 
    GetTimes, 
    Booking, 
    ElearningCourses, 
    ElearningEnquiry, 
    Courses,
    HourlyCourses,
    HourlySimulatorCourses,
    MultidayCourses,
    Code14Courses,
)

urlpatterns = [
    path('<pk>/<int:month>/<int:year>/', BookTraining.as_view(), name="book-training"),
    path('booking-success/<pk>/', BookingSuccess.as_view(), name="booking-success"),
    path('get-times/', GetTimes.as_view(), name="get-times"),
    path('booking/<pk>/<str:date>/', Booking.as_view(), name="booking"),
    path('elearning-courses', ElearningCourses.as_view(), name="elearning-courses"),
    path('elearning-enquiry/<int:course_id>/', ElearningEnquiry.as_view(), name="elearning-enquiry"),
    path('', Courses.as_view(), name="courses"),
    path('hourly-courses/', HourlyCourses.as_view(), name="hourly-courses"),
    path('hourly-simulator-courses/', HourlySimulatorCourses.as_view(), name="hourly-simulator-courses"),
    path('multiday-courses/', MultidayCourses.as_view(), name="multiday-courses"),
    path('code14-courses/', Code14Courses.as_view(), name="code14-courses"),
]