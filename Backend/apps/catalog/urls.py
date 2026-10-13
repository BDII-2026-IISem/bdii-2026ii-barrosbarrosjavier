from rest_framework.routers import SimpleRouter

from apps.catalog.views import ProductViewSet

router = SimpleRouter(use_regex_path=False)
router.register("products", ProductViewSet, basename="product")

urlpatterns = router.urls
