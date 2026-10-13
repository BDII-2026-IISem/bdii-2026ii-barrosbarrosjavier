from rest_framework.routers import SimpleRouter

from apps.catalog.views import (
    ProductViewSet,
    SupplyViewSet,
    RecipeViewSet,
    RecipeSupplyViewSet,
    PromotionViewSet,
)

router = SimpleRouter(use_regex_path=False)
router.register("products", ProductViewSet, basename="product")
router.register("supplies", SupplyViewSet, basename="supply")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("recipe-supplies", RecipeSupplyViewSet, basename="recipe-supply")
router.register("promotions", PromotionViewSet, basename="promotion")

urlpatterns = router.urls
