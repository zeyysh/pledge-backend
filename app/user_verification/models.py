from django.contrib.auth import get_user_model
from django.db import models


class Verification(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ManyToManyField(get_user_model(), null=True)
