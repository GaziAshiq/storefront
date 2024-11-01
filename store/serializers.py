from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers

from .models import Product, Collection


class ProductSerializer(serializers.ModelSerializer):
    price: Decimal = serializers.DecimalField(source='unit_price', max_digits=10, decimal_places=2,
                                              min_value=Decimal('0.01'))
    price_with_tax: Decimal = serializers.SerializerMethodField(method_name='get_price_with_tax')
    collection = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='store:collection_detail'
    )

    class Meta:
        model: Product = Product
        fields: list = ['id', 'title', 'price', 'price_with_tax', 'collection']

    @staticmethod
    def get_price_with_tax(obj: Product) -> Decimal:
        # Calculate price with tax and set to 2 decimal places
        price_with_tax = obj.unit_price * Decimal(1.10)
        return price_with_tax.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model: Collection = Collection
        fields: list = ['id', 'title', 'featured_product']

# region base Serializers
# class ProductSerializer(serializers.Serializer):
#     """
#     The ProductSerializer class is a custom serializer for the Product model.
#     here I don't use the ModelSerializer class because I want to customize the fields.
#     """
#     id: int = serializers.IntegerField(read_only=True)
#     title: str = serializers.CharField(max_length=255)
#     price: Decimal = serializers.DecimalField(max_digits=6, decimal_places=2,
#                                               source='unit_price')  # customize the field name for the JSON output
#     price_with_tax: Decimal = serializers.SerializerMethodField(method_name='get_price_with_tax')  # add a custom field
#
#     # collection: Collection = serializers.PrimaryKeyRelatedField(read_only=True)  # use the primary key of the Collection model
#     # collection: Collection = serializers.StringRelatedField()  # use the __str__ method of the Collection model
#     collection: Collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),
#                                                                  view_name='collection_detail')  # use the URL of the Collection model
#
#     @staticmethod
#     def get_price_with_tax(obj: Product) -> Decimal:
#         return obj.unit_price * Decimal(1.10)
# endregion
