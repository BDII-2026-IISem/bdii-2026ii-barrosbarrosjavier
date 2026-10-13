from rest_framework.routers import SimpleRouter

from apps.production.views import (
    ProductionBatchViewSet,
    SupplyMovementViewSet,
)

router = SimpleRouter(use_regex_path=False)
router.register("production-batches", ProductionBatchViewSet, basename="production-batch")
router.register("supply-movements", SupplyMovementViewSet, basename="supply-movement")

urlpatterns = router.urls
