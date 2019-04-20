from django import forms

from crispy_forms import helper

from . import models


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = models.Reminder
        fields = ('follow_up',)


class ReminderForm(forms.ModelForm):
    reminder_search = forms.CharField()

    insurance = forms.CharField()

    created_from = forms.DateField()
    created_to = forms.DateField()

    class Meta:
        model = models.Reminder
        fields = (
            'reminder_search',
            'insurance',
            'created_from',
            'created_to',
            'result'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['reminder_search'].widget.attrs.update({'autofocus': True})

        self.fields['result'].label += ':'

        self.helper = helper.FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'


class UnpaidClaimReminderForm(forms.ModelForm):
    class Meta:
        model = models.UnpaidClaimReminder
        exclude = ('claim', 'created',)


class OrderArrivedReminderForm(forms.ModelForm):
    class Meta:
        model = models.OrderArrivedReminder
        exclude = ('order', 'created',)


class BenefitsReminderForm(forms.ModelForm):
    class Meta:
        model = models.BenefitsReminder
        exclude = ('client', 'coverages', 'created',)
