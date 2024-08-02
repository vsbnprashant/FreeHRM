# employee_management/management/commands/clear_contenttypes.py

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Clears the django_content_type table'

    def handle(self, *args, **kwargs):
        ContentType.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared django_content_type table'))