from django.contrib import admin
from clients.models import Client, Prescription, Insurance, Claim, Dependent, CoverageType, InsuranceClaim

admin.site.register(Client)
admin.site.register(Prescription)
admin.site.register(Insurance)
admin.site.register(CoverageType)
admin.site.register(Claim)
admin.site.register(InsuranceClaim)
admin.site.register(Dependent)
