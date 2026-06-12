
from .models import Product,Order
from .permissions import IsStafforReadOnly,IsOwnerOrStaff
from .serializers import ProductSerializer,OrderSerializer
from rest_framework import generics,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStafforReadOnly]

    def get_queryset(self):
        queryset= Product.objects.all()

        in_stock=self.request.query_params.get('in_stock')
        search= self.request.query_params.get('search')

        if in_stock:
            queryset=queryset.filter(stock_quantity__gte=1)

        if search:
            queryset=queryset.filter(Q(name__icontains=search) | Q(sku__icontains=search))

        return queryset




class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):

        queryset = (
            Order.objects
            .select_related("customer")
            .prefetch_related(
                "items",
                "items__product"
            )
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            customer=self.request.user
        )

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrStaff]



    def get_queryset(self):
        queryset = (
            Order.objects
            .prefetch_related(
                "items",
                "items__product"
            )
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            customer=self.request.user
        )

class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):

        order = (
            Order.objects
            .select_for_update()
            .prefetch_related(
                "items",
                "items__product"
            )
            .get(pk=pk)
        )

        if (
            not request.user.is_staff
            and order.customer != request.user
        ):
            return Response(
                {"detail": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        if order.status == "shipped":
            return Response(
                {
                    "detail":
                    "Shipped orders cannot be cancelled"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status != "pending":
            return Response(
                {
                    "detail":
                    "Only pending orders may be cancelled"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in order.items.all():

            product = item.product

            product.stock_quantity += item.quantity

            product.save()

        order.status = "cancelled"
        order.save()

        return Response(
            {"message": "Order cancelled"}
        )