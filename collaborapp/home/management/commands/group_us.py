from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    help = "Create group 'us' with full permissions and add users."

    @staticmethod
    def add_user_to_group(group, username):
        u = User.objects.get(username=username)
        u.groups.add(group)
        u.save()

    def add_arguments(self, parser):
        parser.add_argument('username',
                            nargs='+',
                            type=str,
                            help="Add usernames to add to 'us' group, separated by whitespace")

    def handle(self, *args, **kwargs):
        users_to_add = kwargs['username']
        us, created = Group.objects.get_or_create(name='us')

        if created:
            us.save()
            permissions = Permission.objects.all()
            for p in permissions:
                us.permissions.add(p)
                us.save()

            users_to_add = input(": ").split()
            for u in users_to_add:
                try:
                    self.add_user_to_group(us, u)
                except:
                    print("No user with username {}".format(u))
