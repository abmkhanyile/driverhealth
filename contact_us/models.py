from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class ContactFormEnquiry(models.Model):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    contact_num = models.CharField(max_length=25, blank=False)
    message = RichTextField(blank=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.name
