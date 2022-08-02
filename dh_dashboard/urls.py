from django.urls import path
from .views import (
    DHDashboard,
    PostTraining,
    SelectPackage,
)


urlpatterns = [
    path('', DHDashboard.as_view(), name="dh-dashboard"),
    path('select-package/', SelectPackage.as_view(), name="select-package"),
    path('post-training/<pk>/<int:month>/<int:year>/', PostTraining.as_view(), name="post-training"),
]