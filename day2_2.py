#
# crear entorno
#   >python -m venv miEntorno 
#   >pip install -r requirements.txt


# activar entorno desde power shell  o desde el terminal
#   >miEntorno\Scripts\activate
#   >cd weekk1 
#   >py day1.ph          


# programa para analizar el resultado de una web
# con OLLAMA



import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import markdown
import webbrowser
 



# Constants
#OLLAMA_API = "http://192.168.1.56:11434/api/chat"
OLLAMA_API = "http://127.0.0.1:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"



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
 

def messages(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def messages_for(website):
    return {
            "model": MODEL,
            "messages": messages(website),
            "stream": False
        }





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

 


def display_summary(url):
    website = Website(url)
    payload = messages_for(website)     
    response = requests.post(
            OLLAMA_API, 
            json=payload, 
            headers=HEADERS
    )    
    devuelve = response.json()['message']['content']
    html = markdown.markdown(devuelve)
    with open("output_ollama.html", "w") as f:
        f.write(html)
    webbrowser.open("output_ollama.html")




#display_summary("https://edwarddonner.com")
#display_summary("https://www.rtve.es/noticias/")
display_summary("https://www.alcaide.info/")

 