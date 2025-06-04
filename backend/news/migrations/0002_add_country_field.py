from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(
                max_length=2,
                choices=[
                    ('us', 'United States'),
                    ('gb', 'United Kingdom'),
                    ('ng', 'Nigeria'),
                    ('ca', 'Canada'),
                    ('au', 'Australia'),
                    ('in', 'India'),
                    ('za', 'South Africa'),
                    ('ke', 'Kenya'),
                    ('gh', 'Ghana'),
                ],
                default='us'
            ),
        ),
    ] 