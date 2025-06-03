import feedparser
from newspaper import Article as NPArticle
from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
from datetime import datetime, timedelta

def get_user_feed(user, toggle='breaking'):
    """
    Get personalized feed for a user based on their interests and preferences.
    """
    try:
        interests = user.interests.all()
        articles = Article.objects.filter(
            Q(category__in=interests) | Q(category__isnull=True)
        ).order_by('-created_at')
        return articles
    except Exception as e:
        print(f"Error in get_user_feed: {str(e)}")
        return []

def fetch_articles():
    """Fetch articles using feedparser and newspaper3k."""
    try:
        rss_feeds = [
            'http://feeds.bbci.co.uk/news/rss.xml',
            'http://rss.cnn.com/rss/edition.rss',
            'http://feeds.reuters.com/reuters/topNews',
            'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'https://www.theguardian.com/world/rss',
        ]

        for feed_url in rss_feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:  # Limit to first 5 entries per feed
                url = entry.link
                title = entry.title
                published = getattr(entry, 'published', None)
                summary = getattr(entry, 'summary', '')

                if Article.objects.filter(url=url).exists():
                    print(f"Article with URL {url} already exists. Skipping.")
                    continue

                # Fetch full article content using newspaper3k
                try:
                    article = NPArticle(url)
                    article.download()
                    article.parse()
                    content = article.text
                    image_url = article.top_image if article.top_image else ''
                except Exception as e:
                    print(f"Failed to fetch full article content for {url}: {e}")
                    content = summary  # fallback to summary
                    image_url = ''

                if not title or not content or not url:
                    print(f"Skipping article with missing fields: {url}")
                    continue

                Article.objects.create(
                    title=title,
                    content=content,
                    summary=summary,
                    url=url,
                    image_url=image_url,
                    category=None,
                    created_at=datetime.now()
                )
                print(f"Created article: {title}")

    except Exception as e:
        print(f"Error in fetch_articles: {str(e)}")

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
