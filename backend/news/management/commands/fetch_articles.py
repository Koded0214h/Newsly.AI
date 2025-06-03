import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
import logging
from newspaper import Article as NewsArticle
from django.core.management.base import BaseCommand
from news.models import Article, Category
from django.conf import settings
import time
from datetime import datetime, timedelta
import json
from django.utils import timezone


logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

session = requests.Session()
session.headers.update(HEADERS)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def fetch_news_articles(sources):
    articles = []
    for source in sources:
        try:
            response = session.get(source, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "xml")
            for item in soup.find_all("item"):
                title = item.find("title").text if item.find("title") else ""
                link = item.find("link").text if item.find("link") else ""
                pub_date = item.find("pubDate").text if item.find("pubDate") else ""
                description = item.find("description").text if item.find("description") else ""
                if not link or not link.startswith("http"):
                    logger.warning(f"Skipping article with invalid link: {link}")
                    continue
                articles.append({
                    "title": title,
                    "link": link,
                    "pub_date": pub_date,
                    "description": description
                })
        except Exception as e:
            logger.error(f"Error fetching from {source}: {e}")
    return articles

def get_full_article_content(url):
    if not url or not url.startswith("http"):
        logger.warning(f"Skipping invalid URL for content fetch: {url}")
        return ""
    try:
        article = NewsArticle(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logger.warning(f"Newspaper3k failed, falling back to BeautifulSoup: {e}")
        try:
            response = session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            return " ".join(p.get_text() for p in paragraphs)
        except Exception as e:
            logger.error(f"Error parsing with BeautifulSoup: {e}")
            return ""

def generate_summary(content):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                {"role": "user", "content": f"Summarize this article:\n\n{content}"}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return ""

def enrich_article(article):
    try:
        content = get_full_article_content(article["link"])
        summary = generate_summary(content) if content else article.get("description", "")
        return {
            **article,
            "content": content,
            "summary": summary,
            "sentiment": "neutral",
            "readability": "N/A"
        }
    except Exception as e:
        logger.error(f"Error enriching article {article['link']}: {e}")
        return article

def process_single_article(article):
    return enrich_article(article)

def store_articles(articles, max_workers=5):
    seen_links = set()
    filtered_articles = [a for a in articles if a["link"] not in seen_links and not seen_links.add(a["link"])]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single_article, filtered_articles))
    return results

class Command(BaseCommand):
    help = 'Fetch news articles using OpenAI'

    def handle(self, *args, **kwargs):
        try:
            categories = Category.objects.all()

            for category in categories:
                try:
                    recent_articles = Article.objects.filter(
                        category=category,
                        created_at__gte=timezone.now() - timedelta(hours=24)
                    ).count()

                    if recent_articles >= 5:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Category {category.name} already has recent articles'
                            )
                        )
                        continue

                    article = self.generate_news_content(category)
                    if article:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully created article for category {category.name}'
                            )
                        )

                    time.sleep(2)

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error processing category {category.name}: {str(e)}'
                        )
                    )
                    continue

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in fetch_articles command: {str(e)}')
            )

    def generate_news_content(self, category):
        try:
            prompt = f"""Generate a news article about {category.name}. 
            The article should be informative, engaging, and well-structured.
            Include a title, content, and a brief summary.
            Format the response as JSON with the following structure:
            {{
                "title": "Article Title",
                "content": "Article Content",
                "summary": "Brief Summary"
            }}"""

            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a news article generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            article_data = json.loads(response.choices[0].message.content.strip())
            if not article_data or not isinstance(article_data, dict):
                self.stdout.write(
                    self.style.ERROR('Invalid response format from OpenAI')
                )
                return None

            article = Article.objects.create(
                title=article_data.get('title', ''),
                content=article_data.get('content', ''),
                summary=article_data.get('summary', ''),
                category=category
            )

            return article

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating article: {str(e)}')
            )
            return None