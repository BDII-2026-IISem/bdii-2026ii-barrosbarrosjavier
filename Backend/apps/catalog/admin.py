from django.contrib import admin

from apps.catalog.models import (
    Product,
    Supply,
    Recipe,
    RecipeSupply,
    Promotion,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "status")
    list_filter = ("status",)
    search_fields = ("sku", "name", "description")
    list_editable = ("price", "status")
    ordering = ("name",)
    fieldsets = (
        ("Información", {"fields": ("sku", "name", "description")}),
        ("Precio", {"fields": ("price",)}),
        ("Estado", {"fields": ("status",)}),
    )


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "unit_of_measure", "min_stock", "status")
    list_filter = ("status", "unit_of_measure")
    search_fields = ("code", "name")
    list_editable = ("min_stock", "status")
    ordering = ("name",)
    fieldsets = (
        ("Información", {"fields": ("code", "name", "unit_of_measure")}),
        ("Stock", {"fields": ("min_stock",)}),
        ("Estado", {"fields": ("status",)}),
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "product__name", "description")
    list_editable = ("status",)
    ordering = ("name",)
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Información", {"fields": ("product", "name", "description")}),
        ("Estado", {"fields": ("status",)}),
        (
            "Auditoría",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")


@admin.register(RecipeSupply)
class RecipeSupplyAdmin(admin.ModelAdmin):
    list_display = ("main", "related", "relation_data", "status")
    list_filter = ("status",)
    search_fields = ("main__name", "related__name")
    list_editable = ("status",)
    ordering = ("main_id", "related_id")
    autocomplete_fields = ("main", "related")
    fieldsets = (
        ("Relación", {"fields": ("main", "related", "relation_data")}),
        ("Estado", {"fields": ("status",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("main", "related")


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "description")
    list_editable = ("status",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Información", {"fields": ("name", "description")}),
        ("Estado", {"fields": ("status",)}),
        (
            "Auditoría",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
