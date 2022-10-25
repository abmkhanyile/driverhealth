from __future__ import absolute_import, unicode_literals
# from companies.models import Company

from celery import shared_task



@shared_task
def update_limits(x, y):
    return x+y
    # companies = Company.objects.all()
    # for company in companies:
    #     if company.driver_requests_limit != 10:
    #         company.driver_requests_limit = 10
    #         company.save()
        
        