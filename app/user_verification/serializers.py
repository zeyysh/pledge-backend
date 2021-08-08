from rest_framework import serializers

from user_verification.models import VerificationLevel


class VerificationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationLevel
        fields = "__all__"
