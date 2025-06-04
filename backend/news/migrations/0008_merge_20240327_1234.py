from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_update_article_metrics'),
        ('news', '0007_alter_userpreference_user_delete_user'),
    ]

    operations = [
        # No operations needed, this is just a merge migration
    ] 