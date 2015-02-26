import collections
from decimal import Decimal

from django.db import models
from django.core.urlresolvers import reverse

from clients import models as client_models
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

    def get_absolute_url(self):
        return reverse('shoe_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


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

    def dispensed(self):
        # dispensed date with ordered date does not count as it implies
        # +1 for ordered and -1 for dispensed
        return self.shoeorder_set.filter(
            dispensed_date__isnull=False,  # with
            ordered_date__isnull=True  # without
        ).count()

    class Meta:
        unique_together = (('shoe', 'size'),)

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

        quantity = self.Field(
            fields['quantity'].field,
            self.quantity - dispensed
        )
        fields.update(
            {"quantity": quantity}
        )

        return fields

    def get_absolute_url(self):
        return self.shoe.get_absolute_url()

    def __unicode__(self):
        try:
            shoe = self.shoe
        except:
            shoe = None
        return "Size: %s - %s" % (self.size, shoe)

    def __str__(self):
        return self.__unicode__()


class Order(models.Model, model_utils.FieldList):
    SHOE = "s"
    COVERAGE_TYPES = client_models.Coverage.COVERAGE_TYPES
    ORDER_TYPES = COVERAGE_TYPES + ((SHOE, "Shoe"),)

    order_type = models.CharField(
        "Order Type", max_length=4, choices=ORDER_TYPES)

    claimant = models.ForeignKey(
        client_models.Person, verbose_name="Claimant")

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
            order = ShoeOrder.objects.get(pk=self.pk)
            return order.shoe_attributes.shoe.credit_value
        except:
            pass
        try:
            order = CoverageOrder.objects.get(pk=self.pk)
            return order.credit_value
        except:
            pass
        return 0

    def get_absolute_url(self):
        try:
            order = ShoeOrder.objects.get(pk=self.pk)
        except:
            pass
        try:
            order = CoverageOrder.objects.get(pk=self.pk)
        except:
            pass
        return order.get_absolute_url()

    def get_all_fields(self):
        fields = super(Order, self).get_all_fields()

        reordered_fields = collections.OrderedDict()
        for k, v in fields.items():
            reordered_fields.update(
                {k: self.Field(v.field, v.value)}
            )
            if k == "claimant":
                try:
                    order = ShoeOrder.objects.get(pk=self.pk)
                    value = order.shoe_attributes
                except:
                    value = ""
                shoe_field = self.Field(
                    self.PseudoForeignKey("Shoe"),
                    value
                )
                reordered_fields.update(
                    {"shoe": shoe_field}
                )
                # try:
                #     order = CoverageOrder.objects.get(pk=self.pk)
                # except:
                #     pass

        return reordered_fields

    def __unicode__(self):
        return "%s - %s" % (
            self.get_order_type_display(), self.claimant)

    def __str__(self):
        return self.__unicode__()


class ShoeOrder(Order):
    shoe_attributes = models.ForeignKey(
        ShoeAttributes, verbose_name="Shoe")

    def get_all_fields(self):
        fields = super(ShoeOrder, self).get_all_fields()

        fields.pop('order_ptr')
        # remove this PseudoForeignKey field as
        #  it's a duplicate of shoe_attributes
        fields.pop('shoe')

        return fields

    def save(self):
        self.order_type = Order.SHOE
        super(ShoeOrder, self).save()

    def get_absolute_url(self):
        return reverse('shoe_order_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s - %s" % (
            self.get_order_type_display(), self.claimant)

    def __str__(self):
        return self.__unicode__()


class CoverageOrder(Order):
    quantity = models.IntegerField(
        "Quantity", default=0)
    credit_value = models.IntegerField(
        "Credit Value", default=0)
    vendor = models.CharField(
        "Vendor", max_length=32)

    def get_all_fields(self):
        fields = super(CoverageOrder, self).get_all_fields()

        fields.pop('order_ptr')

        return fields

    def get_absolute_url(self):
        return reverse('coverage_order_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s - %s" % (
            self.get_order_type_display(), self.claimant)

    def __str__(self):
        return self.__unicode__()


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
