from django.urls import path

from shop_service.views import ProductListView, OrderCreateView

urlpatterns = [
    path(
        "list/",
        ProductListView.as_view(),
        name="product-list",
    ),
    path(
        "create_order/",
        OrderCreateView.as_view(),
        name="order-create",
    ),
]

app_name = "shop_service"
