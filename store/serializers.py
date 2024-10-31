from decimal import Decimal
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.Serializer):
    id: int = serializers.IntegerField(read_only=True)
    title: str = serializers.CharField(max_length=255)
    price: Decimal = serializers.DecimalField(max_digits=6, decimal_places=2,
                                              source='unit_price')  # customize the field name for the JSON output
    price_with_tax: Decimal = serializers.SerializerMethodField(method_name='get_price_with_tax')  # add a custom field

    @staticmethod
    def get_price_with_tax(obj: Product) -> Decimal:
        return obj.unit_price * Decimal(1.10)
