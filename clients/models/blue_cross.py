from django.db import models
from django.core import urlresolvers

from utils import model_utils

from .claims import Claim


class BlueCross(models.Model, model_utils.FieldList):
    claim = models.OneToOneField(Claim)

    date = models.DateField()

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'blue_cross_fill_out', kwargs={'claim_pk': self.claim.pk}
        )

    def __str__(self):
        return "Claim ID: {}".format(self.claim_id)
