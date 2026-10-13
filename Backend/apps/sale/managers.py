from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.catalog.models import Product


class SaleQuerySet(models.QuerySet):
    def register(self, *, client_id, sale_date, items, taxes):
        """Registra una venta con sus líneas dentro de una sola transacción.

        - Crea la cabecera Sale.
        - Crea las líneas SaleDetail con el precio histórico.
        - Recalcula subtotal, taxes y total.
        - Si cualquier paso falla, no queda ningún registro.
        """
        if not items:
            raise ValidationError({"items": ["La venta requiere al menos un producto."]})

        taxes = Decimal(taxes).quantize(Decimal("0.01"))
        if taxes < 0:
            raise ValidationError({"taxes": ["Los impuestos no pueden ser negativos."]})

        quantities = {}
        for item in items:
            quantity = int(item["quantity"])
            if quantity < 1:
                raise ValidationError({"items": ["La cantidad debe ser al menos 1."]})
            product_id = item["product_id"]
            quantities[product_id] = quantities.get(product_id, 0) + quantity

        with transaction.atomic():
            locked_products = {
                product.id: product
                for product in Product.objects.select_for_update()
                .filter(pk__in=quantities)
                .order_by("id")
            }
            if len(locked_products) != len(quantities):
                raise ValidationError({"items": ["Hay productos que no existen."]})

            for product_id in quantities:
                product = locked_products[product_id]
                if not product.status:
                    raise ValidationError(
                        {"items": [f"El producto {product.name} no está activo."]}
                    )

            sale = self.model(
                client_id=client_id,
                date=sale_date,
                subtotal=Decimal("0.00"),
                taxes=taxes,
                total=Decimal("0.00"),
                status="paid",
            )
            sale.save()

            subtotal = Decimal("0.00")
            for item in items:
                product = locked_products[item["product_id"]]
                unit_price = product.price
                quantity = int(item["quantity"])
                line_total = (unit_price * quantity).quantize(Decimal("0.01"))
                sale.details.create(
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total=line_total,
                )
                subtotal += line_total

            subtotal = subtotal.quantize(Decimal("0.01"))
            total = (subtotal + taxes).quantize(Decimal("0.01"))
            sale.subtotal = subtotal
            sale.total = total
            sale.save(update_fields=["subtotal", "taxes", "total"])

            return sale


class SaleManager(models.Manager.from_queryset(SaleQuerySet)):
    pass
