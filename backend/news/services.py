from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
import openai
from django.conf import settings

def get_user_feed(user):
    """
    Get personalized feed for a user based on their interests and preferences.
    """
    # Get user's interests
    interests = user.interests.all()
    
    # Get articles that match user's interests
    articles = Article.objects.filter(
        Q(category__in=interests) | Q(category__isnull=True)
    ).order_by('-created_at')
    
    return articles

def generate_summary(text, max_length=150):
    """
    Generate a summary of the given text using OpenAI's API.
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Generate summary
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                {"role": "user", "content": f"Please summarize this article in {max_length} characters or less: {text}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract and return the summary
        summary = response.choices[0].message.content.strip()
        return summary[:max_length]
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return text[:max_length] + "..." if len(text) > max_length else text 