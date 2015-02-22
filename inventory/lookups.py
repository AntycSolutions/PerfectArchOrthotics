from django.utils.encoding import force_text
from django.utils.html import escape
from django.core.urlresolvers import reverse

from inventory import models
from utils.search import get_query as search_get_query

from ajax_select import LookupChannel


class ShoeLookup(LookupChannel):
    model = models.ShoeAttributes

    def get_query(self, q, request):
        fields = ['size',
                  'shoe__name', 'shoe__brand', 'shoe__style', 'shoe__sku',
                  'shoe__colour']
        query = search_get_query(q, fields)
        queryset = models.ShoeAttributes.objects.filter(query)

        return queryset

    def get_result(self, obj):
        # foreach option in dropdown
        result = "%s - %s - %s - %s - %s - Size: %s Quantity: %s" % (
            obj.shoe.brand, obj.shoe.style, obj.shoe.name, obj.shoe.sku,
            obj.shoe.colour,
            obj.size, obj.quantity
        )
        return escape(force_text(result))

    def format_item_display(self, obj):
        # item in deck
        result = "<a href='%s'>%s Size: %s Quantity: %s</a>" % (
            reverse('shoe_detail', kwargs={'pk': obj.pk}),
            escape(force_text(obj.shoe.name)),
            escape(force_text(obj.size)),
            escape(force_text(obj.quantity)),
        )

        return result
