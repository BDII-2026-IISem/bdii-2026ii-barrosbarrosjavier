from rest_framework import serializers

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
