import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import NEWS_API_KEY

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news,cnn&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    return [article["title"] for article in response["articles"]]

if __name__ == "__main__":
    for news in get_news():
        print(news)
