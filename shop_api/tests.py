from typing import OrderedDict

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status

from shop_service.models import Category, Product, Order

SHOP_API_URL = reverse("shop_api:order-list")


def _ordered_dict_to_str(ordered_dict: OrderedDict):
    price = float(ordered_dict["price"])
    products_str = (
        f"{ordered_dict['category']}:"
        f" {ordered_dict['name']} ({price if price % 1 != 0 else int(price)})"
    )
    return products_str


class ShopAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin", "test_pass", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(name="Laptop")
        self.product1 = Product.objects.create(
            name="HP", category=self.category, user=self.user, price=780.5
        )

        self.product2 = Product.objects.create(
            name="LG", category=self.category, user=self.user, price=580
        )
        self.order = Order.objects.create(
            name="Test2", email="noreply@gmail.com"
        )
        self.order.product.set([self.product2])

    def test_order_creation(self):
        payload = {
            "name": "Test",
            "email": "test@gmail.com",
            "products": [self.product1.id],
        }

        response = self.client.post(SHOP_API_URL, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])
        self.assertEqual(response.data["email"], payload["email"])

        products = response.data["products"][0]
        products_str = _ordered_dict_to_str(products)
        self.assertEqual(str(self.product1), products_str)

    def test_order_creation_error(self):
        non_existent_index = 100
        payload = {
            "name": "Test",
            "email": "test@gmail.com",
            "products": [non_existent_index],
        }

        response = self.client.post(SHOP_API_URL, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            f"Product index {non_existent_index} does not exist!",
        )

    def test_order_list(self):
        response = self.client.get(SHOP_API_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products = response.data[0].pop("products")[0]
        products_str = _ordered_dict_to_str(products)
        self.assertEqual(str(self.product2), products_str)

        for key in response.data[0].keys():
            self.assertEqual(response.data[0][key], getattr(self.order, key))
