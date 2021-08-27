from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SaleViewSet

app_name = "sales"

router = DefaultRouter()
router.register("", SaleViewSet, basename="sale")

urlpatterns = [
    path("", include(router.urls)),
]
