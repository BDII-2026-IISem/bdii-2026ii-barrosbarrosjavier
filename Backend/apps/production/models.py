from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from apps.catalog.models import Recipe, Supply
from apps.common.models import TimeStampedModel


class ProductionBatch(TimeStampedModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name="production_batches",
        db_column="recipe_id",
    )
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "production_batches"
        verbose_name = "lote de producción"
        verbose_name_plural = "lotes de producción"
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class SupplyMovement(models.Model):
    production_batch = models.ForeignKey(
        ProductionBatch,
        on_delete=models.PROTECT,
        related_name="supply_movements",
        db_column="production_batch_id",
        null=True,
        blank=True,
    )
    supply = models.ForeignKey(
        Supply,
        on_delete=models.PROTECT,
        related_name="supply_movements",
        db_column="supply_id",
    )
    type = models.CharField(max_length=50)
    date = models.DateTimeField()
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "supply_movements"
        verbose_name = "movimiento de insumo"
        verbose_name_plural = "movimientos de insumos"
        ordering = ["-date", "id"]

    def __str__(self):
        return f"{self.type} - {self.supply} ({self.quantity})"
