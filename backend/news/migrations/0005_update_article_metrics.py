from django.db import migrations
from news.services import analyze_sentiment, analyze_reading_level

def update_article_metrics(apps, schema_editor):
    Article = apps.get_model('news', 'Article')
    articles = Article.objects.all()
    
    for article in articles:
        try:
            # Update sentiment score
            if article.sentiment_score is None:
                article.sentiment_score = analyze_sentiment(article.content)
            
            # Update reading level
            if article.reading_level is None:
                article.reading_level = analyze_reading_level(article.content)
        except Exception as e:
            print(f"Error processing article {article.id}: {str(e)}")
            continue
    
    # Use bulk_update for better performance
    Article.objects.bulk_update(articles, ['sentiment_score', 'reading_level'])

def reverse_update_metrics(apps, schema_editor):
    # No need to reverse this operation
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_update_article_fields'),
    ]

    operations = [
        migrations.RunPython(update_article_metrics, reverse_update_metrics),
    ] 