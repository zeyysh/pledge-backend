from django.shortcuts import render
from rest_framework import generics

from .models import Pledge
from .serializers import PledgeSerializer


class PledgeList(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


class PledgeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


def swagger_view(request):
    return render(request, 'dist/index.html')
