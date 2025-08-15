from ..models import CustomUser
from ..services.news_fetcher import NewsFetcher

def fetch_news_for_all_users():
    for user in CustomUser.objects.all():
        interests = user.interests.all()
        country = getattr(user, "preferred_country", None)
        fetcher = NewsFetcher()
        
        # Fetch for each interest
        for interest in interests:
            fetcher.fetch_and_save(interest.name, language="en", country=country)
            fetcher.fetch_and_save(interest.name, language="en", country=None)
        
        # Fetch global topics
        global_topics = ["world", "technology", "science"]
        for topic in global_topics:
            fetcher.fetch_and_save(topic, language="en", country=None)