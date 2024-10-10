import requests
import selectorlib
import time
import sqlite3
from send_email import send_email


url = "https://programmer100.pythonanywhere.com/tours/"

# Headers make the website think that the script is a browser
headers = HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, url):
        """Scrape the page source from the URL"""
        response = requests.get(url, headers=headers)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Database:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(url)
        extracted = event.extract(scraped)

        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            row = database.read(extracted)
            if not row: # this line means "if the row is not present in the db", because read will return an empty list
                        # if row not present and [] = False, where if the list exist [1,2] = True;
                        # so 'not row' = 'not True', or in other words, false, or empty
                database.store(extracted)
                send_email(message=f"Hey, there is a new event: {extracted}")
        time.sleep(2)
