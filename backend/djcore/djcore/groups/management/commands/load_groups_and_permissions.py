from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):

    # Show this when the user types help
    help = "My test command"

    groups = [
        {
            'name': 'Admin',
            'permissions': [
                #"view_map",
                #"add_map",
            ],
        }
    ]


    def handle(self, *args, **options):
        for group_dict in self.groups:
            check_if_exist = Group.objects.filter(name=group_dict.get('name'))
            if check_if_exist.count() == 0:
                group = Group.objects.create(name=group_dict.get('name'))
            else:
                group = check_if_exist.get()
            permissions = Permission.objects.filter(codename__in=group_dict.get('permissions')).all()
            # print((group_dict['name']))
            # print((group_dict['permissions']))
            # print(permissions)
            group.permissions.add( *permissions )

        self.stdout.write("Doing All The Things!")
