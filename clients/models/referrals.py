import decimal

from django.db import models

from .claims import Claim
from .clients import Client


class Referral(models.Model):
    client = models.ForeignKey(Client)
    claims = models.ManyToManyField(Claim)
    credit_value = models.DecimalField(
        "Credit Value",
        max_digits=3,
        decimal_places=2,
        default=decimal.Decimal(0.00)
    )

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.client_id,
        }

    def __str__(self):
        return "Credit Value: {} - Client ID: {}".format(
            self.credit_value, self.client_id
        )
