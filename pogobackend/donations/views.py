from django.shortcuts import render

# Create your views here.
from donations.models import Donator
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.user.is_superuser:
        social_accounts = SocialAccount.objects.all()
        donation_queryset = Donator.objects.all()
        context = {'user_information': ""}
    else:
        social_accounts = SocialAccount.objects.get(user=request.user)
        if social_accounts.provider == 'discord':
            name = f'{social_accounts.extra_data["username"]}#' \
                   f'{social_accounts.extra_data["discriminator"]}'
        else:
            name = social_accounts.user.username
        try:
            donation_queryset = Donator.objects.get(user=social_accounts)
            balance = donation_queryset.balance
            last_payment = donation_queryset.last_payment
            first_payment = donation_queryset.first_payment
            monthly_paid = donation_queryset.monthly_paid
            days_until_payment = donation_queryset.days_until_payment
        except Donator.DoesNotExist:
            balance = 0
            last_payment = "never"
            first_payment = "never"
            monthly_paid = False
            days_until_payment = "never"

        user_information = {'name':name, 'balance': balance, 'last_payment': last_payment, 'first_payment': first_payment, 'monthly_paid': monthly_paid, 'days_until_payment':days_until_payment}
        context = {'user_information': user_information}
    return render(request, 'home.html', context)

@login_required
def post_login(request):
    return render(request, 'post_login.html')

