import operator

from django.core import urlresolvers
from django.db import models
from django.utils import timezone

from .insurance_info import Coverage


from utils import model_utils


class Item(models.Model, model_utils.FieldList):
    COVERAGE_TYPES = Coverage.COVERAGE_TYPES
    WOMENS = 'wo'
    MENS = 'me'
    UNISEX = 'un'
    GENDERS = (
        (WOMENS, "Women's"),
        (MENS, "Men's"),
        (UNISEX, "Unisex"),
    )

    coverage_type = models.CharField(
        "Coverage Type", max_length=4, choices=COVERAGE_TYPES)
    gender = models.CharField(
        "Gender", max_length=4, choices=GENDERS,
        blank=True)
    product_code = models.CharField(
        "Product Code", max_length=12, unique=True)
    # Should be name or changed to TextField
    description = models.CharField(
        "Description", max_length=128)
    cost = models.IntegerField(
        "Cost", default=0)
    unit_price = models.IntegerField(
        "Retail", default=0)

    money_fields = ['cost', 'unit_price']

    # ManyToManyField
    # Claim
    # ForeignKey
    # ClaimItem

    def get_values(self, datetime):
        # support prefetch_related with python level filtering instead of
        #  db filtering (to reduce queries) as this can be called many times
        item_histories = self.itemhistory_set.all()

        if item_histories:
            if timezone.is_naive(datetime):
                datetime = timezone.make_aware(datetime)

            item_histories_before = []
            item_histories_after = []
            for item_history in item_histories:
                if item_history.created <= datetime:
                    item_histories_before.append(item_history)
                else:
                    item_histories_after.append(item_history)

            if item_histories_before:
                item_history = max(
                    item_histories_before, key=operator.attrgetter('created')
                )
            else:
                item_history = min(
                    item_histories_after, key=operator.attrgetter('created')
                )

            unit_price = item_history.unit_price
            cost = item_history.cost
        else:
            unit_price = self.unit_price
            cost = self.cost

        return {'unit_price': unit_price, 'cost': cost}

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy('item_detail', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # store cost/unit_price in case it changes
        self._initial_cost = self.cost
        self._initial_unit_price = self.unit_price

    def save(self, *args, **kwargs):
        initial_cost = self._initial_cost
        initial_unit_price = self._initial_unit_price
        new_cost = self.cost != initial_cost
        new_unit_price = self.unit_price != initial_unit_price
        if self.pk and (new_cost or new_unit_price):
            ItemHistory.objects.create(
                item=self, cost=initial_cost, unit_price=initial_unit_price
            )

        super().save(*args, **kwargs)

        self._initial_cost = self.cost
        self._initial_unit_price = self.unit_price

    def __str__(self):
        return "{} - {}".format(self.product_code, self.description)


class ItemHistory(models.Model):
    item = models.ForeignKey(Item)

    cost = models.IntegerField()

    unit_price = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cost: ${} - Unit Price: ${} - {} - Item ID: {}'.format(
            self.cost, self.unit_price, self.created, self.item_id
        )
