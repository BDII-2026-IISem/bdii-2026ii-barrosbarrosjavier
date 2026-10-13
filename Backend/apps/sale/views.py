from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.sale.models import Sale, SaleDetail, Payment
from apps.sale.serializers import (
    SaleSerializer,
    SaleDetailSerializer,
    PaymentSerializer,
)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.prefetch_related("details").all()
    serializer_class = SaleSerializer
    permission_classes = [AllowAny]
    lookup_value_converter = "int"


class SaleDetailViewSet(viewsets.ModelViewSet):
    queryset = SaleDetail.objects.select_related("sale", "product").all()
    serializer_class = SaleDetailSerializer
    permission_classes = [AllowAny]
    lookup_value_converter = "int"


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]
    lookup_value_converter = "int"
