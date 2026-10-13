from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.catalog.views import (
    ProductViewSet,
    SupplyViewSet,
    RecipeViewSet,
    RecipeSupplyViewSet,
    PromotionViewSet,
    AvailableProductListAPIView,
)

router = SimpleRouter(use_regex_path=False)
router.register("products", ProductViewSet, basename="product")
router.register("supplies", SupplyViewSet, basename="supply")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("recipe-supplies", RecipeSupplyViewSet, basename="recipe-supply")
router.register("promotions", PromotionViewSet, basename="promotion")

urlpatterns = [
    path(
        "products/available/",
        AvailableProductListAPIView.as_view(),
        name="product-available",
    ),
]
urlpatterns += router.urls
