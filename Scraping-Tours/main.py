import requests
import selectorlib
import time
from send_email import send_email


url = "https://programmer100.pythonanywhere.com/tours/"

# Headers make the website think that the script is a browser
headers = HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=headers)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read():
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        content = read()

        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message=f"Hey, there is a new event: {extracted}")
        time.sleep(2)
