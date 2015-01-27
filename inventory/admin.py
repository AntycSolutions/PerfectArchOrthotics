from django.contrib import admin

from inventory.models import Shoe, ShoeAttributes


class ShoeAttributesInline(admin.TabularInline):
    model = ShoeAttributes


class ShoeAdmin(admin.ModelAdmin):
    inlines = (ShoeAttributesInline,)

admin.site.register(ShoeAttributes)
admin.site.register(Shoe, ShoeAdmin)
