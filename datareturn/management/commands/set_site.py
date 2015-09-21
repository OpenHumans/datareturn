from django.core.management.base import BaseCommand, CommandError

from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Create an admin user for an email address.'

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        site = Site.objects.all()[0]
        site.domain = options['domain']
        site.name = options['name']
        site.save()
