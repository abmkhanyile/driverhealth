from django.contrib import admin
from .models import TrainingCourse, Code14Course, TrainingEvent, Course_Enrollees

admin.site.register(TrainingCourse)
admin.site.register(Code14Course)
admin.site.register(Course_Enrollees)
admin.site.register(TrainingEvent)
