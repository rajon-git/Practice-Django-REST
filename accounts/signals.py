from .models import Profile
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
import random
from django.utils import timezone


# if token genertae
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

#     if not instance.is_active:
#         uid = urlsafe_base64_encode(force_bytes(instance.pk))
#         token = default_token_generator.make_token(instance)
#         activation_url = f"http://localhost:8000{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"

#         subject = "Activate your account"
#         message = f"""
#                 Hi {instance.username},

#                 Please activate your account by clicking the link below:

#                 {activation_url}

#                 If you did not register, you can ignore this email.
#                 """
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]

#         send_mail(subject, message, from_email, recipient_list)

# if otp send
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        otp = str(random.randint(100000, 999999))
        Profile.objects.create(user=instance, otp=otp, otp_created_at=timezone.now())

        if not instance.is_active:
            subject = "Your account activation OTP"
            message = f"""
                Hi {instance.username},

                Your OTP for account activation is: {otp}

                It expires in 1 minutes.

                If you did not register, please ignore this email.
                """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.email]

            send_mail(subject, message, from_email, recipient_list)
