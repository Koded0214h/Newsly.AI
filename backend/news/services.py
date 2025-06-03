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
                except Exception as e:
                    print(f"Failed to fetch full article content for {url}: {e}")
                    content = summary  # fallback to summary

                if not title or not content or not url:
                    print(f"Skipping article with missing fields: {url}")
                    continue

                Article.objects.create(
                    title=title,
                    content=content,
                    summary=summary,
                    url=url,
                    category=None,
                    created_at=datetime.now()
                )
                print(f"Created article: {title}")

    except Exception as e:
        print(f"Error in fetch_articles: {str(e)}")
