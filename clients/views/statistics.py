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
        revenue_claims = clients_models.Claim.objects.select_related(
            'insurance',
        ).annotate(
            invoice_revenue=(
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
            total_revenue=F('expected_back_revenue') + F('invoice_revenue')
        )

        outstanding_claims = clients_models.Claim.objects.annotate(
            total_amount=Sum(
                Coalesce(F('claimcoverage__claimitem__item__unit_price'), 0)
                * Coalesce(F('claimcoverage__claimitem__quantity'), 0)
            ),
        )

        # annotatations are done via join and not subquery, this duplicates
        #  data and makes it so that the two above queries cannot be joined
        invoice_revenue = 0
        expected_back_revenue = 0
        outstanding_fees = 0
        outstanding_assignment_clients_set = set()
        outstanding_non_assignment_clients_set = set()
        claims = zip(revenue_claims, outstanding_claims)
        for revenue_claim, outstanding_claim in claims:
            amount_remaining = 0
            if outstanding_claim.total_amount > revenue_claim.total_revenue:
                amount_remaining = (
                    outstanding_claim.total_amount
                    - revenue_claim.total_revenue
                )
                if revenue_claim.insurance.benefits is 'na':
                    outstanding_non_assignment_clients_set.add(
                        revenue_claim.patient_id
                    )
                elif revenue_claim.insurance.benefits is 'a':
                    outstanding_assignment_clients_set.add(
                        revenue_claim.patient_id
                    )
            invoice_revenue += revenue_claim.invoice_revenue
            expected_back_revenue += revenue_claim.expected_back_revenue
            outstanding_fees += amount_remaining

        total_revenue = invoice_revenue + expected_back_revenue
        outstanding_assignment_clients = len(
            outstanding_assignment_clients_set
        )
        outstanding_non_assignment_clients = len(
            outstanding_non_assignment_clients_set
        )
        stats_dict = {
            'invoice_revenue': invoice_revenue,
            'expected_back_revenue': expected_back_revenue,
            'outstanding_fees': outstanding_fees,
            'total_revenue': total_revenue,
            'total': total_revenue + outstanding_fees,
            'outstanding_assignment_clients': outstanding_assignment_clients,
            'outstanding_non_assignment_clients':
                outstanding_non_assignment_clients,
            'total_outstanding_clients': (
                outstanding_assignment_clients
                + outstanding_non_assignment_clients
            ),
        }

        return stats_dict

    def _insurance_company_stats(self):
        # Total expected back and number of claims
        date_queryset = views._date_search(
            self.request, ["claim__submitted_datetime"],
            clients_models.Insurance
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
                    Q(benefits='a')
                    & Q(claim__claimcoverage__actual_paid_date__isnull=False),
                    then='claim__claimcoverage__expected_back',
                ),
                default=0,
            )),
            pending_assignment_expected_back=Sum(Case(
                When(
                    Q(benefits='a')
                    & Q(claim__claimcoverage__actual_paid_date__isnull=True),
                    then='claim__claimcoverage__expected_back',
                ),
                default=0,
            )),
            num_claims=Count('claim', distinct=True),
        ).annotate(
            total_assignment_expected_back=(
                F('assignment_expected_back')
                + F('pending_assignment_expected_back')
            ),
        ).annotate(
            expected_back__sum=(
                F('non_assignment_expected_back')
                + F('total_assignment_expected_back')
            )
        )

        # Total amount claimed
        date_queryset = views._date_search(
            self.request, ["claim__submitted_datetime"],
            clients_models.Insurance
        )
        insurances_amount_claimed = date_queryset.values(
            'provider'
        ).annotate(
            assignment_amount_claimed=Sum(Case(
                When(
                    benefits='a',
                    then=Coalesce(
                        F('claim__claimcoverage__claimitem__item__unit_price'),
                        0
                    )
                    * Coalesce(
                        F('claim__claimcoverage__claimitem__quantity'),
                        0
                    )
                ),
                default=0,
            )),
            non_assignment_amount_claimed=Sum(Case(
                When(
                    benefits='na',
                    then=Coalesce(
                        F('claim__claimcoverage__claimitem__item__unit_price'),
                        0
                    )
                    * Coalesce(
                        F('claim__claimcoverage__claimitem__quantity'),
                        0
                    )
                ),
                default=0,
            )),
        ).annotate(
            amount_claimed__sum=(
                F('assignment_amount_claimed')
                + F('non_assignment_amount_claimed')
            )
        )
        # Combine the 2 above query's results into one
        insurances_chain = chain(
            insurances_expected_back,
            insurances_amount_claimed
        )

        return self._merge_by_key(insurances_chain, 'provider')

    def _insurance_company_stats_totals(self, insurances):
        insurances_totals = {
            'num_claims': 0,
            'non_assignment_expected_back': 0,
            'assignment_expected_back': 0,
            'pending_assignment_expected_back': 0,
            'total_assignment_expected_back': 0,
            'expected_back__sum': 0,
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
            if 'amount_claimed__sum' in insurance:
                insurances_totals['amount_claimed__sum'] += \
                    (insurance['amount_claimed__sum'] or 0)
            else:
                insurance['amount_claimed__sum'] = 0
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
            if 'expected_back__sum' in insurance:
                insurances_totals['expected_back__sum'] += \
                    (insurance['expected_back__sum'] or 0)
            else:
                insurance['expected_back__sum'] = 0

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
