from django.core.management.base import BaseCommand
from news.services import fetch_articles_from_newsdata_with_category
from news.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch news articles from various sources'

    def handle(self, *args, **options):
        self.stdout.write('Starting to fetch articles...')
        
        # Get all users
        users = CustomUser.objects.all()
        
        # Fetch articles for each user's country and interests
        for user in users:
            self.stdout.write(f'Fetching articles for user: {user.email}')
            country = user.country
            interests = user.interests.all()
            
            if not country or not interests.exists():
                self.stdout.write(self.style.WARNING(f'Skipping user {user.email} - no country or interests set'))
                continue
                
            for category in interests:
                self.stdout.write(f'Fetching {category.name} articles for {country}')
                articles = fetch_articles_from_newsdata_with_category(country, category.name)
                self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(articles)} articles for {country}, {category.name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored news articles.'))
