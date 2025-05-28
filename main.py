import time
import smtplib
import environ
import requests

from dotenv import load_dotenv

from bs4 import BeautifulSoup, Tag, NavigableString

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import List, Tuple, Any

load_dotenv()

env = environ.Env()

website_urls: List[str] = env.get_value("WEBSITE_URLS").split(",")
email = env.get_value("EMAIL_FROM")
emails_to = env.get_value("EMAILS_TO")
password = env.get_value("PASSWORD")
target_strings: List[str] = env.get_value("TARGET_STRINGS").split(",")
sleep_time: int = env.get_value("SLEEP_TIME", int) 
sleep_time_after_detection: int = env.get_value("SLEEP_TIME_AFTER_DETECTION", int)
class_or_id = env.get_value("CLASS_OR_ID")

from threading import Thread

class Crawler(Thread):

    def __init__(self, *, url, target_string):
        self.found = False
        self.url = url
        self.target_string = target_string
        self.current_content = "first"
        Thread.__init__(self)
    
    def run(self):
        while True:
            print(f"{self.url} - Scraping...")
            try:
                res = self.scrap()
                result: str = "".join(str(element) for element in res)
            except:
                result: str = ""

            if self.current_content != "first":
                print(f"{self.url} - Checking for changes...")
                changed: bool = self.has_chaged(result=result)

                if changed:
                    print(f"{self.url} - Changes found!")
                    print(f"{self.url} - Sending emails...")
                    sent = self.send_email(result)

                    if sent:
                        print(f"{self.url} - Emails sent.")
                        self.found=True
                else:
                    print(f"{self.url} - No changes detected.")
            self.current_content = result
            self.sleep()

    def scrap(self) ->  (Tag | NavigableString | None):
        content = requests.get(self.url, verify=False)
        soup = BeautifulSoup(content.text, features="html.parser")

        if class_or_id=="class":
            return soup.find_all(class_=self.target_string)
        else:
            return soup.find_all(id_=self.target_string)

    def has_chaged(self, result: str) -> bool:
        return result != self.current_content 
    
    def send_email(self, result)-> bool:
        msg= MIMEMultipart()

        msg["From"] = email
        msg["Subject"] = "CRAWLER - Update detected."
        msg["To"] = emails_to.replace(",", ", ")

        msg.attach(MIMEText(self.get_message(result=result), "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email, password)
                server.sendmail(email, emails_to.split(","), msg.as_string())
            return True
        except Exception as e:
            print(f"{self.url} - Error: {e}")
            return False
    
    def get_message(self, result: str) -> str:
        return f"The following update was detected on the website {self.url}: \n Old: \n {self.current_content} \n New: \n {result}."
    
    def sleep(self) -> None:
        if self.found:
            print(f"{self.url} - Sleeping for {sleep_time_after_detection} seconds...")
            time.sleep(sleep_time_after_detection)
            self.current_content="first"
            self.found=False

        else:
            print(f"{self.url} - Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)

    def get_config(self) -> Tuple[str, str]:
        return self.url, self.target_string

if __name__=="__main__":
    if len(website_urls) != len(target_strings):
        raise ValueError()

    crawlers: List[Crawler] = []

    for i,website in enumerate(website_urls):
        crawler = Crawler(url=website, target_string=target_strings[i])

        crawlers.append(crawler)

        crawler.start()

    while True:
        for i,crawler in enumerate(crawlers):
            if not crawler.is_alive():
                url, target_string = crawler.get_config()

                crawlers.remove(crawler)

                new_crawler = Crawler(url=url, target_string=target_string)

                crawlers.append(new_crawler)

                new_crawler.start()

                break
