from django.urls import path
from . import views

# URLConf
app_name = 'store'

# region Class-based views URL patterns (New way)
urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('collection/', views.CollectionList.as_view(), name='collection_list'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection_detail'),
]
# endregion

# region Function-based views URL patterns (Old way)
# urlpatterns += [
    # path('', views.product_list, name='product_list'),
    # path('<int:id>/', views.product_detail, name='product_detail'),
    # path('collection/', views.collection_list, name='collection_list'),
    # path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
# ]
# endregion
