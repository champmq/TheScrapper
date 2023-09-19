import json
from argparse import ArgumentParser

import requests
from requests.exceptions import MissingSchema

from modules.info_reader import InfoReader
from modules.scrapper import Scrapper

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
parser.add_argument("-u", "--url", required=False,
                    help="The URL of the target.")
parser.add_argument("-us", "--urls", required=False,
                    help="The URL of the target.")
parser.add_argument("-c", "--crawl", default=False, required=False, action="store_true",
                    help="Use every URL found on the site and hunt it down for information.")
parser.add_argument("-b", "--banner", default=False, required=False, action="store_true",
                    help="Use every URL found on the site and hunt it down for information.")
parser.add_argument("-s", "--sm", default=False, required=False, action="store_true",
                    help="Extract infos from the SocialMedia accounts.")
parser.add_argument("-o", "--output", default=False, required=False, action="store_true",
                    help="Save the output in a JSON file.")
parser.add_argument("-v", "--verbose", default=False, required=False, action="store_true",
                    help="Verbose output mode.")
args = parser.parse_args()


def verbPrint(content: str):
    if args.verbose:
        print(content)
    pass


target_type = ""
if not args.url and not args.urls:
    exit("Please add --url or --urls")
else:
    if args.url:
        target_type = "URL"
    else:
        target_type = "FILE"

if not args.banner:
    print(banner)

if target_type == "URL":
    if not (args.url.startswith("https://") or args.url.startswith("http://")):
        args.url = "http://" + args.url

    print("*" * 50 + "\n" + f"Target: {args.url}" + "\n" + "*" * 50 + "\n")

    requests.get(args.url)

    url: str = args.url
    verbPrint("Scraping (and crawling) started")
    scrap = Scrapper(url=url, crawl=args.crawl)
    verbPrint("Scraping (and crawling) done\nReading and sorting information")
    IR = InfoReader(content=scrap.getText())
    emails: list = IR.getEmails()
    numbers = IR.getPhoneNumber()
    sm: list = IR.getSocials()
    verbPrint("Reading and sorting information done")

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
    if args.output:
        out = {
            "E-Mails": emails,
            "SocialMedia": sm,
            "Numbers": numbers
        }
        file_name = url.lower().replace(
            "http://", "").replace("https://", "").replace("/", "")
        json.dump(out, open(f"output/{file_name}.json", "w+"), indent=4)

elif target_type == "FILE":
    out = []
    for url in open(args.urls, "r").readlines():
        url = url.replace("\n", "")
        print("\n\n")

        if "https://" not in url:
            url = "https://" + url

        print("*" * 50 + "\n" + f"Target: {url}" + "\n" + "*" * 50 + "\n")

        requests.get(url)
        verbPrint("Scraping (and crawling) started")
        scrap = Scrapper(url=url, crawl=args.crawl)
        verbPrint("Scraping (and crawling) done\nReading and sorting information")
        IR = InfoReader(content=scrap.getText())
        emails: list = IR.getEmails()
        numbers = IR.getPhoneNumber()
        sm: list = IR.getSocials()
        out.append({
            "Target": url,
            "E-Mails": emails,
            "SocialMedia": sm,
            "Numbers": numbers
        })
        verbPrint("Reading and sorting information done")
        print("E-Mails:\n" + "\n - ".join(emails))
        print("Numbers:\n" + "\n - ".join(numbers))
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

    if args.output:
        file_name = args.urls.replace("/", "_")
        json.dump(out, open(f"output/{file_name}.json", "w+"), indent=4)
