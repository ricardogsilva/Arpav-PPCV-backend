from django.core.management import BaseCommand
from djcore.djcore.users.models import User

# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):

    # Show this when the user types help
    help = "My test command"

    def handle(self, *args, **options):
        u = User(username='inkode', email='info@inkode.it')
        u.set_password('inkode')
        u.is_superuser = True
        u.is_staff = True
        u.save()

        self.stdout.write("Doing All The Things!")
