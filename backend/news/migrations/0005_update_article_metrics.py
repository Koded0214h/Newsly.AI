from django.db import migrations
from textblob import TextBlob

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity  # -1 to 1
    except Exception as e:
        print(f"Error in analyze_sentiment: {str(e)}")
        return 0

def analyze_reading_level(text):
    try:
        blob = TextBlob(text)
        # Use average sentence length as a proxy for reading level
        sentences = blob.sentences
        if not sentences:
            return 0
        avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences)
        # Map average sentence length to a scale 1-10
        score = min(max((avg_sentence_length - 5) / 3, 1), 10)
        return score
    except Exception as e:
        print(f"Error in analyze_reading_level: {str(e)}")
        return 0

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