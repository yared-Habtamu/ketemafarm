from django.db import models
from users.models import User


class Product(models.Model):
    CATEGORIES = [
        ('VEGETABLES', 'Vegetables'),
        ('FRUITS', 'Fruits'),
        ('TOOLS', 'Farming Tools'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.farmer.phone}"
