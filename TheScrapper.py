import requests

from modules.scrapper import Scrapper
from modules.info_reader import InfoReader

banner = """
▄▄▄█████▓ ██░ ██ ▓█████   ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███   ██▓███  ▓█████  ██▀███  
▓  ██▒ ▓▒▓██░ ██▒▓█   ▀ ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▒ ▓██░ ▒░▒██▀▀██░▒███   ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄   ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
  ▒██▒ ░ ░▓█▒░██▓░▒████▒▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
  ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
    ░     ▒ ░▒░ ░ ░ ░  ░░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░     ░▒ ░      ░ ░  ░  ░▒ ░ ▒░
  ░       ░  ░░ ░   ░   ░  ░  ░  ░          ░░   ░   ░   ▒   ░░       ░░          ░     ░░   ░ 
          ░  ░  ░   ░  ░      ░  ░ ░         ░           ░  ░                     ░  ░   ░     
                                 ░                                                            
                                  
"""
print(banner +
      "*" * 40 + "\n" + "This tool will scrape emails\nand social media accounts." + "\n" + "*" * 40 +
      "\n")
main_url = input("Enter the URL of the website:")
other_urls = input("Enter other URLS like the imprint in this format: (URL1, URL2, URL3, ...): ")

urls = [main_url]
if other_urls != "":
    [urls.append(u) for u in other_urls.split(",")]
contents = [requests.get(u).text for u in urls]
cleaned_contents = Scrapper(urls=urls).getText()
urls = Scrapper(contents=contents, urls=[main_url]).getURLs()
IR = InfoReader(content={"text": cleaned_contents, "urls": urls})
emails = IR.getEmails()
# numbers = IR.getPhoneNumber()
sm = IR.getSocials()
print("\n")
print("E-Mails: " + ", ".join(emails))
# print("Numbers:" + ", ".join(numbers))
print("SocialMedia: " + ", ".join(sm))
