from django.urls import path
from . import views

# URLConf
app_name = 'store'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('collection/', views.collection_list, name='collection_list'),
    path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
]
