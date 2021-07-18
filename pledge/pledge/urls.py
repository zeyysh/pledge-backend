from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from users import views as uviews

schema_view = get_schema_view(title='Pledge API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

router = routers.DefaultRouter()
router.register('users', uviews.UserViewSet, basename='user-list')
router.register('api/login', uviews.LoginView, basename='login')
urlpatterns = [
    path('', schema_view),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('document/', include('document.urls')),
    path('notification/', include('notification.urls')),
    path('payment/', include('payment.urls')),
    path('pledge_app/', include('pledge_app.urls')),
    path('users_url/', include('users.urls')),
    path('openapi/', get_schema_view()),
]
