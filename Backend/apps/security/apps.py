from django.apps import AppConfig


class SecurityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.security"
    label = "security"

    def ready(self):
        # Carga la extensión OpenApiAuthenticationExtension para que
        # Swagger muestre el botón Authorize con Bearer.
        from apps.security import schema  # noqa: F401
