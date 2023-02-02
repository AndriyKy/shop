from django.urls import path

from shop_service.views import (
    ProductListView,
    OrderCreateView,
    OrderWithJQueryCreateView,
)

urlpatterns = [
    path(
        "products/",
        ProductListView.as_view(),
        name="product-list",
    ),
    path(
        "create_order/",
        OrderCreateView.as_view(),
        name="order-create",
    ),
    path(
        "create_order/jquery/",
        OrderWithJQueryCreateView.as_view(),
        name="order-jquery-create",
    ),
]

app_name = "shop_service"
