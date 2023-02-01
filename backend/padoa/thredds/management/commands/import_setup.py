from django.core.management import BaseCommand, call_command
from oauth2_provider.models import Application
import json

# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):

    # Show this when the user types help
    help = "This will import all importable things"

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
        # call_command('import_client')
        call_command('import_super_user')
        # call_command('load_groups_and_permissions')
        call_command('import_attributes')
        call_command('import_regions')
        call_command('import_layers')
