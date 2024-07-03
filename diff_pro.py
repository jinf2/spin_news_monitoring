import feedparser
import openai
import requests
from datetime import datetime
from bs4 import BeautifulSoup

openai.api_key=''

def extract_GPT_diff(article_content):
    prompt = f"Extract the name, position, and a summary of the content related to the professor from the following article.  and separate them by school. The result will be presented with professor's name:, position:, and summary:\n\n{article_content}"
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
    lists = soup.find_all(['ul', 'ol']) #Extract bulleted and numbered lists(unordered list and ordered list)
    list_content = []
    for line in lists:
        items = line.find_all('li') #find all list item
        list_content.append('\n'.join([f"{item.text}" for item in items]))
    full_content = content+'\n\n'+'\n\n'.join(list_content)
    return full_content

def diff_art(url):
    news_content=get_content(url)
    result=extract_GPT_diff(news_content)
    return result

def main():
    news = 'https://theconversation.com/should-ai-be-permitted-in-college-classrooms-4-scholars-weigh-in-212176'
    result=diff_art(news)
    print(result)
    print("----------------------------------------------------------------------------------------------------")
    

if __name__ == "__main__":
    main()


    