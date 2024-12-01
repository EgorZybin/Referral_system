from rest_framework import serializers
from .models import User, Referral


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_invite_code']


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['user', 'referred_user']
