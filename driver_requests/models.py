from email.policy import default
from django.db import models
from django.utils import timezone

# stores all driver requests.
class Driver_Request(models.Model):
    REQUEST_TYPE = [
        (1, 'Full-Time Employment'),
        (2, 'Part-Time Employment'),
        (3, 'Once-Off hire'),
        (4, 'Internship'),
        (5, 'Learnership'),
    ] 
    driver = models.ForeignKey('dhclients.DHClient', related_name="driver_requests", on_delete=models.CASCADE, blank=False)
    company = models.ForeignKey('companies.Company', related_name="company_requests", on_delete=models.CASCADE, blank=False)
    req_id = models.CharField(max_length=25, blank=False)
    employment_type = models.SmallIntegerField(default=1, choices=REQUEST_TYPE)
    access_granted = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('Driver Requests')
        ordering = ['-date_created']

    def __str__(self) -> str:
        return f'{self.req_id} {self.driver.user.get_full_name()} {self.company}'

    def ret_last_status(self):
        return RequestStatus.objects.filter(driver_req=self).latest('date_created')


# records the status of the driver request
class RequestStatus(models.Model):
    STATUS = [
        (1, 'Recruitment process initiated'),
        (2, 'Driver informed and accepted'),
        (3, 'Driver informed and rejected'),
        (4, 'Recruitment process initiated'),
        (5, 'All necessary checks done (i.e. criminal, medical, etc)'),
        (6, 'Driver employed'),
        (7, 'Other'),
        (8, 'Request Accepted'),
        (9, 'Request Rejected'),
    ]
    status = models.SmallIntegerField(choices=STATUS, blank=False)
    driver_req = models.ForeignKey('driver_requests.Driver_Request', related_name="request_statuses", on_delete=models.CASCADE, blank=False)
    note = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        ordering = ['-date_created']
