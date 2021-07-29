from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from users.views import empty_view, FacebookLogin

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
# schema_view = get_schema_view(title='API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('rest_auth.urls')),
    path('api/register/', include('rest_auth.registration.urls'), name="register"),
    path('api/register/verify-email/', empty_view, name='account_email_verification_sent'),
    path('password-reset/<uidb64>/<token>/', empty_view, name='password_reset_confirm'),
    url('api/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    path('users/', include('users.urls')),
    path("admin/", admin.site.urls),
    path('document/', include('document.urls')),
    path('notification/', include('notification.urls')),
    path('payment/', include('payment.urls')),
    path('pledge_app/', include('pledge_app.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
