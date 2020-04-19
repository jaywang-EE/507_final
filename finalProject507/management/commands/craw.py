from django.core.management.base import BaseCommand, CommandError

from finalProject507.crawlers.crawler import craw_covid_cron
from djangoherokuapp import settings

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if settings.ON_HEROKU:
            self.stdout.write(self.style.SUCCESS("start crawing..."))
            craw_covid_cron()
            self.stdout.write(self.style.SUCCESS('Successfully crawed'))
        else:
            print("ON_HEROKU is set to false...")

