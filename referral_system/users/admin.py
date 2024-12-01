from django.contrib import admin


# Register your models here.

from .models import User, Referral

admin.site.register(User)
admin.site.register(Referral)

