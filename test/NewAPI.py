import requests
from newsapi import NewsApiClient

NEWAPI_KEY = '1832c2de74754ce5a8bb056173a27b83'

query = 'uiuc'
url = f'https://newsapi.org/v2/everything?q={query}&sources=google-news&apiKey={NEWAPI_KEY}'
url = f'https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey=1832c2de74754ce5a8bb056173a27b83'
# https://newsapi.org/v2/everything?q=apple&from=2024-06-18&to=2024-06-18&sortBy=popularity&apiKey=1832c2de74754ce5a8bb056173a27b83

req = requests.get(url)
data = req.json()

if data['status'] == 'ok':
    for article in data['articles']:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}\n")
else:
    print("Failed")


# newsapi = NewsApiClient(api_key=NEWAPI_KEY)

# headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           sources='bbc-news,the-verge',
#                                           category='business',
#                                           language='en',
#                                           country='us')

# # everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2017-12-01',
#                                       to='2017-12-12',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)

#top-headlines/sources
# sources = newsapi.get_sources()