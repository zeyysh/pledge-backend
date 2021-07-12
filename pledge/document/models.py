import datetime
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from pledge.users.models import User, Invite


class Document(models.Model):
    name = models.CharField(max_length=55)
    date_created = models.DateTimeField(editable=False)
    file_extension = models.ForeignKey('contenttypes.ContentType', null=True, blank=True, editable=False, on_delete=models.CASCADE)
    document_id = models.IntegerField(null=True, blank=True, editable=False)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    signer = models.ManyToManyField("Signer", on_delete=models.CASCADE)
    sign_here = models.ForeignKey("SignHere", on_delete=models.CASCADE)


class Signer(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    token = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(editable=False)
    client_user_id = models.IntegerField(null=True, blank=True, editable=False)
    recipient_id = models.IntegerField(null=True, blank=True, editable=False)


class SignHere(models.Model):
    document = models.ForeignKey("SignHere", on_delete=models.CASCADE)
    anchor_string = models.CharField(max_length=255)
    anchor_units = models.CharField(max_length=255)
    anchor_y_offset = models.CharField(max_length=255)
    anchor_x_offset = models.CharField(max_length=255)


class SignResponse(models.Model):
    return_url = models.URLField()
