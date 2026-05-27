from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MYJOBS API",
        default_version="v1",
        description="Company Review & Compensation Platform API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            email="support@myjobs.com"
        ),
        license=openapi.License(
            name="MIT License"
        ),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Swagger UI
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # Redoc
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # JSON/YAML schema
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),

    path("accounts/", include("accounts.urls")),
    path("analytics/", include("analytics.urls")),
    path("companies/", include("companies.urls")),
    path("compensation/", include("compensation.urls")),
    path("myprofile/", include("myprofile.urls")),
    path("reviews/", include("reviews.urls")),
]