from datetime import datetime, timedelta
from itertools import chain
from collections import defaultdict

from django.views.generic import TemplateView
from django.db.models import Count, Sum, F, Q, Case, When
from django.db.models.functions import Coalesce

from utils import views
from clients import models as clients_models
from inventory import models as inventory_models


class Statistics(TemplateView):
    template_name = "clients/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(Statistics, self).get_context_data(**kwargs)

        context['stats'] = self._stats()

        # Insurance company stats
        if ('df' in self.request.GET) and self.request.GET['df'].strip():
            query_string = self.request.GET['df']
            context['df'] = query_string
        if ('dt' in self.request.GET) and self.request.GET['dt'].strip():
            query_string = self.request.GET['dt']
            context['dt'] = query_string
        insurances = self._insurance_company_stats()
        context['insurances'] = insurances
        context['insurances_totals'] = self._insurance_company_stats_totals(
            insurances
        )

        context['shoes'] = self._top_ten_best_sellers()

        context['old_ordered_date_orders'] = self._old_ordered_date_orders()
        context['old_arrived_date_orders'] = self._old_arrvied_date_orders()

        return context

    def _stats(self):
        revenue_claims = clients_models.Claim.objects.annotate(
            revenue=(
                Coalesce(F('invoice__payment_made'), 0)
                + Coalesce(F('invoice__deposit'), 0)
            ),
            expected_back_revenue=Sum(
                Case(
                    When(
                        Q(insurance__benefits='a')
                        & Q(claimcoverage__actual_paid_date__isnull=False),
                        then='claimcoverage__expected_back',
                    ),
                    default=0,
                )
            ),
        ).annotate(
            total_revenue=F('expected_back_revenue') + F('revenue')
        )

        outstanding_claims = clients_models.Claim.objects.annotate(
            total_amount=Sum(
                F('claimcoverage__claimitem__item__unit_price')
                * F('claimcoverage__claimitem__quantity')
            ),
        )

        # annotatations are done via join and not subquery, this duplicates
        #  data and makes it so that the two above queries cannot be joined
        revenue = 0
        outstanding_fees = 0
        outstanding_clients = set()
        claims = zip(revenue_claims, outstanding_claims)
        for revenue_claim, outstanding_claim in claims:
            amount_remaining = 0
            if outstanding_claim.total_amount > revenue_claim.total_revenue:
                amount_remaining = (
                    outstanding_claim.total_amount
                    - revenue_claim.total_revenue
                )
            revenue += revenue_claim.total_revenue
            outstanding_fees += amount_remaining
            outstanding_clients.add(revenue_claim.patient_id)

        stats_dict = {
            'revenue': revenue,
            'outstanding_fees': outstanding_fees,
            'total': revenue + outstanding_fees,
            'outstanding_clients': len(outstanding_clients)
        }

        return stats_dict

    def _insurance_company_stats(self):
        # Number of claims
        date_queryset = views._date_search(
            self.request, ["claim__submitted_datetime"],
            clients_models.Insurance
        )
        insurances_num_claims = date_queryset.values(
            'provider'
        ).annotate(
            num_claims=Count('claim'),
        )
        # Total expected back
        date_queryset = views._date_search(
            self.request, ["claim__submitted_datetime"],
            clients_models.Insurance
        )
        insurances_expected_back = date_queryset.values(
            'provider'
        ).annotate(
            expected_back__sum=Sum('claim__claimcoverage__expected_back')
        )
        # Total amount claimed
        date_queryset = views._date_search(
            self.request, ["claim__submitted_datetime"],
            clients_models.Insurance
        )
        insurances_amount_claimed = date_queryset.values(
            'provider'
        ).annotate(
            amount_claimed__sum=Sum(
                'claim__claimcoverage__claimitem__item__unit_price',
                field='"clients_item"."unit_price"'
                      ' * "clients_claimitem".quantity'
            )
        )
        # Combine the 3 above query's results into one
        insurances_chain = chain(
            insurances_num_claims,
            insurances_expected_back,
            insurances_amount_claimed
        )

        return self._merge_by_key(insurances_chain, 'provider')

    def _insurance_company_stats_totals(self, insurances):
        insurances_totals = {
            'num_claims': 0,
            'expected_back__sum': 0,
            'amount_claimed__sum': 0
        }
        for insurance in insurances:
            insurances_totals['num_claims'] += insurance['num_claims']
            insurances_totals['amount_claimed__sum'] += \
                insurance['amount_claimed__sum'] or 0
            insurances_totals['expected_back__sum'] += \
                insurance['expected_back__sum'] or 0

        return insurances_totals

    def _merge_by_key(self, dicts, key):
        merged = defaultdict(dict)

        for dict_ in dicts:
            merged[dict_[key]].update(dict_)

        return merged.values()

    def _top_ten_best_sellers(self):
        # Top 10 best sellers
        shoes = inventory_models.Shoe.objects.annotate(
            num_orders=Count('shoeattributes__shoeorder')
        ).order_by('-num_orders')[:10]
        return shoes

    def _old_ordered_date_orders(self):
        # Old ordered orders
        cutoff = datetime.now() - timedelta(days=30)
        orders = inventory_models.Order.objects.filter(
            dispensed_date__isnull=True,
            arrived_date__isnull=True,
            ordered_date__lte=cutoff,
        )
        return orders

    def _old_arrvied_date_orders(self):
        # Old arrived orders
        cutoff = datetime.now() - timedelta(days=30)
        orders = inventory_models.Order.objects.filter(
            dispensed_date__isnull=True,
            arrived_date__lte=cutoff,
        )
        return orders
