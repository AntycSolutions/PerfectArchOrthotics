from django.db import models as db_models
from django.utils.encoding import force_text
from django.utils.html import escape
from django.core.urlresolvers import reverse

from inventory import models
from simple_search.utils import get_query as search_get_query

from ajax_select import LookupChannel


class ShoeLookup(LookupChannel):
    model = models.ShoeAttributes

    def get_query(self, q, request):
        fields = [
            'size',
            'shoe__name', 'shoe__brand', 'shoe__style', 'shoe__sku',
            'shoe__colour'
        ]
        query = search_get_query(q, fields)
        queryset = models.ShoeAttributes.objects.select_related(
            'shoe'
        ).prefetch_related(
            db_models.Prefetch(
                'shoeorder_set',
                # see dispensed() in clients_models.ShoeAttributes
                queryset=models.ShoeOrder.objects.filter(
                    dispensed_date__isnull=False,  # with
                    ordered_date__isnull=True  # without
                ),
                to_attr='dispensed_set'
            ),
            db_models.Prefetch(
                'shoeorder_set',
                # see returned() in clients_models.ShoeAttributes
                queryset=models.ShoeOrder.objects.filter(
                    returned_date__isnull=False  # with
                ),
                to_attr='returned_set'
            )
        ).filter(query)

        return queryset

    def _get_shoe(self, obj):
        result = ""
        if obj.shoe.brand:
            result += "Brand: %s " % (obj.shoe.brand)
        if obj.shoe.style:
            result += "Style: %s " % (obj.shoe.style)
        result += "Name: %s " % (obj.shoe.name)
        if obj.shoe.sku:
            result += "SKU: %s " % (obj.shoe.sku)
        if obj.shoe.colour:
            result += "Colour: %s " % (obj.shoe.colour)

        if hasattr(obj, 'dispensed_set'):  # use prefetch above
            dispensed = len(obj.dispensed_set)
            returned = len(obj.returned_set)
        else:
            dispensed = obj.dispensed()
            returned = obj.returned()
        result += "Size: %s Quantity: %s" % (
            obj.size, obj.quantity - dispensed + returned
        )

        result = escape(force_text(result))

        return result

    def format_match(self, obj):
        # foreach option in dropdown
        result = self._get_shoe(obj)

        return result

    def format_item_display(self, obj):
        # item in deck
        result = self._get_shoe(obj)

        result = "<a href='%s'>%s</a>" % (
            reverse('shoe_detail', kwargs={'pk': obj.shoe.pk}),
            result,
        )

        return result

    def check_auth(self, request):
        if not request.user.has_perm('inventory.can_lookup_shoe_attributes'):
            super().check_auth(request)
