from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from donations.models import Donation
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from pogobackend.settings import BOT_TOKEN
from donations.bot import RoleBot
import asyncio

whitelist = ['Bree#2002']

guild_to_roles = {
    409418083632152577 : [616562233475989514]
}


@login_required
def index(request):
    if request.user.is_superuser:
        social_accounts = SocialAccount.objects.all()
        donation_queryset = Donation.objects.all()
        context = {'user_information': ""}
    else:
        social_accounts = SocialAccount.objects.get(user=request.user)
        donation_queryset = Donation.objects.get(user=social_accounts)
        user_information = {'balance': donation_queryset.balance, 'last_payment': donation_queryset.last_payment}
        context = {'user_information': user_information}
    return render(request, 'html/home.html', context)

def update_users(request):
    bot = RoleBot(guild_to_roles=guild_to_roles, members=whitelist)
    bot.run(token=BOT_TOKEN)
