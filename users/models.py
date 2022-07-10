from django.db import models

# Create your models here.
class CustomUser(models.Model):
    username = models.CharField()
    password = models.CharField()
    first_name =models.CharField()
    last_name =models.CharField()
    email = models.EmailField()
    contactNumber = models.CharField()
    driverhealth_id = models.CharField()
    terms = models.BooleanField()
    is_superuser = models.BooleanField()
    is_active = models.BooleanField()


class DriverProfile(models.Model):
    pass