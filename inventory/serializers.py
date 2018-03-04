from rest_framework import serializers

from . import models


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shoe
        fields = '__all__'
