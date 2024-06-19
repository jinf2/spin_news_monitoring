# from openai import OpenAI
import openai
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import re

GN_API = 'AIzaSyDbkPjuqmmcAp5Xa8-IkBtQXW87beEJEQ8'
CSE_ID = 'b1edb08f8728642a2'
openai.api_key='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'

def get_news(query, num_results=3, time_range=None):
    news_service = build('customsearch', 'v1', developerKey=GN_API)
    search_rest = {
        'q': query,
        'cx': CSE_ID,
        'num': num_results, 
        'lr': 'lang_en',  ## Language should be use in English
        'sort': 'date', 
        'dateRestrict' : time_range,## Limit the search for news events that appear
    }
    result = news_service.cse().list(**search_rest).execute()
    return result.get('items', [])

def extract_GPT(article_content):
    # prompt = f" Analyze the mentioned Professor from this link. \n\n{article_content} The result will be presented with the professor's name, position and a summary of the professor's content related to the news."
    prompt = f"Extract the name, position, and a summary of the content related to the professor from the following article:\n\n{article_content} The result will be presented with the professor's name, position and a summary of the professor's content related to the news."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Extract professor information from news articles."},
                  {"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def main():
    query = 'UIUC professor'
    # related to UIUC but exclude "word"
    # query = 'UIUC -word'

    ## eg. for one year
    # current_time = datetime.today()
    # past_time = current_time - timedelta(days=365)
    # date = f'y{current_time.year - past_time.year}'
    ## eg. for one week
    # date = 'w1' 
    ## eg. for 3 days
    # date = 'd3' 
    
    articles = get_news(query, time_range=None)

    for article in articles:
        title = article.get('title')
        snippet = article.get('snippet')
        link = article.get('link')
        print(f"\nTitle: {title}\n Snippet: {snippet}\n Link: {link}\n")
        news_info = f"Link: {link}"

        professor_info = extract_GPT(news_info)
        print(f"Professor Info:\n",professor_info)
        
        # print(f"Title: {title}")
        # print(f"Professor Info: {professor_info}")
        # print(f"Link: {link}\n")

if __name__ == "__main__":
    main()

