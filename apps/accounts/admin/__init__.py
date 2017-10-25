from django.contrib import admin

from apps.accounts.models import *


admin.site.register(Scheduler)
admin.site.register(Resident)
admin.site.register(AccountManager)

admin.site.register(Speciality)
admin.site.register(ResidencyProgram)
