from django.core.management.base import BaseCommand
from news.services import fetch_articles_from_newsdata
from news.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch news articles from various sources'

    def handle(self, *args, **options):
        self.stdout.write('Starting to fetch articles...')
        
        # Get unique countries from users
        countries = CustomUser.objects.values_list('country', flat=True).distinct()
        
        # Fetch articles for each country
        for country in countries:
            self.stdout.write(f'Fetching articles for country: {country}')
            articles = fetch_articles_from_newsdata(country)
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(articles)} articles for {country}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored news articles.'))
