import collections

from django import http
from django.views import generic
from django.conf import settings
from django.core import urlresolvers
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients.views import views
from clients.forms import forms
from clients import models


class ReceiptCreate(mixins.UserPassesTestMixin, generic.CreateView):
    model = models.Receipt
    form_class = forms.ReceiptForm
    template_name = 'utils/generics/create.html'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = urlresolvers.reverse(
            'receipt_list', kwargs={'claim_pk': self.kwargs['claim_pk']}
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.claim_id = self.kwargs['claim_pk']
        self.object.save()

        return http.HttpResponseRedirect(self.get_success_url())


class ReceiptDetail(generic.DetailView):
    model = models.Receipt
    template_name = 'utils/generics/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name

        Button = collections.namedtuple('Button', ['url', 'text'])
        context['footer_buttons'] = [
            Button(
                urlresolvers.reverse(
                    'receipt',
                    kwargs={'pk': self.object.pk, '_type': 'MERCHANT'}
                ),
                'Merchant Copy'
            ),
            Button(
                urlresolvers.reverse(
                    'receipt',
                    kwargs={'pk': self.object.pk, '_type': 'CUSTOMER'}
                ),
                'Customer Copy',
            ),
        ]

        return context


class ReceiptUpdate(mixins.UserPassesTestMixin, generic.UpdateView):
    model = models.Receipt
    form_class = forms.ReceiptForm
    template_name = 'utils/generics/update.html'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context


class ReceiptDelete(
    mixins.UserPassesTestMixin,
    views_utils.PermissionMixin,
    generic.DeleteView,
):
    model = models.Receipt
    template_name = 'utils/generics/delete.html'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_receipt',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        return urlresolvers.reverse(
            'receipt_list', kwargs={'claim_pk': self.object.claim.pk}
        )


def receipt_view(request, pk, _type):
    types = ['MERCHANT', 'CUSTOMER']

    if _type not in types:
        raise Exception('Unhandled receipt type')

    receipt = models.Receipt.objects.get(pk=pk)

    bill_to = settings.BILL_TO[0][1]

    name = bill_to.split('\n')[0].replace('Inc.', '')
    address = bill_to.split('\n')[1].replace('.', '')
    city_province_postal_code = bill_to.split('\n')[2]
    city_province, postal_code = city_province_postal_code.split('  ')
    phone = bill_to.split('\n')[4].replace('Phone:', '')

    return views.render_to_pdf(
        request,
        'clients/pdfs/receipt.html',
        {
            'name': name,
            'address': address,
            'city_province': city_province,
            'postal_code': postal_code,
            'phone': phone,
            'receipt': receipt,
            'receipt_class': models.Receipt,
            'type': _type,
        }
    )


class ReceiptList(generic.ListView):
    model = models.Receipt
    template_name = 'utils/generics/list.html'
    paginate_by = 20

    def get_paginate_by(self, queryset):
        if self.request.session.get('rows_per_page', False):
            self.paginate_by = self.request.session['rows_per_page']
        if (
            'rows_per_page' in self.request.GET and
                self.request.GET['rows_per_page'].strip()
                ):
            self.paginate_by = self.request.GET['rows_per_page']
            self.request.session['rows_per_page'] = self.paginate_by

        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['rows_per_page'] = self.request.session.get(
            'rows_per_page', self.paginate_by)
        context['hidden_fields'] = [
            'MID',
            'TID',
            'REF',
            'batch',
            'RRN',
            'APPR',
            'trace',
            'AID',
            'TVR',
            'TSI',
        ]

        Create = collections.namedtuple(
            'Create', ['model_name', 'indefinite_article', 'url'],
        )
        context['create_list'] = [
            Create(
                models.Receipt._meta.verbose_name,
                'a',
                urlresolvers.reverse(
                    'receipt_create',
                    kwargs={'claim_pk': self.kwargs['claim_pk']}
                ),
            ),
        ]

        return context

    def get_queryset(self):
        # Start from all, drilldown to q
        queryset = super().get_queryset()

        queryset = queryset.filter(claim_id=self.kwargs['claim_pk'])

        return queryset
