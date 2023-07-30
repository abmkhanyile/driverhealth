from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.conf import settings

class LegalDocs(models.Model):
    doc_name = models.CharField(max_length=100, blank=True)
    doc_text = RichTextField(blank=True)
    doc_id = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = ('Legal Documents')

    def __str__(self):
        return self.doc_name

# this models holds the legal documents for employing a driver.
class RecruitmentLegalDoc(models.Model):  
    DOC_TYPE = [
        (1, 'Candidate Consent Form'),
        (2, 'DriverHealth Terms of Engagement'),
        (3, 'Other'),
        (4, 'Service Level Agreement'),
    ]
    document = models.FileField(upload_to='Recruitment_docs/', blank=False)
    doc_type = models.SmallIntegerField(choices=DOC_TYPE, blank=False)
    other_doc = models.CharField(max_length=300, blank=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=False)
    
    class Meta:
        verbose_name_plural = ('Recruitment Documents')

    def retDocument(self):
        return 'https://{}/{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, self.document)

