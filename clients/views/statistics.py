from datetime import datetime, timedelta
from itertools import chain
from collections import defaultdict
from decimal import Decimal

from django.views.generic import TemplateView
from django.db import models as db_models
from django.db.models import Count, Sum, F, Q, Case, When, Prefetch
from django.db.models.functions import Coalesce
from django.core import urlresolvers
from django import utils

from simple_search import search
from utils import views_utils
from clients import models as clients_models
from inventory import models as inventory_models
from clients.views import views


class ClaimsStatistics(views_utils.PermissionMixin, TemplateView):
    template_name = "clients/statistics/claims_statistics.html"

    def get_permissions(self):
        permissions = {
            'permission': 'clients.view_statistics',
            'redirect': urlresolvers.reverse_lazy('index'),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Overdue claims
        overdue_claims = _overdue_claims()
        overdue_claims_rows_per_page = views_utils._get_paginate_by(
            self.request,
            'overdue_claims_rows_per_page'
        )
        context['overdue_claims_rows_per_page'] = overdue_claims_rows_per_page
        context['overdue_claims_list_paginated'] = views_utils._paginate(
            self.request,
            overdue_claims,
            'overdue_claims_page',
            overdue_claims_rows_per_page
        )

        # Outstanding fees, revenue, Claims overpaid, Claims underpaid
        stats = _stats()
        claims_greater_rows_per_page = views_utils._get_paginate_by(
            self.request,
            'claims_greater_rows_per_page'
        )
        context['claims_greater_rows_per_page'] = claims_greater_rows_per_page
        stats['claims_greater_list_paginated'] = views_utils._paginate(
            self.request,
            stats['claims_greater_list'],
            'claims_greater_page',
            claims_greater_rows_per_page
        )
        claims_less_rows_per_page = views_utils._get_paginate_by(
            self.request,
            'claims_less_rows_per_page'
        )
        context['claims_less_rows_per_page'] = claims_less_rows_per_page
        stats['claims_less_list_paginated'] = views_utils._paginate(
            self.request,
            stats['claims_less_list'],
            'claims_less_page',
            claims_less_rows_per_page
        )
        context['stats'] = stats

        # Insurance providers date filter
        if ('df' in self.request.GET) and self.request.GET['df'].strip():
            query_string = self.request.GET['df']
            context['df'] = query_string
        if ('dt' in self.request.GET) and self.request.GET['dt'].strip():
            query_string = self.request.GET['dt']
            context['dt'] = query_string
        insurances = _insurance_providers_stats(self.request)
        context['insurances'] = insurances
        context['insurances_totals'] = _insurance_providers_stats_totals(
            insurances
        )

        return context


class InventoryOrdersStatistics(views_utils.PermissionMixin, TemplateView):
    template_name = "clients/statistics/inventory_orders_statistics.html"

    def get_permissions(self):
        permissions = {
            'permission': 'clients.view_statistics',
            'redirect': urlresolvers.reverse_lazy('index'),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        totals = self._in_stock_and_cost_of_inventory()
        context['total_in_stock'] = totals['total_in_stock']
        context['total_cost_of_inventory'] = totals['total_cost_of_inventory']

        context['shoes'] = self._top_ten_best_sellers()

        context['old_ordered_date_orders'] = _old_ordered_date_orders()
        context['old_arrived_date_orders'] = _old_arrvied_date_orders()
        context['order_class'] = inventory_models.Order
        context['ordered_hidden_fields'] = ['arrived_date', 'dispensed_date']
        context['arrived_hidden_fields'] = ['dispensed_date']

        return context

    def _in_stock_and_cost_of_inventory(self):
        total_in_stock = 0
        total_cost_of_inventory = Decimal(0.00)
        shoe_attributes_objects = inventory_models.ShoeAttributes.objects
        shoe_attributes_list = shoe_attributes_objects.select_related(
            'shoe'
        ).prefetch_related(
            db_models.Prefetch(
                'shoeorder_set',
                # see dispensed() in clients_models.ShoeAttributes
                queryset=inventory_models.ShoeOrder.objects.filter(
                    dispensed_date__isnull=False,  # with
                    ordered_date__isnull=True  # without
                ),
                to_attr='dispensed_set'
            ),
            db_models.Prefetch(
                'shoeorder_set',
                # see returned() in clients_models.ShoeAttributes
                queryset=inventory_models.ShoeOrder.objects.filter(
                    returned_date__isnull=False  # with
                ),
                to_attr='returned_set'
            )
        )
        for shoe_attributes in shoe_attributes_list:
            # use prefetch above
            actual_quantity = (
                shoe_attributes.quantity -
                len(shoe_attributes.dispensed_set) +
                len(shoe_attributes.returned_set)
            )
            total_in_stock += actual_quantity
            total_cost_of_inventory += (
                actual_quantity * shoe_attributes.shoe.cost
            )

        return {'total_in_stock': total_in_stock,
                'total_cost_of_inventory': total_cost_of_inventory}

    def _top_ten_best_sellers(self):
        shoes = inventory_models.Shoe.objects.annotate(
            num_orders=Count('shoeattributes__shoeorder')
        ).order_by('-num_orders')[:10]

        return shoes


def insurance_stats_report(request):
    insurances = _insurance_providers_stats(request)

    return views.render_to_pdf(
        request,
        'clients/pdfs/insurance_stats.html',
        {
            'title': 'Insurance Statistics Report',
            'pagesize': 'A4 landscape',
            'stats': _stats(),
            'insurances': insurances,
            'insurances_totals': _insurance_providers_stats_totals(insurances)
        }
    )


def overdue_claims_report(request):
    return views.render_to_pdf(
        request,
        'clients/pdfs/overdue_claims.html',
        {
            'title': 'Overdue Claims Report',
            'pagesize': 'A4 landscape',
            'overdue_claims': _overdue_claims(),
            'claim_class': clients_models.Claim,
            'hidden_fields': ['fileset', 'insurance_paid_date']
        }
    )


def old_ordered_date_orders_report(request):
    return views.render_to_pdf(
        request,
        'clients/pdfs/old_orders.html',
        {
            'title': 'Old Ordered Date Orders Report',
            'pagesize': 'A4 landscape',
            'orders': _old_ordered_date_orders(),
            'order_class': inventory_models.Order,
            'hidden_fields': ['arrived_date', 'dispensed_date']
        }
    )


def old_arrived_date_orders_report(request):
    return views.render_to_pdf(
        request,
        'clients/pdfs/old_orders.html',
        {
            'title': 'Old Arrived Date Orders Report',
            'pagesize': 'A4 landscape',
            'orders': _old_arrvied_date_orders(),
            'order_class': inventory_models.Order,
            'hidden_fields': ['dispensed_date']
        }
    )


def _stats():
    revenue_claims = clients_models.Claim.objects.select_related(
        'patient__client',
        'patient__dependent__primary',
    ).prefetch_related(
        'insurances',
    ).annotate(
        invoice_revenue=(
            Coalesce(F('invoice__payment_made'), 0) +
            Coalesce(F('invoice__deposit'), 0)
        ),
        expected_back_revenue=Sum(
            Case(
                When(
                    Q(insurances__benefits='a') &
                    Q(claimcoverage__actual_paid_date__isnull=False),
                    then='claimcoverage__expected_back',
                ),
                default=0,
            )
        ),
    ).annotate(
        total_revenue=F('expected_back_revenue') + F('invoice_revenue')
    ).order_by('id')

    outstanding_claims = clients_models.Claim.objects.select_related(
        'patient__client',
        'patient__dependent__primary',
    ).annotate(
        total_amount=Sum((
            # TODO: need to use get_unit_price
            Coalesce(F('claimcoverage__claimitem__item__unit_price'), 0) *
            Coalesce(F('claimcoverage__claimitem__quantity'), 0)
        ), output_field=db_models.DecimalField()),
    ).order_by('id')

    # annotatations are done via join and not subquery, this duplicates
    #  data and makes it so that the two above queries cannot be joined
    non_assignment_invoice_revenue = 0
    assignment_invoice_revenue = 0
    expected_back_revenue = 0
    outstanding_fees = 0
    outstanding_assignment_clients_set = set()
    outstanding_non_assignment_clients_set = set()
    claims = zip(revenue_claims, outstanding_claims)
    claims_greater_list = []
    claims_less_list = []
    for revenue_claim, outstanding_claim in claims:
        if revenue_claim.id != outstanding_claim.id:
            raise Exception(
                "ID's do not match. %s %s" % (
                    revenue_claim.id, outstanding_claim.id
                )
            )

        amount_remaining = 0
        if outstanding_claim.total_amount > revenue_claim.total_revenue:
            claims_less_list.append(revenue_claim)
            amount_remaining = (
                outstanding_claim.total_amount -
                revenue_claim.total_revenue
            )
            has_na = False
            has_a = False
            for insurance in revenue_claim.insurances.all():
                if insurance.benefits == 'na':
                    has_na = True
                elif insurance.benefits == 'a':
                    has_a = True
            if has_na:
                outstanding_non_assignment_clients_set.add(
                    revenue_claim.patient_id
                )
            if has_a:
                outstanding_assignment_clients_set.add(
                    revenue_claim.patient_id
                )
            if not has_na and not has_a:
                raise Exception(
                    'Unhandled benefit type for %s' % (
                        revenue_claim,
                    )
                )
        elif outstanding_claim.total_amount < revenue_claim.total_revenue:
            claims_greater_list.append(revenue_claim)

        has_na = False
        has_a = False
        for insurance in revenue_claim.insurances.all():
            if insurance.benefits == 'na':
                has_na = True
            elif insurance.benefits == 'a':
                has_a = True
        if has_na:
            non_assignment_invoice_revenue += \
                revenue_claim.invoice_revenue
        if has_a:
            assignment_invoice_revenue += \
                revenue_claim.invoice_revenue
        if not has_na and not has_a:
            raise Exception(
                'Unhandled benefit type for %s' % (
                    revenue_claim,
                )
            )

        expected_back_revenue += revenue_claim.expected_back_revenue
        outstanding_fees += amount_remaining

    invoice_revenue = (
        non_assignment_invoice_revenue + assignment_invoice_revenue
    )
    total_revenue = invoice_revenue + expected_back_revenue
    outstanding_assignment_clients = len(
        outstanding_assignment_clients_set
    )
    outstanding_non_assignment_clients = len(
        outstanding_non_assignment_clients_set
    )
    stats_dict = {
        'non_assignment_invoice_revenue': non_assignment_invoice_revenue,
        'assignment_invoice_revenue': assignment_invoice_revenue,
        'invoice_revenue': invoice_revenue,
        'expected_back_revenue': expected_back_revenue,
        'outstanding_fees': outstanding_fees,
        'total_revenue': total_revenue,
        'total': total_revenue + outstanding_fees,
        'outstanding_assignment_clients': outstanding_assignment_clients,
        'outstanding_non_assignment_clients':
            outstanding_non_assignment_clients,
        'total_outstanding_clients': (
            outstanding_assignment_clients +
            outstanding_non_assignment_clients
        ),
        'claims_greater_list': claims_greater_list,
        'claims_less_list': claims_less_list,
    }

    return stats_dict


def _insurance_providers_stats(request):
    # Expected back and number of claims
    date_queryset = search.simple_search(
        request,
        model=clients_models.Insurance,
        date_fields=["claim__submitted_datetime"]
    )
    insurances_expected_back = date_queryset.values(
        'provider',
    ).annotate(
        non_assignment_expected_back=Sum(Case(
            When(
                benefits='na',
                then='claim__claimcoverage__expected_back',
            ),
            default=0,
        )),
        assignment_expected_back=Sum(Case(
            When(
                Q(benefits='a') &
                Q(claim__claimcoverage__actual_paid_date__isnull=False),
                then='claim__claimcoverage__expected_back',
            ),
            default=0,
        )),
        pending_assignment_expected_back=Sum(Case(
            When(
                Q(benefits='a') &
                Q(claim__claimcoverage__actual_paid_date__isnull=True),
                then='claim__claimcoverage__expected_back',
            ),
            default=0,
        )),
        num_claims=Count('claim', distinct=True),
    ).annotate(
        total_assignment_expected_back=(
            F('assignment_expected_back') +
            F('pending_assignment_expected_back')
        ),
    )

    # Invoices
    date_queryset = search.simple_search(
        request,
        model=clients_models.Insurance,
        date_fields=["claim__submitted_datetime"]
    )
    insurances_invoices = date_queryset.values(
        'provider',
    ).annotate(
        non_assignment_invoice_revenue=Sum(Case(
            When(
                benefits='na',
                then=(
                    Coalesce(F('claim__invoice__payment_made'), 0) +
                    Coalesce(F('claim__invoice__deposit'), 0)
                )
            ),
            default=0,
        )),
        assignment_invoice_revenue=Sum(Case(
            When(
                benefits='a',
                then=(
                    Coalesce(F('claim__invoice__payment_made'), 0) +
                    Coalesce(F('claim__invoice__deposit'), 0)
                )
            ),
            default=0,
        )),
    ).annotate(
        total_invoice_revenue=(
            F('non_assignment_invoice_revenue') +
            F('assignment_invoice_revenue')
        ),
    )

    # Amount claimed
    date_queryset = search.simple_search(
        request,
        model=clients_models.Insurance,
        date_fields=["claim__submitted_datetime"]
    )
    insurances_amount_claimed = date_queryset.values(
        'provider'
    ).annotate(
        assignment_amount_claimed=Sum(Case(
            When(
                benefits='a',
                then=Coalesce(
                    # TODO: use get_unit_price
                    F('claim__claimcoverage__claimitem__item__unit_price'),
                    0
                ) *
                Coalesce(
                    F('claim__claimcoverage__claimitem__quantity'),
                    0
                )
            ),
            default=0,
            output_field=db_models.DecimalField(),
        )),
        non_assignment_amount_claimed=Sum(Case(
            When(
                benefits='na',
                then=Coalesce(
                    # TODO: use get_unit_price
                    F('claim__claimcoverage__claimitem__item__unit_price'),
                    0
                ) *
                Coalesce(
                    F('claim__claimcoverage__claimitem__quantity'),
                    0
                )
            ),
            default=0,
            output_field=db_models.DecimalField(),
        )),
    ).annotate(
        amount_claimed__sum=db_models.ExpressionWrapper((
            F('assignment_amount_claimed') + F('non_assignment_amount_claimed')
        ), output_field=db_models.DecimalField())
    )

    # Combine the 3 above query's results into one
    insurances_chain = chain(
        insurances_expected_back,
        insurances_invoices,
        insurances_amount_claimed,
    )

    insurances = _merge_by_key(insurances_chain, 'provider')
    sorted_insurances = sorted(insurances,
                               key=lambda insurance: insurance['provider'])

    return sorted_insurances


def _insurance_providers_stats_totals(insurances):
    insurances_totals = {
        'num_claims': 0,
        'non_assignment_expected_back': 0,
        'assignment_expected_back': 0,
        'pending_assignment_expected_back': 0,
        'total_assignment_expected_back': 0,
        'expected_back__sum': 0,
        'non_assignment_invoice_revenue': 0,
        'assignment_invoice_revenue': 0,
        'total_invoice_revenue': 0,
        'total_revenue': 0,
        'non_assignment_amount_claimed': 0,
        'assignment_amount_claimed': 0,
        'amount_claimed__sum': 0
    }
    for insurance in insurances:
        if 'num_claims' in insurance:
            insurances_totals['num_claims'] += \
                (insurance['num_claims'] or 0)
        else:
            insurance['num_claims'] = 0
        if 'non_assignment_amount_claimed' in insurance:
            insurances_totals['non_assignment_amount_claimed'] += \
                (insurance['non_assignment_amount_claimed'] or 0)
        else:
            insurance['non_assignment_amount_claimed'] = 0
        if 'assignment_amount_claimed' in insurance:
            insurances_totals['assignment_amount_claimed'] += \
                (insurance['assignment_amount_claimed'] or 0)
        else:
            insurance['assignment_amount_claimed'] = 0
        if 'non_assignment_expected_back' in insurance:
            insurances_totals['non_assignment_expected_back'] += \
                (insurance['non_assignment_expected_back'] or 0)
        else:
            insurance['non_assignment_expected_back'] = 0
        if 'assignment_expected_back' in insurance:
            insurances_totals['assignment_expected_back'] += \
                (insurance['assignment_expected_back'] or 0)
        else:
            insurance['assignment_expected_back'] = 0
        if 'pending_assignment_expected_back' in insurance:
            insurances_totals['pending_assignment_expected_back'] += \
                (insurance['pending_assignment_expected_back'] or 0)
        else:
            insurance['pending_assignment_expected_back'] = 0
        if 'total_assignment_expected_back' in insurance:
            insurances_totals['total_assignment_expected_back'] += \
                (insurance['total_assignment_expected_back'] or 0)
        else:
            insurance['total_assignment_expected_back'] = 0
        if 'non_assignment_invoice_revenue' in insurance:
            insurances_totals['non_assignment_invoice_revenue'] += \
                (insurance['non_assignment_invoice_revenue'] or 0)
        else:
            insurance['non_assignment_invoice_revenue'] = 0
        if 'assignment_invoice_revenue' in insurance:
            insurances_totals['assignment_invoice_revenue'] += \
                (insurance['assignment_invoice_revenue'] or 0)
        else:
            insurance['assignment_invoice_revenue'] = 0

    # Totals of totals
    insurances_totals['amount_claimed__sum'] = (
        (insurances_totals['non_assignment_amount_claimed'] or 0) +
        (insurances_totals['assignment_amount_claimed'] or 0)
    )
    insurances_totals['expected_back__sum'] = (
        (insurances_totals['non_assignment_expected_back'] or 0) +
        (insurances_totals['total_assignment_expected_back'] or 0)
    )
    insurances_totals['total_invoice_revenue'] = (
        (insurances_totals['non_assignment_invoice_revenue'] or 0) +
        (insurances_totals['assignment_invoice_revenue'] or 0)
    )
    insurances_totals['total_revenue'] = (
        (insurances_totals['total_invoice_revenue'] or 0) +
        (insurances_totals['assignment_expected_back'] or 0)
    )

    return insurances_totals


def _merge_by_key(dicts, key):
    merged = defaultdict(dict)

    for dict_ in dicts:
        merged[dict_[key]].update(dict_)

    return merged.values()


def _overdue_claims():
    cutoff = utils.timezone.now() - timedelta(days=30)
    overdue_claims = clients_models.Claim.objects.select_related(
        'patient__client',
        'patient__dependent__primary',
    ).filter(
        submitted_datetime__lte=cutoff,
        claimcoverage__actual_paid_date__isnull=True
    ).order_by('submitted_datetime').distinct()

    return overdue_claims


def _old_ordered_date_orders():
    cutoff = datetime.now() - timedelta(days=30)
    orders = inventory_models.Order.objects.select_related(
        'claimant__client',
        'claimant__dependent__primary',
        'shoeorder__shoe_attributes__shoe',
        'coverageorder',
        'adjustmentorder'
    ).filter(
        dispensed_date__isnull=True,
        arrived_date__isnull=True,
        ordered_date__lte=cutoff,
    )

    return orders


def _old_arrvied_date_orders():
    cutoff = datetime.now() - timedelta(days=30)
    orders = inventory_models.Order.objects.select_related(
        'claimant__client',
        'claimant__dependent__primary',
        'shoeorder__shoe_attributes__shoe',
        'coverageorder',
        'adjustmentorder'
    ).filter(
        dispensed_date__isnull=True,
        arrived_date__lte=cutoff,
    )

    return orders
