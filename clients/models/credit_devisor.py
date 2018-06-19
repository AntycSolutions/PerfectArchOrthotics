import decimal

from django.db import models
from django.template import defaultfilters


class CreditDivisor(models.Model):
    value = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=decimal.Decimal(0.00)
    )
    created = models.DateTimeField()

    def __str__(self):
        created = defaultfilters.date(self.created, "N j, Y, P")

        return 'Value: {} - {}'.format(self.value, created)
