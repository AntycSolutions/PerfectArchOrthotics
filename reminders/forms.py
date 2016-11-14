from django import forms

from . import models


class ClaimReminderForm(forms.ModelForm):

    class Meta:
        model = models.ClaimReminder
        exclude = ('claim', 'created',)


class OrderReminderForm(forms.ModelForm):

    class Meta:
        model = models.OrderReminder
        exclude = ('order', 'created',)
