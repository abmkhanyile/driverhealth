from __future__ import absolute_import, unicode_literals

from celery import shared_task



@shared_task
def create_new_users():
    with open("miscellaneous/users_customuser.csv", mode='r', encoding = 'utf-8') as f:
        print(f.readline)
        
        