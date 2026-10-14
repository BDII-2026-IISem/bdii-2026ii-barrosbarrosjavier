from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

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
from apps.security.permissions import HasResourceAccess


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]
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


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("product").all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]


class RecipeSupplyViewSet(viewsets.ModelViewSet):
    queryset = RecipeSupply.objects.select_related("main", "related").all()
    serializer_class = RecipeSupplySerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]


class AvailableProductListAPIView(ListAPIView):
    """Lista solo los productos activos (status=True)."""

    permission_classes = [IsAuthenticated, HasResourceAccess]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(status=True)
