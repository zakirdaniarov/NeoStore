from rest_framework import serializers
from .models import Product, Order, Reviews


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', "price", 'category']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', "category", 'created_at']


class ReviewListAPI(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'product', 'reviewer', 'review_text', 'rating', 'created_at']

    def create(self, validated_data):
        validated_data['rating'] = validated_data.pop('rating')
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'quantity', "payment_method"]

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


