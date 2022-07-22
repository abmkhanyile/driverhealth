from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

# this models holds all the courses on offer
class TrainingCourse(models.Model):
    course_name = models.CharField(max_length=150, blank=False)
    duration = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    course_details = RichTextField()
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.course_name


class Code14Course(models.Model):
    course_name = models.CharField(max_length=150, blank=False)
    duration = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    course_details = RichTextField()
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.course_name

# this is an intermediary table for the Trainees and TrainingEvent relationship.
class Course_Enrollees(models.Model):
    enrollee = models.ForeignKey('dhclients.DHClient', on_delete=models.CASCADE, blank=False) 
    course_event = models.ForeignKey('training_courses.TrainingEvent', on_delete=models.CASCADE, blank=False)
    paid = models.BooleanField(default=False)


# holds all training events.
class TrainingEvent(models.Model):
    training_course = models.ForeignKey('training_courses.TrainingCourse', related_name="course_events", on_delete=models.CASCADE, blank=False)
    enrollees = models.ManyToManyField('dhclients.DHClient', through='Course_Enrollees', blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.training_course.course_name

