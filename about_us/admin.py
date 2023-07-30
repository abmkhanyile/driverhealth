from django.contrib import admin
from .models import About_Us

@admin.register(About_Us)
class About_Us_Admin(admin.ModelAdmin):
    exclude=("about_us_id ",)
    readonly_fields=('about_us_id', )
    list_display = ['compName']


