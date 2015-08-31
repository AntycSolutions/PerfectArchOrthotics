import collections

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.forms import fields as form_fields
from django.forms.models import BaseInlineFormSet

from utils.search import get_query
from utils import model_utils
from inventory.models import Shoe, ShoeAttributes


class CreateShoeView(CreateView):
    template_name = 'utils/generics/create.html'
    model = Shoe
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        shoe_form = self.get_form(form_class)

        ShoeShoeAttributesFormSet = inlineformset_factory(
            Shoe,
            ShoeAttributes,
            extra=1,
            exclude=('shoe',)
        )
        shoe_attributes_formset = ShoeShoeAttributesFormSet()

        return self.render_to_response(
            self.get_context_data(
                form=shoe_form,
                formset=shoe_attributes_formset
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        shoe_form = self.get_form(form_class)

        ShoeShoeAttributesFormSet = inlineformset_factory(
            Shoe,
            ShoeAttributes,
            extra=1,
            exclude=('shoe',)
        )
        shoe_attributes_formset = ShoeShoeAttributesFormSet(request.POST)

        for field in shoe_form:
            if isinstance(field.field, form_fields.ImageField):
                field.field.validators = [model_utils._validate_image]

        if (shoe_form.is_valid()
                and shoe_attributes_formset.is_valid()):
            return self.form_valid(
                shoe_form,
                shoe_attributes_formset
            )
        else:
            return self.form_invalid(
                shoe_form,
                shoe_attributes_formset
            )

    def form_valid(self, form,
                   shoe_attributes_formset
                   ):
        self.object = form.save()
        try:
            shoe_attributes_formset.instance = self.object
            shoe_attributes_formset.save()
        except IntegrityError as e:
            if "UNIQUE" in str(e) or "unique" in str(e):
                self.object.delete()
                messages.add_message(self.request, messages.ERROR,
                                     "That Size already exists for this Shoe.")
                return self.form_invalid(form, shoe_attributes_formset)
            raise e

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,
                     shoe_attributes_formset
                     ):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=shoe_attributes_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super(CreateShoeView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        context['form_type'] = 'multipart/form-data'
        context['inline_model_name'] = ShoeAttributes._meta.verbose_name
        context['cancel_url'] = reverse('shoe_list')

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class ListShoeView(ListView):
    template_name = "utils/generics/list.html"
    model = Shoe
    paginate_by = 20

    def get_paginate_by(self, queryset):
        if self.request.session.get('rows_per_page', False):
            self.paginate_by = self.request.session['rows_per_page']
        if ('rows_per_page' in self.request.GET
                and self.request.GET['rows_per_page'].strip()):
            self.paginate_by = self.request.GET['rows_per_page']
            self.request.session['rows_per_page'] = self.paginate_by
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(ListShoeView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        context['rows_per_page'] = self.request.session.get(
            'rows_per_page', self.paginate_by)

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            context['q'] = query_string

        Option = collections.namedtuple('Option', ['value',
                                                   'value_display',
                                                   'selected'])
        Select = collections.namedtuple('Select', ['label', 'options'])
        categories = []
        for category in Shoe.CATEGORIES:
            if ("category" in self.request.GET
                    and self.request.GET["category"].strip()
                    and self.request.GET["category"] == category[0]):
                categories.append(Option(category[0], category[1], True))
            else:
                categories.append(Option(category[0], category[1], False))
        sizes = []
        for size in ShoeAttributes.SIZES:
            if ("size" in self.request.GET
                    and self.request.GET["size"].strip()
                    and self.request.GET["size"] == size[0]):
                sizes.append(Option(size[0], size[1], True))
            else:
                sizes.append(Option(size[0], size[1], False))
        selects = collections.OrderedDict()
        selects.update({"category": Select("Category", categories)})
        selects.update({"size": Select("Size", sizes)})
        context['selects'] = selects

        return context

    def get_queryset(self):
        # Start from all, drilldown to q
        queryset = super(ListShoeView, self).get_queryset()

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            fields = ['brand', 'style', 'name', 'sku', 'colour', 'description']
            query_string = self.request.GET['q']
            shoe_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(shoe_query)
            else:
                queryset = Shoe.objects.filter(shoe_query)

        if ('category' in self.request.GET
                and self.request.GET['category'].strip()):
            fields = ['category']
            query_string = self.request.GET['category']
            shoe_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(shoe_query)
            else:
                queryset = Shoe.objects.filter(shoe_query)

        if ('size' in self.request.GET
                and self.request.GET['size'].strip()):
            fields = ['shoeattributes__size']
            query_string = self.request.GET['size']
            shoe_query = get_query(query_string, fields, exact=True)
            if queryset:
                queryset = queryset.filter(shoe_query)
            else:
                queryset = Shoe.objects.filter(shoe_query)

        return queryset.distinct()


class DetailShoeView(DetailView):
    template_name = "utils/generics/detail.html"
    model = Shoe

    def get_context_data(self, **kwargs):
        context = super(DetailShoeView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        context['inline_set'] = self.object.shoeattributes_set.extra(
            select={'size_int': 'cast(size as real)'}
        ).order_by('size_int')
        context['inline_model_name'] = ShoeAttributes._meta.verbose_name
        return context


class BaseShoeShoeAttributesFormSet(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseShoeShoeAttributesFormSet, self).add_fields(
            form, index
        )
        ordered_fields = collections.OrderedDict()
        for k, v in form.fields.items():
            if k == "quantity":
                v.widget = form_fields.HiddenInput()
            ordered_fields.update({k: v})
            if k == "id":
                ordered_fields.update(
                    {'new_quantity': form_fields.IntegerField(
                        label="Quantity", initial=(
                            form.instance.quantity - form.instance.dispensed()
                        )
                     )
                     }
                )

        form.fields = ordered_fields

    def save_existing(self, form, instance, commit=True):
        new_quantity = form.cleaned_data['new_quantity']

        obj = form.save(commit=commit)
        obj.quantity = new_quantity + obj.dispensed()
        if commit:
            obj.save()

        return obj


class UpdateShoeView(UpdateView):
    template_name = 'utils/generics/update.html'
    model = Shoe
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        shoe_form = self.get_form(form_class)

        ShoeShoeAttributesFormSet = inlineformset_factory(
            Shoe,
            ShoeAttributes,
            formset=BaseShoeShoeAttributesFormSet,
            extra=1,
            exclude=('shoe',)
        )
        shoe_attributes_formset = ShoeShoeAttributesFormSet(
            instance=self.object
        )

        return self.render_to_response(
            self.get_context_data(
                form=shoe_form,
                formset=shoe_attributes_formset
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        shoe_form = self.get_form(form_class)

        ShoeShoeAttributesFormSet = inlineformset_factory(
            Shoe,
            ShoeAttributes,
            formset=BaseShoeShoeAttributesFormSet,
            extra=1,
            exclude=('shoe',)
        )
        shoe_attributes_formset = ShoeShoeAttributesFormSet(
            request.POST, instance=self.object)

        for field in shoe_form:
            if isinstance(field.field, form_fields.ImageField):
                field.field.validators = [model_utils._validate_image]

        if (shoe_form.is_valid()
                and shoe_attributes_formset.is_valid()):
            return self.form_valid(
                shoe_form,
                shoe_attributes_formset
            )
        else:
            return self.form_invalid(
                shoe_form,
                shoe_attributes_formset
            )

    def form_valid(self, form, shoe_attributes_formset):
        self.object = form.save(commit=False)
        try:
            shoe_attributes_formset.save()
        except IntegrityError as e:
            if "UNIQUE" in str(e) or "unique" in str(e):
                messages.add_message(self.request, messages.ERROR,
                                     "That Size already exists for this Shoe.")
                return self.form_invalid(form, shoe_attributes_formset)
            raise e

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, shoe_attributes_formset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=shoe_attributes_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        context['form_type'] = 'multipart/form-data'
        context['inline_model_name'] = ShoeAttributes._meta.verbose_name
        context['inline_model_name_plural'] = \
            ShoeAttributes._meta.verbose_name_plural
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class DeleteShoeView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = Shoe

    def get_context_data(self, **kwargs):
        context = super(DeleteShoeView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('shoe_list')
        return self.success_url
