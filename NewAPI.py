import requests

NEWAPI_KEY = '1832c2de74754ce5a8bb056173a27b83'
query = 'uiuc'
url = f'https://newsapi.org/v2/everything?q={query}&sources=google-news&apiKey={NEWAPI_KEY}'

req = requests.get(url)
data = req.json()

if data['status'] == 'ok':
    for article in data['articles']:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}\n")
else:
    print("Failed")