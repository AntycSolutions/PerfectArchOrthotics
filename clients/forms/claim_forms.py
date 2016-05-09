import itertools

from django import forms
from django.forms import models as forms_models

from bootstrap3_datetime import widgets as bs3_widgets

from utils.forms import (
    fields as utils_fields, widgets as utils_widgets, forms as utils_forms
)

from clients import models


class ClaimForm(forms.ModelForm):
    submitted_datetime = forms.DateTimeField(
        label="Submitted Datetime",
        input_formats=['%Y-%m-%d %I:%M %p'],
        widget=bs3_widgets.DateTimePicker(
            options={"format": "YYYY-MM-DD hh:mm a"},
            attrs={"class": "form-control",
                   # am/pm -> AM/PM
                   "style": "text-transform: uppercase; float: none;"},
        )
    )
    claim_package = utils_fields.MultiFileField(
        label="Claim Package",
        required=False,
        max_file_size=3.0 * 1024 * 1024  # mb*kb*b,
    )

    class Meta:
        model = models.Claim
        exclude = ('coverages',)

    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id', None)
        if not client_id:
            if 'instance' not in kwargs:
                raise Exception(
                    'Please provide a client_id kwarg or provide an instance'
                )
            client_id = kwargs.get('instance').patient.get_client().id
        client = models.Client.objects.get(id=client_id)

        super().__init__(*args, **kwargs)

        file_list = []
        if self.instance.claimattachment_set.exists():
            file_list = [
                claim_attachment.attachment
                for claim_attachment in self.instance.claimattachment_set.all()
            ]
        files = kwargs.get('files', None)
        if files:
            # files require attr url to be displayed
            for key in files:
                if 'claim_package' in key:
                    if hasattr(files, 'getlist'):
                        _file_value = files.getlist(key)
                    else:
                        _file_value = files.get(key)
                    if isinstance(_file_value, list):
                        for _file in _file_value:
                            _file.url = 'media/temp/' + _file.name
                            file_list.append(_file)
                    else:
                        _file = _file_value
                        _file.url = 'media/temp/' + _file.name
                        file_list.append(_file)
        claim_package = self.fields['claim_package']
        claim_package.widget = \
            utils_widgets.ConfirmMultiFileMultiWidget(
                form_id="update_claim_form",  # html
                form=self,
                field_name='claim_package',
                file_count=len(file_list)
            )
        self.initial['claim_package'] = file_list

        self.client = client

        patients = []
        spouse = None
        for dependent in client.dependent_set.all():
            if dependent.relationship == models.Dependent.SPOUSE:
                spouse = dependent.id
            patients.append(dependent.id)
        patients.append(client.id)
        patient = self.fields['patient']
        patient.queryset = models.Person.objects.filter(id__in=patients)
        patient.label_from_instance = (
            lambda obj:
                "Client - %s" % obj.full_name() if obj.id == client.id
                else "Spouse - %s" % obj.full_name() if obj.id == spouse
                else "Child - %s" % obj.full_name()
        )

        insurance = self.fields['insurance']
        insurance.queryset = models.Insurance.objects.filter(
            main_claimant__pk__in=patients)
        insurance.label_from_instance = (
            lambda obj:
                "%s - Spouse - %s" % (
                    obj.provider,
                    obj.main_claimant.full_name()
                ) if obj.main_claimant.pk == spouse
                else "%s - Client - %s" % (
                    obj.provider, obj.main_claimant.full_name())
        )
        insurance.widget.attrs['class'] = 'insurance_trigger'

    def save(self, commit=True):
        instance = super().save(commit)

        LAST_INITIAL = object()
        both = itertools.zip_longest(self.cleaned_data['claim_package'],
                                     self.initial['claim_package'],
                                     fillvalue=LAST_INITIAL)
        for _file, initial_datum in both:
            if _file is None or _file == initial_datum:
                continue
            elif _file is False:
                models.ClaimAttachment.objects.get(
                    attachment=initial_datum, claim=instance
                ).delete()
            elif initial_datum is LAST_INITIAL:
                for _new_file in _file:
                    models.ClaimAttachment.objects.create(
                        attachment=_new_file, claim=instance
                    )
            else:
                raise Exception("Unknown Exception during MultiFile save.")

        return instance


class ClaimCoverageInlineFormSet(utils_forms.MinimumNestedFormSet):
    def __init__(self, *args, **kwargs):
        self.empty_prefix = '__coverageprefix__'

        super().__init__(*args, **kwargs)

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix(self.empty_prefix),
            empty_permitted=True
        )
        self.add_fields(form, None)

        return form


class ClaimItemInlineFormSet(utils_forms.MinimumInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.empty_prefix = '__itemprefix__'

        super().__init__(*args, **kwargs)

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix(self.empty_prefix),
            empty_permitted=True
        )
        self.add_fields(form, None)

        return form


ClaimCoverageFormFormSet = utils_forms.minimum_nestedformset_factory(
    models.Claim, models.ClaimCoverage,
    forms_models.inlineformset_factory(
        models.ClaimCoverage, models.ClaimItem,
        formset=ClaimItemInlineFormSet, extra=1, fields='__all__',
    ),
    minimum_name="Coverage", minimum_name_nested="Item",
    formset=ClaimCoverageInlineFormSet,
    extra=1, exclude=('items',),
)


class BiomechanicalGaitModelForm(forms.ModelForm):
    class Meta:
        model = models.BiomechanicalGait
        exclude = ['claim']
