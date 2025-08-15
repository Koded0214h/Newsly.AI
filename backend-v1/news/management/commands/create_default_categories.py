from django.core.management.base import BaseCommand
from news.models import Category

class Command(BaseCommand):
    help = 'Creates default news categories'

    def handle(self, *args, **kwargs):
        default_categories = [
            'Technology',
            'Business',
            'Politics',
            'Science',
            'Health',
            'Entertainment',
            'Sports',
            'Environment',
            'Education',
            'World News'
        ]

        for category_name in default_categories:
            Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'News about {category_name.lower()}'}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category_name}"')
            ) 