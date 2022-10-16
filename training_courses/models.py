from enum import unique
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone



# this models holds all the courses on offer
class TrainingCourse(models.Model):
    course_name = models.CharField(max_length=150, blank=False)
    duration = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    course_details = RichTextField()
    hourly_training = models.BooleanField(default=False)
    elearning = models.BooleanField(default=False)
    thirdparty_course = models.BooleanField(default=False)
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
    comment = models.CharField(max_length=1000, blank=True)
    fully_booked = models.BooleanField(default=False)
    enrollees_num = models.IntegerField(null=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.training_course.course_name

    # returns training dates
    def ret_training_dates(self):
        return self.training_event_dates.all()

    


# holds the dates for the training 
class TrainingDays(models.Model):
    training_slot = models.DateField(blank=False)
    event = models.ForeignKey('training_courses.TrainingEvent', related_name="training_event_dates", on_delete=models.CASCADE, blank=False, null=True)
   
    def __str__(self):
        return str(self.training_slot)
    
    # returns times 
    def ret_times(self):
        return self.training_date_times.all()



# holds time slots
class TrainingTime(models.Model):
    time_slot = models.TimeField(blank=False)
    date = models.ForeignKey('training_courses.TrainingDays', related_name="training_date_times", on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        ordering = ("-time_slot",)

    def __str__(self):
        return str(self.time_slot)

    


# records all booking transactions.
class BookingTransaction(models.Model):
    trans_id = models.CharField(max_length=50, blank=False, unique=True)
    trans_tot = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def ret_course(self):
        return self.transaction_bookings.all()[0].training_event.training_course


# holds all the training bookings 
class TrainingBooking(models.Model):
    client = models.ForeignKey('user_accounts.CustomUser', related_name="client_training_bookings", on_delete=models.CASCADE, blank=True)
    training_event = models.ForeignKey('training_courses.TrainingEvent', related_name="training_event_bookings", on_delete=models.CASCADE, blank=True)
    booking_transaction = models.ForeignKey('training_courses.BookingTransaction', related_name="transaction_bookings", on_delete=models.CASCADE, blank=False, null=True)
    tdate = models.ForeignKey('training_courses.TrainingDays', related_name="date_bookings", on_delete=models.CASCADE, blank=True, null=True)
    stime = models.ForeignKey('training_courses.TrainingTime', related_name="booking_times", on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.client.get_full_name()


# stores all elearning training enquiries
class ElearningEnquiries(models.Model):
    user = models.ForeignKey('user_accounts.CustomUser', related_name="enquired_users", on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=False)
    contact_num = models.CharField(max_length=25, blank=False)
    email = models.EmailField(max_length=200 ,blank=True, null=True)
    message = models.CharField(max_length=500, blank=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.full_name



