from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from document import views

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
urlpatterns = [
    path('', schema_view),
    path('envelope/', views.EnvelopeList.as_view()),
    path('document/', views.DocumentList.as_view()),
    path('envelope/<int:pk>/', views.EnvelopeDetail.as_view()),
    path('document/<int:pk>/', views.DocumentDetail.as_view()),
]
