from django.conf.urls import url
from django.urls import path

from pledge.document.docusign import *

urlpatterns = [
    url(r'^docusign_signature/$', docusign_signature, name='docusign_signature'),
    url(r'^sign_completed/$', sign_completed, name='sign_completed'),
    path('get_envelope_status/<str:envelope_id>', get_envelope_status, name='get_envelope_status'),
]
