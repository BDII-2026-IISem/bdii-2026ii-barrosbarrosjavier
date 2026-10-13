from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.catalog.models import (
    Product,
    Supply,
    Recipe,
    RecipeSupply,
    Promotion,
)
from apps.catalog.serializers import (
    ProductSerializer,
    SupplySerializer,
    RecipeSerializer,
    RecipeSupplySerializer,
    PromotionSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_value_converter = "int"

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value is not None:
            normalized = status_value.strip().lower()
            if normalized in {"true", "1", "active"}:
                queryset = queryset.filter(status=True)
            elif normalized in {"false", "0", "inactive"}:
                queryset = queryset.filter(status=False)
        return queryset

    def perform_destroy(self, instance):
        instance.status = False
        instance.save(update_fields=["status"])


# Serializers y ViewSets para los demás recursos (los publicamos en el ISS-09)
class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("product").all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]


class RecipeSupplyViewSet(viewsets.ModelViewSet):
    queryset = RecipeSupply.objects.select_related("main", "related").all()
    serializer_class = RecipeSupplySerializer
    permission_classes = [AllowAny]


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [AllowAny]
