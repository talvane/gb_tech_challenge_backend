from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates the default groups for the system'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin'):
            user = User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                cpf='48527519003',
                first_name='Admin',
                last_name='Admin'
            )
            user.set_password('gy49y6.')
            user.save()
