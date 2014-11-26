from django.contrib import admin
from django.contrib.auth.models import Group

from clients.models import Client, Prescription, Insurance, Claim, Dependent, \
    CoverageType, InsuranceClaim, Person, Invoice, Item, InsuranceLetter, \
    Laboratory, ProofOfManufacturing

admin.site.register(Client)
admin.site.register(Person)
admin.site.register(Prescription)
admin.site.register(Insurance)
admin.site.register(CoverageType)
admin.site.register(Claim)
admin.site.register(InsuranceClaim)
admin.site.register(Dependent)
admin.site.register(Invoice)
admin.site.register(Item)
admin.site.register(InsuranceLetter)
admin.site.register(Laboratory)
admin.site.register(ProofOfManufacturing)

admin.site.unregister(Group)
