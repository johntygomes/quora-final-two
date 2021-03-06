from django.contrib import admin
from django.urls import path, include
################################################################
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('authentication.urls')),
    path('social-auth/', include('social_auth.urls')),
    ##################################################################
    path('authentication', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('authentication/api/api.json', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('authentication/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# handler404 = 'utils.views.error_404'
# handler500 = 'utils.views.error_500'