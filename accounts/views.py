from django.shortcuts import render
from .serializers import RegisterSerializer, OTPVerifySerializer, EmailOnlySerializer, MyTokenObtainPairSerializer
from django.conf import settings
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from .models import Profile
import random
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all 
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ActiveAccountView(generics.GenericAPIView):
    def get(self,request,uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user and default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Account already activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired activation token.'}, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyOtp(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if profile.otp != otp:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
            if profile.otp_is_expired():
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.save()
            profile.otp = None
            profile.otp_created_at = None
            profile.save()

            return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ResendOTPView(generics.GenericAPIView):
    serializer_class = EmailOnlySerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if user.is_active:
                return Response({"message": "Account already active."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate new OTP
            otp_code = str(random.randint(100000, 999999))
            profile.otp = otp_code
            profile.otp_created_at = timezone.now()
            profile.save()

            subject = "Your new account activation OTP"
            message = f"""
                Hi {user.username},

                Your new OTP code is: {otp_code}

                This code expires in 1 minutes.

                If you did not request this, please ignore.
                """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return Response({"message": "OTP resent successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
