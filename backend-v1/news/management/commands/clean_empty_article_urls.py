from django.core.management.base import BaseCommand
from news.models import Article

class Command(BaseCommand):
    help = 'Delete articles with empty or null URL fields to fix unique constraint errors.'

    def handle(self, *args, **options):
        empty_url_articles = Article.objects.filter(url__isnull=True) | Article.objects.filter(url='')
        count = empty_url_articles.count()
        empty_url_articles.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} articles with empty or null URLs.'))
