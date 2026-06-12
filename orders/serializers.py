from django.db import  transaction
from rest_framework import serializers
from rest_framework.response import Response

from orders.models import Order, Product,OrderItem
from django.db.models import F

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
        ]



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(
        source="items",
        many=True,
        read_only=True
    )

    items = serializers.ListField(
        write_only=True,
        required=False
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "created_at",
            "order_items",
            "items",
            "total",
        ]
        read_only_fields = [
            "id",
            "customer",
            "status",
            "created_at",
            "total",
        ]

    def get_total(self, obj):
        return sum(
            item.price * item.quantity
            for item in obj.items.all()
        )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                "Order cannot be empty."
            )

        for item in value:
            if item.get("quantity") is None:
                raise serializers.ValidationError(
                    "Quantity is required."
                )

            if item["quantity"] <= 0:
                raise serializers.ValidationError(
                    "Quantity must be positive."
                )

            if "product_id" not in item:
                raise serializers.ValidationError(
                    "product_id is required."
                )

        return value

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        items_data = validated_data.pop("items")

        product_ids = [i["product_id"] for i in items_data]

        products = Product.objects.select_for_update().filter(
            id__in=product_ids
        )

        products_map = {p.id: p for p in products}

        for item in items_data:
            if item["product_id"] not in products_map:
                raise serializers.ValidationError(
                    f"Product {item['product_id']} not found"
                )

        for item in items_data:
            product = products_map[item["product_id"]]

            if product.stock_quantity < item["quantity"]:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}"
                )

        order = Order.objects.create(customer=user)

        order_items = []

        for item in items_data:
            product = products_map[item["product_id"]]
            qty = item["quantity"]

            product.stock = F("stock_quantity") - qty
            product.save(update_fields=["stock_quantity"])

            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        return order