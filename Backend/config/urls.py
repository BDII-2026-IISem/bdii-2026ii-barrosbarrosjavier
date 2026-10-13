from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/catalog/", include("apps.catalog.urls")),
    path("api/production/", include("apps.production.urls")),
    path("api/sale/", include("apps.sale.urls")),
]
