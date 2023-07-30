from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.conf import settings


# this model store job listings by companies.
class Job(models.Model):
    owner = models.ForeignKey('companies.Company', related_name="company_jobs", on_delete=models.CASCADE, blank=False)
    applicants = models.ManyToManyField('dhclients.DHClient', related_name="applicants", blank=True)
    job_title = models.CharField(max_length=150, blank=False)
    job_location = models.CharField(max_length=500, blank=True)
    closing_date = models.DateTimeField(blank=False)
    dhref = models.CharField(max_length=15, blank=False)
    ref = models.CharField(max_length=150, blank=True)
    job_details = RichTextField(blank=False)
    active_listing = models.BooleanField(default=False)
    candidate_hired = models.BooleanField(default=False)
    dhcomm_earned = models.BooleanField(default=False)
    hired_candidate = models.ForeignKey('dhclients.DHClient', related_name="candidate_job_successes", on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('Job Listings')
        ordering = ['-date_created']

    def __str__(self):
        return self.job_title



# stores job application data
class JobApplication(models.Model):
    job = models.ForeignKey('careers.Job', related_name="job_applications", on_delete=models.CASCADE, blank=False)
    dhclient = models.ForeignKey('dhclients.DHClient', related_name="dhclient_applications", on_delete=models.CASCADE, blank=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self) -> str:
        return self.job.job_title


class ApplicationDocument(models.Model):
    job_application = models.ForeignKey('careers.JobApplication', related_name='application_documents', on_delete=models.CASCADE, blank=False)
    application_doc = models.FileField(upload_to='Job_Application_Documents/', blank=False)
    creation_date = models.DateTimeField(default=timezone.now, blank=False)
    
    class Meta:
        verbose_name_plural = ('Application Documents')

    def __str__(self) -> str:
        return f'{self.creation_date}'

    def retDocument(self):
        return 'https://{}/{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, self.document)

