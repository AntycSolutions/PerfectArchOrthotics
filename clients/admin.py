from django.contrib import admin
from django.contrib.auth.models import Group
from django.core import urlresolvers
from django.utils import safestring

from clients.models import Client, Insurance, Claim, Dependent, \
    Coverage, Person, Invoice, Item, InsuranceLetter, \
    Laboratory, ProofOfManufacturing, ClaimItem, ClaimCoverage, ClaimAttachment
from clients import models as clients_models


class DependentInline(admin.TabularInline):
    model = Dependent
    fk_name = "client"


class ClientAdmin(admin.ModelAdmin):
    inlines = (DependentInline,)


admin.site.register(Dependent)
admin.site.register(Client, ClientAdmin)


class CoverageInline(admin.TabularInline):
    model = Coverage


class InsuranceAdmin(admin.ModelAdmin):
    inlines = (CoverageInline,)


class PersonAdmin(admin.ModelAdmin):
    inlines = (CoverageInline,)


admin.site.register(Person, PersonAdmin)
admin.site.register(Insurance, InsuranceAdmin)


class ClaimCoverageInline(admin.TabularInline):
    model = ClaimCoverage


class ClaimAttachmentInline(admin.TabularInline):
    model = ClaimAttachment


class ClaimAdmin(admin.ModelAdmin):
    inlines = (ClaimCoverageInline, ClaimAttachmentInline)


class CoverageAdmin(admin.ModelAdmin):
    inlines = (ClaimCoverageInline,)
    list_filter = ('period', ('period_date', admin.AllValuesFieldListFilter),)
    list_display = ('__str__', 'get_update_url',)

    def get_update_url(self, obj):
        update_url = urlresolvers.reverse(
            'insurance_update', kwargs={'insurance_id': obj.insurance.pk}
        )

        return safestring.mark_safe('<a href="{}">Link</a>'.format(update_url))
    get_update_url.short_description = 'Update Link'


admin.site.register(Coverage, CoverageAdmin)
admin.site.register(ClaimAttachment)
admin.site.register(Claim, ClaimAdmin)

admin.site.register(ClaimItem)


class ClaimItemInline(admin.TabularInline):
    model = ClaimItem


class ItemHistoryInline(admin.TabularInline):
    model = clients_models.ItemHistory


class ItemAdmin(admin.ModelAdmin):
    inlines = (ClaimItemInline, ItemHistoryInline)


class ClaimCoverageAdmin(admin.ModelAdmin):
    inlines = (ClaimItemInline,)


admin.site.register(Item, ItemAdmin)
admin.site.register(ClaimCoverage, ClaimCoverageAdmin)

admin.site.register(Invoice)


class LaboratoryInline(admin.TabularInline):
    model = Laboratory


class InsuranceLetterAdmin(admin.ModelAdmin):
    inlines = (LaboratoryInline,)


admin.site.register(Laboratory)
admin.site.register(InsuranceLetter, InsuranceLetterAdmin)

admin.site.register(ProofOfManufacturing)
admin.site.register(clients_models.BiomechanicalGait)
admin.site.register(clients_models.BiomechanicalFoot)

admin.site.register(clients_models.Referral)
admin.site.register(clients_models.Receipt)
admin.site.register(clients_models.CreditDivisor)
admin.site.register(clients_models.Note)

# Unused, don't display
admin.site.unregister(Group)
