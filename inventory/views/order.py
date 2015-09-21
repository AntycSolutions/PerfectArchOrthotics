import collections
from decimal import Decimal

from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages

from utils.search import get_query, get_date_query
from inventory import models
from inventory.forms import forms


class ListOrderView(ListView):
    template_name = "utils/generics/list.html"
    model = models.Order
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
        context = super(ListOrderView, self).get_context_data(**kwargs)
        Create = collections.namedtuple(
            'Create', ['model_name', 'indefinite_article']
        )
        context['create_list'] = [
            Create(models.ShoeOrder._meta.verbose_name, 'a'),
            Create(models.CoverageOrder._meta.verbose_name, 'a'),
            Create(models.AdjustmentOrder._meta.verbose_name, 'an'),
        ]
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['rows_per_page'] = self.request.session.get(
            'rows_per_page', self.paginate_by)
        context['datesearch'] = True

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            context['q'] = query_string
        if ('df' in self.request.GET) and self.request.GET['df'].strip():
            query_string = self.request.GET['df']
            context['df'] = query_string
        if ('dt' in self.request.GET) and self.request.GET['dt'].strip():
            query_string = self.request.GET['dt']
            context['dt'] = query_string

        Option = collections.namedtuple('Option', ['value',
                                                   'value_display',
                                                   'selected'])
        Select = collections.namedtuple('Select', ['label', 'options'])
        order_types = []
        for order_type in models.Order.ORDER_TYPES:
            if ("order_type" in self.request.GET
                    and self.request.GET["order_type"].strip()
                    and self.request.GET["order_type"] == order_type[0]):
                order_types.append(Option(order_type[0], order_type[1], True))
            else:
                order_types.append(Option(order_type[0], order_type[1], False))
        selects = collections.OrderedDict()
        selects.update({"order_type": Select("Order Type", order_types)})
        context['selects'] = selects

        return context

    def get_queryset(self):
        # Start from all, drilldown to q
        queryset = super(ListOrderView, self).get_queryset()

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            fields = ['claimant__first_name', 'claimant__last_name',
                      'description',
                      'coverageorder__vendor',
                      'shoeorder__shoe_attributes__shoe__brand']
            query_string = self.request.GET['q']
            order_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(order_query)
            else:
                queryset = models.Order.objects.filter(order_query)

        if ('order_type' in self.request.GET
                and self.request.GET['order_type'].strip()):
            fields = ['order_type']
            query_string = self.request.GET['order_type']
            order_query = get_query(query_string, fields, exact=True)
            if queryset:
                queryset = queryset.filter(order_query)
            else:
                queryset = models.Order.objects.filter(order_query)

        if (('df' in self.request.GET) and self.request.GET['df'].strip()
                and ('dt' in self.request.GET)
                and self.request.GET['dt'].strip()):
            date_fields = ['ordered_date', 'arrived_date', 'dispensed_date']
            query_date_from_string = self.request.GET['df']
            query_date_to_string = self.request.GET['dt']
            order_query = get_date_query(query_date_from_string,
                                         query_date_to_string, date_fields)
            if order_query:
                if queryset:
                    queryset = queryset.filter(order_query)
                else:
                    queryset = models.Order.objects.filter(order_query)
            else:
                messages.add_message(self.request, messages.WARNING,
                                     "Invalid date. Please use MM/DD/YYYY.")
        elif ('df' in self.request.GET) and self.request.GET['df'].strip():
            date_fields = ['ordered_date', 'arrived_date', 'dispensed_date']
            query_date_from_string = self.request.GET['df']
            order_query = get_date_query(query_date_from_string,
                                         None, date_fields)
            if order_query:
                if queryset:
                    queryset = queryset.filter(order_query)
                else:
                    queryset = models.Order.objects.filter(order_query)
            else:
                messages.add_message(self.request, messages.WARNING,
                                     "Invalid date. Please use MM/DD/YYYY.")
        elif ('dt' in self.request.GET) and self.request.GET['dt'].strip():
            date_fields = ['ordered_date', 'arrived_date', 'dispensed_date']
            query_date_to_string = self.request.GET['dt']
            order_query = get_date_query(None,
                                         query_date_to_string, date_fields)
            if order_query:
                if queryset:
                    queryset = queryset.filter(order_query)
                else:
                    queryset = models.Order.objects.filter(order_query)
            else:
                messages.add_message(self.request, messages.WARNING,
                                     "Invalid date. Please use MM/DD/YYYY.")

        return queryset.distinct().extra(
            select={
                'null_both': ' inventory_order.dispensed_date'
                             ' is null'
                             ' and inventory_order.ordered_date'
                             ' is null',
                'null_dispensed_date': ' inventory_order.dispensed_date'
                                       ' is null',
                # 'null_ordered_date': ' inventory_order.ordered_date'
                #                      ' is null',
            }
        ).order_by(
            'null_both',
            'null_dispensed_date',
            '-dispensed_date',
            '-ordered_date',
            # '-null_ordered_date',
        )


class ShoeCreateOrderView(CreateView):
    template_name = 'utils/generics/create.html'
    model = models.ShoeOrder
    form_class = forms.ShoeOrderForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        order_form = form_class(**self.get_form_kwargs())
        if "person_pk" in self.kwargs:
            person_pk = self.kwargs["person_pk"]
            order_form.fields['claimant'].initial = person_pk
        return order_form

    def form_valid(self, form):
        self.object = form.save(commit=False)

        client_credit = self.object.claimant.get_client().credit()
        shoe_credit_value = self.object.shoe_attributes.shoe.credit_value

        if shoe_credit_value > client_credit:
            messages.add_message(
                self.request, messages.WARNING,
                "Shoe's Credit Value (%s) is greater than "
                "Client's Credit (%s)." % (shoe_credit_value,
                                           client_credit))
            # return self.form_invalid(form)

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ShoeCreateOrderView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['autocomplete'] = True
        context['cancel_url'] = reverse('order_list')

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class CoverageCreateOrderView(CreateView):
    template_name = 'utils/generics/create.html'
    model = models.CoverageOrder
    form_class = forms.CoverageOrderForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        order_form = form_class(**self.get_form_kwargs())
        if "person_pk" in self.kwargs:
            person_pk = self.kwargs["person_pk"]
            order_form.fields['claimant'].initial = person_pk
        return order_form

    def form_valid(self, form):
        self.object = form.save(commit=False)

        client_credit = self.object.claimant.get_client().credit()
        credit_value = self.object.credit_value

        if credit_value > client_credit:
            messages.add_message(
                self.request, messages.WARNING,
                "Credit Value (%s) is greater than "
                "Client's Credit (%s)." % (credit_value,
                                           client_credit))
            # return self.form_invalid(form)

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(
            CoverageCreateOrderView,
            self
        ).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['cancel_url'] = reverse('order_list')

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class AdjustmentCreateOrderView(CreateView):
    template_name = 'utils/generics/create.html'
    model = models.AdjustmentOrder
    form_class = forms.AdjustmentOrderForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        order_form = form_class(**self.get_form_kwargs())
        if "person_pk" in self.kwargs:
            person_pk = self.kwargs["person_pk"]
            order_form.fields['claimant'].initial = person_pk
        return order_form

    def form_valid(self, form):
        self.object = form.save()

        client_credit = self.object.claimant.get_client().credit()
        adjustment_credit_value = self.object.credit_value

        if adjustment_credit_value > client_credit:
            messages.add_message(
                self.request, messages.WARNING,
                "Adjustment's Credit Value (%s) is greater than "
                "Client's Credit (%s)." % (adjustment_credit_value,
                                           client_credit))

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(
            AdjustmentCreateOrderView,
            self
        ).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['cancel_url'] = reverse('order_list')

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class ShoeDetailOrderView(DetailView):
    template_name = "utils/generics/detail.html"
    model = models.ShoeOrder

    def get_context_data(self, **kwargs):
        context = super(ShoeDetailOrderView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        return context


class CoverageDetailOrderView(DetailView):
    template_name = "utils/generics/detail.html"
    model = models.CoverageOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name

        return context


class AdjustmentDetailOrderView(DetailView):
    template_name = "utils/generics/detail.html"
    model = models.AdjustmentOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name

        return context


class ShoeUpdateOrderView(UpdateView):
    template_name = 'utils/generics/update.html'
    model = models.ShoeOrder
    form_class = forms.ShoeOrderForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.shoe_attributes:
            client_credit = self.object.claimant.get_client().credit()
            shoe_credit_value = self.object.shoe_attributes.shoe.credit_value
            old_shoe_attributes = self.get_object().shoe_attributes
            if old_shoe_attributes:
                client_credit += old_shoe_attributes.shoe.credit_value
            if shoe_credit_value > client_credit:
                messages.add_message(
                    self.request, messages.WARNING,
                    "Shoe's Credit Value (%s) is greater than "
                    "Client's Credit (%s)." % (shoe_credit_value,
                                               client_credit))
                # return self.form_invalid(form)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ShoeUpdateOrderView, self).get_context_data(**kwargs)

        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['autocomplete'] = True
        context['cancel_url'] = reverse('shoe_order_detail',
                                        kwargs={'pk': self.object.pk})

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class CoverageUpdateOrderView(UpdateView):
    template_name = 'utils/generics/update.html'
    model = models.CoverageOrder
    form_class = forms.CoverageOrderForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        client_credit = self.object.claimant.get_client().credit()
        credit_value = self.object.credit_value
        old_credit_value = self.get_object().credit_value
        if old_credit_value:
            client_credit += old_credit_value
        if credit_value > client_credit:
            messages.add_message(
                self.request, messages.WARNING,
                "Credit Value (%s) is greater than "
                "Client's Credit (%s)." % (credit_value,
                                           client_credit))
            # return self.form_invalid(form)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['cancel_url'] = reverse('coverage_order_detail',
                                        kwargs={'pk': self.object.pk})

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class AdjustmentUpdateOrderView(UpdateView):
    template_name = 'utils/generics/update.html'
    model = models.AdjustmentOrder
    form_class = forms.AdjustmentOrderForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        client_credit = Decimal(self.object.claimant.get_client().credit())
        credit_value = self.object.credit_value
        old_credit_value = self.get_object().credit_value
        if old_credit_value:
            client_credit += old_credit_value
        if credit_value > client_credit:
            messages.add_message(
                self.request, messages.WARNING,
                "Credit Value (%s) is greater than "
                "Client's Credit (%s)." % (credit_value,
                                           client_credit))
            # return self.form_invalid(form)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        context['cancel_url'] = reverse('adjustment_order_detail',
                                        kwargs={'pk': self.object.pk})

        return context

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()
        return self.success_url


class ShoeDeleteOrderView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = models.ShoeOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('order_list')
        return self.success_url


class CoverageDeleteOrderView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = models.CoverageOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('order_list')
        return self.success_url


class AdjustmentDeleteOrderView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = models.AdjustmentOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('order_list')
        return self.success_url
