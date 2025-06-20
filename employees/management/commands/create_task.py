from django.core.management import BaseCommand
from employees.models import Task


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        title, _ = Task.objects.all().delete()
        title, _ = Task.objects.get_or_create(title="programming",
                                             date="2025-12-11")
