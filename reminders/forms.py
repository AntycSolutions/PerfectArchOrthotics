from django import forms

from crispy_forms import helper

from . import models


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = models.Reminder
        fields = ('follow_up',)


class ReminderForm(forms.ModelForm):
    created_from = forms.DateField()
    created_to = forms.DateField()

    insurance = forms.CharField()

    class Meta:
        model = models.Reminder
        exclude = ('follow_up', 'created')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
