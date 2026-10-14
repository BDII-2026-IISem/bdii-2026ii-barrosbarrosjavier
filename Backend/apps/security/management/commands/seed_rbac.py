from django.core.management.base import BaseCommand
from django.urls import resolve
from django.urls.exceptions import Resolver404

from apps.common.status import RecordStatus
from apps.security.models import Resource, ResourceRole, Role, RoleUser


# Lista de (method, sample_path) que el rol admin recibe.
# El path es solo una muestra: resolve(sample).route devuelve el patrón
# real (api/catalog/products/<int:pk>/) que el permiso comparará.
SEEDS = [
    # Catálogo
    ("GET",    "/api/catalog/products/"),
    ("POST",   "/api/catalog/products/"),
    ("GET",    "/api/catalog/products/1/"),
    ("PUT",    "/api/catalog/products/1/"),
    ("PATCH",  "/api/catalog/products/1/"),
    ("DELETE", "/api/catalog/products/1/"),
    ("GET",    "/api/catalog/products/available/"),

    ("GET",    "/api/catalog/supplies/"),
    ("POST",   "/api/catalog/supplies/"),
    ("GET",    "/api/catalog/supplies/1/"),
    ("PUT",    "/api/catalog/supplies/1/"),
    ("PATCH",  "/api/catalog/supplies/1/"),
    ("DELETE", "/api/catalog/supplies/1/"),

    ("GET",    "/api/catalog/recipes/"),
    ("POST",   "/api/catalog/recipes/"),
    ("GET",    "/api/catalog/recipes/1/"),
    ("PUT",    "/api/catalog/recipes/1/"),
    ("PATCH",  "/api/catalog/recipes/1/"),
    ("DELETE", "/api/catalog/recipes/1/"),

    ("GET",    "/api/catalog/recipe-supplies/"),
    ("POST",   "/api/catalog/recipe-supplies/"),
    ("GET",    "/api/catalog/recipe-supplies/1/"),
    ("PUT",    "/api/catalog/recipe-supplies/1/"),
    ("PATCH",  "/api/catalog/recipe-supplies/1/"),
    ("DELETE", "/api/catalog/recipe-supplies/1/"),

    ("GET",    "/api/catalog/promotions/"),
    ("POST",   "/api/catalog/promotions/"),
    ("GET",    "/api/catalog/promotions/1/"),
    ("PUT",    "/api/catalog/promotions/1/"),
    ("PATCH",  "/api/catalog/promotions/1/"),
    ("DELETE", "/api/catalog/promotions/1/"),

    # Producción
    ("GET",    "/api/production/production-batches/"),
    ("POST",   "/api/production/production-batches/"),
    ("GET",    "/api/production/production-batches/1/"),
    ("PUT",    "/api/production/production-batches/1/"),
    ("PATCH",  "/api/production/production-batches/1/"),
    ("DELETE", "/api/production/production-batches/1/"),

    ("GET",    "/api/production/supply-movements/"),
    ("POST",   "/api/production/supply-movements/"),
    ("GET",    "/api/production/supply-movements/1/"),
    ("PUT",    "/api/production/supply-movements/1/"),
    ("PATCH",  "/api/production/supply-movements/1/"),
    ("DELETE", "/api/production/supply-movements/1/"),

    # Ventas
    ("GET",    "/api/sale/sales/"),
    ("POST",   "/api/sale/sales/"),
    ("GET",    "/api/sale/sales/1/"),
    ("DELETE", "/api/sale/sales/1/"),

    # Matriz RBAC
    ("GET",    "/api/users/"),
    ("POST",   "/api/users/"),
    ("GET",    "/api/users/1/"),
    ("PUT",    "/api/users/1/"),
    ("PATCH",  "/api/users/1/"),
    ("DELETE", "/api/users/1/"),

    ("GET",    "/api/roles/"),
    ("POST",   "/api/roles/"),
    ("GET",    "/api/roles/1/"),
    ("PUT",    "/api/roles/1/"),
    ("PATCH",  "/api/roles/1/"),
    ("DELETE", "/api/roles/1/"),

    ("GET",    "/api/role-users/"),
    ("POST",   "/api/role-users/"),
    ("GET",    "/api/role-users/1/"),
    ("PUT",    "/api/role-users/1/"),
    ("PATCH",  "/api/role-users/1/"),
    ("DELETE", "/api/role-users/1/"),

    ("GET",    "/api/resources/"),
    ("POST",   "/api/resources/"),
    ("GET",    "/api/resources/1/"),
    ("PUT",    "/api/resources/1/"),
    ("PATCH",  "/api/resources/1/"),
    ("DELETE", "/api/resources/1/"),

    ("GET",    "/api/resource-roles/"),
    ("POST",   "/api/resource-roles/"),
    ("GET",    "/api/resource-roles/1/"),
    ("PUT",    "/api/resource-roles/1/"),
    ("PATCH",  "/api/resource-roles/1/"),
    ("DELETE", "/api/resource-roles/1/"),
]


class Command(BaseCommand):
    help = (
        "Sincroniza la matriz RBAC con las rutas reales de la API. "
        "Crea/activa el rol admin y le concede todos los recursos. "
        "Con --username, asigna el rol al usuario indicado."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            dest="username",
            default=None,
            help="Username del usuario al que se asigna el rol admin.",
        )
        parser.add_argument(
            "--role",
            dest="role_name",
            default="admin",
            help="Nombre del rol que se crea/reactiva (default: admin).",
        )

    def handle(self, *args, **options):
        role_name = options["role_name"]
        username = options["username"]

        role, created = Role.objects.get_or_create(
            name=role_name,
            defaults={
                "description": f"Rol {role_name} sembrado por seed_rbac",
                "status": RecordStatus.ACTIVE,
            },
        )
        if not created and role.status != RecordStatus.ACTIVE:
            role.status = RecordStatus.ACTIVE
            role.save(update_fields=["status", "updated_at"])
            self.stdout.write(f"Rol '{role_name}' reactivado")

        created_resources = 0
        created_grants = 0

        for method, sample_path in SEEDS:
            try:
                match = resolve(sample_path)
            except Resolver404:
                self.stderr.write(
                    f"Ruta no encontrada: {sample_path} (method={method})"
                )
                continue
            route = match.route
            resource, r_created = Resource.objects.get_or_create(
                method=method,
                route=route,
                defaults={
                    "name": f"{method} {route}",
                    "status": RecordStatus.ACTIVE,
                },
            )
            if r_created:
                created_resources += 1
            elif resource.status != RecordStatus.ACTIVE:
                resource.status = RecordStatus.ACTIVE
                resource.save(update_fields=["status", "updated_at"])

            grant, g_created = ResourceRole.objects.get_or_create(
                resource=resource,
                role=role,
                defaults={"status": RecordStatus.ACTIVE},
            )
            if g_created:
                created_grants += 1
            elif grant.status != RecordStatus.ACTIVE:
                grant.status = RecordStatus.ACTIVE
                grant.save(update_fields=["status", "updated_at"])

        if username:
            from django.contrib.auth import get_user_model

            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stderr.write(f"Usuario '{username}' no existe. Se omite RoleUser.")
            else:
                if user.status != RecordStatus.ACTIVE:
                    user.status = RecordStatus.ACTIVE
                    user.save(update_fields=["status", "updated_at"])
                RoleUser.objects.get_or_create(
                    role=role,
                    user=user,
                    defaults={"status": RecordStatus.ACTIVE},
                )
                self.stdout.write(
                    f"Rol '{role_name}' asignado a '{username}'"
                )

        self.stdout.write(self.style.SUCCESS(
            f"Recursos RBAC sincronizados: "
            f"{created_resources} nuevos, {created_grants} concesiones nuevas. "
            f"Total de recursos: {Resource.objects.count()}, "
            f"Total de concesiones del rol '{role_name}': "
            f"{ResourceRole.objects.filter(role=role).count()}"
        ))
