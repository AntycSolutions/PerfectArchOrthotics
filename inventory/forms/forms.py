from django import forms
from django.utils import safestring

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

        order_type = self.fields['order_type']
        is_ORTHOTICS = (
            self.instance.pk and
            self.instance.order_type == clients_models.Coverage.ORTHOTICS
        )
        if is_ORTHOTICS:
            choices = ((clients_models.Coverage.ORTHOTICS, 'Orthotics'),)
        else:
            choices = order_type.choices
            choices.remove((models.Order.SHOE, "Shoe"))
            choices.remove((models.Order.ADJUSTMENT, "Adjustment"))
            choices.remove((clients_models.Coverage.ORTHOTICS, 'Orthotics'))
        order_type.choices = choices

    class Meta:
        model = models.CoverageOrder
        exclude = ('claim',)


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
