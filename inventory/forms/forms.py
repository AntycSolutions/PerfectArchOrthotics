from django import forms

from inventory import models


class ShoeOrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShoeOrderForm, self).__init__(*args, **kwargs)

        queryset = self.fields['claimant'].queryset
        queryset = queryset.extra(
            select={
                'lower_first_name': 'lower(first_name)'
                }).order_by('lower_first_name')
        self.fields['claimant'].queryset = queryset

    class Meta:
        model = models.ShoeOrder
        exclude = ('order_type',)


class CoverageOrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CoverageOrderForm, self).__init__(*args, **kwargs)

        queryset = self.fields['claimant'].queryset
        queryset = queryset.extra(
            select={
                'lower_first_name': 'lower(first_name)'
                }).order_by('lower_first_name')
        self.fields['claimant'].queryset = queryset

        choices = self.fields['order_type'].choices
        choices.remove((models.Order.SHOE, "Shoe"))
        self.fields['order_type'].choices = choices

    class Meta:
        model = models.CoverageOrder
        fields = '__all__'
