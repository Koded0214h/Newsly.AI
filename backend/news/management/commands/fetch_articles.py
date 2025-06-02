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
from datetime import datetime, timedelta
import openai
import json
from circuitbreaker import circuit
import psutil
from django.db import transaction
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configure logging
logger = logging.getLogger(__name__)

# Topic keywords mapping remains the same
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

def check_system_resources():
    """Check if system has enough resources to proceed"""
    mem = psutil.virtual_memory()
    if mem.percent > 90:
        logger.warning("High memory usage detected (%d%%)", mem.percent)
        return False
    return True

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

@circuit(failure_threshold=3, recovery_timeout=60)
def fetch_news_articles():
    if not check_system_resources():
        return []
        
    if settings.DEBUG:
        logger.info(f"Full NewsAPI key: {settings.NEWS_API_KEY}")
    else:
        logger.info(f"Using NewsAPI key: {settings.NEWS_API_KEY[:5]}...")
    
    api_key = settings.NEWS_API_KEY
    if not api_key:
        logger.error("NEWS_API_KEY not found in settings!")
        return []
    
    try:
        with requests.Session() as session:
            session.timeout = 10
            url = f'https://newsapi.org/v2/top-headlines?language=en&pageSize=20&apiKey={api_key}'
            response = session.get(url)
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
    """Fetch the full article content with improved error handling"""
    if not check_system_resources():
        return None
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        url = url.replace('\\u003d', '=').replace('\\/', '/')
        
        with requests.Session() as session:
            session.timeout = 15
            response = session.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'meta', 'link', 'noscript', 'iframe', 'picture', 'svg', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Content extraction strategies
            content = None
            strategies = [
                lambda: soup.find('article'),
                lambda: soup.find('main'),
                lambda: soup.find('div', class_=re.compile(r'article|content|story|post|entry|main', re.I)),
                lambda: soup.body
            ]
            
            for strategy in strategies:
                if content and len(content) > 100:
                    break
                try:
                    container = strategy()
                    if container:
                        paragraphs = container.find_all('p')
                        content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                except Exception:
                    continue
            
            if content:
                content = re.sub(r'\s+', ' ', content)
                content = re.sub(r'\n\s*\n', '\n\n', content).strip()
                content = re.sub(r'(Click here to read more|Subscribe to|Sign up for).*$', '', content, flags=re.IGNORECASE)
                
                if len(content) < 100:
                    content = container.get_text(separator='\n', strip=True)
                    content = re.sub(r'\s+', ' ', content).strip()
                
                return content if len(content) > 100 else None
                
        return None
        
    except requests.exceptions.HTTPError as e:
        logger.warning(f"HTTP error for {url}: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request error for {url}: {str(e)}")
    except Exception as e:
        logger.warning(f"Error processing {url}: {str(e)}")
    return None

def store_articles(api_articles):
    if not api_articles or not check_system_resources():
        logger.warning("No articles to store or insufficient resources")
        return

    # Get or create categories
    categories = {
        name.lower(): Category.objects.get_or_create(name=name)[0]
        for name in TOPIC_KEYWORDS.keys()
    }
    categories['general'] = Category.objects.get_or_create(name="General")[0]

    # Process articles in parallel with thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for item in api_articles:
            if not all(key in item for key in ['title', 'url']):
                logger.warning("Skipping article with missing fields: {item.get('title', 'Unknown')}")
                continue
                
            futures.append(executor.submit(process_single_article, item, categories))
        
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    logger.info(f"Processed article: {result}")
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}")

def process_single_article(item, categories):
    """Process a single article in a thread-safe manner"""
    try:
        with transaction.atomic():
            content = item.get('content', '') or ''
            description = item.get('description', '') or ''

            if len(content) < 100:
                full_content = get_full_article_content(item['url'])
                if full_content and len(full_content) > len(content):
                    content = full_content

            if len(content) < 100:
                content = description

            if not content:
                logger.warning(f"Skipping article with no content: {item['title']}")
                return None

            content = content.replace('…', '').replace('...', '').strip()
            text = (item['title'] + ' ' + content).lower()
            category = get_topic_for_text(text, categories)

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
                return f"✅ Added: {article.title} (Category: {category.name})"
            else:
                return f"⏭ Exists: {article.title}"

    except Exception as e:
        logger.error(f"Error storing article {item.get('title', 'Unknown')}: {str(e)}")
        return None

def enrich_article(article):
    """Enrich article with additional metadata"""
    try:
        text = article.content or article.summary or ""
        article.sentiment = analyze_sentiment(text)
        article.reading_difficulty = get_readability_score(text)

        if not article.summary or len(article.summary) < 50:
            text = text.replace('\n', ' ').strip()
            text = ' '.join(text.split())
            
            try:
                article.summary = generate_summary(text)
                logger.info(f"Generated summary for: {article.title}")
            except Exception as e:
                logger.error(f"Summarization failed for {article.title}: {str(e)}")
                if not article.summary:
                    article.summary = article.content[:200] + '...'

        article.save()
        logger.info(f"✨ Enriched: {article.title}")
    except Exception as e:
        logger.error(f"Error enriching article {article.title}: {str(e)}")

@circuit(failure_threshold=2, recovery_timeout=120)
def generate_news_content(category):
    """Generate news content with circuit breaker and proper error handling"""
    if not check_system_resources():
        logger.warning("Skipping generation due to resource constraints")
        return None

    try:
        client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=30.0  # Overall timeout
        )
        
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
        
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using faster model
            messages=[
                {"role": "system", "content": "You are a professional news writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            timeout=20.0  # Request timeout
        )
        
        logger.info(f"OpenAI API call took {time.time() - start_time:.2f} seconds")
        
        try:
            content = response.choices[0].message.content
            article_data = json.loads(content.strip())
            
            if not all(k in article_data for k in ['title', 'content', 'summary']):
                raise ValueError("Missing required fields in OpenAI response")
                
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            url = f"https://newsly.ai/articles/{category.name.lower()}/{timestamp}"
            
            with transaction.atomic():
                article = Article.objects.create(
                    title=article_data['title'],
                    content=article_data['content'],
                    summary=article_data['summary'],
                    url=url,
                    category=category,
                    created_at=timezone.now(),
                    is_ai_generated=True
                )
                enrich_article(article)
                return article
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from OpenAI")
        except ValueError as e:
            logger.error(f"Invalid response format: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing OpenAI response: {str(e)}")
            
    except openai.APITimeoutError:
        logger.error("OpenAI API timeout")
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in generate_news_content: {str(e)}")
        
    return None

class Command(BaseCommand):
    help = 'Fetches news articles using OpenAI'

    def handle(self, *args, **kwargs):
        try:
            # Get all categories
            categories = Category.objects.all()
            
            # Generate articles for each category
            for category in categories:
                # Check if we need to generate new articles
                last_article = Article.objects.filter(category=category).order_by('-created_at').first()
                
                if not last_article or (timezone.now() - last_article.created_at) > timedelta(hours=24):
                    # Generate new article
                    article = self.generate_news_content(category)
                    if article:
                        self.stdout.write(self.style.SUCCESS(f'Generated new article for {category.name}: {article.title}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Failed to generate article for {category.name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in fetch_articles: {str(e)}'))

    def generate_news_content(self, category):
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
            
            You must respond with a valid JSON object in this exact format:
            {{
                "title": "article headline",
                "content": "full article content",
                "summary": "brief summary"
            }}
            
            Do not include any text before or after the JSON object. The response must be a valid JSON object that can be parsed directly.
            """
            
            # Generate content using OpenAI
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a professional news writer. Write realistic, engaging news articles. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={ "type": "json_object" }
            )
            
            # Parse the response
            content = response.choices[0].message.content.strip()
            
            # Log the raw response for debugging
            self.stdout.write(f"Raw response: {content}")
            
            try:
                import json
                article_data = json.loads(content)
                
                # Validate required fields
                required_fields = ['title', 'content', 'summary']
                if not all(field in article_data for field in required_fields):
                    raise ValueError(f"Missing required fields in response. Got: {list(article_data.keys())}")
                
                # Create a unique URL (using timestamp and category)
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                url = f"https://newsly.ai/articles/{category.name.lower()}/{timestamp}"
                
                # Create the article
                article = Article.objects.create(
                    title=article_data['title'],
                    content=article_data['content'],
                    summary=article_data['summary'],
                    url=url,
                    category=category,
                    created_at=timezone.now()
                )
                
                return article
                
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'Invalid JSON response: {str(e)}'))
                self.stdout.write(self.style.ERROR(f'Raw content: {content}'))
                return None
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating news content: {str(e)}'))
            return None