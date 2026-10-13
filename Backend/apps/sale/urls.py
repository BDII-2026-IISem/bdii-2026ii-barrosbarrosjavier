from rest_framework.routers import SimpleRouter

from apps.sale.views import SaleViewSet, SaleDetailViewSet, PaymentViewSet

router = SimpleRouter(use_regex_path=False)
router.register("sales", SaleViewSet, basename="sale")
router.register("sale-details", SaleDetailViewSet, basename="sale-detail")
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls
