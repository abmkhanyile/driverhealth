from django.core.management.base import BaseCommand, CommandError
from user_accounts.models import CustomUser
from dhclients.models import DHClient
from dhclients.createusers import CreateNewUsers




class Command(BaseCommand):
    help = 'Performs the process of matching tenders to the keywords they belong to.'

    def handle(self, *args, **options):
        createusers = CreateNewUsers()
        createusers.action()