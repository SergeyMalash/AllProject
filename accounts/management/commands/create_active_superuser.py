from django.core.management import BaseCommand

from accounts.models import Account


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = Account.objects.create_superuser('admin', 'admin@admin.com', 'admin', is_active=True)
        if admin:
            print("Администратор создан успешно - login/password: admin/admin")

