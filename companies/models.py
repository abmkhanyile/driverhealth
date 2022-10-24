from email.policy import default
from django.db import models
from django.utils import timezone
from django.conf import settings


# this models holds all companies that do business with driver health
class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="company_admins", blank= True)
    company_name = models.CharField(max_length=150, blank=False)
    company_reg_num = models.CharField(max_length=30, blank=True)
    vat_num = models.CharField(max_length=30, blank=True)
    contact_person = models.CharField(max_length=80, blank=False)
    contact_num1 = models.CharField(max_length=20, blank=False)
    contact_num2 = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=500, blank=False)
    country = models.ForeignKey('countries.Country', on_delete=models.CASCADE, blank=False)
    note = models.CharField(max_length=500, blank=True)
    driver_requests_limit = models.SmallIntegerField(default=10, blank=False)
    creation_date = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('Companies')

    def __str__(self):
        return self.company_name


# this model holds all Company documents e.g. Company Registration documents
class CompanyDocument(models.Model):
    company = models.ForeignKey('companies.Company', related_name='company_documents', on_delete=models.CASCADE, blank=False)
    document_name = models.CharField(max_length=250, blank=False)
    document = models.FileField(upload_to='Company_Documents/', blank=False)
    creation_date = models.DateTimeField(default=timezone.now, blank=False)
    
    class Meta:
        verbose_name_plural = ('Company Documents')

    def retDocument(self):
        return 'https://{}/{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, self.document)
