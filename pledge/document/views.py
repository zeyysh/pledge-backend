# api/views.py
from rest_framework import generics

from .models import Envelope, Document
from .serializers import EnvelopeSerializer, DocumentSerializer


class EnvelopeList(generics.ListCreateAPIView):
    """
    post:
        Return a user instance.

    get:
        Return all users, ordered by most recently joined.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    queryset = Envelope.objects.all()
    serializer_class = EnvelopeSerializer


class DocumentList(generics.ListCreateAPIView):
    """
    post:
        Return a user instance.

    get:
        Return all users, ordered by most recently joined.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class EnvelopeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Return a user instance.

    post:
        Return all users, ordered by most recently joined.

    delete:
        Remove an existing user.

    put:
        Update one or more fields on an existing user.

    patch:
        Update a user.
    """
    queryset = Envelope.objects.all()
    serializer_class = EnvelopeSerializer
