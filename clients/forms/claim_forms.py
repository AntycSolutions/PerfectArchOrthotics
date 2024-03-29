from django import forms
from django.forms import models as forms_models

from bootstrap3_datetime import widgets as bs3_widgets

from utils.forms import (
    fields as utils_fields,
    widgets as utils_widgets,
    forms as utils_forms,
    form_utils as utils_form_utils
)

from clients import models


class DateTimePicker(bs3_widgets.DateTimePicker):
    class Media:
        extend = False  # we inject our own media below with fallbackjs compat


class ClaimForm(forms.ModelForm):
    submitted_datetime = forms.DateTimeField(
        label="Submitted Datetime",
        input_formats=['%Y-%m-%d %I:%M %p'],
        widget=DateTimePicker(
            options={"format": "YYYY-MM-DD hh:mm a"},
            attrs={
                "class": "form-control",
                # am/pm -> AM/PM
                "style": "text-transform: uppercase; float: none;"
            },
            div_attrs={
                'class': 'input-group',
            }
        )
    )
    claim_package = utils_fields.MultiFileField(
        label="Claim Package",
        required=False,
        max_file_size=7.0 * 1024 * 1024,  # mb*kb*b
        help_text=(
            'Hold Ctrl (on Windows) or Cmd (on a Mac) to select multiple files'
        )
    )

    class Meta:
        model = models.Claim
        exclude = ('coverages', 'insurance',)

    class Media:
        js = (
            utils_form_utils.MediaStr(
                'clients/js/claim.js',
                shim=['jQuery.fn.select2']
            ),
            utils_form_utils.MediaStr(
                'bootstrap3_datetime/js/moment.min.js',
                key='moment',
            ),
            utils_form_utils.MediaStr(
                'bootstrap3_datetime/js/bootstrap-datetimepicker.min.js',
                key='jQuery.fn.datetimepicker',
                shim=['jQuery.fn.modal', 'moment']
            ),
        )
        css = {
            'all': (
                'bootstrap3_datetime/css/bootstrap-datetimepicker.min.css',
            )
        }

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

        file_list = [
            claim_attachment.attachment
            for claim_attachment in self.instance.claimattachment_set.all()
        ]
        files = kwargs.get('files', None)
        if files:  # value can be set to None
            # temp files (UploadedFile) require attr url to be displayed
            for key in files:
                if 'claim_package' == key:
                    _file_list = files.get(key)
                    for _file in _file_list:
                        # /media/temp/ (from CreateClaimWizard.file_storage)
                        _file.url = '/media/temp/' + _file.name
                        file_list.append(_file)
        claim_package = self.fields['claim_package']
        claim_package.widget = \
            utils_widgets.ConfirmClearableMultiFileMultiWidget(
                form_id="claim_form",  # html
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

        insurances = self.fields['insurances']
        insurances.queryset = models.Insurance.objects.filter(
            main_claimant__pk__in=patients
        )
        insurances.label_from_instance = (
            lambda obj:
                "%s - Spouse - %s" % (
                    obj.provider,
                    obj.main_claimant.full_name()
                ) if obj.main_claimant.pk == spouse
                else "%s - Client - %s" % (
                    obj.provider, obj.main_claimant.full_name())
        )
        insurances.widget.attrs['class'] = 'insurance_trigger'

        # add fallbackjs compat
        self.fields['submitted_datetime'].widget.js_template = '''
            <script>
                (function(window) {
                    var callback = function() {
                        fallback.ready(['jQuery.fn.datetimepicker'], function() {
                            $(function(){
                                $("#%(picker_id)s:has(input:not([readonly],[disabled]))").datetimepicker(%(options)s);
                                $("#%(input_id)s:not([readonly],[disabled])").datetimepicker(%(options)s);
                            });
                        });
                    };
                    if(window.addEventListener)
                        window.addEventListener("load", callback, false);
                    else if (window.attachEvent)
                        window.attachEvent("onload", callback);
                    else window.onload = callback;
                })(window);
            </script>
        '''  # noqa

    def clean(self):
        cleaned_data = super().clean()

        patient = cleaned_data.get('patient')
        insurances = cleaned_data.get('insurances', [])
        has_coverage = False
        for insurance in insurances:
            coverages = insurance.coverage_set.all()
            for coverage in coverages:
                if coverage.claimant_id == patient.id:
                    has_coverage = True
                    break
        if insurances and not has_coverage:
            raise forms.ValidationError(
                'No Coverage for {} found in the selected Insurances'.format(
                    patient
                )
            )


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


class ClaimItemModelForm(forms.ModelForm):
    class Meta:
        model = models.ClaimItem
        fields = '__all__'

    class Media:
        js = (
            utils_form_utils.MediaStr(
                'clients/js/claim_item.js',
                shim=['jQuery.fn.select2']
            ),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['item'].widget.attrs = {'class': 'item-select'}


ClaimCoverageFormFormSet = utils_forms.minimum_nestedformset_factory(
    models.Claim, models.ClaimCoverage,
    forms_models.inlineformset_factory(
        models.ClaimCoverage, models.ClaimItem,
        form=ClaimItemModelForm,
        formset=ClaimItemInlineFormSet, extra=1, fields='__all__',
    ),
    minimum_name="Coverage", minimum_name_nested="Item",
    formset=ClaimCoverageInlineFormSet,
    extra=1, exclude=('items',),
)


class BiomechanicalGaitModelForm(forms.ModelForm):
    class Meta:
        model = models.BiomechanicalGait
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        client_pk = kwargs.pop('client_pk', None)

        super().__init__(*args, **kwargs)

        if not client_pk:
            client_pk = self.instance.patient.get_client().pk

        client = models.Client.objects.get(pk=client_pk)
        dependents = client.dependent_set.all()
        person_pks = [(client_pk, client.full_name())]
        for dependent in dependents:
            person_pks.append((dependent.pk, dependent.full_name()))

        self.fields['patient'].widget = forms.Select(choices=person_pks)


class BiomechanicalGait2ModelForm(forms.ModelForm):
    class Meta:
        model = models.BiomechanicalGait2
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        client_pk = kwargs.pop('client_pk', None)

        super().__init__(*args, **kwargs)

        if not client_pk:
            client_pk = self.instance.patient.get_client().pk

        client = models.Client.objects.get(pk=client_pk)
        dependents = client.dependent_set.all()
        person_pks = [(client_pk, client.full_name())]
        for dependent in dependents:
            person_pks.append((dependent.pk, dependent.full_name()))

        self.fields['patient'].widget = forms.Select(choices=person_pks)


class BiomechanicalFootModelForm(forms.ModelForm):
    class Meta:
        model = models.BiomechanicalFoot
        exclude = ['claim']
