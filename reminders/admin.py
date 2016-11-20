from django.contrib import admin

from . import models


admin.site.register(models.UnpaidClaimReminder)
admin.site.register(models.OrderArrivedReminder)
admin.site.register(models.ClaimOrderReminder)
