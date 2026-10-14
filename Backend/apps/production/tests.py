import json
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Product, Supply, Recipe
from apps.common.testing import create_active_user, grant_crud
from apps.production.models import ProductionBatch, SupplyMovement


class ProductionApiTests(APITestCase):
    def setUp(self):
        # Usuario con concesión completa en producción
        self.user = create_active_user(
            username="prod-user",
            email="prod@hornoraiz.test",
        )
        grant_crud(
            self.user,
            "/api/production/production-batches/",
            "/api/production/production-batches/1/",
        )
        grant_crud(
            self.user,
            "/api/production/supply-movements/",
            "/api/production/supply-movements/1/",
        )
        self.client.force_authenticate(user=self.user)

        # Datos base
        product = Product.objects.create(
            sku="PROD-ISS09-001", name="Pan ISS09", price=Decimal("1000.00")
        )
        self.supply = Supply.objects.create(
            code="SUP-ISS09-001", name="Harina ISS09",
            unit_of_measure="kg", min_stock=Decimal("5.00"),
        )
        self.recipe = Recipe.objects.create(product=product, name="Receta ISS09")

    def test_create_production_batch(self):
        response = self.client.post(
            "/api/production/production-batches/",
            {"recipe": self.recipe.id, "name": "Lote ISS09"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], True)

        wire = json.loads(response.content)
        self.assertEqual(wire["recipeName"], "Receta ISS09")
        self.assertIn("createdAt", wire)
        self.assertNotIn("created_at", wire)

    def test_create_supply_movement_with_batch(self):
        batch = ProductionBatch.objects.create(recipe=self.recipe, name="Lote Test")
        response = self.client.post(
            "/api/production/supply-movements/",
            {
                "productionBatch": batch.id,
                "supply": self.supply.id,
                "type": "IN",
                "date": timezone.now().isoformat(),
                "quantity": "10.00",
                "status": "completed",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wire = json.loads(response.content)
        self.assertEqual(wire["supplyName"], "Harina ISS09")
        self.assertEqual(wire["productionBatchName"], "Lote Test")

    def test_list_production_batches(self):
        response = self.client.get("/api/production/production-batches/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_supply_movements(self):
        response = self.client.get("/api/production/supply-movements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
