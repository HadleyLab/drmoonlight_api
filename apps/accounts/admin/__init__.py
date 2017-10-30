from django.contrib import admin

from apps.accounts.models import *
from .resident import ResidentAdmin
from .scheduler import SchedulerAdmin
from .account_manager import AccountManagerAdmin
from .superuser import SuperUserAdmin


admin.site.register(Scheduler, SchedulerAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(AccountManager, AccountManagerAdmin)
admin.site.register(SuperUser, SuperUserAdmin)

admin.site.register(Speciality)
admin.site.register(ResidencyProgram)
