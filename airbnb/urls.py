from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from airbnb.health_checks import (
    health_check, liveness_probe, readiness_probe, metrics
)
from listings.auth_views import (
    CustomTokenObtainPairView, register_user, request_password_reset,
    confirm_password_reset, user_profile
)

schema_view = get_schema_view(
    openapi.Info(
        title="Airbnb Backend API",
        default_version="v1",
        description="API documentation for Airbnb Clone project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', register_user, name='register'),
    path('api/password-reset/', request_password_reset, name='password-reset'),
    path('api/password-reset-confirm/', confirm_password_reset, name='password-reset-confirm'),
    path('api/profile/', user_profile, name='profile'),
    # Main API
    path('api/', include('listings.urls')),
    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Health checks
    path('health/', health_check, name='health-check'),
    path('health/live/', liveness_probe, name='liveness-probe'),
    path('health/ready/', readiness_probe, name='readiness-probe'),
    path('metrics/', metrics, name='prometheus-metrics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
