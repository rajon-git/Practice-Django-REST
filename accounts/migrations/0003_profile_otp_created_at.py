# Generated by Django 5.2.3 on 2025-06-24 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
