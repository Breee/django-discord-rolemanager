import allauth.account.signals
import requests
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.models import User, Group, AnonymousUser
from donations.models import AllowedDiscordServer
from django.contrib.auth import logout


import logging
logger = logging.getLogger('default')
