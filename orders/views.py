
from .models import Product
from .permissions import IsStafforReadOnly
from .serializers import ProductSerializer
from rest_framework import generics
from  django.db.models import Q

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStafforReadOnly]

    def get_queryset(self):
        queryset= Product.objects.all()

        in_stock=self.request.query_params.get('in_stock')
        search= self.request.query_params.get('search')

        if in_stock:
            queryset=queryset.filter(stock__gte=1)

        if search:
            queryset=queryset.filter(Q(name__icontains=search) | Q(sku__icontains=search))

        return queryset

