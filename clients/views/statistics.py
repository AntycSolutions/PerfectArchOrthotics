from datetime import datetime, timedelta
from itertools import chain
from collections import defaultdict

from django.views.generic import TemplateView
from django.db.models import Count, Sum

from utils import views
from clients import models as clients_models
from inventory import models as inventory_models


class Statistics(TemplateView):
    template_name = "clients/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(Statistics, self).get_context_data(**kwargs)

        statistics = clients_models.SiteStatistics.objects.get_or_create(
            pk=0
        )[0]
        context['statistics'] = statistics

        # Insurance company stats
        if ('df' in self.request.GET) and self.request.GET['df'].strip():
            query_string = self.request.GET['df']
            context['df'] = query_string
        if ('dt' in self.request.GET) and self.request.GET['dt'].strip():
            query_string = self.request.GET['dt']
            context['dt'] = query_string
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
        insurances = self._merge_by_key(insurances_chain, 'provider')
        context['insurances'] = insurances

        # Top 10 best sellers
        shoes = inventory_models.Shoe.objects.annotate(
            num_orders=Count('shoeattributes__shoeorder')
        ).order_by('-num_orders')[:10]
        context['shoes'] = shoes

        # Old ordered orders
        cutoff = datetime.now() - timedelta(days=30)
        orders = inventory_models.Order.objects.filter(
            dispensed_date__isnull=True,
            arrived_date__isnull=True,
            ordered_date__lte=cutoff,
        )
        context['old_ordered_date_orders'] = orders

        # Old arrived orders
        orders = inventory_models.Order.objects.filter(
            dispensed_date__isnull=True,
            arrived_date__lte=cutoff,
        )
        context['old_arrived_date_orders'] = orders

        return context

    def _merge_by_key(self, dicts, key):
        merged = defaultdict(dict)

        for dict_ in dicts:
            merged[dict_[key]].update(dict_)

        return merged.values()
