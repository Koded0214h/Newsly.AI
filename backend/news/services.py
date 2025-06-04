import feedparser
from newspaper import Article as NPArticle
from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
from datetime import datetime, timedelta
import requests
from django.conf import settings
from textblob import TextBlob
import nltk
from django.utils import timezone
import logging
from django.conf import settings
from environ import Env

# Initialize the environment
env = Env()

logger = logging.getLogger(__name__)

def get_user_feed(user, toggle='all'):
    """
    Get personalized feed for a user based on their interests and preferences.
    """
    try:
        # Get user's preferred categories
        preferred_categories = user.interests.all()
        
        # Base query with country filter
        articles = Article.objects.filter(
            category__in=preferred_categories,
            published_at__isnull=False
        ).order_by('-published_at')
        
        # Apply country filter if available
        if hasattr(user, 'country'):
            articles = articles.filter(source__country=user.country)
        
        # Apply toggle filter
        if toggle == 'breaking':
            articles = articles.filter(is_breaking=True)
        
        return articles
    except Exception as e:
        logger.error(f"Error getting user feed: {str(e)}")
        return Article.objects.none()

def fetch_articles():
    """Fetch articles using Newsdata.io API."""
    try:
        # Download required NLTK data
        download_nltk_data()
        
        # Get all unique countries from users
        countries = CustomUser.objects.values_list('country', flat=True).distinct()
        
        for country in countries:
            try:
                articles = fetch_articles_from_newsdata(country)
                logger.info(f"Successfully fetched {len(articles)} articles for {country}")
            except Exception as e:
                logger.error(f"Error fetching articles for {country}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error in fetch_articles: {str(e)}")

def fetch_articles_from_newsdata(country_code='ng'):
    """Fetch articles from Newsdata.io API"""
    api_key = settings.NEWSDATA_API_KEY
    url = f'https://newsdata.io/api/1/news?apikey={api_key}&country={country_code}&language=en'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            articles = []
            for article_data in data.get('results', []):
                try:
                    # Ensure summary is not null
                    summary = article_data.get('description', '')
                    if not summary:
                        summary = article_data.get('title', '')  # Use title as fallback
                    
                    # Ensure title is not too long
                    title = article_data.get('title', '')[:500]  # Truncate to 500 chars
                    
                    # Convert naive datetime to timezone-aware
                    pub_date = article_data.get('pubDate')
                    if pub_date:
                        pub_date = timezone.make_aware(datetime.fromisoformat(pub_date.replace('Z', '+00:00')))
                    
                    # Get or create default category
                    default_category, _ = Category.objects.get_or_create(name='General')
                    
                    # Create or update article
                    article, created = Article.objects.get_or_create(
                        url=article_data['link'],
                        defaults={
                            'title': title,
                            'content': article_data.get('content', '')[:10000],  # Truncate content if too long
                            'summary': summary,  # No truncation needed for TextField
                            'source': f"{article_data.get('source_id', '')[:200]}_{country_code}",  # Include country in source
                            'published_at': pub_date,
                            'image_url': article_data.get('image_url'),
                            'is_breaking': article_data.get('is_breaking', False),
                            'category': default_category,  # Assign default category
                        }
                    )
                    
                    if created:
                        # Analyze sentiment and reading level
                        if article.content:
                            blob = TextBlob(article.content)
                            article.sentiment_score = blob.sentiment.polarity
                            article.reading_level = calculate_reading_level(article.content)
                            article.save()
                    
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
            
            return articles
        else:
            logger.error(f"Newsdata.io API error: {data.get('message', 'Unknown error')}")
            return []
            
    except Exception as e:
        logger.error(f"Error fetching from Newsdata.io: {str(e)}")
        return []

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

def calculate_reading_level(text):
    """Calculate the Flesch Reading Ease score"""
    try:
        blob = TextBlob(text)
        sentences = blob.sentences
        words = blob.words
        syllables = sum(count_syllables(word) for word in words)
        
        if not sentences or not words:
            return 0
            
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        # Flesch Reading Ease formula
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        return max(0, min(100, score))  # Normalize between 0 and 100
    except Exception as e:
        logger.error(f"Error calculating reading level: {str(e)}")
        return 0

def count_syllables(word):
    """Count the number of syllables in a word"""
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    previous_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_is_vowel:
            count += 1
        previous_is_vowel = is_vowel
    
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
    return count

from textblob import TextBlob

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity  # -1 to 1
    except Exception as e:
        print(f"Error in analyze_sentiment: {str(e)}")
        return 0

def analyze_reading_level(text):
    try:
        blob = TextBlob(text)
        # Use average sentence length as a proxy for reading level
        sentences = blob.sentences
        if not sentences:
            return 0
        avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences)
        # Map average sentence length to a scale 1-10
        score = min(max((avg_sentence_length - 5) / 3, 1), 10)
        return score
    except Exception as e:
        print(f"Error in analyze_reading_level: {str(e)}")
        return 0
