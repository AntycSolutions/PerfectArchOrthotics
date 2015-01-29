from decimal import Decimal

from django.db import models
from django.core.urlresolvers import reverse

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
        return "Shoe (%s) - %s" % (self.pk, self.name)

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

    class Meta:
        unique_together = (('shoe', 'size'),)

    def get_absolute_url(self):
        return self.shoe.get_absolute_url()

    def __unicode__(self):
        return "Shoe Attributes (%s) - %s" % (self.pk, self.shoe)

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
