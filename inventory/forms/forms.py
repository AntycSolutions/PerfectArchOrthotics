from django import forms

from inventory import models

from ajax_select import make_ajax_field


class ShoeOrderForm(forms.ModelForm):
    shoe_attributes = make_ajax_field(
        models.ShoeOrder, 'shoe_attributes', 'shoe',
        show_help_text=True
    )

    def clean(self):
        cleaned_data = super(ShoeOrderForm, self).clean()
        if 'shoe_attributes' in cleaned_data:
            shoe_attributes = cleaned_data['shoe_attributes']
            ordered_date = cleaned_data['ordered_date']
            dispensed_date = cleaned_data['dispensed_date']

            if (shoe_attributes and shoe_attributes.quantity > 0
                    and not dispensed_date
                    and not ordered_date):
                raise forms.ValidationError(
                    "%s is in stock. Please enter the Dispensed Date." % (
                        shoe_attributes
                    )
                )

            if (shoe_attributes and shoe_attributes.quantity <= 0
                    and not dispensed_date
                    and not ordered_date):
                raise forms.ValidationError(
                    "%s is not in stock. Please enter the Ordered Date." % (
                        shoe_attributes
                    )
                )

            if (shoe_attributes and shoe_attributes.quantity <= 0
                    and dispensed_date
                    and not ordered_date):
                raise forms.ValidationError(
                    "%s is not in stock and the Dispensed Date was entered."
                    " The Ordered Date must be entered to"
                    " indicate the Shoe was ordered and can be dispensed." % (
                        shoe_attributes
                    )
                )

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
        choices.remove((models.Order.ADJUSTMENT, "Adjustment"))
        self.fields['order_type'].choices = choices

    class Meta:
        model = models.CoverageOrder
        fields = '__all__'


class AdjustmentOrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdjustmentOrderForm, self).__init__(*args, **kwargs)

        queryset = self.fields['claimant'].queryset
        queryset = queryset.extra(
            select={
                'lower_first_name': 'lower(first_name)'
                }).order_by('lower_first_name')
        self.fields['claimant'].queryset = queryset

    class Meta:
        model = models.AdjustmentOrder
        exclude = ('order_type',
                   'ordered_date', 'arrived_date', 'dispensed_date')
