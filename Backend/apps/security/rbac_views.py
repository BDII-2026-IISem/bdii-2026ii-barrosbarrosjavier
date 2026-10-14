from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.status import RecordStatus
from apps.security.models import (
    Resource,
    ResourceRole,
    Role,
    RoleUser,
    User,
)
from apps.security.permissions import HasResourceAccess
from apps.security.serializers import (
    ProfileSerializer,
    ResourceRoleSerializer,
    ResourceSerializer,
    RoleSerializer,
    RoleUserSerializer,
    UserSerializer,
)


class ProfileAPIView(RetrieveUpdateAPIView):
    """Perfil del usuario autenticado. JWT con token, sin RBAC."""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet con baja lógica y filtro ?status=.

    - DELETE cambia status a inactive en lugar de borrar la fila.
    - ?status=active o ?status=inactive filtra la lista.
    """

    permission_classes = [IsAuthenticated, HasResourceAccess]
    lookup_value_converter = "int"

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value:
            normalized = status_value.strip().lower()
            if normalized in {"active", "true", "1"}:
                queryset = queryset.filter(status=RecordStatus.ACTIVE)
            elif normalized in {"inactive", "false", "0"}:
                queryset = queryset.filter(status=RecordStatus.INACTIVE)
        return queryset

    def perform_destroy(self, instance):
        instance.status = RecordStatus.INACTIVE
        instance.save(update_fields=["status", "updated_at"])


class UserViewSet(SoftDeleteModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class RoleViewSet(SoftDeleteModelViewSet):
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer


class RoleUserViewSet(SoftDeleteModelViewSet):
    queryset = RoleUser.objects.select_related("role", "user").all()
    serializer_class = RoleUserSerializer


class ResourceViewSet(SoftDeleteModelViewSet):
    queryset = Resource.objects.all().order_by("id")
    serializer_class = ResourceSerializer


class ResourceRoleViewSet(SoftDeleteModelViewSet):
    queryset = ResourceRole.objects.select_related("resource", "role").all()
    serializer_class = ResourceRoleSerializer
