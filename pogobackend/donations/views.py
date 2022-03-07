from django.shortcuts import render

# Create your views here.
from donations.models import Donator, Donation, Transaction
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from .forms import DonateForm, SettingsForm
from django.http import HttpResponseRedirect
from pogobackend.celery import subtract_fee
from django.utils import timezone

@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    settings_form = SettingsForm()
    if request.method == 'POST':
        pass
    else:
        if request.user.is_superuser:
            social_accounts = SocialAccount.objects.all()
            donator_queryset = Donator.objects.all()
            user_information_list = []
            total = {"users": 0, "balance": 0, "transactions": 0, "devices": 0}
            for donator in donator_queryset:
                name = f'{donator.user.extra_data["username"]}#' \
                       f'{donator.user.extra_data["discriminator"]}'
                balance = donator.balance
                paid = donator.paid
                accepted = Donation.objects.filter(donator=donator, completed=True).aggregate(Sum('amount'))[
                    'amount__sum']
                pending = Donation.objects.filter(donator=donator, completed=False).aggregate(Sum('amount'))[
                    'amount__sum']
                last_payment = donator.last_payment
                first_payment = donator.first_payment
                monthly_paid = donator.monthly_paid
                days_until_payment = donator.days_until_payment
                autopay = donator.autopay
                precious = donator.precious
                user_information = {'name': name,
                                    'balance': balance, 'paid': paid,
                                'accepted':      accepted if accepted is not None else 0,
                                'pending':       pending if pending is not None else 0,
                                'last_payment':  last_payment, 'first_payment': first_payment,
                                'monthly_paid':  monthly_paid, 'days_until_payment': days_until_payment,
                                'settings_form': settings_form,
                                'autopay':       autopay,
                                'precious':      precious
                                }
                user_information_list.append(user_information)
                total["balance"] += balance
                if monthly_paid:
                    transactions = Transaction.objects.filter(donator=donator, date__range=[last_payment, timezone.now()])
                    transactions = transactions.aggregate(Sum('amount'))['amount__sum']
                    total["users"] += 1
                    total["transactions"] += transactions  if transactions is not None else 0
                total["devices"] = total["transactions"] / 12.0
            
            context = {'user_information': user_information_list, 'total': total}
        return render(request, 'home.html', context)

@login_required
def me(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print(request.POST)
        form = SettingsForm(request.POST or None)
        if form.is_valid():
            social_accounts = SocialAccount.objects.get(user=request.user)
            donator = Donator.objects.get(user=social_accounts)
            donator.autopay = True if ("autopay" in request.POST and request.POST["autopay"]) else False
            donator.fee = request.POST["fee"] if ("fee" in request.POST and request.POST["fee"]) else 4.0
            donator.save()
            subtract_fee.delay(social_accounts.user_id)
        return HttpResponseRedirect('/me')
    else:
        social_accounts = SocialAccount.objects.get(user=request.user)
        if social_accounts.provider == 'discord':
            name = f'{social_accounts.extra_data["username"]}#' \
                   f'{social_accounts.extra_data["discriminator"]}'
        else:
            name = social_accounts.user.username
        try:
            donator = Donator.objects.get(user=social_accounts)
            balance = donator.balance
            paid = donator.paid
            accepted = Donation.objects.filter(donator=donator, completed=True).aggregate(Sum('amount'))[
                'amount__sum']
            pending = Donation.objects.filter(donator=donator, completed=False).aggregate(Sum('amount'))[
                'amount__sum']
            last_payment = donator.last_payment
            first_payment = donator.first_payment
            monthly_paid = donator.monthly_paid
            fee = donator.fee
            days_until_payment = donator.days_until_payment
            autopay = donator.autopay
            precious = donator.precious
        except Donator.DoesNotExist:
            balance = 0.0
            pending = 0.0
            paid = 0.0
            fee = 4.0
            accepted = 0.0
            last_payment = "never"
            first_payment = "never"
            monthly_paid = False
            days_until_payment = "never"
            autopay = False
            precious = False
        settings_form = SettingsForm(initial={"autopay": autopay, "fee": fee})
        user_information = {'name':               name, 'balance': balance, 'paid': paid,
                            'accepted':           accepted if accepted is not None else 0,
                            'pending':            pending if pending is not None else 0,
                            'last_payment':       last_payment, 'first_payment': first_payment,
                            'monthly_paid':       monthly_paid, 'days_until_payment': days_until_payment,
                            'settings_form':      settings_form,
                            'autopay': autopay,
                            'precious': precious,
                            'fee': fee,
                            }
        context = {'user_information': user_information}
    return render(request, 'me.html', context)

@login_required
def post_login(request):
    return render(request, 'post_login.html')

@login_required
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
            donation = Donation(donator=donator, amount=form.cleaned_data['amount'], note=form.cleaned_data['note'], completed=False)
            donation.save()
        return HttpResponseRedirect('/me')

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


@login_required
def pay(request):
    if request.method == 'POST':
        social_account = SocialAccount.objects.get(user=request.user)
        subtract_fee.delay(social_account.user_id, authorized=True)
        return HttpResponseRedirect('/me')
