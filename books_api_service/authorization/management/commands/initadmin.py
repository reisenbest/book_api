from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


#инициализация супер пользователя если его нет (для докера)
class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            username = 'admin'
            email = 'admin@admin.com'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(username=username, email=email, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            print('Admin account created successfully.')
        else:
            print('Admin account already exists.')
