from django.db import models

from users.models import User

CUSTOMER_TYPE = [
    ('', 'unverified'),
    ('', 'personal'),
    ('', 'business'),
    ('', 'receive-only'),
]

CUSTOMER_STATUS = [
    ('', 'unverified'),
    ('', 'retry'),
    ('', 'document'),
    ('', 'verified'),
    ('', 'suspended'),
    ('', 'deactivated'),
]


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    type = models.CharField(choices=CUSTOMER_TYPE, max_length=50)
    status = models.CharField(choices=CUSTOMER_STATUS, max_length=50)
    created = models.BooleanField()


class FundingSource(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    bankAccountType = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    created = models.DateTimeField()
    balance = models.CharField(max_length=100)
    removed = models.BooleanField()
    channels = models.CharField(max_length=100)
    bankName = models.CharField(max_length=100)
    iavAccountHolders = models.CharField(max_length=100)
    fingerprint = models.CharField(max_length=100)


class Transfer(models.Model):
    self = models.URLField()
    source = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='source')
    destination = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='destination_funding')
    source_funding_source = models.OneToOneField('FundingSource', on_delete=models.CASCADE,
                                                 related_name='source_funding')
    destination_funding_source = models.OneToOneField('FundingSource', on_delete=models.CASCADE)
    cancel = models.BooleanField()
    fees = models.FloatField()
    status = models.CharField(max_length=50)
    amount = models.FloatField()
    created = models.DateTimeField(auto_now=True)
