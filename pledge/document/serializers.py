# api/serializers.py
from rest_framework import serializers

from .models import Envelope, Document


class EnvelopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envelope
        fields = ('envelope_id', 'status', 'emailSubject', 'recipients', 'statusDateTime')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'date_created', 'file_extension', 'document_id', 'status')
