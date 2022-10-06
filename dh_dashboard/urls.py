from django.urls import path
from .views import (
    DHDashboard,
    PostTraining,
    SelectPackage,
    DriverList,
    DProfile,
    AddRemark,
)


urlpatterns = [
    path('', DHDashboard.as_view(), name="dh-dashboard"),
    path('select-package/', SelectPackage.as_view(), name="select-package"),
    path('driverlist/', DriverList.as_view(), name="driverlist"),
    path('driverprofile/<pk>/', DProfile.as_view(), name="driverprofile"),
    path('addremark/<pk>/', AddRemark.as_view(), name="addremark"),
    path('post-training/<pk>/<int:month>/<int:year>/', PostTraining.as_view(), name="post-training"),
]