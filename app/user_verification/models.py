from django.db import models


class VerificationLevel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    # user = models.ManyToManyField(get_user_model(), null=True)
    scope = models.ManyToManyField("Scope", null=True)

    def __str__(self):
        return self.name


class Scope(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    endpoint = models.ManyToManyField("Endpoint")


class Endpoint(models.Model):
    url = models.URLField()
