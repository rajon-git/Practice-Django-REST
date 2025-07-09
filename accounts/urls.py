from django.urls import path 
from .views import RegisterView, ActiveAccountView, VerifyOtp, ResendOTPView, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/",RegisterView.as_view(), name='register'),
    path("login/", MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<uidb64>/<token>/', ActiveAccountView.as_view(), name='activate'),
    path('verify-otp/', VerifyOtp.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
] 


