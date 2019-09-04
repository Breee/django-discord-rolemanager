from django.core.management.base import BaseCommand
from donations.models import Donator
from django.utils import timezone


class Command(BaseCommand):
    help = 'subtract fee from each donator.'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('-f', '--force', default=False, action='store_true')
        parser.add_argument('-p', '--pay', default=False, action='store_true')
        parser.add_argument('-d', '--days', default=False, action='store_true')
        parser.add_argument('-m', '--month', default=False, action='store_true')
        parser.add_argument('--user')


    def handle(self, *args, **kwargs):
        if kwargs.get('user'):
            donator_queryset = Donator.objects.filter(user__user_id=kwargs.get('user'))
        else:
            donator_queryset = Donator.objects.all()
        for donator in donator_queryset:
            if (donator.balance >= donator.fee and donator.days_until_payment <= 0 and not donator.monthly_paid) or kwargs.get('force'):
                if kwargs.get('pay'):
                    donator.paid = donator.paid + donator.fee
                if kwargs.get('days'):
                    donator.days_until_payment = 30
                if kwargs.get('month'):
                    donator.monthly_paid = True
                donator.last_payment = timezone.now()
                donator.save()
