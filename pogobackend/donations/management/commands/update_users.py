from django.core.management.base import BaseCommand
from pogobackend.settings import BOT_TOKEN
from donations.bot import RoleBot
from donations.models import Donator, GuildToRoleRelation
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q

class Command(BaseCommand):
    help = 'update users'

    def handle(self, *args, **kwargs):
        # get donators
        donators = Donator.objects.filter(Q(monthly_paid=True) | Q(precious=True)).values_list('user__user_id',flat=True)
        members = SocialAccount.objects.filter(user__in=donators)
        # get guild_to_role mapping
        guild_to_roles = dict()
        donator_roles = GuildToRoleRelation.objects.all()
        for obj in donator_roles:
            if obj.guild.guild_id not in guild_to_roles:
                guild_to_roles[obj.guild.guild_id] = [obj.role.role_id]
            else:
                guild_to_roles[obj.guild.guild_id].append(obj.role.role_id)
        discord_members = []
        for mem in members:
            discord_members.append(int(mem.uid))
        bot = RoleBot(guild_to_roles=guild_to_roles, members=discord_members)
        bot.run(BOT_TOKEN)