from django.core.management.base import BaseCommand
from donations.models import Donator


class Command(BaseCommand):
    help = 'set each donator to precious=false'

    def handle(self, *args, **kwargs):
        Donator.objects.all().update(precious=False)
