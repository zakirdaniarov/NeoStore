from django.db import models
from authorization.models import User


class Product(models.Model):
    CATEGORY_PRODUCT = (
        ('digital services', 'digital services'),
        ('cosmetics and body care', 'cosmetics and body care'),
        ('food and beverage', 'food and beverage'),
        ('health and wellness', 'health and wellness'),
        ('household items', 'household items'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=150, choices=CATEGORY_PRODUCT)
    is_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Reviews(models.Model):
    product = models.ForeignKey(Product, related_name='product_reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.reviewer} on {self.product}'


class Order(models.Model):
    CATEGORY_PRODUCT = (
        ('credit card', 'credit card'),
        ('bank transfer', 'bank transfer'),
        ('paypal', 'paypal'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    quantity = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=200, choices=CATEGORY_PRODUCT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ordered {self.quantity} {self.product}'





