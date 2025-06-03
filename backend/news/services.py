from django.core.cache import cache
from .models import Article, CustomUser, Category
from django.db.models import Q
from datetime import datetime, timedelta
import newspaper

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

def fetch_articles():
    """Fetch articles for all categories using newspaper3k."""
    try:
        # Define news source URLs for scraping
        news_sources = [
            'https://www.bbc.com/news',
            'https://www.cnn.com',
            'https://www.reuters.com',
            'https://www.nytimes.com',
            'https://www.theguardian.com/international',
            # Add more sources as needed
        ]
        
        for source_url in news_sources:
            paper = newspaper.build(source_url, memoize_articles=False)
            for article in paper.articles[:5]:  # Limit to first 5 articles per source
                try:
                    article.download()
                    article.parse()
                    article.nlp()
                    
                    title = article.title
                    content = article.text
                    summary = article.summary
                    url = article.url
                    
                    if not title or not content or not url:
                        print(f"Skipping article with missing fields from {url}")
                        continue
                    
                    # Check if article with this URL already exists
                    if Article.objects.filter(url=url).exists():
                        print(f"Article with URL {url} already exists. Skipping.")
                        continue
                    
                    # Assign category as None or implement category mapping if needed
                    new_article = Article.objects.create(
                        title=title,
                        content=content,
                        summary=summary,
                        url=url,
                        category=None,
                        created_at=datetime.now()
                    )
                    print(f"Created article: {title}")
                except Exception as e:
                    print(f"Error processing article from {source_url}: {str(e)}")
                    
    except Exception as e:
        print(f"Error in fetch_articles: {str(e)}")
