from django.core.management.base import BaseCommand
from pogobackend.settings import RABBITMQ_HOST,RABBITMQ_PORT,RABBITMQ_USERNAME,RABBITMQ_PASSWORD,RABBITMQ_CONSUMER_QUEUE
from donations.models import Donator, GuildToRoleRelation
from django.db.models import Q
import pika
import json


class Command(BaseCommand):
    help = 'update users'

    def add_arguments(self, parser):
        # Positional arguments are standalone name
        parser.add_argument('user_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        user_ids = kwargs.get('user_ids')
        user_ids_int = [int(x) for x in user_ids]
        # get donators and partition into donators and no donators.
        give_roles = Donator.objects.filter(
            (Q(monthly_paid=True) | Q(precious=True)) & Q(user__uid__in=user_ids)).values_list('user__uid', flat=True)
        # discord uid must be int since rewrite.
        give_roles = [int(x) for x in give_roles]
        take_roles = [int(x) for x in user_ids_int if x not in give_roles]
        # get guild_to_role mapping
        donator_roles = GuildToRoleRelation.objects.all()
        guild_to_roles = [{"guild_id": obj.guild.guild_id, "role_id": obj.role.role_id} for obj in donator_roles]
        message = {
            "guild_to_roles": guild_to_roles,
            "role_assignments": {
                                  "give_role": give_roles if give_roles else [],
                                  "take_role": take_roles if take_roles else []
                                }
        }
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
        channel = connection.channel()

        channel.queue_declare(queue=RABBITMQ_CONSUMER_QUEUE)
        channel.basic_publish(exchange='', routing_key=RABBITMQ_CONSUMER_QUEUE,
                              body=json.dumps(message))
        connection.close()

