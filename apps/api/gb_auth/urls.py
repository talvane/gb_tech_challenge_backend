from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = "gb_auth"

router = DefaultRouter()
router.register("", UserViewSet, basename="dealer")

urlpatterns = [
    path("", include(router.urls)),
]
