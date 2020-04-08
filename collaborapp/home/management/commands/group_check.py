from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = "Check whether private 'us' group and relevant users 'sadie' and 'martin' exist."

    def handle(self, *args, **kwargs):
        try:
            us = Group.objects.get(name='us')
            us_group_exists = True
        except:
            us_group_exists = False

        existing_users = dict()
        for user in ('sadie', 'martin'):
            try:
                u = User.objects.get(username=user)
                existing_users[user] = True
            except:
                existing_users[user] = False

        if us_group_exists and existing_users['sadie'] and existing_users['martin']:
            print('All is well. Group and users exist. If you added a user recently, you may have to delete the group.')
        elif us_group_exists:
            print('Group exists. Double-check usernames: ', existing_users)
        elif existing_users['sadie'] and existing_users['martin']:
            print("Users 'sadie' and 'martin' exist. Run 'group_us' to add them to the 'us' group.")
        else:
            print("Double-check usernames: ", existing_users)
