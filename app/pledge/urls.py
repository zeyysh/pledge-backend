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
    path('api/', include(router.urls)),
    path("admin/", admin.site.urls),
    path('', schema_view),
    path('openapi/', get_schema_view()),
    path('document/', include('document.urls')),
    path('notification/', include('notification.urls')),
    path('payment/', include('payment.urls')),
    path('pledge_app/', include('pledge_app.urls')),
    path('users/', include('users.urls')),

]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
