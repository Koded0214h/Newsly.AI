from django.core.management.base import BaseCommand
from news.models import Category

class Command(BaseCommand):
    help = 'Creates default news categories'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Technology',
                'description': 'Latest news in tech, gadgets, and digital innovation'
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
                'description': 'Movies, music, TV shows, and celebrity news'
            },
            {
                'name': 'Sports',
                'description': 'Sports news, scores, and athlete updates'
            },
            {
                'name': 'Politics',
                'description': 'Political news, policy changes, and government updates'
            },
            {
                'name': 'Environment',
                'description': 'Environmental news, climate change, and sustainability'
            },
            {
                'name': 'Education',
                'description': 'Education news, academic research, and learning trends'
            },
            {
                'name': 'World',
                'description': 'International news and global events'
            }
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created category "{category.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category.name}" already exists')) 