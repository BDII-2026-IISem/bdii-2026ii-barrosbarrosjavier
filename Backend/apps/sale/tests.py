import json
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Product
from apps.common.testing import create_active_user, grant
from apps.sale.models import Sale, SaleDetail


class AuthenticatedSaleTest(APITestCase):
    """Base: user con concesión para POST/GET en sales y GET/DELETE en detail."""

    def setUp(self):
        self.user = create_active_user(
            username="sale-user",
            email="sale@hornoraiz.test",
        )
        grant(self.user, "GET", "/api/sale/sales/")
        grant(self.user, "POST", "/api/sale/sales/")
        grant(self.user, "GET", "/api/sale/sales/1/")
        grant(self.user, "DELETE", "/api/sale/sales/1/")
        self.client.force_authenticate(user=self.user)


class SaleTransactionTests(AuthenticatedSaleTest):
    def setUp(self):
        super().setUp()
        self.water = Product.objects.create(
            sku="WAT-001", name="Agua", price=Decimal("10.00"), status=True,
        )
        self.bread = Product.objects.create(
            sku="BRE-001", name="Pan", price=Decimal("4.50"), status=True,
        )

    def _payload(self, items, taxes="0.00"):
        return {
            "clientId": None,
            "saleDate": timezone.now().isoformat(),
            "taxes": taxes,
            "items": items,
        }

    def test_register_snapshots_price_and_totals(self):
        response = self.client.post(
            "/api/sale/sales/",
            self._payload([
                {"productId": self.water.id, "quantity": 2},
                {"productId": self.bread.id, "quantity": 1},
            ]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["subtotal"], "24.50")
        self.assertEqual(response.data["taxes"], "0.00")
        self.assertEqual(response.data["total"], "24.50")
        self.assertEqual(response.data["status"], "paid")

        wire = json.loads(response.content)
        self.assertIn("clientId", wire)
        self.assertIn("date", wire)
        self.assertNotIn("client_id", wire)

        water_line = next(
            line for line in wire["details"]
            if line["product"] == self.water.id
        )
        self.assertEqual(water_line["unitPrice"], "10.00")
        self.assertEqual(water_line["total"], "20.00")

    def test_price_change_doesnt_affect_existing_sale(self):
        response = self.client.post(
            "/api/sale/sales/",
            self._payload([{"productId": self.water.id, "quantity": 1}]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sale_id = response.data["id"]

        self.water.refresh_from_db()
        self.water.price = Decimal("99.00")
        self.water.save()

        sale = Sale.objects.get(pk=sale_id)
        detail = sale.details.first()
        self.assertEqual(detail.unit_price, Decimal("10.00"))
        self.assertEqual(sale.total, Decimal("10.00"))

    def test_empty_items_is_rejected(self):
        response = self.client.post(
            "/api/sale/sales/",
            self._payload([]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)

    def test_inactive_product_is_rejected(self):
        self.water.status = False
        self.water.save()
        response = self.client.post(
            "/api/sale/sales/",
            self._payload([{"productId": self.water.id, "quantity": 1}]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)

    def test_nonexistent_product_is_rejected(self):
        response = self.client.post(
            "/api/sale/sales/",
            self._payload([{"productId": 999999, "quantity": 1}]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)


class SaleReadAndVoidTests(AuthenticatedSaleTest):
    def setUp(self):
        super().setUp()
        self.water = Product.objects.create(
            sku="WAT-002", name="Agua 2", price=Decimal("10.00"), status=True,
        )

    def _register_sale(self, quantity=1):
        response = self.client.post(
            "/api/sale/sales/",
            {
                "clientId": None,
                "saleDate": timezone.now().isoformat(),
                "taxes": "0.00",
                "items": [{"productId": self.water.id, "quantity": quantity}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        return response.data["id"]

    def test_list_returns_the_registered_sale(self):
        sale_id = self._register_sale()
        response = self.client.get("/api/sale/sales/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(row["id"] == sale_id for row in response.data))

    def test_detail_keeps_historical_price(self):
        sale_id = self._register_sale()
        Product.objects.filter(pk=self.water.pk).update(price=Decimal("99.00"))
        detail = self.client.get(f"/api/sale/sales/{sale_id}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["details"][0]["unit_price"], "10.00")

    def test_void_cancels_sale_and_is_idempotent(self):
        sale_id = self._register_sale(quantity=2)
        first = self.client.delete(f"/api/sale/sales/{sale_id}/")
        self.assertEqual(first.status_code, status.HTTP_204_NO_CONTENT)

        sale = Sale.objects.get(pk=sale_id)
        self.assertEqual(sale.status, "cancelled")

        second = self.client.delete(f"/api/sale/sales/{sale_id}/")
        self.assertEqual(second.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Sale.objects.filter(pk=sale_id).count(), 1)

    def test_void_does_not_delete_sale_details(self):
        sale_id = self._register_sale()
        self.client.delete(f"/api/sale/sales/{sale_id}/")
        self.assertEqual(SaleDetail.objects.filter(sale_id=sale_id).count(), 1)
