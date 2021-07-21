from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=55)
    family = models.CharField(max_length=100)
