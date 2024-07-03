import feedparser
import openai
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    author = soup.find('meta', attrs={'name': 'author'}) # get author
    author = author['content'] if author else 'No author' # check the author exist or not
    paragraphs = soup.find_all('p') # returns a list of all matching tags(the main textual content of the webpage)
    content = '\n'.join([p.text for p in paragraphs])# concatenates the text strings into a single string, with each paragraph separated by a newline character
    lists = soup.find_all(['ul', 'ol']) #Extract bulleted and numbered lists(unordered list and ordered list)
    list_content = []
    for line in lists:
        items = line.find_all('li') #find all list item
        list_content.append('\n'.join([f"{item.text}" for item in items]))
    full_content = content+'\n\n'+'\n\n'.join(list_content)
    return full_content

def main():
    url = 'https://news.google.com/rss/articles/CBMiLmh0dHBzOi8vYmxvZ3MuaWxsaW5vaXMuZWR1L3ZpZXcvNjc1OC85MTA4MTgzOTfSAQA?oc=5'
    content=get_content(url)
    print("----------------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()