from django import forms

from shop_service.models import Product, Order


class ProductSearchForm(forms.Form):
    category = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by category ..."}
        ),
    )


class OrderForm(forms.ModelForm):
    product = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Product.objects.prefetch_related("category"),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Order
        fields = "__all__"
