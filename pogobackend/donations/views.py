from django.shortcuts import render

# Create your views here.
from donations.models import Donation
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.user.is_superuser:
        social_accounts = SocialAccount.objects.all()
        donation_queryset = Donation.objects.all()
        context = {'user_information': ""}
    else:
        social_accounts = SocialAccount.objects.get(user=request.user)
        try:
            donation_queryset = Donation.objects.get(user=social_accounts)
            balance = donation_queryset.balance
            last_payment = balance = donation_queryset.last_payment
        except Donation.DoesNotExist:
            balance = 0
            last_payment = "never"

        user_information = {'balance': balance, 'last_payment': last_payment}
        context = {'user_information': user_information}
    return render(request, 'home.html', context)

def post_login(request):
    return render(request, 'post_login.html')

