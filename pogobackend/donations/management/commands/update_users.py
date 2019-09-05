from django.core.management.base import BaseCommand
from pogobackend.settings import BOT_TOKEN
from donations.bot import RoleBot
from donations.models import Donator, GuildToRoleRelation
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q
import asyncio

class Command(BaseCommand):
    help = 'update users'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('user_ids', nargs='+')

    def handle(self, *args, **kwargs):
        user_ids = kwargs.get('user_ids').split(' ')
        user_ids_int = [int(x) for x in user_ids]
        # get donators and partition into donators and no donators.
        give_roles = Donator.objects.filter((Q(monthly_paid=True) | Q(precious=True)) & Q(user__uid__in=user_ids)).values_list('user__uid',flat=True)
        # discord uid must be int since rewrite.
        give_roles = [int(x) for x in give_roles]
        take_roles = [int(x) for x in user_ids_int if x not in give_roles]
        # get guild_to_role mapping
        guild_to_roles = dict()
        donator_roles = GuildToRoleRelation.objects.all()
        for obj in donator_roles:
            if obj.guild.guild_id not in guild_to_roles:
                guild_to_roles[obj.guild.guild_id] = [obj.role.role_id]
            else:
                guild_to_roles[obj.guild.guild_id].append(obj.role.role_id)
        discord_members = {
            'give_roles': give_roles if give_roles else [],
            'take_roles': take_roles if take_roles else []
        }
        loop = asyncio.new_event_loop()
        bot = RoleBot(guild_to_roles=guild_to_roles, members=discord_members, loop=loop)
        bot.run(BOT_TOKEN)
