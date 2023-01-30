from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    RELATED_NAME = "products"

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name=RELATED_NAME
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name=RELATED_NAME
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category}: {self.name} ({self.price})"


class Order(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.ManyToManyField(to=Product, related_name="orders")

    def __str__(self):
        return f"{self.name} - {self.email}: {list(self.product.all())}"
