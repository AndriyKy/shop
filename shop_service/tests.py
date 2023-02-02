from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from shop_service.models import Category, Product

PRODUCTS_URL = reverse("shop_service:product-list")


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user", "test_pass")
        phone = Category.objects.create(name="Smartphone")
        Product.objects.create(
            name="Redmi",
            category=phone,
            user=self.user,
            price=155.8,
        )

        self.headphone = Category.objects.create(name="Headphone")
        Product.objects.create(
            name="Samsung",
            category=self.headphone,
            user=self.user,
            price=73,
        )

    def test_products_search_form(self):
        search_term = {"category": self.headphone.name}
        response = self.client.get(path=PRODUCTS_URL, data=search_term)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response, search_term["category"], count=1, html=True
        )
