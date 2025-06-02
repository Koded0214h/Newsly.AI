import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import openai
import logging
import time
from newspaper import Article

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

session = requests.Session()
session.headers.update(HEADERS)

def fetch_news_articles(sources):
    articles = []
    for source in sources:
        try:
            response = session.get(source)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            for item in soup.find_all("item"):
                title = item.find("title").text if item.find("title") else ""
                link = item.find("link").text if item.find("link") else ""
                pub_date = item.find("pubDate").text if item.find("pubDate") else ""
                description = item.find("description").text if item.find("description") else ""
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
    try:
        article = Article(url)
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a summarization bot."},
                {"role": "user", "content": f"Summarize this article: {content}"},
            ],
            max_tokens=300
        )
        return response.choices[0].message['content'].strip()
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
    results = []
    seen_links = set()
    articles = [a for a in articles if a["link"] not in seen_links and not seen_links.add(a["link"])]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single_article, articles))
    return results

def generate_news_content(categories):
    try:
        prompt = f"Generate engaging news content on the following categories: {', '.join(categories)}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a journalist."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logger.error(f"Error generating news content: {e}")g
        return ""


