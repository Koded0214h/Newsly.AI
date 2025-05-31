import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
import textstat
from news.models import Article, Topic, Category
import logging
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
from bs4 import BeautifulSoup
import html
from django.conf import settings

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

logger = logging.getLogger(__name__)

TOPIC_KEYWORDS = {
    "Business": {"business", "economy", "market", "stock", "trade", "finance", "bank", "investment", "company", "corporate", "dollar", "profit", "revenue", "shares", "stock market", "wall street"},
    "Politics": {"politics", "government", "election", "president", "congress", "senate", "democrat", "republican", "policy", "vote", "campaign", "legislation", "bill", "law", "administration", "minister", "parliament"},
    "Entertainment": {"entertainment", "movie", "film", "music", "celebrity", "show", "tv", "theater", "concert", "festival", "actor", "actress", "director", "hollywood", "bollywood"},
    "Environment": {"environment", "climate", "nature", "wildlife", "conservation", "pollution", "sustainability", "global warming", "green", "ecology", "recycle", "carbon", "emissions"},
    "Health": {"health", "medicine", "medical", "doctor", "hospital", "disease", "virus", "covid", "pandemic", "vaccine", "treatment", "wellness", "fitness", "nutrition", "mental health"},
    "Science": {"science", "research", "study", "scientist", "experiment", "discovery", "space", "nasa", "astronomy", "physics", "chemistry", "biology", "laboratory", "technology"},
    "Sports": {"sports", "game", "match", "tournament", "league", "player", "team", "score", "goal", "win", "lose", "coach", "athlete", "olympics", "football", "soccer", "basketball", "baseball", "tennis", "cricket"},
    "Technology": {"technology", "tech", "computer", "software", "hardware", "internet", "ai", "artificial intelligence", "robot", "robotics", "startup", "app", "application", "gadget", "device", "smartphone", "mobile", "web", "cloud", "data", "cyber", "security"},
}

def get_topic_for_text(text, topics):
    text = text.lower()
    best_topic = topics['general']
    max_matches = 0
    for topic_name, keywords in TOPIC_KEYWORDS.items():
        matches = sum(1 for word in keywords if word in text)
        if matches > max_matches:
            max_matches = matches
            best_topic = topics[topic_name.lower()]
    return best_topic

def fetch_news_articles():
    # Log the full API key for debugging (only in development)
    if settings.DEBUG:
        logger.info(f"Full NewsAPI key: {settings.NEWS_API_KEY}")
    else:
        logger.info(f"Using NewsAPI key: {settings.NEWS_API_KEY[:5]}...")  # Only log first 5 chars for security
    
    url = f'https://newsapi.org/v2/top-headlines?language=en&pageSize=20&apiKey={settings.NEWS_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            logger.error(f"NewsAPI returned error: {data.get('message', 'Unknown error')}")
            return []
            
        articles = data.get('articles', [])
        logger.info(f"Successfully fetched {len(articles)} articles from NewsAPI")
        return articles
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return []

def get_full_article_content(url):
    """Fetch the full article content from the article URL, fallback gracefully if blocked."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Clean up URL if needed
        url = url.replace('\\u003d', '=').replace('\\/', '/')
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'meta', 'link', 'noscript', 'iframe', 'picture', 'svg', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Try different strategies to find the main content
        content = None
        
        # Strategy 1: Look for common article containers
        article_containers = soup.find_all(['article', 'main', 'div'], class_=lambda x: x and any(term in str(x).lower() for term in ['article', 'content', 'story', 'post', 'entry', 'main']))
        
        if article_containers:
            content_div = article_containers[0]
            paragraphs = content_div.find_all('p')
            content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        
        # Strategy 2: Look for specific news site patterns
        if not content or len(content) < 100:
            # WSJ specific
            if 'wsj.com' in url:
                content_div = soup.find('div', {'class': 'article-content'})
                if content_div:
                    paragraphs = content_div.find_all('p')
                    content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            
            # ABC News specific
            elif 'abcnews.go.com' in url:
                content_div = soup.find('div', {'class': 'article-copy'})
                if content_div:
                    paragraphs = content_div.find_all('p')
                    content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        
        # Strategy 3: Fallback to body if no specific container found
        if not content or len(content) < 100:
            content_div = soup.body or soup
            paragraphs = content_div.find_all('p')
            content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        
        # Clean up the content
        if content:
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            content = re.sub(r'\n\s*\n', '\n\n', content)  # Normalize line breaks
            content = content.strip()
            
            # Remove common unwanted patterns
            content = re.sub(r'Click here to read more.*$', '', content, flags=re.IGNORECASE)
            content = re.sub(r'Subscribe to.*$', '', content, flags=re.IGNORECASE)
            content = re.sub(r'Sign up for.*$', '', content, flags=re.IGNORECASE)
            
            # If content is still too short, try getting all text
            if len(content) < 100:
                content = content_div.get_text(separator='\n', strip=True)
                content = re.sub(r'\s+', ' ', content)
                content = re.sub(r'\n\s*\n', '\n\n', content)
                content = content.strip()
        
        return content if content and len(content) > 100 else None
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            logger.warning(f"Authentication required for {url}")
        elif e.response.status_code == 403:
            logger.warning(f"Access forbidden for {url}")
        elif e.response.status_code == 404:
            logger.warning(f"Article not found at {url}")
        else:
            logger.warning(f"HTTP error for {url}: {str(e)}")
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request error for {url}: {str(e)}")
        return None
    except Exception as e:
        logger.warning(f"Could not fetch full content for {url}: {str(e)}")
        return None

def store_articles(api_articles):
    if not api_articles:
        logger.warning("No articles to store")
        return

    # Get or create categories
    categories = {
        'business': Category.objects.get_or_create(name="Business")[0],
        'politics': Category.objects.get_or_create(name="Politics")[0],
        'entertainment': Category.objects.get_or_create(name="Entertainment")[0],
        'environment': Category.objects.get_or_create(name="Environment")[0],
        'health': Category.objects.get_or_create(name="Health")[0],
        'science': Category.objects.get_or_create(name="Science")[0],
        'sports': Category.objects.get_or_create(name="Sports")[0],
        'technology': Category.objects.get_or_create(name="Technology")[0],
        'general': Category.objects.get_or_create(name="General")[0]
    }

    for item in api_articles:
        # Skip articles without required fields
        if not all(key in item for key in ['title', 'url']):
            logger.warning(f"Skipping article with missing required fields: {item.get('title', 'Unknown')}")
            continue

        # Initialize content from API
        content = item.get('content', '') or ''
        description = item.get('description', '') or ''

        # Try to fetch full content if API content is too short
        if len(content) < 100:
            full_content = get_full_article_content(item['url'])
            if full_content and len(full_content) > len(content):
                content = full_content

        # Fallback to description if content is still too short
        if len(content) < 100:
            content = description

        # Skip if no usable content
        if not content:
            logger.warning(f"Skipping article with no usable content: {item['title']}")
            continue

        # Clean up the content
        content = content.replace('…', '').replace('...', '').strip()
        
        # Determine category based on content and title
        text = (item['title'] + ' ' + content).lower()
        category = get_topic_for_text(text, categories)

        try:
            article, created = Article.objects.get_or_create(
                url=item['url'],
                defaults={
                    'title': item['title'],
                    'content': content,
                    'summary': description,
                    'image_url': item.get('urlToImage', ''),
                    'category': category,
                }
            )

            if created:
                enrich_article(article)
                logger.info(f"✅ Added and enriched: {article.title} (Category: {category.name})")
            else:
                logger.info(f"⏭ Already exists: {article.title}")

        except Exception as e:
            logger.error(f"Error storing article {item.get('title', 'Unknown')}: {str(e)}")

def recategorize_existing_articles():
    """Recategorize all existing articles"""
    logger.info("Starting article recategorization...")
    articles = Article.objects.all()
    topics = {
        'business': Category.objects.get_or_create(name="Business")[0],
        'politics': Category.objects.get_or_create(name="Politics")[0],
        'entertainment': Category.objects.get_or_create(name="Entertainment")[0],
        'environment': Category.objects.get_or_create(name="Environment")[0],
        'health': Category.objects.get_or_create(name="Health")[0],
        'science': Category.objects.get_or_create(name="Science")[0],
        'sports': Category.objects.get_or_create(name="Sports")[0],
        'technology': Category.objects.get_or_create(name="Technology")[0],
        'general': Category.objects.get_or_create(name="General")[0]
    }
    
    for article in articles:
        text = (article.title + ' ' + article.content).lower()
        article.category = get_topic_for_text(text, topics)
        article.save()
        logger.info(f"Recategorized: {article.title} -> {article.category.name}")
    
    logger.info("Article recategorization complete!")

def analyze_sentiment(text):
    """
    Simple sentiment analysis based on positive and negative word lists
    """
    positive_words = {'good', 'great', 'excellent', 'positive', 'success', 'win', 'happy', 'best', 'better', 'improve', 'up', 'rise', 'gain'}
    negative_words = {'bad', 'poor', 'negative', 'fail', 'loss', 'worst', 'worse', 'down', 'fall', 'decline', 'problem', 'issue', 'concern'}
    
    # Convert text to lowercase and split into words
    words = set(re.findall(r'\b\w+\b', text.lower()))
    
    # Count positive and negative words
    positive_count = len(words.intersection(positive_words))
    negative_count = len(words.intersection(negative_words))
    
    # Calculate sentiment score (-1 to 1)
    total = positive_count + negative_count
    if total == 0:
        return 0.0
    
    score = (positive_count - negative_count) / total
    return round(score, 3)

def get_readability_score(text):
    try:
        return round(textstat.flesch_reading_ease(text), 2)  # 0–100 scale
    except Exception as e:
        logger.error(f"❌ Readability analysis error: {str(e)}")
        return 50.0  # neutral fallback

def generate_summary(text, target_words=100):
    """Generate a summary with exactly target_words using LSA (Latent Semantic Analysis)"""
    try:
        # Create a parser
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        # Create stemmer
        stemmer = Stemmer("english")
        
        # Create summarizer
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        
        # Start with a reasonable number of sentences
        sentences_count = 5
        summary = summarizer(parser.document, sentences_count)
        summary_text = " ".join([str(sentence) for sentence in summary])
        
        # Count words in the summary
        word_count = len(summary_text.split())
        
        # Adjust number of sentences until we get close to target_words
        while word_count < target_words and sentences_count < len(parser.document.sentences):
            sentences_count += 1
            summary = summarizer(parser.document, sentences_count)
            summary_text = " ".join([str(sentence) for sentence in summary])
            word_count = len(summary_text.split())
        
        # If we have too many words, trim to exactly target_words
        if word_count > target_words:
            words = summary_text.split()
            summary_text = " ".join(words[:target_words])
        
        return summary_text
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return text[:200] + "..."  # Fallback to first 200 characters

def enrich_article(article):
    text = article.content or article.summary or ""
    article.sentiment = analyze_sentiment(text)
    article.reading_difficulty = get_readability_score(text)

    # Generate summary if none or too short (< 50 chars)
    if not article.summary or len(article.summary) < 50:
        try:
            # Clean and prepare text for summarization
            text = text.replace('\n', ' ').strip()
            # Remove extra spaces
            text = ' '.join(text.split())
            
            # Generate summary
            article.summary = generate_summary(text)
            logger.info(f"Generated summary for: {article.title}")
        except Exception as e:
            logger.error(f"Summarization failed for {article.title}: {str(e)}")
            # Fallback to description if summarization fails
            if not article.summary:
                article.summary = article.content[:200] + '...'

    article.save()
    logger.info(f"✨ Enriched: {article.title}")

class Command(BaseCommand):
    help = 'Fetches top headlines from News API and stores them in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recategorize',
            action='store_true',
            help='Recategorize existing articles'
        )

    def handle(self, *args, **options):
        if options['recategorize']:
            self.stdout.write("🔄 Recategorizing existing articles...")
            recategorize_existing_articles()
            self.stdout.write(self.style.SUCCESS("✅ Recategorization complete!"))
            return

        self.stdout.write("🚀 Fetching news...")
        articles = fetch_news_articles()
        
        if not articles:
            self.stdout.write(self.style.ERROR("❌ No articles fetched from NewsAPI"))
            return
            
        self.stdout.write(self.style.SUCCESS(f"📰 Retrieved {len(articles)} articles"))
        store_articles(articles)
        self.stdout.write(self.style.SUCCESS("✅ Done.")) 