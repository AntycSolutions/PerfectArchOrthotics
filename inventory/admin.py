from django.contrib import admin

from inventory import models


class ShoeAttributesInline(admin.TabularInline):
    model = models.ShoeAttributes


class ShoeAdmin(admin.ModelAdmin):
    inlines = (ShoeAttributesInline,)

admin.site.register(models.ShoeAttributes)
admin.site.register(models.Shoe, ShoeAdmin)

admin.site.register(models.Order)
admin.site.register(models.ShoeOrder)
admin.site.register(models.CoverageOrder)
