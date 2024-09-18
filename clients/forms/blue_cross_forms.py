from django import forms

from clients import models


class BlueCrossModelForm(forms.ModelForm):
    class Meta:
        model = models.BlueCross
        exclude = ('claim',)
