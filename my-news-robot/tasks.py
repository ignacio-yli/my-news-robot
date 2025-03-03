from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from openai import OpenAI
import email_task
browser = Selenium()

from RPA.Browser.Selenium import Selenium
from robocorp.tasks import task

browser = Selenium()

@task
def minimal_task():
    open_browser()
    articles = extract_articles()
    email_task.send_email("vitafull96@gmail.com", articles)
    close_browser()

def open_browser():
    browser.open_available_browser("https://www.sciencedaily.com/")

def close_browser(): 
    browser.close_all_browsers()


#This function visits the webpage of ScienceDaily and extracts info from their Top News section.
def extract_articles():
    try:
        article_containers = browser.find_elements("css:div#science_heroes div.col-md-6")
        articles = []

        for container in article_containers:
            try:
                title_element = browser.find_element("css:div.latest-head a", container)
                date_element = browser.find_element("css:span.story-date", container)
                article_text = extract_article_text(title_element.get_attribute('href'))

                if article_text:
                    review = review_scientific_article(article_text)
                    
                    article = {
                        'title': title_element.text,
                        'link': title_element.get_attribute('href'),
                        'date': clean_string(date_element.text),
                        'text': article_text,
                        'review': review  
                    }
                    articles.append(article)
                else:
                    error_catcher(e)
                    print(f"Failed to extract text for article: {title_element.text}")

            except Exception as article_error:
                error_catcher(e)
                print(f"Error extracting article details: {article_error}")

        return articles

    except Exception as e:
        print(f"Error in extract_articles: {e}")
        error_catcher(e)
        return []

#This function cleans up the date extracted from the article.
def clean_string(str):
    str.replace('�', '').strip()
    str.replace("—", "")
    return str

#This function extracts the text from the article. 
def extract_article_text(url):
    try:
        browser.open_available_browser(url)
   
        browser.wait_until_element_is_visible("css:div#text", timeout=10)
        
        paragraphs = browser.find_elements("css:div#text p") 
     
        article_text = "\n\n".join([p.text for p in paragraphs])
        
        return article_text
    
    except Exception as e:
        print(f"Error extracting the article text: {e}")
        error_catcher(e)
        return None
    
    finally:
        browser.close_browser()


#this function takes the article to OpenAI to review it for the user. the key is written down here because it has restrictions of use and it is only 
#for academic purposes. In a real life scenario I would hide it.
def review_scientific_article(text):
    try:
        client = OpenAI(api_key="sk")
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a scientific article reviewer. Read and make a short(max 80 words) truthful pitch."},
                {"role": "user", "content": text}
            ]
        )
        
        message = completion.choices[0].message.content
        return message
    
    except Exception as e:
        print(f"An error occurred: {e}")
        error_catcher(e)

def error_catcher(e):
        email_task.send_error_email(e)
