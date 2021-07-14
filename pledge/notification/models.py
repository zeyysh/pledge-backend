from django.db import models
from django_jsonfield_backport.models import JSONField  # noqa

from pledge.users.models import User


class Notification(models.Model):
    id = models.IntegerField()
    source = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    source_display_name = models.CharField(max_length=150, null=True)
    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    obj = models.IntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=100)
    channels = JSONField(default=list)
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
