from django.db import models
from django.db.models import fields
from favorites.models import Favorites
from rest_framework import serializers

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def validate(self, attrs):
        queryset = Favorites.objects.filter(product = attrs['product'], user = attrs['user'])
        if queryset.exists():
            raise serializers.ValidationError('Ürün zaten favorilere eklenmiş.')
        return attrs