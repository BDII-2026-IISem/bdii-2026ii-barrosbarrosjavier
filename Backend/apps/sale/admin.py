from django.contrib import admin

from apps.sale.models import Sale, SaleDetail, Payment


class SaleDetailInline(admin.TabularInline):
    """Muestra las líneas de la venta en la ficha, de solo lectura."""

    model = SaleDetail
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ("product", "quantity", "unit_price", "total", "notes")
    readonly_fields = ("product", "quantity", "unit_price", "total", "notes")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_id",
        "date",
        "subtotal",
        "taxes",
        "total",
        "status",
    )
    list_filter = ("status", "date")
    search_fields = ("client_id",)
    ordering = ("-date",)
    date_hierarchy = "date"
    readonly_fields = (
        "client_id",
        "date",
        "subtotal",
        "taxes",
        "total",
        "status",
    )
    fieldsets = (
        ("Información de la venta", {"fields": ("client_id", "date", "status")}),
        (
            "Totales",
            {"fields": ("subtotal", "taxes", "total"), "classes": ("collapse",)},
        ),
    )
    inlines = (SaleDetailInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ("sale", "product", "quantity", "unit_price", "total")
    list_filter = ("product__status",)
    search_fields = ("sale__id", "product__name", "product__sku")
    ordering = ("-sale__date", "id")
    readonly_fields = ("sale", "product", "quantity", "unit_price", "total", "notes")
    fieldsets = (
        (
            "Línea",
            {"fields": ("sale", "product", "quantity", "unit_price", "total")},
        ),
        ("Notas", {"fields": ("notes",)}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("sale", "product")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reference_type",
        "reference_id",
        "method",
        "amount",
        "date",
        "status",
    )
    list_filter = ("status", "method", "reference_type", "date")
    search_fields = ("reference_type", "method")
    ordering = ("-date",)
    date_hierarchy = "date"
    fieldsets = (
        (
            "Referencia",
            {"fields": ("reference_type", "reference_id", "method")},
        ),
        ("Monto", {"fields": ("amount", "date")}),
        ("Estado", {"fields": ("status",)}),
    )
