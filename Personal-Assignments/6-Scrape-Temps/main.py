import requests
import selectorlib
from datetime import datetime
import sqlite3


url = "https://programmer100.pythonanywhere.com/"

# Headers make the website think that the script is a browser
headers = HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("data.db")

def scrape(url):
    response = requests.get(url, headers=headers)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temps"]
    return value

def store(extracted):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")  # Date and time in "YYYY-MM-DD HH:MM:SS" format
    extracted = int(extracted)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temps VALUES(?,?)", (date_str, extracted))
    connection.commit()

if __name__ == "__main__":
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        store(extracted)
