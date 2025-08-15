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
