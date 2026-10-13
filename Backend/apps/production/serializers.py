from rest_framework import serializers

from apps.production.models import ProductionBatch, SupplyMovement


class ProductionBatchSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(source="recipe.name", read_only=True)

    class Meta:
        model = ProductionBatch
        fields = [
            "id",
            "recipe",
            "recipe_name",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "recipe_name", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class SupplyMovementSerializer(serializers.ModelSerializer):
    supply_name = serializers.CharField(source="supply.name", read_only=True)
    production_batch_name = serializers.CharField(
        source="production_batch.name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = SupplyMovement
        fields = [
            "id",
            "production_batch",
            "production_batch_name",
            "supply",
            "supply_name",
            "type",
            "date",
            "quantity",
            "notes",
            "status",
        ]
        read_only_fields = ["id", "supply_name", "production_batch_name"]
        extra_kwargs = {
            "production_batch": {"required": False, "allow_null": True},
            "notes": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_notes(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value
