from django.urls import path

from orders.views import ProductListCreateApiView

urlpatterns = [
    path('products/', ProductListCreateApiView.as_view(), name='products'),
]