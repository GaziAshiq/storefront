from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


# Create your views here.
@api_view(['GET'])
def product_list(request: Request) -> Response:
    return Response([
        {
            'id': 1,
            'name': 'Product 1',
            'price': 100.0,
        },
        {
            'id': 2,
            'name': 'Product 2',
            'price': 200.0,
        },
    ])


@api_view(['GET'])
def product_detail(request: Request, pk: int) -> Response:
    return Response({
        'id': pk,
        'name': f'Product {pk}',
        'price': pk * 100.0,
    })
