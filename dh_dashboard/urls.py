from django.urls import path
from training_courses.models import TrainingCourse
from .views import (
    DHDashboard,
    PostTraining,
    SelectPackage,
    DriverList,
    DProfile,
    AddRemark,
    RequestedDrivers,
    DriverReq,
    AcceptRequest,
    RejectRequest,
    skip_steps2_condition,
    skip_steps3_condition,
    skip_steps4_condition,
    skip_steps5_condition,
    skip_steps6_condition,
    skip_steps7_condition,
    PostTraingSession,
    TrainingPostSuccess,
)

urlpatterns = [
    path('', DHDashboard.as_view(), name="dh-dashboard"),
    path('select-package/', SelectPackage.as_view(), name="select-package"),
    path('driverlist/', DriverList.as_view(), name="driverlist"),
    path('driverprofile/<pk>/', DProfile.as_view(), name="driverprofile"),
    path('addremark/<pk>/', AddRemark.as_view(), name="addremark"),
    path('post-training/<pk>/<int:month>/<int:year>/', PostTraining.as_view(), name="post-training"),
    path('requested-drivers/', RequestedDrivers.as_view(), name="requested-drivers"),
    path('driver-req/<pk>/', DriverReq.as_view(), name="driver-req"),
    path('accept-req/<pk>/', AcceptRequest.as_view(), name="accept-req"),
    path('reject-req/<pk>/', RejectRequest.as_view(), name="reject-req"),
    path('post-training/', PostTraingSession.as_view(condition_dict={'0': True, '1': skip_steps2_condition, '2': skip_steps3_condition, '3': skip_steps4_condition, '4': skip_steps5_condition, '5': skip_steps6_condition, '6': skip_steps7_condition}), name="post-training"),
    path('training-post-success/', TrainingPostSuccess.as_view(), name="training-post-success")

]