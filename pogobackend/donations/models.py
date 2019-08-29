from django.db import models
from allauth.socialaccount.models import SocialAccount
from datetime import datetime
from django.utils.timezone import now

class Donation(models.Model):
    user = models.ForeignKey(SocialAccount, on_delete=models.CASCADE,blank=True, null=True)
    balance = models.FloatField(default=0.0)
    fee = models.FloatField(default=0.0)
    precious = models.BooleanField(default=False)
    last_payment = models.DateTimeField(default=now)
    monthly_paid = models.BooleanField(default=False)

class AllowedDiscordServer(models.Model):
    server_id = models.CharField(db_index=True, max_length=128)
    name = models.CharField(max_length=128, default=None, blank=True, null=True)
