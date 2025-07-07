from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone

class CustomUserCreate(BaseUserManager):
    def create_user(self,email, password =None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        
        email = self.normalize_email(email)

        if not extra_fields.get('username'):
            extra_fields['username'] =  email.split('@')[0]

        extra_fields.setdefault('is_active', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_active', False)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('username'):
            extra_fields['username'] =  email.split('@')[0]
        
        return self.create_user(email,password, **extra_fields)
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserCreate()

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    phone = models.CharField(max_length=11, blank= True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # if send otp
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def otp_is_expired(self):
        if self.otp_created_at:
            expiry_time = self.otp_created_at + timezone.timedelta(minutes=1)
            return timezone.now() > expiry_time
        return True 


    def __str__(self):
        return f"Profile of {self.user.email}"

