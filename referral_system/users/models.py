import random
import string
from django.db import models


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    activated_invite_code = models.BooleanField(default=False)
    inviter = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.phone_number


class Referral(models.Model):
    user = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.phone_number} referred {self.referred_user.phone_number}"
