# TODO: qualify imports
import collections

from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from simple_search.utils import get_query
from clients.models import Item


class CreateItemView(mixins.UserPassesTestMixin, CreateView):
    template_name = 'utils/generics/create.html'
    model = Item
    fields = '__all__'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super(CreateItemView, self).get_context_data(**kwargs)

        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['cancel_url'] = reverse('item_list')

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy(
            'item_detail', kwargs={'pk': self.object.pk}
        )

        return self.success_url


class ListItemView(ListView):
    template_name = "utils/generics/list.html"
    model = Item
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
        context = super(ListItemView, self).get_context_data(**kwargs)

        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['rows_per_page'] = self.request.session.get(
            'rows_per_page', self.paginate_by)
        context['search'] = True

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            context['q'] = query_string

        Option = collections.namedtuple('Option', ['value',
                                                   'value_display',
                                                   'selected'])
        Select = collections.namedtuple('Select', ['label', 'options'])
        genders = []
        for gender in Item.GENDERS:
            if ("gender" in self.request.GET
                    and self.request.GET["gender"].strip()
                    and self.request.GET["gender"] == gender[0]):
                genders.append(Option(gender[0], gender[1], True))
            else:
                genders.append(Option(gender[0], gender[1], False))
        coverage_types = []
        for coverage_type in Item.COVERAGE_TYPES:
            if ("coverage_type" in self.request.GET
                    and self.request.GET["coverage_type"].strip()
                    and self.request.GET["coverage_type"] == coverage_type[0]):
                coverage_types.append(
                    Option(coverage_type[0], coverage_type[1], True))
            else:
                coverage_types.append(
                    Option(coverage_type[0], coverage_type[1], False))
        selects = collections.OrderedDict()
        selects.update(
            {"coverage_type": Select("Coverage Type", coverage_types)})
        selects.update({"gender": Select("Gender", genders)})
        context['selects'] = selects

        return context

    def get_queryset(self):
        # Start from all, drilldown to q
        queryset = super(ListItemView, self).get_queryset()

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            fields = ['gender', 'product_code', 'description']
            query_string = self.request.GET['q']
            item_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(item_query)
            else:
                queryset = Item.objects.filter(item_query)

        if ('gender' in self.request.GET
                and self.request.GET['gender'].strip()):
            fields = ['gender']
            query_string = self.request.GET['gender']
            item_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(item_query)
            else:
                queryset = Item.objects.filter(item_query)

        if ('coverage_type' in self.request.GET
                and self.request.GET['coverage_type'].strip()):
            fields = ['coverage_type']
            query_string = self.request.GET['coverage_type']
            item_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(item_query)
            else:
                queryset = Item.objects.filter(item_query)

        return queryset


class DetailItemView(DetailView):
    template_name = "utils/generics/detail.html"
    model = Item

    def get_context_data(self, **kwargs):
        context = super(DetailItemView, self).get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name

        return context


class UpdateItemView(mixins.UserPassesTestMixin, UpdateView):
    template_name = 'utils/generics/update.html'
    model = Item
    fields = '__all__'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['cancel_url'] = reverse('item_list')

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('item_detail',
                                        kwargs={'pk': self.object.pk})

        return self.success_url


class DeleteItemView(
    mixins.UserPassesTestMixin, views_utils.PermissionMixin, DeleteView
):
    template_name = 'utils/generics/delete.html'
    model = Item

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_item',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('item_list')

        return self.success_url
