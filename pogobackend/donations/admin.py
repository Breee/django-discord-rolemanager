from django.contrib import admin
from donations.models import Donator, Donation, RawDonation, AllowedDiscordServer, DiscordRole,DiscordGuild,GuildToRoleRelation
# Register your models here.

admin.site.register(Donator)
admin.site.register(Donation)
admin.site.register(RawDonation)
admin.site.register(AllowedDiscordServer)
admin.site.register(DiscordRole)
admin.site.register(DiscordGuild)
admin.site.register(GuildToRoleRelation)
