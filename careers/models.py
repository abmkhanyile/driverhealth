from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone


# this model store job listings by companies.
class Job(models.Model):
    owner = models.ForeignKey('companies.Company', related_name="company_jobs", on_delete=models.CASCADE, blank=False)
    applicants = models.ManyToManyField('dhclients.DHClient', related_name="applicants", blank=True)
    job_title = models.CharField(max_length=150, blank=False)
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

