from django.contrib import admin
from .models import DHClient, ClientDocument, EmploymentHistory

admin.site.register(DHClient)
admin.site.register(ClientDocument)
admin.site.register(EmploymentHistory)

# Register your models here.
