import feedparser
import openai
import requests
from datetime import datetime
from bs4 import BeautifulSoup

openai.api_key='sk-proj-1DCgp9acoWkhtGFy0citT3BlbkFJlA4riT3ycrSYjY3eE53Z'

def extract_GPT_3(article_content):
    # prompt = f" Analyze the mentioned Professor from this link. \n\n{article_content} The result will be presented with the professor's name, position and a summary of the professor's content related to the news."
    prompt = f"Extract the name, position, and a summary of the content related to the professor from the following article.The result will be presented with  professor's name: , position: , and summary: .\n\n{article_content}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Extract professor information from news articles."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def extract_GPT_4(article_content):
    # prompt = f" Analyze the mentioned Professor from this link. \n\n{article_content} The result will be presented with the professor's name, position and a summary of the professor's content related to the news."
    prompt = f"Extract the name, position, and a summary of the content related to the professor from the following article.The result will be presented with  professor's name: , position: , and summary: .\n\n{article_content}"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "Extract professor information from news articles."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    author = soup.find('meta', attrs={'name': 'author'}) # get author
    author = author['content'] if author else 'No author' # check the author exist or not
    paragraphs = soup.find_all('p') # returns a list of all matching tags(the main textual content of the webpage)
    content = '\n'.join([p.text for p in paragraphs])# concatenates the text strings into a single string, with each paragraph separated by a newline character
    return content

def main():
    query = 'uiuc%20professor'
    #%20 mean empty space; uiuc%20-professor means uiuc exclude professor
    #uiuc%20when%3A1d%20-professor means uiuc exclude professor in past 24h/1d
    url = f'https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US%3Aen&oc=11&q={query}'
    feed = feedparser.parse(url)

    #sort the news by time
    news_items = []
    for entry in feed.entries:
        time = entry.published_parsed  # Published time in struct_time format
        pub_datetime = datetime(*time[:6])  # Convert to datetime object
        news_items.append((pub_datetime, entry))
    news_bytime = sorted(news_items, key=lambda x: x[0], reverse=True)

    num = 0
    for pub_time, article in news_bytime:
        if num < 5:
            print("\n")
            print("News number: ",num+1)
            print(f"Title: {article.title}")
            print(f"Published: {pub_time}")
            print(f"Link: {article.link}")
            print(f"Source: {article.source['title']}\n")
            num+=1
            # print(f"Description: {article.description}")
        else:
            break
        content=get_content(article.link)
        news_info = f"Title: {article.title}, Published: {article.published}, Link: {article.link},Source: {article.source['title']}, Content:{content}"
        professor_info_3 = extract_GPT_3(news_info)
        professor_info_4 = extract_GPT_4(news_info)
        print("gpt-3.5-turbo:\n",professor_info_3,"\n")
        print("gpt-4-turbo:\n",professor_info_4,"\n")
        print("----------------------------------------------------------------------------------------------------")
    # Check what is in news_bytime
    # at=3
    # for i in news_bytime:
    #     if(at>0):
    #         print("\n",i)
    #         at-=1

if __name__ == "__main__":
    main()


    