from .models import Product
from rest_framework import serializers
from accounts.serializers import AccountSerializer
from django.core.validators import MinValueValidator


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
        extra_kwargs = {
            "seller_id": {"read_only": True},
            "quantity": {"validators": [MinValueValidator(0)]},
            "price": {"validators": [MinValueValidator(0)]},
        }


class ProductDetailSerializer(serializers.ModelSerializer):

    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]
        extra_kwargs = {
            "quantity": {"validators": [MinValueValidator(0)]},
            "price": {"validators": [MinValueValidator(0)]},
        }

