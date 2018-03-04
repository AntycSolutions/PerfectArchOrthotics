from rest_framework import viewsets, permissions

from perfect_arch_orthotics import api_helpers
from . import models, serializers


class ShoeModelViewSet(viewsets.ModelViewSet, api_helpers.HistoryMixin):
    queryset = models.Shoe.objects.all()
    serializer_class = serializers.ShoeSerializer
    permission_classes = [permissions.IsAuthenticated]
    history_aliases = ['shoe']
