from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from MapApi import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(signals.user_login, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# Create your models here.
