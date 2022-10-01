from django.db import models

from authentication.models import CustomerProfile, User
from .choices import ProductStatus, RateFrequency
from .managers import ProductManager


class Product(models.Model):
    status = models.CharField(max_length=50, choices=ProductStatus.choices)

    # Managers
    objects = ProductManager()

    # FK
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)

    # Rate
    rate_frequency = models.CharField(max_length=50, choices=RateFrequency.choices, default="WEEK")
    rate_times = models.PositiveIntegerField(default=4)
    rate = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    # Product
    description = models.TextField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField(null=True)  # Cron
    quantity = models.PositiveIntegerField(default=1)

    # Dates
    date_create = models.DateTimeField(auto_now_add=True)
    date_extend = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)