from django.core.management.base import BaseCommand
from donations.models import Donator,Transaction
from django.utils import timezone

class Command(BaseCommand):
    help = 'subtract fee from each donator.'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('-f', '--force', default=False, action='store_true')
        parser.add_argument('-p', '--pay', default=False, action='store_true')
        parser.add_argument('-d', '--days', default=False, action='store_true')
        parser.add_argument('-m', '--month', default=False, action='store_true')
        parser.add_argument('-a', '--authorized', default=False, action='store_true')
        parser.add_argument('--user')


    def handle(self, *args, **kwargs):
        if kwargs.get('user'):
            donator_queryset = Donator.objects.filter(user__user_id=kwargs.get('user'))
        else:
            donator_queryset = Donator.objects.all()
        for donator in donator_queryset:
            if (donator.balance >= donator.fee and donator.days_until_payment <= 0 and not donator.monthly_paid and (donator.autopay or kwargs.get('authorized'))) or kwargs.get('force'):
                if kwargs.get('pay'):
                    donator.paid = donator.paid + donator.fee
                if kwargs.get('days'):
                    donator.days_until_payment = 30
                if kwargs.get('month'):
                    donator.monthly_paid = True
                donator.last_payment = timezone.now()
                donator.save()
                new_transaction, created = Transaction.objects.create(donator=donator, amount=donator.fee, date=timezone.now())
                new_transaction.save()
                
