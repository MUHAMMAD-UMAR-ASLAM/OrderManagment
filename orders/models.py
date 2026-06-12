from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from orders.choices import Status

class Product(models.Model):
    name=models.CharField(max_length=200)
    sku=models.CharField(max_length=200,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock_quantity=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.sku}"

class Order(models.Model):
    status=models.CharField(default=Status.PENDING,choices=Status.choices,max_length=10)
    customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} {self.status}"


class OrderItem(models.Model):
    quantity=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(1)])
    price=models.DecimalField(max_digits=10,decimal_places=2)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} {self.quantity}"





