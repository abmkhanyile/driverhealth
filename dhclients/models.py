from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField


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
    crossborder = models.BooleanField(default=True)
    location = models.CharField(max_length=150, blank=False)
    # Beginning of the filtering fields
    locality = models.CharField(max_length=250, blank=True)
    sublocality = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)
    administrative_area_level_1 = models.CharField(max_length=250, blank=True)
    administrative_area_level_2 = models.CharField(max_length=250, blank=True)
    # End of the filtering filtering fields
    rating = models.SmallIntegerField(default=0, blank=False, null=True, choices=STAR_CHOICES)
    dh_test_comment = models.CharField(max_length=1500, blank=True) 
    tested = models.BooleanField(default=False, blank=True)
    in_job_market = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='Profile_Pics/', blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('DH Clients')

    def __str__(self):
        return f'{self.user.get_full_name()}' 



# holds the driver docuements
class ClientDocument(models.Model):
    DOC_TYPE = [
        (1, 'CV'),
        (2, 'Driver\'s Licence'),
        (3, 'PrDP / Medical Certificate'),
        (4, 'ID Document'),
        (5, 'Passport'),
        (6, 'Other'),
    ]
    DOC_VISIBILITY = [
        (1, 'Make Public'),
        (2, 'Make Private'),
    ]
    client = models.ForeignKey('dhclients.DHClient', related_name='client_documents', on_delete=models.CASCADE, blank=False, null=True)
    document = models.FileField(upload_to='Client_Documents/', blank=False)
    doc_type = models.IntegerField(choices=DOC_TYPE, blank=False, null=True)
    doc_visibility = models.IntegerField(choices=DOC_VISIBILITY, default=1, blank=False, null=True)
    other_type = models.CharField(max_length=60, blank=True, null=True)
    doc_name = models.CharField(max_length=300, blank=False, null=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=False)
    
    class Meta:
        verbose_name_plural = ('Client Documents')

    def retDocument(self):
        return 'https://{}/{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, self.document)


# this model holds the client's employment history
class EmploymentHistory(models.Model):
    dhclient = models.ForeignKey('dhclients.DHClient', related_name="client_employment_history", on_delete=models.CASCADE, blank=False, null=True)
    company_name = models.CharField(max_length=150, blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    role = models.CharField(max_length=100, blank=False)
    duties = models.CharField(max_length=2000, blank=False)
    contact_person = models.CharField(max_length=50, blank=False)
    contact_num = models.CharField(max_length=50, blank=False)
    contact_permission = models.BooleanField(blank=False)
    creation_date = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.company_name

