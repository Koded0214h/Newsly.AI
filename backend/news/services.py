from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
import openai
from django.conf import settings
from textblob import TextBlob
import re
import os
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import sent_tokenize
import json

def get_user_feed(user, toggle='breaking'):
    """
    Get personalized feed for a user based on their interests and preferences.
    """
    try:
        # Get user's interests
        interests = user.interests.all()
        
        # Get articles that match user's interests
        articles = Article.objects.filter(
            Q(category__in=interests) | Q(category__isnull=True)
        ).order_by('-created_at')
        
        return articles
    except Exception as e:
        print(f"Error in get_user_feed: {str(e)}")
        return []

def generate_summary(text, max_words=200):
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create prompt for summary generation
        prompt = f"""Generate a concise summary of the following text in {max_words} words or less.
        Text: {text}
        Return only the summary text."""
        
        # Get summary from OpenAI
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a summarization expert. Provide clear and concise summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        # Get the summary
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return ""

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
        return 5

def generate_news_content(category):
    """Generate news content for a given category using OpenAI."""
    try:
        # Check if OPENAI_API_KEY is set
        if not settings.OPENAI_API_KEY:
            print("Error: OPENAI_API_KEY is not set in environment variables.")
            return None

        # Log masked API key presence
        if settings.OPENAI_API_KEY:
            print("OPENAI_API_KEY is set.")
        else:
            print("OPENAI_API_KEY is empty or None.")

        # Set up OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Defensive check for category and category name
        if category is None:
            print("Warning: category is None, using 'general' as category name.")
            category_name = "general"
        else:
            try:
                category_name = category.name if category.name else "general"
            except Exception as e:
                print(f"Error accessing category.name: {str(e)}")
                category_name = "general"
        print(f"Generating article for category: '{category_name}'")

        # Create a prompt for the category
        prompt = f"""Generate a realistic news article about {category_name}. 
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
        print(f"Raw OpenAI response content: {content}")
        import json
        try:
            article_data = json.loads(content)
        except Exception as e:
            print(f"Error parsing article JSON: {str(e)}")
            return None
        
        # Validate article_data fields presence and non-empty
        required_fields = ('title', 'content', 'summary')
        if not all(k in article_data for k in required_fields):
            print(f"Error: article_data missing required fields: {article_data}")
            return None
        for field in required_fields:
            if not article_data[field] or not article_data[field].strip():
                print(f"Error: article_data field '{field}' is empty: {article_data}")
                return None
        
        # Create a unique URL (using timestamp with microseconds and category)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        url = f"https://newsly.ai/articles/{category_name.lower()}/{timestamp}"

        # Validate URL is not empty or malformed, fallback to UUID
        import uuid
        if not url or url == "https://newsly.ai/articles//" or url.isspace():
            fallback_uuid = uuid.uuid4()
            url = f"https://newsly.ai/articles/{category_name.lower()}/{fallback_uuid}"
            print(f"Warning: Generated URL was empty or invalid, using fallback URL: {url}")
        
        print(f"Generated article URL: {url}")
        
        # Check if article with this URL already exists
        if Article.objects.filter(url=url).exists():
            print(f"Article with URL {url} already exists. Skipping creation.")
            return None
        
        # Create the article
        try:
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
            print(f"Error creating article in DB: {str(e)}")
            return None
        
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
                    print(f"Successfully created article for category {category.name}")
                else:
                    print(f"Error generating article for category {category.name}")
                    
    except Exception as e:
        print(f"Error in fetch_articles: {str(e)}")
