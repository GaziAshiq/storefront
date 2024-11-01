from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Product, Collection
from .serializers import ProductSerializer


# Create your views here.
@api_view(['GET'])
def product_list(request: Request) -> Response:
    products:Product = Product.objects.select_related('collection').all()
    serializer:ProductSerializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request: Request, id: int) -> Response:
    product:Product = (get_object_or_404
                       (Product, pk=id)) #get_objector_404 is a shortcut to get an object or raise a 404 error
    serializer:ProductSerializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def collection_detail(request: Request, pk: int) -> Response:
    # collection:Collection = (get_object_or_404(Collection, pk=id))
    return Response('ok')