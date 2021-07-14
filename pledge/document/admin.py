from django.contrib import admin

from document.models import Document, Tab, Template, Envelope, Recipient, SignResponse

admin.site.register(Document)
admin.site.register(Tab)
admin.site.register(Template)
admin.site.register(Envelope)
admin.site.register(Recipient)
admin.site.register(SignResponse)
