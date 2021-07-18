from rest_framework import serializers

from .models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = (
            'self', 'source', 'destination', 'source_funding_source', 'destination_funding_source', 'cancel', 'fees',
            'status', 'amount', 'created')
