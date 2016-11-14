from django.contrib import admin

from . import models


admin.site.register(models.ClaimReminder)
admin.site.register(models.OrderReminder)
