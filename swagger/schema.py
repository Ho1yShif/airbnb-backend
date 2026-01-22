"""
Swagger/OpenAPI Schema Configuration
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="AirBnB Clone API",
        default_version='v1',
        description="API documentation for AirBnB Clone project",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@airbnb-clone.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
