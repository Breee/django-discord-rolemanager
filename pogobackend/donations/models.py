from django.db import models
from allauth.socialaccount.models import SocialAccount
from django.utils.timezone import now

class Donator(models.Model):
    user = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, unique=True)
    balance = models.FloatField(default=0.0)
    paid = models.IntegerField(default=0.0)
    fee = models.FloatField(default=2.0)
    precious = models.BooleanField(default=False)
    last_payment = models.DateTimeField(default=now)
    first_payment = models.DateTimeField(default=now)
    monthly_paid = models.BooleanField(default=False)
    days_until_payment = models.IntegerField(default=0)
    autopay = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.extra_data['username']}#{self.user.extra_data['discriminator']} - {self.balance}"

class Donation(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    note = models.CharField(max_length=128, default="")
    date = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.donator.user.extra_data['username']}#{self.donator.user.extra_data['discriminator']} [amount: {self.amount}] [completed: {self.completed}]"

class RawDonation(models.Model):
    username = models.CharField(max_length=128)
    uid = models.CharField(max_length=128)
    amount = models.FloatField(default=0.0)

class DiscordGuild(models.Model):
    guild_id = models.BigIntegerField(db_index=True)
    guild_name = models.CharField(max_length=128, blank=True, null=True, default='Unknown')

    def __str__(self):
        return f'{self.guild_name} - {self.guild_id}'

class DiscordRole(models.Model):
    role_id = models.BigIntegerField()
    role_name = models.CharField(max_length=128, blank=True,null=True, default='donator')

    def __str__(self):
        return f'{self.role_name} - {self.role_id}'

class GuildToRoleRelation(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)
    role = models.ForeignKey(DiscordRole, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.guild.guild_name} - {self.role.role_name}'

class AllowedDiscordServer(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.guild.guild_name}'

