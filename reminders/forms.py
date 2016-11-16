from django import forms

from . import models


class UnpaidClaimReminderForm(forms.ModelForm):
    class Meta:
        model = models.UnpaidClaimReminder
        exclude = ('claim', 'created',)


class OrderArrivedReminderForm(forms.ModelForm):
    class Meta:
        model = models.OrderArrivedReminder
        exclude = ('order', 'created',)
