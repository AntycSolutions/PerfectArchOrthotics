from django import forms
from django.forms import models as forms_models

from clients import models


class InsuranceForm(forms.ModelForm):

    class Meta:
        model = models.Insurance
        exclude = ('main_claimant', 'claimants')


class InsuranceCoverageInlineFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        main_claimant_id = kwargs.pop('main_claimant_id', None)
        if not main_claimant_id:
            raise Exception('Please provide a main_claimant_id')

        super().__init__(*args, **kwargs)

        person = models.Person.objects.select_related(
            'client', 'dependent__primary'
        ).get(pk=main_claimant_id)
        client = person.get_client()
        dependents = client.dependent_set.all()
        dependents_pks = []
        for dependent in dependents:
            dependents_pks.append(dependent.pk)
        person_pks = dependents_pks + [client.pk]
        claimants = models.Person.objects.filter(pk__in=person_pks)
        self.form.base_fields['claimant'].queryset = claimants

        self.form.base_fields['claimant'].label_from_instance = (
            lambda obj: obj.full_name()
        )

        self.form.base_fields['period_date'].help_text = \
            'Only the month and day is important'

    def clean(self):
        super().clean()

        for form in self.forms:
            period = form.cleaned_data.get('period', None)
            period_date = form.cleaned_data.get('period_date', None)
            is_BENEFIT_YEAR = period == models.Coverage.BENEFIT_YEAR
            if is_BENEFIT_YEAR and not period_date:
                msg = models.Coverage.MISSING_PERIOD_DATE
                form.add_error('period', msg)
                form.add_error('period_date', msg)


InsuranceCoverageFormSet = forms_models.inlineformset_factory(
    models.Insurance,
    models.Coverage,
    formset=InsuranceCoverageInlineFormSet,
    extra=1,
    exclude=('insurance',)
)
