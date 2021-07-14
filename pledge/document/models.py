from django.db import models

from pledge.users.models import User

ENVELOPE_STATUS = [
    ('', 'sent'),
    ('', 'delivered'),
    ('', 'completed'),
    ('', 'autoresponded'),
    ('', 'declined'),
]

RECIPIENT_STATUS = [
    ('created', 'created'),
    ('sent', 'sent'),
    ('delivered', 'delivered'),
    ('', 'signed'),
    ('', 'declined'),
    ('', 'completed'),
    ('', 'recipients'),
    ('', 'autoresponded'),
]

RECIPIENT_TYPE = [
    ('agent', 'Agents'),
    ('carbon copies', 'Carbon_Copies'),
    ('certified deliveries', 'Certified_Deliveries'),
    ('editors', 'Editors'),
    ('intermediaries', 'Intermediaries'),
    ('notaries', 'Notaries'),
    ('seals', 'Seals'),
    ('signers', 'Signers'),
    ('witness', 'Witness'),
]


class Document(models.Model):
    name = models.CharField(max_length=55)
    date_created = models.DateTimeField(editable=False)
    file_extension = models.ForeignKey('contenttypes.ContentType', null=True, blank=True, editable=False,
                                       on_delete=models.CASCADE)
    document_id = models.IntegerField(null=True, blank=True, editable=False)
    status = models.CharField(max_length=55)
    envelope = models.ForeignKey('Envelope', on_delete=models.CASCADE)


class Recipient(models.Model):  # recipient
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    routing_order = models.IntegerField()
    status = models.CharField(choices=RECIPIENT_STATUS, max_length=50)
    digital_signature = models.CharField(max_length=255)  # digital signature
    roll_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(editable=False)
    client_user_id = models.IntegerField(null=True, blank=True, editable=False)
    recipient_id = models.IntegerField(null=True, blank=True, editable=False)
    recipient_type = models.CharField(choices=RECIPIENT_TYPE, max_length=50)


class Tab(models.Model):  # tabs
    document = models.ForeignKey("Tab", on_delete=models.CASCADE)
    anchor_string = models.CharField(max_length=255)
    anchor_units = models.CharField(max_length=255)
    anchor_y_offset = models.CharField(max_length=255)
    anchor_x_offset = models.CharField(max_length=255)


class SignResponse(models.Model):
    return_url = models.URLField()


class Template(models.Model):
    documents = models.ForeignKey('Document', on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField(max_length=200)
    status = models.CharField(max_length=50)
    recipients = models.ForeignKey('Recipient', on_delete=models.CASCADE)
    template_id = models.IntegerField()  # A GUID value that identifies a DocuSign template


class Envelope(models.Model):
    envelope_id = models.IntegerField()  # "eead435f-xxxx-xxxx-xxxx-25b7d8523d2b"
    status = models.CharField(choices=ENVELOPE_STATUS, max_length=50)
    emailSubject = models.TextField(max_length=200)
    recipients = models.ForeignKey('Recipient', on_delete=models.CASCADE)
    statusDateTime = models.DateTimeField()  # "2020-08-18T23:36:26.8830000Z"
