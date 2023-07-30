from ckeditor.fields import RichTextField
from django.db import models

# This model holds the About Us text.

class About_Us(models.Model):
    compName = models.CharField(max_length=250, blank=True)
    compRegNum = models.CharField(max_length=30, blank=True)
    VAT_num = models.CharField(max_length=25, default="Not VAT registered.")
    contactNumber = models.CharField(max_length=30, blank=True)
    faxNumber = models.CharField(max_length=30, blank=True)
    emailAddress = models.CharField(max_length=150, blank=True)
    website = models.CharField(max_length=150, blank=True)
    physicalAddress = RichTextField(blank=True)
    postalAddress = RichTextField(blank=True)
    account_holder = models.CharField(max_length=100, blank=True)
    bankName = models.CharField(max_length=100, blank=True)
    bankAccNum = models.CharField(max_length=30, blank=True)
    accType = models.CharField(max_length=30, blank=True)
    branchName = models.CharField(max_length=50, blank=True)
    branchCode = models.CharField(max_length=20, blank=True)
    swiftCode = models.CharField(max_length=20, blank=True)
    about_us_page_txt = RichTextField(blank=False)
    about_us_id = models.IntegerField(blank=False, default=0)

    class Meta:
        verbose_name_plural = ('About Us')

    def __str__(self):
        return self.compName
