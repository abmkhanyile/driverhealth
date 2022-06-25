from django.db import models
from django.conf import settings
from django.utils import timezone

# this model holds all the DH Clients (i.e. Job Seekers).
class DHClient(models.Model):
    STAR_CHOICES = [
        (0, '0 Star'),
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, primary_key=True)
    nationality = models.ForeignKey('countries.Country', blank=False, null=True, on_delete=models.PROTECT)
    has_passport = models.BooleanField(default=False)
    passport_num = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150, blank=False)
    postal_code = models.CharField(max_length=15, blank=True)
    rating = models.SmallIntegerField(default=0, blank=False, null=True, choices=STAR_CHOICES)
    dh_test_comment = models.CharField(max_length=1500, blank=True) 
    tested = models.BooleanField(default=False, blank=True)
    in_job_market = models.BooleanField(default=True)
    # profile_picture = models.ImageField(upload_to='Profile_Pics/', blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('DH Clients')

    def __str__(self):
        return f'{self.user.get_full_name()}' 

