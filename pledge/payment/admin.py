from django.contrib import admin

from payment.models import Customer, FundingSource, Transfer

admin.site.register(Customer)
admin.site.register(FundingSource)
admin.site.register(Transfer)
