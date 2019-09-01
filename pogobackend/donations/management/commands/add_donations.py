from django.core.management.base import BaseCommand
from pogobackend.settings import BOT_TOKEN
from donations.bot import RoleBot
from donations.models import Donator, Donation
from allauth.socialaccount.models import SocialAccount

class Command(BaseCommand):
    help = 'fetch users from discord, create a mapping user -> id, create mapping id -> amount, then add donators.'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('file')

    def handle(self, *args, **kwargs):
        username_to_id = dict()
        id_to_amount = dict()
        bot = RoleBot(guild_to_roles=None, members=None, username_to_id=username_to_id)
        bot.run(BOT_TOKEN)
        with open(kwargs['file'], 'r') as file:
            next(file)
            for line in file:
                user, amount = line.replace('\n','').replace(' ','').encode('ascii', 'ignore').decode("utf-8").lower().split('\t')
                id = username_to_id[user]
                if id not in id_to_amount:
                    id_to_amount[id] = float(amount)
                else:
                    id_to_amount[id] += float(amount)
        for id,amount in id_to_amount.items():
            user = SocialAccount.objects.all().filter(uid=str(id)).first()
            if user:
                donator, created = Donator.objects.update_or_create(user=user)
                donator.save()
                donation = Donation.objects.update_or_create(donator=donator, amount=amount, note="initial donation", completed=True)
                donation.save()
