import json

from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Product


class ProductApiTests(APITestCase):
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


class AvailableProductApiTests(APITestCase):
    def test_available_filter(self):
        self.client.post(
            "/api/catalog/products/",
            {"sku": "AV-001", "name": "Pan activo",
             "description": "Disponible", "price": "1000.00"},
            format="json",
        )
        inactive = self.client.post(
            "/api/catalog/products/",
            {"sku": "AV-002", "name": "Pan inactivo",
             "description": "No disponible", "price": "2000.00"},
            format="json",
        )
        pk = inactive.data["id"]
        self.client.delete(f"/api/catalog/products/{pk}/")

        available = self.client.get("/api/catalog/products/available/")
        self.assertEqual(available.status_code, 200)
        self.assertEqual(len(available.data), 1)
        self.assertEqual(available.data[0]["sku"], "AV-001")

        stored = Product.objects.get(pk=pk)
        self.assertEqual(stored.status, False)

        all_products = self.client.get("/api/catalog/products/")
        self.assertGreaterEqual(len(all_products.data), 2)
