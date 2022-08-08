from django.contrib import admin
from .models import TrainingCourse, Code14Course, TrainingEvent, Course_Enrollees, TrainingDays, TrainingBooking

admin.site.register(TrainingCourse)
admin.site.register(Code14Course)
admin.site.register(Course_Enrollees)
admin.site.register(TrainingBooking)
admin.site.register(TrainingDays)


class DrivingTestAdmin(admin.ModelAdmin):
    # list_display = ('test_date', 'name', 'location', 'country',)
    filter_horizontal = ('slots',)

admin.site.register(TrainingEvent, DrivingTestAdmin)