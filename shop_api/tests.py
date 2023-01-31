from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status

from shop_service.models import Category, Product

SHOP_API_URL = reverse("shop_api:order-list")


class ShopAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "test_pass", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(name="Laptop")
        self.product = Product.objects.create(
            name="HP", category=self.category, user=self.user, price=780.5
        )

    def test_order_creation(self):  # TODO: complete tests
        payload = {
            "name": "Test",
            "email": "test@gmail.com",
            "product": [self.product.id],
        }

        response = self.client.post(SHOP_API_URL, data=payload)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
