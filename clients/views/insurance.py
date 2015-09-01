from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.forms.models import inlineformset_factory
from django.core import urlresolvers

from clients.models import Insurance, Person, Client, Dependent, Coverage
from clients.forms.forms import InsuranceForm


class UpdateInsuranceView(UpdateView):
    template_name = 'utils/generics/update.html'
    model = Insurance
    form_class = InsuranceForm
    slug_field = "id"
    slug_url_kwarg = "insurance_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['inline_model_name'] = Coverage._meta.verbose_name
        context['inline_model_name_plural'] = \
            Coverage._meta.verbose_name_plural
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        insurance_form = self.get_form(form_class)

        InsuranceCoverageFormSet = inlineformset_factory(
            Insurance,
            Coverage,
            extra=1,
            exclude=('insurance',)
        )
        coverage_formset = InsuranceCoverageFormSet(
            instance=self.object)

        try:
            main_claimant = Dependent.objects.get(
                pk=self.object.main_claimant.pk)
            client = main_claimant.get_client()
            dependents = client.dependent_set.all()
        except:
            client = Client.objects.get(
                id=self.object.main_claimant.pk)
            dependents = client.dependent_set.all()
        dependents_pks = list(dependents.values_list('pk', flat=True))
        pks = dependents_pks + [client.pk]
        claimants = Person.objects.filter(pk__in=pks)
        label = (lambda obj: obj.full_name())
        coverage_formset.form.base_fields[
            'claimant'].queryset = claimants
        coverage_formset.form.base_fields[
            'claimant'].label_from_instance = label
        for coverage_form in coverage_formset:
            coverage_form.fields['claimant'].queryset = claimants
            coverage_form.fields['claimant'].label_from_instance = label

        return self.render_to_response(
            self.get_context_data(form=insurance_form,
                                  formset=coverage_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        insurance_form = self.get_form(form_class)

        InsuranceCoverageFormSet = inlineformset_factory(
            Insurance,
            Coverage,
            extra=1,
            exclude=('insurance',)
        )
        coverage_formset = InsuranceCoverageFormSet(
            request.POST, instance=self.object)

        try:
            main_claimant = Dependent.objects.get(
                pk=self.object.main_claimant.pk)
            client = main_claimant.get_client()
            dependents = client.dependent_set.all()
        except:
            client = Client.objects.get(
                id=self.object.main_claimant.pk)
            dependents = client.dependent_set.all()
        dependents_pks = list(dependents.values_list('pk', flat=True))
        pks = dependents_pks + [client.pk]
        claimants = Person.objects.filter(pk__in=pks)
        label = (lambda obj: obj.full_name())
        coverage_formset.form.base_fields[
            'claimant'].queryset = claimants
        coverage_formset.form.base_fields[
            'claimant'].label_from_instance = label
        for coverage_form in coverage_formset:
            coverage_form.fields['claimant'].queryset = claimants
            coverage_form.fields['claimant'].label_from_instance = label

        if (insurance_form.is_valid()
                and coverage_formset.is_valid()):
            return self.form_valid(insurance_form, coverage_formset)
        else:
            return self.form_invalid(insurance_form, coverage_formset)

    def form_valid(self, form, coverage_formset):
        self.object = form.save()
        coverage_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, coverage_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  formset=coverage_formset)
        )

    def get_success_url(self):
        self.success_url = self.object.main_claimant.get_absolute_url()

        return self.success_url


class DeleteInsuranceView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = Insurance
    slug_field = "id"
    slug_url_kwarg = "insurance_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()

        return self.success_url


class CreateInsuranceView(CreateView):
    template_name = 'utils/generics/create.html'
    model = Insurance
    form_class = InsuranceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        context['inline_model_name'] = Coverage._meta.verbose_name
        context['inline_model_name_plural'] = \
            Coverage._meta.verbose_name_plural
        context['cancel_url'] = urlresolvers.reverse(
            'client', kwargs={'client_id': self.kwargs['client_id']}
        )

        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        insurance_form = self.get_form(form_class)

        InsuranceCoverageFormSet = inlineformset_factory(
            Insurance,
            Coverage,
            extra=1,
            exclude=('insurance',)
        )
        coverage_formset = InsuranceCoverageFormSet()

        if 'spouse_id' in self.kwargs:
            main_claimant = Dependent.objects.get(id=self.kwargs['spouse_id'])
            client = main_claimant.client
            dependents = client.dependent_set.all()
        else:
            client = Client.objects.get(id=self.kwargs['client_id'])
            dependents = client.dependent_set.all()
        dependents_pks = list(dependents.values_list('pk', flat=True))
        pks = dependents_pks + [client.pk]
        claimants = Person.objects.filter(pk__in=pks)
        label = (lambda obj: obj.full_name())
        coverage_formset.form.base_fields[
            'claimant'].queryset = claimants
        coverage_formset.form.base_fields[
            'claimant'].label_from_instance = label
        for coverage_form in coverage_formset:
            coverage_form.fields['claimant'].queryset = claimants
            coverage_form.fields['claimant'].label_from_instance = label

        return self.render_to_response(
            self.get_context_data(form=insurance_form,
                                  formset=coverage_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        insurance_form = self.get_form(form_class)

        InsuranceCoverageFormSet = inlineformset_factory(
            Insurance,
            Coverage,
            extra=1,
            exclude=('insurance',)
        )
        coverage_formset = InsuranceCoverageFormSet(request.POST)

        if 'spouse_id' in self.kwargs:
            main_claimant = Dependent.objects.get(id=self.kwargs['spouse_id'])
            client = main_claimant.client
            dependents = client.dependent_set.all()
        else:
            client = Client.objects.get(id=self.kwargs['client_id'])
            dependents = client.dependent_set.all()
        dependents_pks = list(dependents.values_list('pk', flat=True))
        pks = dependents_pks + [client.pk]
        claimants = Person.objects.filter(pk__in=pks)
        label = lambda obj: obj.full_name()
        coverage_formset.form.base_fields[
            'claimant'].queryset = claimants
        coverage_formset.form.base_fields[
            'claimant'].label_from_instance = label
        for coverage_form in coverage_formset:
            coverage_form.fields['claimant'].queryset = claimants
            coverage_form.fields['claimant'].label_from_instance = label

        if (insurance_form.is_valid()
                and coverage_formset.is_valid()):
            return self.form_valid(insurance_form, coverage_formset)
        else:
            return self.form_invalid(insurance_form, coverage_formset)

    def form_valid(self, form, coverage_formset):
        self.object = form.save(commit=False)
        if 'spouse_id' in self.kwargs:
            main_claimant = Dependent.objects.get(id=self.kwargs['spouse_id'])
        else:
            main_claimant = Client.objects.get(id=self.kwargs['client_id'])
        self.object.main_claimant = main_claimant
        self.object.save()
        coverage_formset.instance = self.object
        coverage_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, coverage_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  formset=coverage_formset)
        )

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()

        return self.success_url
