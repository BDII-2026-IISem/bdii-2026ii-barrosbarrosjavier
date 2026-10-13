from rest_framework import serializers

from apps.catalog.models import Product, Supply, Recipe, RecipeSupply, Promotion


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "sku": {"max_length": 50},
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = [
            "id",
            "code",
            "name",
            "unit_of_measure",
            "min_stock",
            "status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "code": {"max_length": 50},
            "name": {"min_length": 2, "max_length": 100},
            "unit_of_measure": {"max_length": 30},
        }


class RecipeSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "product",
            "product_name",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "product_name", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value


class RecipeSupplySerializer(serializers.ModelSerializer):
    main_name = serializers.CharField(source="main.name", read_only=True)
    related_name = serializers.CharField(source="related.name", read_only=True)

    class Meta:
        model = RecipeSupply
        fields = [
            "id",
            "main",
            "main_name",
            "related",
            "related_name",
            "relation_data",
            "status",
        ]
        read_only_fields = ["id", "main_name", "related_name"]
        extra_kwargs = {
            "relation_data": {"required": False, "allow_null": True, "allow_blank": True},
        }


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"min_length": 2, "max_length": 100},
            "description": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_description(self, value):
        if value is None or str(value).strip() == "":
            return None
        return value
