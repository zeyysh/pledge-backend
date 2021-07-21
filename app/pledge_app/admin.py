from django.contrib import admin

from pledge_app.models import Lender, Pledge, Counter, Contract, Proposal, ProposalResponse, Payment, Borrower, \
    bankAccount

admin.site.register(Pledge)
admin.site.register(Lender)
admin.site.register(Borrower)
admin.site.register(Proposal)
admin.site.register(ProposalResponse)
admin.site.register(Counter)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(bankAccount)
