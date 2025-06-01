from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
import openai
from django.conf import settings
from textblob import TextBlob
import re
import os
from datetime import datetime, timedelta

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

def generate_news_content(category):
    """Generate news content for a given category using OpenAI."""
    try:
        # Set up OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create a prompt for the category
        prompt = f"""Generate a realistic news article about {category.name}. 
        The article should be informative, engaging, and current.
        Include:
        1. A catchy headline
        2. A detailed article body (at least 500 words)
        3. A brief summary (2-3 sentences)
        
        Format the response as JSON with these fields:
        {{
            "title": "article headline",
            "content": "full article content",
            "summary": "brief summary"
        }}
        """
        
        # Generate content using OpenAI
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional news writer. Write realistic, engaging news articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse the response
        content = response.choices[0].message.content
        import json
        article_data = json.loads(content)
        
        # Create a unique URL (using timestamp and category)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        url = f"https://newsly.ai/articles/{category.name.lower()}/{timestamp}"
        
        # Create the article
        article = Article.objects.create(
            title=article_data['title'],
            content=article_data['content'],
            summary=article_data['summary'],
            url=url,
            category=category,
            created_at=datetime.now()
        )
        
        return article
        
    except Exception as e:
        print(f"Error generating news content: {str(e)}")
        return None

def fetch_articles():
    """Fetch articles for all categories."""
    try:
        # Get all categories
        categories = Category.objects.all()
        
        # Generate articles for each category
        for category in categories:
            # Check if we need to generate new articles
            last_article = Article.objects.filter(category=category).order_by('-created_at').first()
            
            if not last_article or (datetime.now() - last_article.created_at) > timedelta(hours=24):
                # Generate new article
                article = generate_news_content(category)
                if article:
                    print(f"Generated new article for {category.name}: {article.title}")
                else:
                    print(f"Failed to generate article for {category.name}")
                    
    except Exception as e:
        print(f"Error in fetch_articles: {str(e)}")

def analyze_sentiment(text):
    """Analyze the sentiment of text using OpenAI."""
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Analyze the sentiment of the following text and return a score from -1 (very negative) to 1 (very positive)."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=10
        )
        
        # Parse the response to get a float between -1 and 1
        score = float(response.choices[0].message.content.strip())
        return max(min(score, 1), -1)  # Ensure score is between -1 and 1
        
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return 0

def analyze_reading_level(text):
    """Analyze the reading level of text using OpenAI."""
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Analyze the reading level of the following text and return a score from 1 (elementary) to 10 (advanced)."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=10
        )
        
        # Parse the response to get a float between 1 and 10
        score = float(response.choices[0].message.content.strip())
        return max(min(score, 10), 1)  # Ensure score is between 1 and 10
        
    except Exception as e:
        print(f"Error analyzing reading level: {str(e)}")
        return 5  # Return middle value as default 