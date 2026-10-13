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


class SaleReadAndVoidTests(APITestCase):
    def setUp(self):
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
        # Cambiar el precio del producto después de vender
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

        # Segunda llamada: idempotente
        second = self.client.delete(f"/api/sale/sales/{sale_id}/")
        self.assertEqual(second.status_code, status.HTTP_204_NO_CONTENT)

        # La fila sigue existiendo
        self.assertEqual(Sale.objects.filter(pk=sale_id).count(), 1)
        sale.refresh_from_db()
        self.assertEqual(sale.status, "cancelled")

    def test_void_does_not_delete_sale_details(self):
        sale_id = self._register_sale()
        self.client.delete(f"/api/sale/sales/{sale_id}/")
        self.assertEqual(SaleDetail.objects.filter(sale_id=sale_id).count(), 1)
