import collections
from decimal import Decimal

from django.db import models
from django.core import urlresolvers
from django.utils import timezone

from auditlog.registry import auditlog
from clients import models as clients_models
from utils import model_utils


class Shoe(models.Model, model_utils.FieldList):
    WOMENS = 'wo'
    MENS = 'me'
    JUNIOR = 'ju'
    KIDS = 'ki'
    CATEGORIES = ((WOMENS, "Women's"),
                  (MENS, "Men's"),
                  (JUNIOR, "Junior"),
                  (KIDS, "Kids"),)
    ORDERABLE = 'or'
    DISCONTINUED = 'di'
    AVAILABILITIES = ((ORDERABLE, "Orderable"),
                      (DISCONTINUED, "Discontinued"),)

    image = model_utils.ImageField(
        "Image", upload_to='inventory/shoes/%Y/%m/%d',
        null=True, blank=True)
    category = models.CharField(
        "Category", max_length=4, choices=CATEGORIES,
        blank=True)
    availability = models.CharField(
        "Availability", max_length=4, choices=AVAILABILITIES,
        blank=True)
    brand = models.CharField(
        "Brand", max_length=32,
        blank=True)
    style = models.CharField(
        "Style", max_length=32,
        blank=True)
    name = models.CharField(
        "Name", max_length=32)
    sku = models.CharField(
        "SKU", max_length=32,
        blank=True)
    colour = models.CharField(
        "Colour", max_length=32,
        blank=True)
    description = models.TextField(
        "Description",
        blank=True)
    credit_value = models.IntegerField(
        "Credit Value", default=0)
    cost = models.DecimalField(
        "Cost", max_digits=6, decimal_places=2, default=Decimal(0.00))

    money_fields = ['cost']

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy('shoe_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class ShoeAttributes(models.Model, model_utils.FieldList):
    """
        Women's 5-11 [halfs]
        Men's 7-14 [halfs]
        Junior 3-6.5 [halfs]
        Kids 9-3 (9, 10, 11, 12, 13, 1, 2, 3)
    """
    SIZE_RANGE = range(30, 141, 5)  # Use 141 to include 140
    SIZES = [("1", "1"), ("2", "2")] + [("%g" % (i / 10),
                                         "%g" % (i / 10)) for i in SIZE_RANGE]

    shoe = models.ForeignKey(
        Shoe, verbose_name="Shoe")
    size = models.CharField(
        "Size", max_length=4, choices=SIZES)
    quantity = models.IntegerField(
        "Quantity", default=0)

    def get_additional_data(self):
        # track shoe_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'shoe_id': self.shoe_id,
        }

    def dispensed(self):
        # dispensed date with ordered date does not count as it implies
        # +1 for ordered and -1 for dispensed
        return self.shoeorder_set.filter(
            dispensed_date__isnull=False,  # with
            ordered_date__isnull=True  # without
        ).count()

    def returned(self):
        return self.shoeorder_set.filter(returned_date__isnull=False).count()

    class Meta:
        unique_together = (('shoe', 'size'),)
        verbose_name_plural = "Shoe attributes"
        permissions = (('can_lookup_shoe_attributes',
                        'Can Lookup Shoe Attributes'),)

    def get_all_fields(self):
        fields = super(ShoeAttributes, self).get_all_fields()

        dispensed = self.dispensed()
        # dispensed_field = model_utils.FieldList.Field(
        #     model_utils.FieldList.PseudoField("Dispensed"),
        #     dispensed
        # )
        # fields.update(
        #     {"dispensed": dispensed_field}
        # )

        returned = self.returned()

        quantity = self.Field(
            fields['quantity'].field,
            self.quantity - dispensed + returned
        )
        fields.update(
            {"quantity": quantity}
        )

        return fields

    def get_absolute_url(self):
        return self.shoe.get_absolute_url()

    def get_str(self):
        try:
            shoe = self.shoe
            brand = shoe.brand
            colour = shoe.colour
        except Shoe.DoesNotExist:
            shoe = None

        return "Size: {} - {}: {} - {}".format(
            self.size, brand, shoe, colour
        )

    def __str__(self):
        return "Size: {} - Quantity: {} - Shoe ID: {}".format(
            self.size, self.quantity, self.shoe_id
        )


class Order(models.Model, model_utils.FieldList):
    SHOE = "s"
    ADJUSTMENT = "a"
    COVERAGE_TYPES = clients_models.Coverage.COVERAGE_TYPES
    ORDER_TYPES = COVERAGE_TYPES + ((SHOE, "Shoe"),
                                    (ADJUSTMENT, "Adjustment"))

    order_type = models.CharField(
        "Order Type", max_length=4, choices=ORDER_TYPES)

    claimant = models.ForeignKey(
        clients_models.Person, verbose_name="Claimant")

    description = models.TextField(
        "Description",
        blank=True)
    ordered_date = models.DateField(
        "Ordered Date",
        blank=True, null=True)
    arrived_date = models.DateField(
        "Arrived Date",
        blank=True, null=True)
    dispensed_date = models.DateField(
        "Dispensed Date",
        blank=True, null=True)

    def get_credit_value(self):
        try:
            order = self.shoeorder

            return order.shoe_attributes.shoe.credit_value
        except ShoeOrder.DoesNotExist:
            pass
        try:
            order = self.coverageorder
            # ignore quantity as credit_value is already the total

            return order.credit_value
        except CoverageOrder.DoesNotExist:
            pass
        try:
            order = self.adjustmentorder

            return order.credit_value
        except AdjustmentOrder.DoesNotExist:
            pass

        raise Exception('Order is not a Shoe Order, Coverage Order, nor'
                        ' Adjustment Order.')

    def get_absolute_url(self):
        order = None
        try:
            order = self.shoeorder
        except ShoeOrder.DoesNotExist:
            pass
        try:
            order = self.coverageorder
        except CoverageOrder.DoesNotExist:
            pass
        try:
            order = self.adjustmentorder
        except AdjustmentOrder.DoesNotExist:
            pass

        if order:
            return order.get_absolute_url()
        else:
            raise Exception('Order is not a Shoe Order, Coverage Order, nor'
                            ' Adjustment Order.')

    def get_all_fields(self):
        fields = super(Order, self).get_all_fields()

        reordered_fields = collections.OrderedDict()
        for k, v in fields.items():
            reordered_fields.update(
                {k: self.Field(v.field, v.value)}
            )

            if k == "claimant":
                if self.order_type == self.SHOE:
                    try:
                        order = self.shoeorder
                        value = order.shoe_attributes
                    except ShoeOrder.DoesNotExist:
                        value = ""
                else:
                    value = ""

                shoe_field = self.Field(
                    self.PseudoForeignKey("Shoe"), value
                )

                reordered_fields.update(
                    {"shoe": shoe_field}
                )
            elif k == "description":
                if self.order_type == self.SHOE:
                    try:
                        order = self.shoeorder
                        value = order.customer_ordered_date
                    except ShoeOrder.DoesNotExist:
                        value = ""
                elif self.order_type in dict(self.COVERAGE_TYPES):
                    try:
                        order = self.coverageorder
                        value = order.customer_ordered_date
                    except CoverageOrder.DoesNotExist:
                        value = ""
                else:
                    value = ""

                field = self.Field(
                    self.PseudoField("Customer Ordered Date"), value
                )

                reordered_fields.update(
                    {"customer_ordered_date": field}
                )
            elif k == 'dispensed_date':
                if self.order_type == self.SHOE:
                    try:
                        order = self.shoeorder
                        value = order.returned_date
                    except ShoeOrder.DoesNotExist:
                        value = ""
                else:
                    value = ""

                shoe_field = self.Field(
                    self.PseudoField("Returned Date"), value
                )

                reordered_fields.update(
                    {"returned_date": shoe_field}
                )

        return reordered_fields

    def __str__(self):
        return "{} - Person ID: {}".format(
            self.get_order_type_display(), self.claimant_id
        )


class ShoeOrder(Order):
    customer_ordered_date = models.DateField(blank=True, null=True)

    returned_date = models.DateField(blank=True, null=True)

    shoe_attributes = models.ForeignKey(
        ShoeAttributes, verbose_name="Shoe")

    def get_additional_data(self):
        # track client_id, shoe_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.claimant_id,
            'shoe_id': self.shoe_attributes.shoe_id,
        }

    def get_all_fields(self):
        fields = super(ShoeOrder, self).get_all_fields()

        fields.pop('order_ptr')
        # remove this PseudoForeignKey field as
        #  it's a duplicate of shoe_attributes
        fields.pop('shoe')

        return fields

    def save(self, *args, **kwargs):
        self.order_type = Order.SHOE
        super(ShoeOrder, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'shoe_order_detail', kwargs={'pk': self.pk}
        )

    def __str__(self):
        return "{} - Shoe Attributes ID: {} - Person ID: {}".format(
            self.get_order_type_display(),
            self.shoe_attributes_id,
            self.claimant_id
        )


class CoverageOrder(Order):
    customer_ordered_date = models.DateField(blank=True, null=True)

    claim = models.ForeignKey(clients_models.Claim, blank=True, null=True)

    quantity = models.IntegerField(
        "Quantity", default=0)
    credit_value = models.DecimalField(
        "Credit Value", max_digits=3, decimal_places=2, default=Decimal(0.00)
    )
    vendor = models.CharField(
        "Vendor", max_length=32)

    # As Orders being tied to Claims is a newer feature we need to support
    #  Claims/Orders created before this feature existed
    ORDERS_TIED_TO_CLAIMS_START_DATETIME = timezone.make_aware(
        # TODO: make this the day of deployment
        timezone.datetime(2016, 11, 24)
    )

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.claimant_id,
        }

    def get_all_fields(self):
        fields = super(CoverageOrder, self).get_all_fields()

        fields.pop('order_ptr')
        fields.pop('shoe')

        if self.order_type != clients_models.Coverage.ORTHOTICS:
            fields.pop('claim')

        return fields

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'coverage_order_detail', kwargs={'pk': self.pk}
        )

    def __str__(self):
        return "{} - Person ID: {}".format(
            self.get_order_type_display(), self.claimant_id
        )


class AdjustmentOrder(Order):
    credit_value = models.DecimalField(
        "Credit Value", max_digits=3, decimal_places=2, default=Decimal(0.00))

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.claimant_id,
        }

    def get_all_fields(self):
        fields = super(AdjustmentOrder, self).get_all_fields()

        fields.pop('order_ptr')
        fields.pop('shoe')
        fields.pop('customer_ordered_date')

        return fields

    def save(self):
        self.order_type = Order.ADJUSTMENT
        super(AdjustmentOrder, self).save()

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'adjustment_order_detail', kwargs={'pk': self.pk}
        )

    def __str__(self):
        return "{} - Person ID: {}".format(
            self.get_order_type_display(), self.claimant_id
        )


"""
    Reports:
    1)how much shoes that is in inventory
    - separate by Brands, style, sku
    2)how much money is invested in inventory
    -separate by brands, style, sku
    3)Best sellers
    4)best sizes sellers
    5)size curve
    6) low inventory notifications
    - sent by notification can be sent by email
"""

auditlog.register(Shoe)
auditlog.register(ShoeAttributes)
auditlog.register(Order)
auditlog.register(ShoeOrder)
auditlog.register(CoverageOrder)
auditlog.register(AdjustmentOrder)
