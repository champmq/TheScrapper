from argparse import ArgumentParser

import requests
from requests.exceptions import MissingSchema
from modules.scrapper import Scrapper
from modules.info_reader import InfoReader

banner: str = """
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


parser = ArgumentParser(description="TheScrapper - Contact finder")
parser.add_argument("-u", "--url", required=True,
                    help="The URL of the target.")
parser.add_argument("-c", "--crawl", default=True, required=False, action="store_true",
                    help="Use every URL found on the site and hunt it down for information.")
parser.add_argument("-b", "--banner", default=False, required=False, action="store_true",
                    help="Use every URL found on the site and hunt it down for information.")
parser.add_argument("-s", "--sm", default=True, required=False, action="store_true",
                    help="Extract infos from the SocialMedia accounts.")
args = parser.parse_args()

if not args.banner:
    print(banner)

print("*" * 50 + "\n" + f"TheScrapper - Find possible ways to contact a site.\nTarget: {args.url}" + "\n" + "*" * 50 + "\n")

try:
    requests.get(args.url)
except MissingSchema:
    raise "MissingSchema, please add http(s). Example: https://example.com"

url: str = args.url
scrap = Scrapper(url=url, crawl=args.crawl)
IR = InfoReader(content=scrap.getText())
emails: list = IR.getEmails()
numbers = IR.getPhoneNumber()
sm: list = IR.getSocials()

print("\n")
print("E-Mails: " + "\n - ".join(emails))
print("Numbers:" + "\n - ".join(numbers))
if args.sm:
    print("SocialMedia: ")
    sm_info = IR.getSocialsInfo()
    for x in sm_info:
        url = x["url"]
        info = x["info"]
        if info:
            print(f" - {url}:")
            for y in info:
                print(f"     - {y}: {info[y]}")
        else:
            print(f" - {url}")
else:
    print("SocialMedia: " + ", ".join(sm))
