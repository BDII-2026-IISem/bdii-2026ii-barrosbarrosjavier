from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.production.models import ProductionBatch, SupplyMovement
from apps.production.serializers import (
    ProductionBatchSerializer,
    SupplyMovementSerializer,
)
from apps.security.permissions import HasResourceAccess


class ProductionBatchViewSet(viewsets.ModelViewSet):
    queryset = ProductionBatch.objects.select_related("recipe").all()
    serializer_class = ProductionBatchSerializer
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
        instance.save(update_fields=["status", "updated_at"])


class SupplyMovementViewSet(viewsets.ModelViewSet):
    queryset = SupplyMovement.objects.select_related(
        "production_batch", "supply"
    ).all()
    serializer_class = SupplyMovementSerializer
    permission_classes = [IsAuthenticated, HasResourceAccess]
    lookup_value_converter = "int"
