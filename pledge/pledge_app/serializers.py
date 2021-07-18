from rest_framework import serializers

from .models import Pledge


class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = (
            'name', 'lender', 'borrower', 'amount', 'status', 'created_date', 'complete_funded',
            'deposit', 'information')
