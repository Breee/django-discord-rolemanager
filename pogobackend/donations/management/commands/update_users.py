from django.core.management.base import BaseCommand
from pogobackend.settings import BOT_TOKEN
from donations.bot import RoleBot
from donations.models import Donation
from allauth.socialaccount.models import SocialAccount
from datetime import datetime,timedelta
from django.db.models import Q

whitelist = ['Bree#2002']

guild_to_roles = {
    409418083632152577 : [616562233475989514]
}

class Command(BaseCommand):
    help = 'update users'

    def handle(self, *args, **kwargs):
        donators = Donation.objects.filter(Q(monthly_paid=True) | Q(precious=True)).values_list('user__user_id',flat=True)
        members = SocialAccount.objects.filter(user__in=donators)
        discord_members = []
        for mem in members:
            if mem.extra_data:
                extra_data = mem.extra_data
                if 'username' in extra_data and 'discriminator' in extra_data:
                    discord_members.append(f"{mem.extra_data['username']}#{mem.extra_data['discriminator']}")
        bot = RoleBot(guild_to_roles=guild_to_roles, members=discord_members)
        bot.run(BOT_TOKEN)