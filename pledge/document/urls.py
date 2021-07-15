# from django.conf.urls import url
# from django.urls import include
# from rest_framework import routers
# from rest_framework.schemas import get_schema_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
# from rest_framework_swagger.views import get_swagger_view
# # schema_view = get_swagger_view(title='Project Name')
# schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
#
#
# urlpatterns = [
#     url('', schema_view, name="docs"),
# ]
from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from document import views

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
urlpatterns = [
    # ... previously defined routes
    path('', schema_view),
    path('', views.EnvelopeList.as_view()),
    path('test/', views.DocumentList.as_view()),
    path('<int:pk>/', views.EnvelopeDetail.as_view()),

]
