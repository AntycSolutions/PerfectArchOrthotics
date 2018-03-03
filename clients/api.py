from rest_framework import viewsets, permissions

from perfect_arch_orthotics import api_helpers
from . import models, serializers


class ClientModelViewSet(viewsets.ModelViewSet, api_helpers.HistoryMixin):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    history_aliases = ['client']
