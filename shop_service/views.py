from django.urls import reverse_lazy
from django.views import generic

from shop_service.forms import ProductSearchForm, OrderForm
from shop_service.models import Product, Order


class ProductListView(generic.ListView):
    model = Product
    template_name = "shop/product_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category = self.request.GET.get("category", "")
        context["search_form"] = ProductSearchForm(
            initial={"category": category}
        )

        return context

    def get_queryset(self):
        queryset = Product.objects.select_related(
            "category",
            "user",
        )

        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                category__name__icontains=form.cleaned_data["category"]
            )

        return queryset


class OrderCreateView(generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = "shop/order_form.html"
    success_url = reverse_lazy("shop_service:product-list")


class OrderWithJQueryCreateView(generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = "shop/order_jquery_form.html"
    success_url = reverse_lazy("shop_service:order-jquery-create")
