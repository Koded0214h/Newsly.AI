import requests
from decouple import config

API_KEY = config("NEWS_API_KEY")
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "category": "technology",
    "apiKey": API_KEY
}

res = requests.get(url, params=params)
print(res.json())


from core.models import Topic

interests = [
    "Technology",
    "Science & Space",
    "Health & Medicine",
    "Environment & Climate",
    "Politics & Government",
    "Economy & Finance",
    "Sports",
    "Entertainment & Celebrity",
    "Culture & Lifestyle",
    "Education & Learning",
    "World Affairs",
    "Crime & Law",
    "Business & Startups",
    "Travel & Exploration",
    "Food & Culinary"
]

for interest_name in interests:
    obj, created = Topic.objects.get_or_create(name=interest_name)
    if created:
        print(f"Created topic: {interest_name}")
    else:
        print(f"Topic already exists: {interest_name}")

print("✅ Interest seeding complete!")
