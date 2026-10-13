from django.contrib import admin

from apps.production.models import ProductionBatch, SupplyMovement


@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ("name", "recipe", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "recipe__name", "description")
    list_editable = ("status",)
    ordering = ("name",)
    autocomplete_fields = ("recipe",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Información", {"fields": ("recipe", "name", "description")}),
        ("Estado", {"fields": ("status",)}),
        (
            "Auditoría",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("recipe")


@admin.register(SupplyMovement)
class SupplyMovementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "production_batch",
        "supply",
        "type",
        "quantity",
        "date",
        "status",
    )
    list_filter = ("type", "status", "date")
    search_fields = ("supply__name", "notes")
    ordering = ("-date",)
    date_hierarchy = "date"
    autocomplete_fields = ("production_batch", "supply")
    fieldsets = (
        ("Movimiento", {"fields": ("production_batch", "supply", "type")}),
        ("Detalle", {"fields": ("quantity", "date", "notes")}),
        ("Estado", {"fields": ("status",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "production_batch", "supply"
        )
