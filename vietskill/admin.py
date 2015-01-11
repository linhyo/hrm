from django.contrib import admin
from vietskill.models import StaffProfile


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'sex', 'position', 'email', 'address', 'phone_number', 'picture')

admin.site.register(StaffProfile, StaffProfileAdmin)
