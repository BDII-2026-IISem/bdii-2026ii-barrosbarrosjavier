from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Product
from apps.common.status import RecordStatus
from apps.common.testing import PASSWORD, create_active_user
from apps.security.models import (
    HttpMethod,
    Resource,
    ResourceRole,
    Role,
    RoleUser,
)


def grant(user, method, route, name="test-grant"):
    """Crea Resource + Role + ResourceRole + RoleUser activos para el user."""
    resource = Resource.objects.create(
        name=name,
        method=method,
        route=route,
        status=RecordStatus.ACTIVE,
    )
    role = Role.objects.create(name=f"role-{method}-{route}", status=RecordStatus.ACTIVE)
    ResourceRole.objects.create(
        resource=resource, role=role, status=RecordStatus.ACTIVE,
    )
    RoleUser.objects.create(
        role=role, user=user, status=RecordStatus.ACTIVE,
    )


class AuthenticatedCatalogTest(APITestCase):
    """Base: crea user y le da los permisos RBAC del catálogo."""

    def setUp(self):
        self.user = create_active_user(
            username="catalog-user",
            email="catalog@hornoraiz.test",
        )
        # Conceder TODOS los métodos que usan los tests de Product
        grant(self.user, HttpMethod.GET, "api/catalog/products/", "list-products")
        grant(self.user, HttpMethod.POST, "api/catalog/products/", "create-product")
        grant(self.user, HttpMethod.GET, "api/catalog/products/<int:pk>/", "detail-product")
        grant(self.user, HttpMethod.PUT, "api/catalog/products/<int:pk>/", "update-product")
        grant(self.user, HttpMethod.PATCH, "api/catalog/products/<int:pk>/", "patch-product")
        grant(self.user, HttpMethod.DELETE, "api/catalog/products/<int:pk>/", "delete-product")

        login = self.client.post(
            "/api/auth/login/",
            {"username": "catalog-user", "password": PASSWORD},
            format="json",
        )
        self.access = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")


class ProductApiTests(AuthenticatedCatalogTest):
    def test_create_defaults_and_persists(self):
        response = self.client.post(
            "/api/catalog/products/",
            {
                "sku": "API-001",
                "name": "Pan de API",
                "description": "Producto de prueba API",
                "price": "1500.00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(response.data["sku"], "API-001")

        stored = Product.objects.get(pk=response.data["id"])
        self.assertEqual(stored.name, "Pan de API")

    def test_invalid_name_and_duplicate_sku(self):
        invalid = self.client.post(
            "/api/catalog/products/",
            {"sku": "API-002", "name": "A", "price": "100.00"},
            format="json",
        )
        self.assertEqual(invalid.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.post(
            "/api/catalog/products/",
            {"sku": "API-003", "name": "Pan 3", "price": "100.00"},
            format="json",
        )
        duplicate = self.client.post(
            "/api/catalog/products/",
            {"sku": "API-003", "name": "Pan 4", "price": "200.00"},
            format="json",
        )
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_keeps_the_row(self):
        created = self.client.post(
            "/api/catalog/products/",
            {"sku": "API-004", "name": "Pan 4", "price": "100.00"},
            format="json",
        )
        pk = created.data["id"]
        deleted = self.client.delete(f"/api/catalog/products/{pk}/")
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)

        stored = Product.objects.get(pk=pk)
        self.assertEqual(stored.status, False)

    def test_list_retrieve_and_update(self):
        created = self.client.post(
            "/api/catalog/products/",
            {"sku": "API-005", "name": "Pan 5", "price": "100.00"},
            format="json",
        )
        pk = created.data["id"]

        listed = self.client.get("/api/catalog/products/")
        self.assertEqual(listed.status_code, status.HTTP_200_OK)

        detail = self.client.get(f"/api/catalog/products/{pk}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["name"], "Pan 5")

        updated = self.client.patch(
            f"/api/catalog/products/{pk}/",
            {"price": "250.00"},
            format="json",
        )
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        self.assertEqual(updated.data["price"], "250.00")


class AvailableProductApiTests(AuthenticatedCatalogTest):
    def test_available_filter(self):
        # Crear un producto activo
        self.client.post(
            "/api/catalog/products/",
            {"sku": "AV-001", "name": "Pan activo",
             "description": "Disponible", "price": "1000.00"},
            format="json",
        )
        # Crear un producto y desactivarlo
        inactive = self.client.post(
            "/api/catalog/products/",
            {"sku": "AV-002", "name": "Pan inactivo",
             "description": "No disponible", "price": "2000.00"},
            format="json",
        )
        pk = inactive.data["id"]
        self.client.delete(f"/api/catalog/products/{pk}/")

        # La lista de disponibles incluye solo el activo (endpoint open)
        available = self.client.get("/api/catalog/products/available/")
        self.assertEqual(available.status_code, status.HTTP_200_OK)
        self.assertEqual(len(available.data), 1)
        self.assertEqual(available.data[0]["sku"], "AV-001")

        # La fila del inactivo sigue en la tabla
        stored = Product.objects.get(pk=pk)
        self.assertEqual(stored.status, False)

        # El endpoint normal sí lo lista
        all_products = self.client.get("/api/catalog/products/")
        self.assertGreaterEqual(len(all_products.data), 2)
