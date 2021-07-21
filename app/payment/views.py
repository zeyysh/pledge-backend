from rest_framework import generics

from .models import Transfer
from .serializers import TransferSerializer


class TransferList(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class TransferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
