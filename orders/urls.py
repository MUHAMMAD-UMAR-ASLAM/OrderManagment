from django.urls import path

from .views import (
    ProductListCreateView,
    OrderListCreateView,
    OrderDetailView,
    CancelOrderView,
)

urlpatterns = [

    path(
        "products/",
        ProductListCreateView.as_view(),
        name="products"
    ),

   
    path(
        "orders/",
        OrderListCreateView.as_view(),
        name="order-list"
    ),

    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail"
    ),

    path(
        "orders/<int:pk>/cancel/",
        CancelOrderView.as_view(),
        name="order-cancel"
    ),
]