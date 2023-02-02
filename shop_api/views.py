from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from shop_api.serializers import OrderSerializer, OrderListSerializer
from shop_service.models import Order


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related("product__category")
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer
