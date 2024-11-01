from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Product, Collection
from .serializers import ProductSerializer


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


@api_view(['GET'])
def collection_detail(request: Request, pk: int) -> Response:
    # collection:Collection = (get_object_or_404(Collection, pk=id))
    return Response('ok')
