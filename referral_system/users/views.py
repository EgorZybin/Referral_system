from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Referral
from .serializers import UserSerializer
import random
import string
import time


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class PhoneNumberView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        phone_number = request.data.get('phone_number')
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            # Генерация инвайт-кода
            user.invite_code = generate_invite_code()
            user.save()
            # Имитация задержки
            time.sleep(2)
            return redirect(reverse('users:code_verification', args=[phone_number]))
        if user.activated_invite_code is False:
            return redirect(reverse('users:code_verification', args=[phone_number]))
        else:
            return redirect(reverse('users:user_profile', args=[user.id]))


class CodeVerificationView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, phone_number):
        return render(request, 'users/confirm_code.html', {'phone_number': phone_number})

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        try:
            user = User.objects.get(phone_number=phone_number)
            # Проверка кода подтверждения. Здесь предполагаем, что confirmation_code - это тот код, который нужно ввести
            if user.invite_code == code:
                user.activated_invite_code = True
                user.save()
                # Успешная проверка кода, можно перенаправить на профиль пользователя
                return redirect(reverse('users:user_profile', args=[user.id]))
            else:
                # Код неверный, обработайте ошибку
                return render(request, 'users/confirm_code.html', {
                    'phone_number': phone_number,
                    'error': 'Неверный код. Попробуйте еще раз.'
                })
        except User.DoesNotExist:
            return render(request, 'users/confirm_code.html', {
                'phone_number': phone_number,
                'error': 'Пользователь не найден.'
            })


class UserProfileView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        referrals = Referral.objects.filter(user=user)
        return render(request, 'users/profile.html', {'user': user, 'referrals': referrals}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        invite_code = request.data.get('invite_code')
        user.invite_code = invite_code
        user.save()
        return redirect(reverse('users:user_profile', args=[user.id]))