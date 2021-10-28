from argparse import ArgumentParser

import json
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
parser.add_argument("-u", "--url", required=False,
                    help="The URL of the target.")
parser.add_argument("-us", "--urls", required=False,
                    help="The URL of the target.")
parser.add_argument("-c", "--crawl", default=True, required=False, action="store_true",
                    help="Use every URL found on the site and hunt it down for information.")
parser.add_argument("-b", "--banner", default=False, required=False, action="store_true",
                    help="Use every URL found on the site and hunt it down for information.")
parser.add_argument("-s", "--sm", default=True, required=False, action="store_true",
                    help="Extract infos from the SocialMedia accounts.")
parser.add_argument("-o", "--output", default=True, required=False, action="store_true",
                    help="Save the output in a JSON file.")
args = parser.parse_args()

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
    print(
        "*" * 50 + "\n" + f"Target: {args.url}" + "\n" + "*" * 50 + "\n")

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
    if args.output:
        out = {
            "E-Mails": emails,
            "SocialMedia": sm,
            "Numbers": numbers
        }
        json.dump(out, open(f"output/{url}.json", "w+"), indent=4)

elif target_type == "FILE":
    out = []
    for url in open(args.urls, "r").readlines():
        url = url.replace("\n", "")
        print("\n\n")
        print("*" * 50 + "\n" + f"Target: {url}\n" + "*" * 50)

        try:
            requests.get(url)
        except MissingSchema:
            print(f"[-] MissingSchema for {url}, please add http(s). Example: https://example.com.")

        scrap = Scrapper(url=url, crawl=args.crawl)
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
        json.dump(out, open(f"output/{args.urls}.json", "w+"), indent=4)
