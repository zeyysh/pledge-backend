from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from users import views as uviews

schema_view = get_schema_view(title='API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

router = routers.DefaultRouter()
router.register('users', uviews.UserViewSet, basename='user-list')
router.register('login', uviews.LoginView, basename='login')
urlpatterns = [
    # path("", image_upload, name="upload"),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users/', include('users.urls')),
    path('', schema_view),
    path("admin/", admin.site.urls),
    path('document/', include('document.urls')),
    path('notification/', include('notification.urls')),
    path('payment/', include('payment.urls')),
    path('pledge_app/', include('pledge_app.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
