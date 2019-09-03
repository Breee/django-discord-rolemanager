from django.core.management.base import BaseCommand
from pogobackend.settings import BOT_TOKEN
from donations.bot import RoleBot
from donations.models import Donator, GuildToRoleRelation
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q

class Command(BaseCommand):
    help = 'Check users'

    def handle(self, *args, **kwargs):
        pass
