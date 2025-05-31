from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
import openai
from django.conf import settings
from textblob import TextBlob
import re

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

def analyze_sentiment(text):
    """
    Analyze the sentiment of a text using TextBlob.
    Returns a score between -1 (negative) and 1 (positive).
    """
    try:
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return 0

def analyze_reading_level(text):
    """
    Calculate a simple reading level score based on average word length.
    Returns a score between 1 (easy) and 5 (difficult).
    """
    try:
        # Remove special characters and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 1
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Convert to a 1-5 scale
        if avg_word_length < 4:
            return 1  # Very easy
        elif avg_word_length < 5:
            return 2  # Easy
        elif avg_word_length < 6:
            return 3  # Moderate
        elif avg_word_length < 7:
            return 4  # Difficult
        else:
            return 5  # Very difficult
    except Exception as e:
        print(f"Error analyzing reading level: {str(e)}")
        return 3  # Default to moderate 