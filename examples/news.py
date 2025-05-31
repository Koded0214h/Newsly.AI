import requests

def fetch_news_articles():
    API_KEY = '4f9ba8d377d242d1b8b643eae88e15a6'  # Replace with your actual key
    url = f'https://newsapi.org/v2/top-headlines?language=en&pageSize=20&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print("❌ Error:", response.status_code, response.text)
        return []
