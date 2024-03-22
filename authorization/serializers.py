from rest_framework import serializers
from .models import User
from estore.serializers import OrderSerializer


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")

        if not username.isalnum:
            raise serializers.ValidationError('username should contain alphanumeric characters')

        return attrs

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value.lower()

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class ResendActivationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserActivationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=5)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    my_orders = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'my_orders', 'total_amount']

    def get_my_orders(self, instance):
        orders = instance.order.all()  # Corrected line
        return OrderSerializer(orders, many=True).data

    def get_total_amount(self, instance):
        orders = instance.order.all()
        total_amount = sum(self.calculate_order_total(order) for order in orders)
        return total_amount

    def calculate_order_total(self, order):
        if order.product.is_sale:
            discount = 0.15
            discounted_price = order.product.price * (1 - discount)
            return discounted_price * order.quantity
        else:
            return order.product.price * order.quantity














