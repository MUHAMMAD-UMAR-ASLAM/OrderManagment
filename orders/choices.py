from django.db import models

class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    SHIPPED = "shipped", "Shipped"
    CANCELLED = "cancelled", "Cancelled"
