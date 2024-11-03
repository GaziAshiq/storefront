from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers

from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model: Collection = Collection
        fields: list = ['id', 'title', 'products_count']

    products_count: int = serializers.IntegerField(read_only=True) # read-only won't be included in the POST request


class ProductSerializer(serializers.ModelSerializer):
    price: Decimal = serializers.DecimalField(source='unit_price', max_digits=10, decimal_places=2,
                                              min_value=Decimal('0.01'))
    price_with_tax: Decimal = serializers.SerializerMethodField(method_name='get_price_with_tax')

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='store:collection-detail'
    )

    class Meta:
        model: Product = Product
        fields: list = ['id', 'title', 'description', 'slug', 'inventory', 'price', 'price_with_tax', 'collection']

    @staticmethod
    def get_price_with_tax(obj: Product) -> Decimal:
        # Calculate price with tax and set to 2 decimal places
        price_with_tax: Decimal = obj.unit_price * Decimal(1.10)
        return price_with_tax.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    # region Example of overriding methods
    # I can override the create method to customize the creation of a new object
    # def create(self, validated_data):
    #     # Create a new Product object
    #     product: Product = Product.objects.create(**validated_data)
    #     # product.other = 1 # add a custom field
    #     product.save()  # save the object
    #     return product  # It's called by the serializer.save() method, if we try to create a new object'
    #
    # # I can override the update method to customize the update of an existing object
    # def update(self, instance, validated_data):
    #     # Update an existing Product object
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.save()
    #     return instance  # It's called by the serializer.save() method, if we try to update an existing object'
    # endregion

# region (old) base Serializers
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
