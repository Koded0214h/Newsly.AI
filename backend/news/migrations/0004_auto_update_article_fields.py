from django.db import migrations, models
from django.utils import timezone

def set_published_at(apps, schema_editor):
    Article = apps.get_model('news', 'Article')
    # Use bulk_update for better performance
    articles = Article.objects.all()
    for article in articles:
        if not article.published_at:
            article.published_at = article.created_at or timezone.now()
    Article.objects.bulk_update(articles, ['published_at'])

def reverse_set_published_at(apps, schema_editor):
    # No need to reverse this operation
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_article'),
    ]

    operations = [
        # First, add the fields as nullable
        migrations.AddField(
            model_name='article',
            name='sentiment_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='reading_level',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='published_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        # Then populate the published_at field
        migrations.RunPython(set_published_at, reverse_set_published_at),
        # Finally, make source non-nullable but allow blank
        migrations.AlterField(
            model_name='article',
            name='source',
            field=models.CharField(max_length=100, blank=True),
        ),
    ] 