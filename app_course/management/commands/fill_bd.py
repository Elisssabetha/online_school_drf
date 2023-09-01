from django.core.management import BaseCommand, call_command

from app_course.models import Lesson, Course, Payment
from users.models import User


class Command(BaseCommand):
    """Filling DB with data from the fixture"""
    def handle(self, *args, **options):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Payment.objects.all().delete()
        call_command('loaddata', 'db_data.json')
