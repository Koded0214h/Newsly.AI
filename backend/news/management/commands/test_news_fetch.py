from django.core.management.base import BaseCommand
from news.services import fetch_articles_from_newsdata
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test fetching news articles from Nigeria'

    def handle(self, *args, **options):
        self.stdout.write('Testing news fetch for Nigeria...')
        
        try:
            articles = fetch_articles_from_newsdata(country_code='ng')
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(articles)} articles from Nigeria'))
            
            # Log details of each article
            for article in articles:
                logger.info(f"Article: {article.title}")
                logger.info(f"Source: {article.source}")
                logger.info(f"Category: {article.category}")
                logger.info(f"Published: {article.published_at}")
                logger.info("---")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching articles: {str(e)}'))
            logger.error(f'Error in test_news_fetch: {str(e)}') 