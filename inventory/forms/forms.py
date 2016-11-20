from django import forms
from django.template import defaultfilters

from clients import models as clients_models
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
            customer_ordered_date = cleaned_data['customer_ordered_date']

            new_shoe_order = (
                customer_ordered_date and
                not ordered_date and
                not dispensed_date
            )
            if new_shoe_order:
                return

            # shoe needs to have been either ordered, dispensed, or
            #  ordered and dispensed

            dispensed_date_required = (
                (shoe_attributes and shoe_attributes.quantity > 0) and
                not dispensed_date and
                not ordered_date
            )
            if dispensed_date_required:
                raise forms.ValidationError(
                    "%s is in stock. Please enter the Dispensed Date." % (
                        shoe_attributes.get_str()
                    )
                )

            ordered_date_required = (
                (shoe_attributes and shoe_attributes.quantity <= 0) and
                not dispensed_date and
                not ordered_date
            )
            if ordered_date_required:
                raise forms.ValidationError(
                    "%s is not in stock. Please enter the Ordered Date." % (
                        shoe_attributes.get_str()
                    )
                )

            not_in_stock = (
                (shoe_attributes and shoe_attributes.quantity <= 0) and
                dispensed_date and
                not ordered_date
            )
            if not_in_stock:
                raise forms.ValidationError(
                    "%s is not in stock and the Dispensed Date was entered."
                    " The Ordered Date must be entered to"
                    " indicate the Shoe was ordered and can be dispensed." % (
                        shoe_attributes.get_str()
                    )
                )

    def __init__(self, *args, **kwargs):
        super(ShoeOrderForm, self).__init__(*args, **kwargs)

        queryset = self.fields['claimant'].queryset
        queryset = queryset.extra(
            select={'lower_first_name': 'lower(first_name)'}
        ).order_by('lower_first_name')
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
            }
        ).order_by('lower_first_name')
        self.fields['claimant'].queryset = queryset

        choices = self.fields['order_type'].choices
        choices.remove((models.Order.SHOE, "Shoe"))
        choices.remove((models.Order.ADJUSTMENT, "Adjustment"))
        self.fields['order_type'].choices = choices

        self.fields['claim'].label_from_instance = lambda obj: obj.get_str()

    def clean(self):
        cleaned_data = super().clean()

        order_type = cleaned_data.get('order_type')
        claim = cleaned_data['claim']
        ordered_date = cleaned_data['ordered_date']
        arrived_date = cleaned_data['arrived_date']
        dispensed_date = cleaned_data['dispensed_date']

        cutoff = (
            models.CoverageOrder.ORDERS_TIED_TO_CLAIMS_START_DATETIME.date()
        )

        claim_required = (
            order_type == clients_models.Coverage.ORTHOTICS and
            not claim and
            (
                (ordered_date and ordered_date > cutoff) or
                (arrived_date and arrived_date > cutoff) or
                (dispensed_date and dispensed_date > cutoff)
            )
        )
        if claim_required:
            error = forms.ValidationError(
                'Orthotics Orders must be tied to a Claim if created '
                'after {}. Use the "Create an Orthotics Order" button '
                'when viewing Claims'.format(
                    defaultfilters.date(cutoff)
                )
            )
            self.add_error('order_type', error)
            self.add_error('claim', error)

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
