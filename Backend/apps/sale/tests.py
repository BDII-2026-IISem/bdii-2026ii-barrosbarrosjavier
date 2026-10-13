import json
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Product
from apps.sale.models import Sale, SaleDetail, Payment


class SaleApiTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            sku="SALE-ISS09-001", name="Pan Venta", price=Decimal("500.00")
        )

    def test_create_sale(self):
        response = self.client.post(
            "/api/sale/sales/",
            {
                "clientId": None,
                "date": timezone.now().isoformat(),
                "subtotal": "1000.00",
                "taxes": "190.00",
                "total": "1190.00",
                "status": "paid",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "paid")

        wire = json.loads(response.content)
        self.assertIn("clientId", wire)
        self.assertNotIn("client_id", wire)

    def test_create_sale_detail_recalculates_total(self):
        sale = Sale.objects.create(
            date=timezone.now(), subtotal=Decimal("1000.00"),
            taxes=Decimal("190.00"), total=Decimal("1190.00"), status="paid",
        )
        response = self.client.post(
            "/api/sale/sale-details/",
            {
                "sale": sale.id,
                "product": self.product.id,
                "quantity": "2.00",
                "unitPrice": "500.00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total"], "1000.00")

        wire = json.loads(response.content)
        self.assertEqual(wire["unitPrice"], "500.00")
        self.assertEqual(wire["productName"], "Pan Venta")

    def test_create_payment(self):
        sale = Sale.objects.create(
            date=timezone.now(), subtotal=Decimal("1000.00"),
            taxes=Decimal("190.00"), total=Decimal("1190.00"), status="paid",
        )
        response = self.client.post(
            "/api/sale/payments/",
            {
                "referenceType": "sale",
                "referenceId": sale.id,
                "method": "cash",
                "amount": "1190.00",
                "date": timezone.now().isoformat(),
                "status": "completed",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wire = json.loads(response.content)
        self.assertIn("referenceType", wire)
        self.assertNotIn("reference_type", wire)

    def test_list_sales(self):
        response = self.client.get("/api/sale/sales/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_sale_details(self):
        response = self.client.get("/api/sale/sale-details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_payments(self):
        response = self.client.get("/api/sale/payments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
