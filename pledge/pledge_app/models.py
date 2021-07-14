from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from pledge.users.models import User, Invite

STATUS_CHOICE = {
    (True, 'accepted'),
    (False, 'not accepted')
}


class Pledge(models.Model):
    name = models.TextField(max_length=100)
    lender = models.ManyToManyField('Lender', on_delete=models.CASCADE)
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE, related_name='borrower_user')
    amount = models.IntegerField()
    status = models.BooleanField(choices=STATUS_CHOICE, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    complete_funded = models.BooleanField(default=False)
    deposit = models.FloatField()
    information = models.URLField()


class Lender(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lender_user')


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lender_user')
    connected_bank_account = models.OneToOneField("bankAccount", on_delete=models.CASCADE)
    family_members = models.ForeignKey(User, on_delete=models.CASCADE)


class bankAccount(models.Model):
    token = models.CharField(max_length=150)


class ProposalResponse(models.Model):
    PROPOSAL_STATUS = [
        'accepted',
        'rejected',
        'countered',
    ]
    lender = models.OneToOneField("Lender", on_delete=models.CASCADE)
    status = models.CharField(choices=PROPOSAL_STATUS)
    amount = models.FloatField()
    additional_information = models.URLField()
    counter = models.OneToOneField('Counter', on_delete=models.CASCADE)
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE)


class Proposal(models.Model):
    pledge = models.ForeignKey('Pledge', on_delete=models.CASCADE)
    borrower = models.OneToOneField("Borrower", on_delete=models.CASCADE, related_name='lender_user')
    lender = models.ForeignKey('Lender', on_delete=models.CASCADE)
    description_link = models.URLField()
    approved = models.BooleanField()
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE)


class Counter(models.Model):
    amount = models.FloatField()
    interest_rate = models.FloatField()
    term = models.TextField(max_length=250)
    monthly_payment = models.FloatField()
    message = models.TextField(max_length=1000)


class Contract(models.Model):
    SIGN_STATUS = [
        'lender_signed',
        'borrower_signed',
        'unsigned',
    ]
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=250)
    sign_status = models.CharField(choices=SIGN_STATUS)
    # lender_sign = models.OneToOneField(Signatory, on_delete=models.CASCADE)


class Payment(models.Model):
    TYPE_PAYMENT = (
         'automatic',
         'off_platform',
    )
    STATUS_PAYMENT = (
        'init',
        'pending',
        'finish',
        'canceled',
        'failed',
    )
    pledge = models.ForeignKey('Pledge', on_delete=models.CASCADE)
    type_payment = models.CharField(choices=TYPE_PAYMENT, default=1)
    status_payment = models.IntegerField(choices=STATUS_PAYMENT, default=1)
    information = models.CharField(max_length=255, default='0')
    amount = models.FloatField()
    monthly_date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=now)
