from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserForm


class AccountUserAdmin(UserAdmin):
    form = UserForm
    fieldsets = UserAdmin.fieldsets + (
        ('Info', {'fields': ('role', 'mobile', 'added_by')}),
    )

    list_filter = (
        ('role'),
        ('is_superuser'),
    )

admin.site.register(User, AccountUserAdmin)
