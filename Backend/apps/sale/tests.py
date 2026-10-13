import json
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Product
from apps.sale.models import Sale, SaleDetail


class SaleTransactionTests(APITestCase):
    def setUp(self):
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
        # response.data usa snake_case (nombres internos)
        self.assertEqual(response.data["subtotal"], "24.50")
        self.assertEqual(response.data["taxes"], "0.00")
        self.assertEqual(response.data["total"], "24.50")
        self.assertEqual(response.data["status"], "paid")

        # json.loads(response.content) aplica camelCase (renderizado HTTP)
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
