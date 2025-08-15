from django.core.management.base import BaseCommand
from news.services import fetch_articles
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch news articles from various sources'

    def handle(self, *args, **options):
        self.stdout.write('Starting to fetch articles...')
        fetch_articles()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored news articles.'))
