from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

# this models holds all the courses on offer
class TrainingCourse(models.Model):
    course_name = models.CharField(max_length=150, blank=False)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    course_details = RichTextField()
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        self.course_name


class Code14Course(models.Model):
    course_name = models.CharField(max_length=150, blank=False)
    duration = models.IntegerField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    course_details = RichTextField()
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        self.course_name
