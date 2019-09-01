from django.core.management.base import BaseCommand
from donations.models import Donator
from django.utils import timezone


class Command(BaseCommand):
    help = 'subtract fee from each donator.'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('-f', '--force', default=False, action='store_true')


    def handle(self, *args, **kwargs):
        donator_queryset = Donator.objects.all()
        for donator in donator_queryset:
            print(donator.balance >= donator.fee)
            print(donator.days_until_payment <= 0)
            print(donator.monthly_paid)
            if (donator.balance >= donator.fee and donator.days_until_payment <= 0 and not donator.monthly_paid) or kwargs.get('force'):
                donator.paid = donator.paid + donator.fee
                donator.days_until_payment = 30
                donator.monthly_paid = True
                donator.last_payment = timezone.now()
                donator.save()
