from rest_framework.permissions import BasePermission

from apps.common.status import RecordStatus
from apps.security.models import ResourceRole


class HasResourceAccess(BasePermission):
    """Autoriza por método y patrón de ruta, con negación por defecto.

    Compara request.method con request.resolver_match.route y exige que
    todos los eslabones de la cadena usuario -> rol -> recurso estén
    activos. HEAD se evalúa como GET. OPTIONS, si ya hay usuario, no busca
    recurso (es el preflight, no una operación de negocio).
    """

    message = "No tiene autorización para ejecutar esta operación."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "status", None) != RecordStatus.ACTIVE:
            return False
        if request.method.upper() == "OPTIONS":
            return True

        match = request.resolver_match
        if match is None:
            return False
        method = request.method.upper()
        if method == "HEAD":
            method = "GET"
        return ResourceRole.objects.filter(
            status=RecordStatus.ACTIVE,
            resource__status=RecordStatus.ACTIVE,
            resource__method=method,
            resource__route=match.route,
            role__status=RecordStatus.ACTIVE,
            role__assignments__user=user,
            role__assignments__status=RecordStatus.ACTIVE,
        ).exists()
