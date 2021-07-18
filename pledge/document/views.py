from rest_framework import generics

from .models import Envelope, Document
from .serializers import EnvelopeSerializer, DocumentSerializer


class EnvelopeList(generics.ListCreateAPIView):

    queryset = Envelope.objects.all()
    serializer_class = EnvelopeSerializer


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class EnvelopeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Envelope.objects.all()
    serializer_class = EnvelopeSerializer


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
