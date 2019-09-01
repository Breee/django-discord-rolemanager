import allauth.account.signals
import requests
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.models import User, Group, AnonymousUser
from donations.models import AllowedDiscordServer, Donation, Donator
from django.contrib.auth import logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone

# method for updating
@receiver(post_save, sender=Donation, dispatch_uid="update_donation")
def update_donation(sender, **kwargs):
    donation = kwargs.get('instance')
    donator = donation.donator
    summed_donations = Donation.objects.filter(donator=donator, completed=True).aggregate(Sum('amount'))['amount__sum']
    balance = (summed_donations if summed_donations is not None else 0) - donator.paid
    Donator.objects.filter(user=donator.user).update(balance=balance, last_payment=timezone.now())

@receiver(post_save, sender=Donator, dispatch_uid="update_donator")
def update_donator(sender, **kwargs):
    donator = kwargs.get('instance')
    summed_donations = Donation.objects.filter(donator=donator, completed=True).aggregate(Sum('amount'))['amount__sum']
    balance = (summed_donations if summed_donations is not None else 0) - donator.paid
    Donator.objects.filter(user=donator.user).update(balance=balance)
