from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.db.models import Count

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

        # Top 10 best sellers
        shoes = inventory_models.Shoe.objects.annotate(
            num_orders=Count('shoeattributes__shoeorder')
        ).order_by('-num_orders')[:10]
        context['shoes'] = shoes

        cutoff = datetime.now() - timedelta(days=30)
        orders = inventory_models.Order.objects.filter(
            dispensed_date__isnull=True,
            arrived_date__isnull=True,
            ordered_date__lte=cutoff,
        )
        context['old_ordered_date_orders'] = orders

        orders = inventory_models.Order.objects.filter(
            dispensed_date__isnull=True,
            arrived_date__lte=cutoff,
        )
        context['old_arrived_date_orders'] = orders

        return context
