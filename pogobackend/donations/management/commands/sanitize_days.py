from django.core.management.base import BaseCommand
from donations.models import Donator
from django.db.models import F
from _datetime import datetime,timezone

from django.utils.timezone import now

class Command(BaseCommand):
    help = 'sanitize days of each donator.'

    def handle(self, *args, **kwargs):
        donators = Donator.objects.all()
        for donator in donators:
            days = (datetime.now(timezone.utc) - donator.last_payment)
            donator.days_until_payment = 30-days.days
            donator.save()


