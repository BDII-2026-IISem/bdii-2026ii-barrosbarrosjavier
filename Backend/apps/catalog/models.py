from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "products"
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Supply(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    unit_of_measure = models.CharField(max_length=30)
    min_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "supplies"
        verbose_name = "insumo"
        verbose_name_plural = "insumos"
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Recipe(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="recipes",
        db_column="product_id",
    )
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "recipes"
        verbose_name = "receta"
        verbose_name_plural = "recetas"
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class RecipeSupply(models.Model):
    main = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name="recipe_supplies",
        db_column="main_id",
    )
    related = models.ForeignKey(
        Supply,
        on_delete=models.PROTECT,
        related_name="recipe_supplies",
        db_column="related_id",
    )
    relation_data = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "recipe_supplies"
        verbose_name = "insumo de receta"
        verbose_name_plural = "insumos de receta"
        ordering = ["main_id", "related_id", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["main", "related"],
                name="recipe_supplies_unique",
            ),
        ]

    def __str__(self):
        return f"{self.main} - {self.related}"


class Promotion(TimeStampedModel):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "promotions"
        verbose_name = "promoción"
        verbose_name_plural = "promociones"
        ordering = ["name", "id"]

    def __str__(self):
        return self.name
