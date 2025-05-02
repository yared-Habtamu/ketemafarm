from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'quantity', 'image']
        read_only_fields = ['farmer']

    def create(self, validated_data):
        validated_data['farmer'] = self.context['request'].user
        return super().create(validated_data)
