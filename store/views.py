from typing import Tuple

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request: Request) -> Response:
    if request.method == 'GET':
        products: Product = Product.objects.select_related('collection').order_by('-id')[0:5]
        serializer: ProductSerializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer: ProductSerializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request: Request, id: int) -> Response:
    product: Product = (get_object_or_404(Product, pk=id))  # get an object or raise a 404 error

    if request.method == 'GET':
        serializer: ProductSerializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer: ProductSerializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer: ProductSerializer = ProductSerializer(product, data=request.data, partial=True,
                                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        temp = product.title
        product.delete()
        return Response({'message': f'{temp} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request: Request) -> Response:
    if request.method == 'GET':
        queryset: Collection = Collection.objects.annotate(products_count=Count('product')).all().order_by('id')
        serializer: CollectionSerializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer: CollectionSerializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def collection_detail(request: Request, pk: int) -> Response:
    collection: Collection = (get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk))

    if request.method == 'GET':
        serializer: CollectionSerializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer: CollectionSerializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer: CollectionSerializer = CollectionSerializer(collection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        temp: Tuple = (collection.id, collection.title)
        if collection.product_set.count() > 0:
            return Response({'message': f'ID: {temp[0]} - {temp[1]} has products, cannot be deleted!'},
                            status=status.HTTP_409_CONFLICT)
        collection.delete()
        return Response({'message': f'ID: {temp[0]} - {temp[1]}, deleted successfully!'},
                        status=status.HTTP_204_NO_CONTENT)
