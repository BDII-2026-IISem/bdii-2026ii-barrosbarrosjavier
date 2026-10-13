from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from apps.common.status import RecordStatus


class HornoRaizJWTAuthentication(JWTAuthentication):
    """JWT con token + verificación de status.

    Rechaza al usuario cuyo status no es active aunque la firma del JWT
    siga siendo válida. Responde 401, no 403.
    """

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if user.status != RecordStatus.ACTIVE or not user.is_active:
            raise AuthenticationFailed(
                "El usuario no está activo.",
                code="user_inactive",
            )
        return user
