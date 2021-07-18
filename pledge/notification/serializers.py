from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'source', 'source_display_name', 'recipient_user', 'action', 'category', 'obj', 'url', 'short_description',
            'channels', 'is_read', 'create_date', 'update_date')
