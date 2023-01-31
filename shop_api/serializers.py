from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop_service.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False, slug_field="name", read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "user",
            "price",
        )


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.ListSerializer(
        child=serializers.IntegerField(
            min_value=1,
            max_value=Product.objects.last().id,
        ),
        allow_empty=False,
        help_text="List of Product indexes",
    )

    def validate(self, attrs):
        data = super(OrderSerializer, self).validate(attrs=attrs)
        product_indexes = Product.objects.values_list("id", flat=True)
        for index in data["product"]:
            if index not in product_indexes:
                raise ValidationError(f"Product index {index} does not exist!")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            products_data = validated_data.pop("product")
            order = Order.objects.create(**validated_data)
            for product_data in products_data:
                order.product.add(product_data)
            return order  # TODO: define why a TypeError appears

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "email",
            "product",
        )


class OrderListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta(OrderSerializer.Meta):
        pass
