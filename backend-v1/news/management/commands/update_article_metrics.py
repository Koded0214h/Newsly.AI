from django.core.management.base import BaseCommand
from news.models import Article
from news.services import analyze_sentiment, analyze_reading_level

class Command(BaseCommand):
    help = 'Updates sentiment scores and reading levels for all articles'

    def handle(self, *args, **kwargs):
        articles = Article.objects.all()
        total = articles.count()
        updated = 0

        self.stdout.write(f"Starting to update {total} articles...")

        for article in articles:
            try:
                # Update sentiment score
                sentiment_score = analyze_sentiment(article.content)
                article.sentiment_score = sentiment_score

                # Update reading level
                reading_level = analyze_reading_level(article.content)
                article.reading_level = reading_level

                article.save()
                updated += 1

                if updated % 10 == 0:  # Progress update every 10 articles
                    self.stdout.write(f"Updated {updated}/{total} articles...")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error updating article {article.id}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} out of {total} articles')
        ) 