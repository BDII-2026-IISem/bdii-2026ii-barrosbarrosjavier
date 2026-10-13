from rest_framework import status
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.sale.models import Sale
from apps.sale.serializers import SaleRegisterSerializer, SaleSerializer


class SaleRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SaleRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = serializer.save()
        sale = Sale.objects.prefetch_related("details__product").get(pk=sale.pk)
        return Response(SaleSerializer(sale).data, status=status.HTTP_201_CREATED)


class SaleReadViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """Lectura y anulación lógica de ventas.

    GET /api/sale/sales/         → lista (ListModelMixin.list)
    GET /api/sale/sales/<pk>/    → detalle (RetrieveModelMixin.retrieve)
    DELETE /api/sale/sales/<pk>/ → anula (DestroyModelMixin.destroy → Sale.void)
    """

    permission_classes = [AllowAny]
    serializer_class = SaleSerializer
    lookup_value_converter = "int"

    def get_queryset(self):
        return (
            Sale.objects.prefetch_related("details__product")
            .order_by("-date", "-id")
        )

    def perform_destroy(self, instance):
        instance.void()


class SaleCollectionAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        handler = SaleRegisterAPIView()
        handler.request = request
        handler.format_kwarg = None
        handler.args = ()
        handler.kwargs = {}
        return handler.post(request)

    def get(self, request, *args, **kwargs):
        handler = SaleReadViewSet()
        handler.request = request
        handler.format_kwarg = None
        handler.args = ()
        handler.kwargs = {}
        handler.action_map = {"get": "list"}
        handler.action = "list"
        return handler.list(request, *args, **kwargs)
