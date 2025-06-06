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
        
        # Base query
        articles = Article.objects.filter(published_at__isnull=False)
        
        # Apply category filter if user has interests
        if preferred_categories.exists():
            articles = articles.filter(category__in=preferred_categories)
        
        # Apply country filter
        if hasattr(user, 'country') and user.country:
            articles = articles.filter(source__iendswith=f"_{user.country.lower()}")
        
        # Apply toggle filter
        if toggle == 'breaking':
            articles = articles.filter(is_breaking=True)
        
        # Order by published date
        articles = articles.order_by('-published_at')
        
        logger.info(f"Fetching feed for user {user.email}")
        logger.info(f"Categories: {[cat.name for cat in preferred_categories]}")
        logger.info(f"Country: {user.country}")
        logger.info(f"Found {articles.count()} articles")
        
        return articles
    except Exception as e:
        logger.error(f"Error getting user feed: {str(e)}")
        return Article.objects.none()

def fetch_articles():
    """Fetch articles using Newsdata.io API for each user's country and interests."""
    try:
        # Download required NLTK data
        download_nltk_data()
        
        # Get all unique countries from users
        countries = CustomUser.objects.values_list('country', flat=True).distinct()
        
        for country in countries:
            try:
                # Fetch all articles for this country at once
                articles = fetch_articles_from_newsdata(country)
                if articles:
                    logger.info(f"Successfully fetched {len(articles)} articles for {country}")
                    
                    # Get all users for this country
                    users = CustomUser.objects.filter(country=country)
                    for user in users:
                        interests = user.interests.all()
                        if not interests.exists():
                            continue
                            
                        # Filter articles by user's interests
                        user_articles = [article for article in articles if article.category in interests]
                        logger.info(f"Filtered {len(user_articles)} articles for user {user.email}")
                        
            except Exception as e:
                logger.error(f"Error fetching articles for {country}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error in fetch_articles: {str(e)}")

def fetch_articles_from_newsdata(country_code):
    """Fetch articles from Newsdata.io API for a specific country."""
    api_key = settings.NEWSDATA_API_KEY
    url = f'https://newsdata.io/api/1/news?apikey={api_key}&country={country_code}&language=en'
    
    try:
        logger.info(f"Fetching news for country: {country_code}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            articles = []
            for article_data in data.get('results', []):
                try:
                    summary = article_data.get('description', '') or article_data.get('title', '')
                    title = article_data.get('title', '')[:500]
                    pub_date = article_data.get('pubDate')
                    if pub_date:
                        pub_date = timezone.make_aware(datetime.fromisoformat(pub_date.replace('Z', '+00:00')))
                    
                    # Get category from article data
                    category_name = article_data.get('category', ['General'])[0]
                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'description': f'News about {category_name}'}
                    )
                    
                    article, created = Article.objects.get_or_create(
                        url=article_data['link'],
                        defaults={
                            'title': title,
                            'content': article_data.get('content', '')[:10000],
                            'summary': summary,
                            'source': f"{article_data.get('source_id', '')[:200]}_{country_code}",
                            'published_at': pub_date,
                            'image_url': article_data.get('image_url'),
                            'is_breaking': article_data.get('is_breaking', False),
                            'category': category,
                        }
                    )
                    
                    if created and article.content:
                        blob = TextBlob(article.content)
                        article.sentiment_score = blob.sentiment.polarity
                        article.reading_level = calculate_reading_level(article.content)
                        article.save()
                    
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
            
            logger.info(f"Successfully processed {len(articles)} articles for {country_code}")
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
