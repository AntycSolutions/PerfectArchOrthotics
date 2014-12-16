from django.contrib import admin
from django.contrib.auth.models import Group

from clients.models import Client, Insurance, Claim, Dependent, \
    CoverageType, Person, Invoice, Item, InsuranceLetter, \
    Laboratory, ProofOfManufacturing, ClaimItem

admin.site.register(Client)
admin.site.register(Person)
admin.site.register(Insurance)
admin.site.register(CoverageType)
admin.site.register(Claim)
admin.site.register(Dependent)
admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(InsuranceLetter)
admin.site.register(Laboratory)
admin.site.register(ProofOfManufacturing)
admin.site.register(ClaimItem)

# Unused, dont display
admin.site.unregister(Group)
