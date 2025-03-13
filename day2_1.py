import os
import webbrowser
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI
import markdown 


# programa PYTHON 3.12.0 para analizar el resultado de una web

load_dotenv(override=True)
# necesitamos un archivo .env con la siguiente línea, el Api Key creado desde tu sesión de https://platform.openai.com/docs/overview
# OPENAI_API_KEY=xxxxxxxxx
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

openai = OpenAI()

#
#
system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}. "
    user_prompt += "The contents of this website is as follows;"
    user_prompt += "please provide a short summary of this website in markdown. "
    user_prompt += "If it includes news or announcements, then summarize these too."
    user_prompt += "I need it in spanish language."
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

        # titulos = soup.find('span', class_='maintitle').text  # para sacar <span class="maintitle">xxx</span>
        # titulos = soup.find('span', id='descuento').text

        # imprimir
        #todos_spans = soup.find_all('span', class_='maintitle') 
        #for span in todos_spans:
        #    print(span.text)


def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    # solo jupiter lab: display(Markdown(summary))
    html = markdown.markdown(summary)
    #print(html)
    with open("output.html", "w") as f:
        f.write(html)
    webbrowser.open("output.html")

display_summary("https://www.alcaide.info/")
