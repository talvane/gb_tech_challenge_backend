from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="GB Tech - Challenge",
        default_version="v1",
        description="Api - GB Tech - Challenge",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="GBTECH"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("dealer/", include("apps.api.gb_auth.urls", namespace="dealer")),
    path("sale/", include("apps.api.sales.urls", namespace="sale")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui(
        "redoc", cache_timeout=0), name="schema-redoc"
    ),
]
