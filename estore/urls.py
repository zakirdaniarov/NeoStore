from django.contrib import admin
from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, OrderCreateAPIView, ReviewCreateAPIView


urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:id>/create-order/', OrderCreateAPIView.as_view(), name='order-create'),
    path('products/<int:id>/create-review/', ReviewCreateAPIView.as_view(), name='tour_create-review'),
]
