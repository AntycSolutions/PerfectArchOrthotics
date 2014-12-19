from django.contrib import admin
from django.contrib.auth.models import Group

from clients.models import Client, Insurance, Claim, Dependent, \
    CoverageType, Person, Invoice, Item, InsuranceLetter, \
    Laboratory, ProofOfManufacturing, ClaimItem, ClaimCoverageType

admin.site.register(Client)
admin.site.register(Person)
admin.site.register(Insurance)
admin.site.register(CoverageType)


class ClaimItemInline(admin.TabularInline):
    model = ClaimItem


class ClaimCoverageTypeInline(admin.TabularInline):
    model = ClaimCoverageType


class ClaimAdmin(admin.ModelAdmin):
    inlines = (ClaimCoverageTypeInline, ClaimItemInline)
admin.site.register(Claim, ClaimAdmin)

admin.site.register(Item)
admin.site.register(Laboratory)
admin.site.register(Dependent)
admin.site.register(Invoice)
admin.site.register(InsuranceLetter)
admin.site.register(ProofOfManufacturing)
admin.site.register(ClaimItem)
admin.site.register(ClaimCoverageType)

# Unused, dont display
admin.site.unregister(Group)
