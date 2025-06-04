from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_article_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='updated_at',
        ),
    ] 