from rest_framework import generics

from user_verification.models import VerificationLevel
from user_verification.serializers import VerificationLevelSerializer


class VerificationLevelList(generics.ListCreateAPIView):
    queryset = VerificationLevel.objects.all()
    serializer_class = VerificationLevelSerializer


class VerificationLevelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VerificationLevel.objects.all()
    serializer_class = VerificationLevelSerializer
