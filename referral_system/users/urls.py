from django.urls import path

from .views import (
    PhoneNumberView,
    CodeVerificationView,
    UserProfileView
)

app_name = 'users'

urlpatterns = [
    path('auth/phone/', PhoneNumberView.as_view(), name='phone_auth'),
    path('auth/code/<str:phone_number>/', CodeVerificationView.as_view(), name='code_verification'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]
