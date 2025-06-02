from django.core.management.base import BaseCommand
from news.models import Article, Category
import openai
from django.conf import settings

class Command(BaseCommand):
    help = 'Recategorize articles based on their content using OpenAI'

    def handle(self, *args, **kwargs):
        try:
            # Get all articles
            articles = Article.objects.all()
            categories = Category.objects.all()
            
            # Set up OpenAI client
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            for article in articles:
                # Create a prompt for category classification
                prompt = f"""Given the following article content, determine the most appropriate category from this list: {', '.join(cat.name for cat in categories)}.
                
                Article Title: {article.title}
                Article Content: {article.content[:1000]}  # Using first 1000 chars for efficiency
                
                Respond with ONLY the category name that best fits this article. Do not include any other text."""
                
                # Get category prediction from OpenAI
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are a news categorization expert. Respond with only the category name."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=50
                )
                
                # Get the predicted category
                predicted_category = response.choices[0].message.content.strip()
                
                # Find the matching category
                try:
                    category = Category.objects.get(name__iexact=predicted_category)
                    article.category = category
                    article.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully recategorized article "{article.title}" to {category.name}'
                        )
                    )
                except Category.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Could not find category "{predicted_category}" for article "{article.title}"'
                        )
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error recategorizing articles: {str(e)}')
            ) 