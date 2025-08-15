import os
import requests
from django.utils.text import slugify
from django.utils.dateparse import parse_datetime
from dotenv import load_dotenv
from django.utils import timezone
from ..models import Article, Category, Topic

load_dotenv()  # Load .env variables

class NewsFetcher:
    def __init__(self, source="newsdata"):
        self.source = source
        self.api_keys = {
            "newsdata": os.getenv("NEWSDATA_API_KEY"),
            "newsapi": os.getenv("NEWSAPI_API_KEY"),
            "gnews": os.getenv("GNEWS_API_KEY")
        }

    def fetch_articles(self, query="Nigeria", language="en", country=None):
        if self.source == "newsdata":
            base_url = "https://newsdata.io/api/1/news"
            params = {
                "apikey": self.api_keys['newsdata'],
                "q": query,
                "language": language.lower() if language else None,
                "country": country.lower() if country else None,
            }
            
            # Remove None values from params
            params = {k: v for k, v in params.items() if v is not None}
            
            try:
                resp = requests.get(base_url, params=params)
                resp.raise_for_status()  # Raises HTTPError for bad responses
                data = resp.json()
                
                if data.get("status") == "error":
                    error_msg = data.get("results", {}).get("message", "Unknown NewsData API error")
                    raise ValueError(f"NewsData API error: {error_msg}")
                    
                return self._parse_articles(data)
                
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Request failed: {str(e)}")

        elif self.source == "newsapi":
            url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={self.api_keys['newsapi']}"

        elif self.source == "gnews":
            url = f"https://gnews.io/api/v4/search?q={query}&lang={language}"
            if country:
                url += f"&country={country}"
            url += f"&token={self.api_keys['gnews']}"

        else:
            raise ValueError("Unsupported news source")

        resp = requests.get(url)
        data = resp.json()

        # Log the request URL and raw response if something goes wrong
        if data.get("status") == "error":
            raise ValueError(f"NewsData API error: {data}")

        return self._parse_articles(data)



    def _parse_articles(self, data):
        articles = []
        if self.source == "newsdata":
            for item in data.get("results", []):
                articles.append({
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "summary": item.get("description", ""),
                    "published_at": timezone.make_aware(parse_datetime(item.get("pubDate"))) if item.get("pubDate") else None,
                    "source": item.get("source_id", ""),
                    "country": item.get("country", ""),
                    "image_url": item.get("image_url"),
                    "categories": item.get("category", []),
                    "content": item.get("content", ""),
                })
        elif self.source == "newsapi":
            for item in data.get("articles", []):
                articles.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "summary": item.get("description", ""),
                    "published_at": timezone.make_aware(parse_datetime(item.get("pubDate"))) if item.get("pubDate") else None,
                    "source": item.get("source", {}).get("name", ""),
                    "image_url": item.get("urlToImage"),
                    "categories": [],
                    "content": item.get("content", ""),
                })
        elif self.source == "gnews":
            for item in data.get("articles", []):
                articles.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "summary": item.get("description", ""),
                    "published_at": timezone.make_aware(parse_datetime(item.get("pubDate"))) if item.get("pubDate") else None,
                    "source": item.get("source", {}).get("name", ""),
                    "image_url": item.get("image"),
                    "categories": [],
                    "content": item.get("content", ""),
                })
        return articles

    def save_articles(self, articles):
        for a in articles:
            if not Article.objects.filter(url=a["url"]).exists():
                article = Article.objects.create(
                    title=a["title"],
                    slug=slugify(a["title"]),
                    url=a["url"],
                    summary=a["summary"],
                    published_at=a["published_at"],
                    source=a["source"],
                    image_url=a["image_url"],
                    content=a["content"],
                )
                for cat_name in a.get("categories", []):
                    category, _ = Category.objects.get_or_create(name=cat_name)
                    article.categories.add(category)
