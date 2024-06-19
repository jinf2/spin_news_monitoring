import feedparser

url = 'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US%3Aen&oc=11&q=uiuc%20professor'

feed = feedparser.parse(url)

num = 0
for article in feed.entries:
    print(f"Title: {article.title}")
    print(f"Published: {article.published}")
    print(f"Link: {article.link}")
    print(f"source: {article.source['title']}\n")
    # print(f"Description: {article.description}")
    if num > 5:
        break
    else:
        num+=1
    