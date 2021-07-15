from django.contrib import admin

from users.models import User, Invite

admin.site.register(User)
admin.site.register(Invite)
