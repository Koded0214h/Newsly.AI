from django.core.management.base import BaseCommand
from news.models import Article, Category
from news.services import fetch_articles
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Fetch news articles using newspaper3k'

    def handle(self, *args, **kwargs):
        try:
            fetch_articles()
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored news articles.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in fetch_articles command: {str(e)}'))
