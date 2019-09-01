from django.shortcuts import render

# Create your views here.
from donations.models import Donator, Donation
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


from .forms import DonateForm
from django.http import HttpResponseRedirect

def donate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DonateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            social_account = SocialAccount.objects.get(user=request.user)
            donator, created = Donator.objects.update_or_create(user=social_account)
            donator.save()
            donation = Donation(donator=donator, amount=form.cleaned_data['amount'], note=form.cleaned_data['note'])
            donation.save()
            return HttpResponseRedirect('/donate/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.user.is_superuser:
            form = DonateForm()
            donations = Donation.objects.all()
        else:
            form = DonateForm()
            social_account = SocialAccount.objects.get(user=request.user)
            donations = Donation.objects.filter(donator__user=social_account)

    return render(request, 'donation.html', {'form': form, 'donations': donations})