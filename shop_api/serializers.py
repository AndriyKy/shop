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
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """Provide Name, Email address and Product model index list to place an order"""

    products = serializers.ListSerializer(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
        source="product",
        help_text="List of Product indexes",
    )

    def validate(self, attrs):
        data = super(OrderSerializer, self).validate(attrs=attrs)
        product_indexes = Product.objects.values_list("id", flat=True)
        for index in data["product"]:
            if index not in product_indexes:
                raise ValidationError(f"Product index {index} does not exist!")
        return data

    def to_representation(self, obj):
        # Helps to correctly display the custom field products
        self.fields["products"] = ProductSerializer(
            many=True, read_only=True, source="product"
        )
        return super().to_representation(obj)

    def create(self, validated_data):
        with transaction.atomic():
            products_data = validated_data.pop("product")
            products_list = Product.objects.filter(pk__in=products_data).all()
            order = Order.objects.create(**validated_data)
            order.product.add(*products_list)
            return order

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "email",
            "products",
        )


class OrderListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source="product")

    class Meta(OrderSerializer.Meta):
        pass
