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
    slots = models.ManyToManyField('training_courses.TrainingDays', blank=False)
    comment = models.CharField(max_length=1000, blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.training_course.course_name

    def natural_key(self):
        return (self.training_course.course_name)


# holds the dates for the training 
class TrainingDays(models.Model):
    training_slot = models.DateTimeField(blank=False)

    def __str__(self):
        return str(self.training_slot)

    def natural_key(self):
        return (self.training_slot)

# holds all the training bookings 
class TrainingBooking(models.Model):
    client = models.ForeignKey('user_accounts.CustomUser', related_name="client_training_bookings", on_delete=models.CASCADE, blank=True)
    training_event = models.ForeignKey('training_courses.TrainingEvent', related_name="training_event_bookings", on_delete=models.CASCADE, blank=True)
    booking_id = models.CharField(max_length=20, unique=True, blank=False)
    paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.booking_id


