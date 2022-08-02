from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.site_header = 'DriverHealth Admin'

class UserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'contactNumber', 'last_login']
    search_fields = ('contactNumber', 'dh_id', 'username', 'first_name',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'dh_id', 'contactNumber', 'is_active', 'is_superuser', 'is_staff', 'user_permissions',  )}),
        # ('Permissions', {'fields': ('is_active', 'is_superuser', 'user_permissions')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'dh_id', 'contactNumber',),
            # 'fields': ('username', 'first_name', 'last_name', 'email', 'contactNumber', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)
