from django.db import migrations

def create_default_topics(apps, schema_editor):
    Topic = apps.get_model('news', 'Topic')
    default_topics = [
        {
            'name': 'Technology',
            'description': 'Latest news about technology, gadgets, and digital innovations'
        },
        {
            'name': 'Business',
            'description': 'Business news, market updates, and economic trends'
        },
        {
            'name': 'Science',
            'description': 'Scientific discoveries, research, and breakthroughs'
        },
        {
            'name': 'Health',
            'description': 'Health news, medical research, and wellness updates'
        },
        {
            'name': 'Entertainment',
            'description': 'Entertainment news, celebrity updates, and cultural trends'
        },
        {
            'name': 'Sports',
            'description': 'Sports news, game updates, and athlete profiles'
        },
        {
            'name': 'Politics',
            'description': 'Political news, policy updates, and government affairs'
        },
        {
            'name': 'Environment',
            'description': 'Environmental news, climate updates, and sustainability'
        }
    ]
    
    for topic_data in default_topics:
        Topic.objects.get_or_create(
            name=topic_data['name'],
            defaults={'description': topic_data['description']}
        )

def remove_default_topics(apps, schema_editor):
    Topic = apps.get_model('news', 'Topic')
    Topic.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('news', '0003_article'),
    ]

    operations = [
        migrations.RunPython(create_default_topics, remove_default_topics),
    ] 