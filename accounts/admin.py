from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import CustomUser, Profile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_superuser']
    ordering = ['email']
    search_fields = ['email', 'username']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
