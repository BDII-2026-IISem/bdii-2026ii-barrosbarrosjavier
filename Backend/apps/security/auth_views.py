import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from apps.common.status import RecordStatus
from apps.security.models import RefreshToken
from apps.security.serializers import (
    LoginSerializer,
    RefreshSerializer,
)
from apps.security.tokens import generate_refresh_value, hash_token

User = get_user_model()


def token_payload(user, raw_refresh):
    """Devuelve el par access + refresh para el cliente."""
    access = AccessToken.for_user(user)
    lifetime = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    return {
        "access": str(access),
        "refresh": raw_refresh,
        "token_type": "Bearer",
        "access_expires_in": lifetime,
    }


def issue_refresh(user, family_id=None):
    """Crea la fila RefreshToken con el hash y devuelve el valor en claro."""
    raw_refresh = generate_refresh_value()
    stored = RefreshToken.objects.create(
        user=user,
        token_hash=hash_token(raw_refresh),
        family_id=family_id or uuid.uuid4(),
        expires_at=RefreshToken.default_expiry(),
        status=RecordStatus.ACTIVE,
    )
    return stored, raw_refresh


def _find_user(username, email):
    """Busca por username, por email, o por ambos si vienen los dos."""
    if username and email:
        return User.objects.filter(username=username, email__iexact=email).first()
    if username:
        return User.objects.filter(username=username).first()
    if email:
        return User.objects.filter(email__iexact=email).first()
    return None


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = _find_user(data.get("username"), data.get("email"))
        invalid = Response(
            {"detail": "Credenciales inválidas."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        if user is None or user.status != RecordStatus.ACTIVE:
            return invalid
        if not user.check_password(data["password"]):
            return invalid

        _stored, raw_refresh = issue_refresh(user)
        return Response(token_payload(user, raw_refresh), status=status.HTTP_200_OK)


class RefreshAPIView(APIView):
    """Rota el refresh y detecta reuso.

    - Busca la fila por hash con select_for_update().
    - Si ya fue rotado, revocado o inactivo → revoca toda la familia → 401.
    - Si está vencido → inactiva ese token → 401.
    - Si el usuario está inactive → inactiva ese token → 401.
    - Si está vigente → emite otro par de la misma familia y marca el
      anterior con replaced_by.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_refresh = serializer.validated_data["refresh"]
        token_hash = hash_token(raw_refresh)

        invalid = Response(
            {"detail": "Refresh token inválido."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        with transaction.atomic():
            stored = (
                RefreshToken.objects.select_for_update()
                .select_related("user")
                .filter(token_hash=token_hash)
                .first()
            )

            if stored is None:
                return invalid

            # Reuso: ya rotado, ya revocado o ya inactivo → apaga la familia
            if (
                stored.replaced_by_id is not None
                or stored.revoked_at is not None
                or stored.status != RecordStatus.ACTIVE
            ):
                RefreshToken.objects.filter(
                    family_id=stored.family_id,
                    status=RecordStatus.ACTIVE,
                ).update(
                    status=RecordStatus.INACTIVE,
                    revoked_at=timezone.now(),
                    updated_at=timezone.now(),
                )
                return invalid

            # Vencido: apaga solo ese token
            if stored.expires_at <= timezone.now():
                stored.status = RecordStatus.INACTIVE
                stored.save(update_fields=["status", "updated_at"])
                return invalid

            # Usuario inactive: apaga solo ese token
            if stored.user.status != RecordStatus.ACTIVE:
                stored.status = RecordStatus.INACTIVE
                stored.save(update_fields=["status", "updated_at"])
                return invalid

            # Vigente: emite otro par de la misma familia
            new_stored, new_raw = issue_refresh(
                stored.user, family_id=stored.family_id
            )
            stored.replaced_by = new_stored
            stored.save(update_fields=["replaced_by", "updated_at"])

            return Response(
                token_payload(stored.user, new_raw),
                status=status.HTTP_200_OK,
            )
