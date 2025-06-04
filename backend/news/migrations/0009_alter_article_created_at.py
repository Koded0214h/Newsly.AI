from django.db import migrations, models
from django.utils import timezone

def set_created_at(apps, schema_editor):
    Article = apps.get_model('news', 'Article')
    # Update any NULL created_at values to current time
    Article.objects.filter(created_at__isnull=True).update(created_at=timezone.now())

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_merge_20240327_1234'),
    ]

    operations = [
        # First, update any NULL values
        migrations.RunPython(set_created_at),
        # Then make the field non-nullable
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ] 