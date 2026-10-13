from decimal import Decimal

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.catalog.models import Product
from apps.sale.models import Sale, SaleDetail, Payment


class SaleDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = SaleDetail
        fields = [
            "id",
            "sale",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "total",
            "notes",
        ]
        read_only_fields = ["id", "product_name", "total"]
        extra_kwargs = {
            "notes": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_notes(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "reference_type",
            "reference_id",
            "method",
            "amount",
            "date",
            "status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "reference_type": {"max_length": 50},
            "method": {"max_length": 50},
            "status": {"max_length": 30},
        }


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "client_id",
            "date",
            "subtotal",
            "taxes",
            "total",
            "status",
            "details",
        ]
        read_only_fields = ["id", "details"]
        extra_kwargs = {
            "client_id": {"required": False, "allow_null": True},
        }


class SaleItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
    )
    quantity = serializers.IntegerField(min_value=1)


class SaleRegisterSerializer(serializers.Serializer):
    client_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    sale_date = serializers.DateTimeField()
    taxes = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
        default=Decimal("0.00"),
    )
    items = SaleItemSerializer(many=True, allow_empty=False)

    def create(self, validated_data):
        items = [
            {"product_id": item["product"].id, "quantity": item["quantity"]}
            for item in validated_data["items"]
        ]
        try:
            return Sale.objects.register(
                client_id=validated_data.get("client_id"),
                sale_date=validated_data["sale_date"],
                taxes=validated_data["taxes"],
                items=items,
            )
        except DjangoValidationError as exc:
            if getattr(exc, "message_dict", None):
                raise serializers.ValidationError(exc.message_dict) from exc
            raise serializers.ValidationError(exc.messages) from exc
