from django.core.management.base import BaseCommand
from news.models import Article, Category
from news.services import fetch_articles
from django.utils import timezone
from datetime import timedelta
import subprocess
import sys

class Command(BaseCommand):
    help = 'Fetch news articles using newspaper3k'

    def handle(self, *args, **kwargs):
        try:
            # Download TextBlob data
            self.stdout.write('Downloading TextBlob data...')
            subprocess.check_call([sys.executable, '-m', 'textblob.download_corpora'])
            self.stdout.write(self.style.SUCCESS('Successfully downloaded TextBlob data.'))

            # Fetch articles
            fetch_articles()
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored news articles.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in fetch_articles command: {str(e)}'))
